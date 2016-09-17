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

def get_column_indices(header_line, headers, order=None):
    positions, i = {}, 0
    if order == None:
        positions["order"] = []
    else:
        positions["order"] = order
    for h in header_line:
        h = h.upper().strip()
        if h in headers:
            positions[h] = i
            if order == None:
                positions["order"].append(h)
        i += 1
    return positions

def make_filtered_csv(infilepath, outfilepath, headers, writeHeader=True, order=None):
    users_dict = {}
    with open(infilepath, 'rb') as fpin, open(outfilepath, 'wb') as fpout:
        in_reader = csv.reader(fpin, delimiter=',')
        out_writer = csv.writer(fpout, delimiter=',')
        header_line = in_reader.next()
        cols = get_column_indices(header_line, headers, order)
        if writeHeader:
            print 'wrote header'
            # out_writer.writerow(cols["order"])
            # hardcoding this
            heading = ["CA", "NY", "FL", "TX", "IL", "WA", "AGE", "MAR", "SEX", "YES_STEM", "NO_STEM", "UNKNOWN_INDUSTRY", "INCOME"]
            # this needs to be modified to only have the columns in cols
            # out_writer.writerow(cols["order"])

            # hardcode
            out_writer.writerow(heading)

        print 'writing filtered csv: ' + outfilepath
        for row in in_reader:
            filtered_row = []
            # for h in cols["order"]:
            #     if h in headers:
            #         filtered_row.append(row[cols[h]])

            # hardcoding again lol
            state = row[cols['ST']]
            if state == '06':
                filtered_row.extend((1, 0, 0, 0, 0, 0))
            elif state == '36':
                filtered_row.extend((0, 1, 0, 0, 0, 0))
            elif state == '12':
                filtered_row.extend((0, 0, 1, 0, 0, 0))
            elif state == '48':
                filtered_row.extend((0, 0, 0, 1, 0, 0))
            elif state == '17':
                filtered_row.extend((0, 0, 0, 0, 1, 0))
            elif state == '53':
                filtered_row.extend((0, 0, 0, 0, 0, 1))
            else:
                # ignore if not one of our preferred state
                continue

            age = int(row[cols['AGEP']])
            if age > 35:
                continue
            filtered_row.append(age)

            marriage_status = row[cols['MAR']]
            if marriage_status == '1':
                filtered_row.append(1)
            else:
                filtered_row.append(0)

            is_stem = row[cols['SCIENGP']]
            if is_stem == '1':
                filtered_row.extend((1, 0, 0))
            elif is_stem == '0':
                filtered_row.extend((0, 1, 0))
            else:
                filtered_row.extend((0, 0, 1))

            try:
                income = int(row[cols['PINCP']])
                if income <= 0:
                    continue
            except:
                continue
            filtered_row.append(income)

            out_writer.writerow(filtered_row)
        print 'finished writing for: ' + outfilepath
        return cols["order"]

def get_all_pcsv(url, csv_names, directory, headers, onefile=None):
    organization = {}
    writeHeader = True
    order = None
    for name in csv_names:
        if name[4] != 'p':
            continue
        print name
        dirpath = os.path.join(directory, name[:-4])
        zippath = os.path.join(dirpath, name)
        id = name[4:7]
        filepath = os.path.join(dirpath, "ss13{}.csv".format(id))
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
        if onefile != None:
            order = make_filtered_csv(filepath, onefile, headers, writeHeader, order)
            writeHeader = False
        else:
            new_filepath = os.path.join(dirpath, "filtered_ss13{}.csv".format(id))
            order = make_filtered_new_csv(filepath, new_filepath, headers, order)
            os.remove(filepath)
    return organization

if __name__ == "__main__":
    with open('headers.json') as data_file:
        headers = json.load(data_file)

    url = "http://www2.census.gov/acs2013_5yr/pums/"

    # to use only a few states, assign to csv_names a list with the corresponding filenames
    # "CA", "NY", "FL", "TX", "IL", "WA"
    csv_names = ['csv_pca.zip', 'csv_pny.zip', 'csv_pfl.zip', 'csv_ptx.zip', 'csv_pil.zip', 'csv_pwa.zip']
    # csv_names = ['csv_pwa.zip', 'csv_pil.zip']
    # csv_names = scrape_names_from_tag_a(url)
    print csv_names

    directory = "{}/{}".format(os.getcwd(), "data")
    if not os.path.isdir(directory):
        os.makedirs(directory)
    fatdata = "{}/{}".format(directory, "fatdata.csv")
    organization = get_all_pcsv(url, csv_names, directory, headers, fatdata)

    with open('organization.json', 'w') as fp:
        json.dump(organization, fp)
