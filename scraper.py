from BeautifulSoup import BeautifulSoup
from bs4 import SoupStrainer
import urllib
import os
import zipfile
import json
import csv

def scrape_names_from_tag_a(url):
    csv_names = []
    print 'scrape'
    html = urllib.urlopen(url).read()
    print 'html obtained'
    relevant = SoupStrainer("a")
    soup = BeautifulSoup(html,parseOnlyThese=relevant)
    for a in soup.findAll('a'):
        if a.string != None and ".zip" in a.string:
            csv_names.append(a.string)
    return csv_names

def get_column_indices(header_line, headers):
    positions, i = {}, 0
    positions["order"] = []
    for h in header_line:
        h = h.upper().strip()
        if h in headers:
            positions[h] = i
            positions["order"].append(h)
        i += 1
    return positions

def make_filtered_new_csv(infilepath, outfilepath, headers):
    users_dict = {}
    with open(infilepath, 'rb') as fpin, open(outfilepath, 'wb') as fpout:
        in_reader = csv.reader(fpin, delimiter=',')
        out_writer = csv.writer(fpout, delimiter=',')
        header_line = in_reader.next()
        cols = get_column_indices(header_line, headers)
        out_writer.writerow(cols["order"])
        print 'writing filtered csv: ' + outfilepath
        for row in in_reader:
            filtered_row = []
            for c in cols["order"]:
                filtered_row.append(row[cols[c]])
            out_writer.writerow(filtered_row)
        print 'finished writing for: ' + outfilepath

def get_all_pcsv(url, csv_names, dest, headers):
    organization = {}
    for name in csv_names:
        if name[4] != 'p':
            continue
        print name
        dirpath = os.path.join(dest, name[:-4])
        zippath = os.path.join(dirpath, name)
        if not os.path.exists(dirpath):
            print 'creating directory: ' + dirpath
            os.makedirs(dirpath)
            urllib.urlretrieve(url+name, "{}/{}".format(dirpath, name))
            zip = zipfile.ZipFile(zippath)
            zip.extractall(dirpath)
            for parent, dirnames, filenames in os.walk(dirpath):
                for fn in filenames:
                    if fn.lower().endswith('.pdf'):
                        os.remove(os.path.join(parent, fn))
                    elif fn.lower().endswith('.zip'):
                        os.remove(os.path.join(parent, fn))
                    else:
                        organization[name] = fn
        id = name[4:7]
        filepath = os.path.join(dirpath, "ss13{}.csv".format(id))
        new_filepath = os.path.join(dirpath, "filtered_ss13{}.csv".format(id))
        make_filtered_new_csv(filepath, new_filepath, headers)
        os.remove(filepath)

    return organization

if __name__ == "__main__":
    with open('headers.json') as data_file:
        headers = json.load(data_file)

    url = "http://www2.census.gov/acs2013_5yr/pums/"
    # csv_names = scrape_names_from_tag_a(url)
    # print csv_names
    dest = "{}/{}".format(os.getcwd(), "data")
    if not os.path.isdir(dest):
        os.makedirs(dest)
    csv_names = ['csv_pme.zip']
    organization = get_all_pcsv(url, csv_names, dest, headers)

    with open('organization.json', 'w') as fp:
        json.dump(organization, fp)
