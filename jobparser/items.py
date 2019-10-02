# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
import re
from scrapy.loader.processors import MapCompose, TakeFirst, Compose


def cleaner_photo(values):
    if values[:2] == '//':
        return f'http:{values}'
    return values

def props_cleaner(prop):
    key = re.search('(?<=label">)(.*)(?=:)', prop).group(0)
    val = re.search('(?<=</span>)(.*)(?=</li>)', prop).group(0)
    return {key: val}

def concat_props(prop):
    res = {}
    for item in prop:
        res.update(item)
    return res

class AvitoRealEstate(scrapy.Item):
    _id = scrapy.Field()
    title = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field(input_processor=MapCompose(cleaner_photo))
    props = scrapy.Field(input_processor=MapCompose(props_cleaner), output_processor=Compose(concat_props))
    price = scrapy.Field(input_processor=Compose(lambda v: int(v[0])), output_processor=TakeFirst())
    currency = scrapy.Field(output_processor=TakeFirst())

class SocialNetworkItem(scrapy.Item):
    _id = scrapy.Field()
    dob = scrapy.Field(output_processor=TakeFirst())
    name = scrapy.Field(output_processor=TakeFirst())
    friends = scrapy.Field()

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


