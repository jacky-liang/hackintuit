from BeautifulSoup import BeautifulSoup
from bs4 import SoupStrainer
import urllib
import os
import shutil
import zipfile
import json

def scrape_names_from_tag_a(url):
    csv_names = []
    print 'scrape'
    html = urllib.urlopen(url).read()
    print 'html'
    relevant = SoupStrainer("a")
    soup = BeautifulSoup(html,parseOnlyThese=relevant)
    for a in soup.findAll('a'):
        if a.string != None and ".zip" in a.string:
            csv_names.append(a.string)
    return csv_names

def get_all_csv(url, csv_names, dest):
    organization = {}
    for name in csv_names:
        print name
        dirpath = os.path.join(dest, name[:-4])
        filepath = os.path.join(dirpath, name)
        if os.path.exists(dirpath):
            shutil.rmtree(dirpath)
        os.makedirs(dirpath)
        urllib.urlretrieve(url+name, "{}/{}".format(dirpath, name))
        zip = zipfile.ZipFile(filepath)
        zip.extractall(dirpath)
        for parent, dirnames, filenames in os.walk(dirpath):
            for fn in filenames:
                if fn.lower().endswith('.pdf'):
                    os.remove(os.path.join(parent, fn))
                elif fn.lower().endswith('.zip'):
                    os.remove(os.path.join(parent, fn))
                else:
                    organization[name] = fn

    return organization

if __name__ == "__main__":
    url = "http://www2.census.gov/acs2013_5yr/pums/"
    csv_names = scrape_names_from_tag_a(url)
    print csv_names
    dest = "{}/{}".format(os.getcwd(), "data")
    os.makedirs(dest)
    organization = get_all_csv(url, csv_names, dest)

    with open('organization.json', 'w') as fp:
        json.dump(organization, fp)
