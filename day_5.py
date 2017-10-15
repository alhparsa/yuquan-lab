# coding=utf-8
import time
from selenium import webdriver
from faker import Faker

from selenium.webdriver.support.wait import WebDriverWait

b = 0

def email_checker(driver):
    time.sleep(25)
    driver.find_element_by_xpath("//td[contains(text(),'Welcome to Instagram')]").click()
    time.sleep(2)
    driver.find_element_by_xpath("//span[contains(text(),'Confirm your email address')]").click()

while (b<5):
    driver_1 = webdriver.Chrome()
    driver_2 = webdriver.Chrome()

    driver_1.get("https://fakemailbox.com/en/")
    driver_2.get("https://www.instagram.com")

    fake = Faker()
    name = fake.name()

    password = "aLV4Zz_56H]kr[[+"
    m = 0
    username=[]
    email = driver_1.find_element_by_id("email-address").get_attribute("value")
    driver_2.find_element_by_name("emailOrPhone").send_keys(email)
    driver_2.find_element_by_name("fullName").send_keys(name)
    driver_2.find_element_by_name("username").click()
    # driver_2.find_element_by_class_name("coreSpriteInputRefresh _8scx2").click()
    # username.append(driver_2.find_element_by_tag_name("username").get_attribute("value"))
    if True:
        print True
        time.sleep(5)
    # el3 = driver.find_element_by_xpath("//*[@class='action-btn cancel alert-display']")
    # driver_2.find_element_by_class_name("_sjplo _3jk0j").click()
    driver_2.find_element_by_xpath("//input[@name='password']").send_keys(password)
    username.append(driver_2.find_element_by_name("username").get_attribute("value"))
    driver_2.find_element_by_xpath("//button[contains(text(),'Sign up')]").click()
    time.sleep(15)
    email_checker(driver_1)
    b+=1


