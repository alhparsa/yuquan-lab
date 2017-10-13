from bs4 import BeautifulSoup
import urllib2
import os
import json
import csv

search_url = "https://www.google.com/search?tbm=isch&q="  # google image search url
items_location = "items.csv"  # location of the file with items
header = {
    'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"
}


def csv_reader(filename):  # csv reader function for the items
    # returns a list with all the items
    items = []
    with open(filename, 'rU') as csv_file:
        reader = csv.reader(csv_file)
        for num, row in enumerate(reader):
            items.insert(num, ", ".join(row))
    return items


def image_getter(enquired_item):
    direc = "Dataset"
    inside = False
    if not os.path.exists(direc):
        os.mkdir(direc)
    for item in enquired_item:
        item = item.split()
        item = '+'.join(item)
        if inside:
            direc = os.path.join("Dataset", item)
        else:
            direc = os.path.join(direc, item)
        if not os.path.exists(direc):
            os.mkdir(direc)
        url = "https://www.google.co.in/search?q=" + item + "&source=lnms&tbm=isch"
        soup = get_soup(url, header)
        counter = 0
        print ("adding images related to " + item)
        for a in soup.find_all("div", {"class": "rg_meta"}):
            Images = []  # contains the link for Large original images, type of  image
            inside = True
            link, Type = json.loads(a.text)["ou"], json.loads(a.text)["ity"]
            Images.append((link, Type))
            if counter>400:
                break
            for i, (img, Type) in enumerate(Images):
                counter += 1
                if counter>400:
                    break
                try:
                    req = urllib2.Request(img, headers={'User-Agent': header})
                    raw_img = urllib2.urlopen(req).read()
                    cntr = len([i for i in os.listdir(direc) if item in i]) + 1
                    print(cntr)

                    if len(Type) == 0:
                        f = open(os.path.join(direc, item + "_" + str(cntr) + ".jpg"), 'wb')
                    else:
                        f = open(os.path.join(direc, item + "_" + str(cntr) + "." + Type), 'wb')

                    f.write(raw_img)
                    f.close()
                except Exception as e:
                    print("could not load : " + img)
                    print(e)


def get_soup(url, header):
    return BeautifulSoup(urllib2.urlopen(urllib2.Request(url, headers=header)), 'html.parser')


inp = input()
if inp == 0:
    inquiries = csv_reader(items_location)
    inquiries.pop(0)
    inquiries.append("air conditioner")
    image_getter(inquiries)

else:
    query = input()
