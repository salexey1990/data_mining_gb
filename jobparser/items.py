# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JobparserItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    name = scrapy.Field()
    salary = scrapy.Field()
    employer_name = scrapy.Field()
    vacancy_link = scrapy.Field()

class JobparserNewItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    name = scrapy.Field()
    salary = scrapy.Field()

class InstagramItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    user = scrapy.Field()
    commented_users = scrapy.Field()
    shortcode = scrapy.Field()
    liked_users = scrapy.Field()

