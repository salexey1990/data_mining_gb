import os
from os.path import join, dirname
from dotenv import load_dotenv
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from jobparser import settings
from jobparser.spiders.hhru import HhruSpider
from jobparser.spiders.superjobru import SuperjobruSpider
from jobparser.spiders.instagram import InstagramSpider
from jobparser.spiders.avito import AvitoSpider
from jobparser.spiders.avitoRealEstate import AvitoRealEstateSpider

do_env = join(dirname(__file__), '.env')
load_dotenv(do_env)

INST_LOGIN = os.getenv('INST_LOGIN')
INST_PWD = os.getenv('INST_PASSWORD')

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    # process.crawl(SuperjobruSpider)
    # process.crawl(HhruSpider)
    # process.crawl(InstagramSpider, ['geekbrains.ru'], INST_LOGIN, INST_PWD)
    process.crawl(AvitoRealEstateSpider)
    process.start()
