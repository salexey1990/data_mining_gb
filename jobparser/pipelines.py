# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from pymongo import MongoClient
from database.base import VacancyDB
from database.models import Vacancy
from scrapy.pipelines.images import ImagesPipeline


class JobparserPipeline(object):
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.vacancy
        self.sql_db = VacancyDB('sqlite:///vacancy.sqlite')

    def process_item(self, item, spider):
        if (spider.name == 'instagram'):
            return self.process_instagram_item(item, spider)
        else:
            return self.process_job_spider(item, spider)

    def process_instagram_item(self, item, spider):
        collection = self.mongo_base[spider.name]
        collection.insert_one(item)

    def process_job_spider(self, item, spider):
        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
        db_item = Vacancy(name=item.get('name'), spider=spider.name, salary=item.get('salary'),
                          employer_name=item.get('employer_name'), vacancy_link=item.get('vacancy_link'))
        self.sql_db.add_salary(db_item)
        return item

class AvitoPhotosPipelines(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item.get('photos'):
            for img in item['photos']:
                try:
                    yield scrapy.Request(img)
                except TypeError:
                    pass

    def item_completed(self, results, item, info):
        if results:
            item['photos'] = [itm[1] for itm in results if itm[0]]
        return item