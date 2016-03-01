#coding:utf-8
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time


browser = webdriver.Firefox() # Get local session of firefox
browser.get("http://www.baidu.com") # Load page
assert u"百度一下" in browser.title
elem = browser.find_element_by_name("wd") # Find the query box
elem.send_keys("seleniumhq" + Keys.RETURN)
time.sleep(0.2) # Let the page load, will be added to the API
try:
    browser.find_element_by_xpath("//a[contains(@href,'seleniumhq')]")
except NoSuchElementException:
    assert 0, "can't find seleniumhq"
browser.close()