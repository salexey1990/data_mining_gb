# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class SuperjobruSpider(scrapy.Spider):
    name = 'superjobru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=python']

    def parse(self, response: HtmlResponse):
        next_page = response.css('a.icMQ_._1_Cht._3ze9n.f-test-button-2::attr(href)').extract_first()
        yield response.follow(next_page, callback=self.parse)

        vacancy = response.css('a.icMQ_._1QIBo._2JivQ._3dPok::attr(href)').extract()

        for link in vacancy:
            yield response.follow(link, callback=self.vacansy_parse)

    def vacansy_parse(self, response: HtmlResponse):
        name = response.css('h1._3mfro.rFbjy.s1nFK._2JVkc::text').extract_first()
        salary = ''.join(response.css('span._3mfro._2Wp8I.ZON4b.PlM3e._2JVkc *::text').extract())
        employer_name = response.css('h2._3mfro.PlM3e._2JVkc._2VHxz._3LJqf._15msI::text').extract_first()
        vacancy_link = response.url
        yield JobparserItem(name=name, salary=salary, employer_name=employer_name, vacancy_link=vacancy_link)

