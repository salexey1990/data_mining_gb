# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader
from jobparser.items import AvitoRealEstate


class AvitoRealEstateSpider(scrapy.Spider):
    name = 'avitoRealEstate'
    allowed_domains = ['avito.ru']
    start_urls = ['https://www.avito.ru/rossiya/kvartiry/prodam?cd=1']

    def parse(self, response: HtmlResponse):
        variant_urls = response.xpath("//div[@class='item-photo ']/a/@href").extract()
        next_page = response.xpath("//a[contains(@class, 'js-pagination-next')]/@href").extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        for vac in variant_urls:
            yield response.follow(vac, callback=self.parse_variant)

    def parse_variant(self, response: HtmlResponse):
        loader = ItemLoader(item=AvitoRealEstate(), response=response)
        loader.add_xpath('photos',
                         '//div[contains(@class, "gallery-img-wrapper")]//div[contains(@class, "gallery-img-frame")]/@data-url')
        loader.add_xpath('title', "//span[@class='title-info-title-text']/text()")
        loader.add_xpath('props', '//li[@class="item-params-list-item"]')
        loader.add_xpath('price', '//span[@class="js-item-price"]/@content')
        loader.add_xpath('currency', '//span[@class="price-value-prices-list-item-currency_sign"]/@content')
        yield loader.load_item()
