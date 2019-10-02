# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from jobparser.items import SocialNetworkItem


class FacebookSpider(scrapy.Spider):
    name = 'facebook'
    allowed_domains = ['facebook.com']
    start_urls = ['http://facebook.com/']

    def __init__(self, login, pswd, start_user, *args, **kwargs):
        self.login = login
        self.pswd = pswd
        self.start_user = start_user
        self.chrome = webdriver.Chrome()
        self.chrome.implicitly_wait(10)
        super().__init__(*args, *kwargs)


    def parse(self, response: HtmlResponse):
        self.chrome.get('https://www.facebook.com')

        login_element = self.chrome.find_element_by_xpath(
            '//input[@class = "inputtext login_form_input_box" and @type = "email"]')
        login_element.send_keys(self.login)

        pswd_element = self.chrome.find_element_by_xpath(
            '//input[@class = "inputtext login_form_input_box" and @type = "password"]')
        pswd_element.send_keys(self.pswd)

        input_btn = self.chrome.find_element_by_xpath('//label[@id = "loginbutton"]/input')
        input_btn.send_keys(Keys.ENTER)
        # profile_link = self.chrome.find_element_by_xpath('//a[@class = "_5afe"]').get_attribute('href')
        yield response.follow(self.start_user,
                              callback=self.parse_profile)

    def parse_profile(self, response: HtmlResponse):
        loader = ItemLoader(item=SocialNetworkItem(), response=response)
        loader.add_xpath('name', '//a[@class = "_2nlw _2nlv"]/text()')
        self.chrome.get(response.url)
        self.chrome.find_element_by_xpath('//a[@data-tab-key = "about"]').send_keys(Keys.ENTER)
        element = WebDriverWait(self.chrome, 10).until(
            EC.presence_of_element_located((By.XPATH, '//a[@interactionclass = "_84vf"]'))
        )
        element.send_keys(Keys.ENTER)
        # self.chrome.find_element_by_xpath('//a[@interactionclass = "_84vf"]').send_keys(Keys.ENTER)
        dob = ''.join(list(map(lambda item: item.get_attribute('textContent'), self.chrome.find_elements_by_xpath('//li[@class = "_3pw9 _2pi4 _2ge8 _4vs2"]//div[@class = "_4bl7 _pt5"]'))))
        self.chrome.find_element_by_xpath('//a[@data-tab-key = "friends"]').send_keys(Keys.ENTER)
        friends = list(map(lambda item: item.get_attribute('href'), self.chrome.find_elements_by_xpath('//a[@class = "_5q6s _8o _8t lfloat _ohe"]')))
        loader.add_value('dob', dob)
        loader.add_value('friends', friends)
        yield loader.load_item()
        for friend in friends:
            yield response.follow(friend, callback=self.parse_profile)
