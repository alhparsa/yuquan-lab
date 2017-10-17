import csv
import json
import os
import time
import urllib2
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def csv_reader(filename):  # csv reader function for the items
    # returns a list with all the items
    items = []
    with open(filename, 'rU') as csv_file:
        reader = csv.reader(csv_file)
        for num, row in enumerate(reader):
            items.insert(num, ", ".join(row))
        items.pop(0)
        items.insert(0, "air conditioner")
    return knowledge_graph(items)  # passes the data to knowledge graph function and then return its output


def knowledge_graph(ls):  # uses conceptnet api to find similar/related words to the given word
    new_ls = []
    for item in ls:
        item = item.split()
        item = "_".join(item)
        new_ls.append(item)
        obj = requests.get("http://api.conceptnet.io/c/en/furniture?rel=/r/" + item + "&limit=1000").json()
        for i in range(len(obj['edges'])):
            if (obj['edges'][i]['start']['language'] == 'en' or obj['edges'][i]['start']['language'] == 'zh') and \
                            obj['edges'][i]['weight'] > 1.:
                if item in new_ls == False:
                    new_ls.appened(obj['edges'][i]['start']['label'])
    return new_ls


def url_getter():  # gets the url of pictures and returns a list of urls with images' urls
    direc = "DataSet"
    inside = False
    if not os.path.exists(direc):
        os.mkdir(direc)
    drive = webdriver.Safari()  # this is used to simulate a browser to get more pictures from google
    drive.get("http://image.google.com")
    items_location = "items.csv"  # location of the file with items
    items = csv_reader(items_location)  # gets the items from csv reader
    for i, item in enumerate(items):
        search_element = drive.find_element_by_id("lst-ib")
        search_element.send_keys(item, Keys.ENTER)  # find the search bar and sends the string value of item
        pics = []
        time.sleep(3)
        load_more(drive)
        imges = drive.find_elements_by_xpath(
            '//div[contains(@class,"rg_meta")]')  # gets a list of images with their image url
        time.sleep(5)
        for images in imges:
            try:
                img_url = json.loads(images.get_attribute('innerHTML'))["ou"]  # finds the url of image
                img_type = json.loads(images.get_attribute('innerHTML'))["ity"]  # finds the type of image (extension)
                pics.append((str(img_url), str(img_type)))
            except Exception as e:
                print "failed: ", e
        pic_downloader(pics, direc, item)
    print pics
    drive.quit()


def pic_downloader(Images, direc, item):  # downloads and writes pictures according to their url and type
    print "getting images related to", item
    folder_name = item.split()
    folder_name = '_'.join(folder_name)  # formats the image's name
    if not os.path.exists(os.path.join(direc, folder_name)):  # creates a folder for the image
        os.mkdir(os.path.join(direc, folder_name))
    direc = os.path.join(direc, folder_name)
    header = {
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"
    }

    for i, (img, Type) in enumerate(Images):  # download the images
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


def load_more(driver):  # simulates the user's behaviour to load more pictures
    for _ in range(9):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
    try:
        time.sleep(5)
        driver.find_element_by_id("smb").click()
    except Exception as e:
        print "couldn't load more pictures" + e
    for _ in range(10):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)


url_getter()
