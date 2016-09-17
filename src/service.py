import SocketServer
import socket
from BaseHTTPServer import BaseHTTPRequestHandler
import json
import logging 
from urlparse import parse_qs
import tflearn
import joblib
import numpy as np

logging.getLogger().setLevel(logging.INFO)

# NN model
logging.info("Loading NN Model.")
l0 = tflearn.input_data(shape=[None,1])
l1 = tflearn.fully_connected(l0, 100, activation='relu')
l2 = tflearn.fully_connected(l1, 1)
net = tflearn.regression(l2, loss="mean_square", restore=False)

data_loaded = joblib.load('models/model.tfl')
model = tflearn.DNN(net)
model.set_weights(l1.W, data_loaded['l1W'])
model.set_weights(l1.b, data_loaded['l1b'])
model.set_weights(l2.W, data_loaded['l2W'])
model.set_weights(l2.b, data_loaded['l2b'])

def perform_prediction(params):
    logging.info("Performing prediction for {0}".format(params))
    
    val = float(params['x'][0])
    X = np.array([[val]])
    
    y = model.predict(X)
    
    return {'y':y}

class MyTCPServer(SocketServer.TCPServer):
    def server_bind(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(self.server_address)

class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path.startswith('/salaries'):
            raw_params = self.path[self.path.index('?')+1:]
            params = parse_qs(raw_params)
            
            result = perform_prediction(params)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(result))            

port = 8080
httpd = MyTCPServer(("", port), MyHandler)
logging.info("Serving...")
httpd.serve_forever()