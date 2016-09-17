import socket
from SocketServer import TCPServer
from BaseHTTPServer import BaseHTTPRequestHandler
from urlparse import parse_qs

import json
import logging 

import tflearn
import joblib
import numpy as np
from city_metrics import get_metrics
logging.getLogger().setLevel(logging.INFO)

# NN model
logging.info("Loading NN Model.")
l0 = tflearn.input_data(shape=[None,10])
l1 = tflearn.fully_connected(l0, 100, activation='relu')
l2 = tflearn.fully_connected(l1, 100, activation='relu')
l3 = tflearn.fully_connected(l2, 50, activation='relu')
lf = tflearn.fully_connected(l3, 1)
net = tflearn.regression(lf, loss="mean_square", restore=False)

data_loaded = joblib.load('models/model.tfl')
model = tflearn.DNN(net)
model.set_weights(l1.W, data_loaded['l1W'])
model.set_weights(l1.b, data_loaded['l1b'])
model.set_weights(l2.W, data_loaded['l2W'])
model.set_weights(l2.b, data_loaded['l2b'])
model.set_weights(l3.W, data_loaded['l3W'])
model.set_weights(l3.b, data_loaded['l3b'])
model.set_weights(lf.W, data_loaded['lfW'])
model.set_weights(lf.b, data_loaded['lfb'])

city_to_state = {'sf':'CA', 'sd':'CA', 'la':'CA', 'se':'WA', 'au':'TX','ny':'NY'}
states = ['CA','NY','FL','TX','IL','WA']

def get_results(params):
    logging.info("Performing computation for {0}".format(params))
    
    city = params['loc'][0]
    state = city_to_state[city]
    
    sex = int(params['sex'][0])
    age = int(params['age'][0])
    mar = int(params['mar'][0])
    stem = int(params['ind'][0])
        
    state_i = states.index(state)
    state_x = [0,0,0,0,0,0]
    state_x[state_i] = 1
    
    x = state_x + [age, mar, sex, stem]
    X = np.array([x])
    salary =model.predict(X)[0][0]
    
    return_data = get_metrics(city,salary)
    
    return_data.update({'salary':salary})
    
    return return_data
    
class MyTCPServer(TCPServer):
    def server_bind(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(self.server_address)

class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path.startswith('/salaries'):
            raw_params = self.path[self.path.index('?')+1:]
            params = parse_qs(raw_params)
            
            result = get_results(params)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(result))
            
httpd = MyTCPServer(("", 8080), MyHandler)
logging.info("Serving...")
httpd.serve_forever()