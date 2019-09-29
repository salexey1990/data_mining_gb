# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserNewItem


class AvitoSpider(scrapy.Spider):
    name = 'avito'
    allowed_domains = ['avito.ru']
    start_urls = ['http://avito.ru/rossiya/vakansii?cd=1&q=python']
    # start_urls = ['http://avito.ru/rossiya/rabota?cd=1&q=python']

    def parse(self, response: HtmlResponse):
        vacancy_urls = response.xpath("//div[@class='item-photo ']/a/@href").extract()
        next_page = response.xpath("//a[contains(@class, 'js-pagination-next')]/@href").extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        for vac in vacancy_urls:
            yield response.follow(vac, callback=self.parse_vacancy)

    def parse_vacancy(self, response: HtmlResponse):
        name = response.xpath("//span[@class='title-info-title-text']/text()").extract_first()
        salary_value = response.xpath("//span[@class='js-item-price']/@content").extract_first()
        salary = {
            'min_value': int(salary_value) if salary_value else None,
            'currency': response.xpath("//span[@itemprop='priceCurrency']/@content").extract_first(),
            'max_value': None
        }
        yield JobparserNewItem(name=name, salary=salary)
