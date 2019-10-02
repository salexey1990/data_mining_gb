from selenium import webdriver
from selenium.webdriver.common.keys import Keys

chrome = webdriver.Chrome()
chrome.get('https://www.facebook.com')

login = chrome.find_element_by_xpath('//input[@class = "inputtext login_form_input_box" and @type = "email"]')
login.send_keys('89858829280')

pswd = chrome.find_element_by_xpath('//input[@class = "inputtext login_form_input_box" and @type = "password"]')
pswd.send_keys('26021990')

input_btn = chrome.find_element_by_xpath('//label[@id = "loginbutton"]/input')
input_btn.send_keys(Keys.ENTER)

print(1)