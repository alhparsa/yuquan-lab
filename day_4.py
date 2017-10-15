import csv
import json
import os
import time
import urllib2
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
    return items


def url_getter():
    direc = "DataSet"
    inside = False
    if not os.path.exists(direc):
        os.mkdir(direc)
    drive = webdriver.Safari()
    drive.get("http://image.google.com")
    items_location = "items.csv"  # location of the file with items
    items = csv_reader(items_location)
    for i, item in enumerate(items):
        search_element = drive.find_element_by_id("lst-ib")
        search_element.send_keys(item, Keys.ENTER)
        time.sleep(3)
        pics = []
        time.sleep(3)
        load_more(drive)
        imges = drive.find_elements_by_xpath('//div[contains(@class,"rg_meta")]')
        time.sleep(5)
        for images in imges:
            try:
                img_url = json.loads(images.get_attribute('innerHTML'))["ou"]
                img_type = json.loads(images.get_attribute('innerHTML'))["ity"]
                pics.append((str(img_url), str(img_type)))
            except Exception as e:
                print "failed: ", e
        pic_downloader(pics, direc, item)
        drive.execute_script("window.scrollTo(document.body.scrollHeight,0);")
        time.sleep(2)
    print pics
    drive.quit()


def pic_downloader(Images, direc, item):
    print "getting images related to", item
    folder_name = item.split()
    folder_name = '_'.join(folder_name)
    if not os.path.exists(os.path.join(direc, folder_name)):
        os.mkdir(os.path.join(direc, folder_name))
    direc = os.path.join(direc, folder_name)
    header = {
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"
    }

    for i, (img, Type) in enumerate(Images):
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


def load_more(driver):
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
