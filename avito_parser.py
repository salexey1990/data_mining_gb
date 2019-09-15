import requests
from pymongo import MongoClient
from bs4 import BeautifulSoup
import time
import random


class AvitoParser:
    def __init__(self):
        self.mongo_url = 'mongodb://localhost:27017'
        self.client = MongoClient('localhost', 27017)
        self.database = self.client.leson2
        self.USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) snap ' \
                          'Chromium/76.0.3809.100 Chrome/76.0.3809.100 Safari/537.36 '
        self.base_url = 'https://www.avito.ru'
        self.url = 'https://www.avito.ru/krasnodarskiy_kray/kvartiry/prodam?cd=1'
        self.avito_page = 1
        self.status_code = 200

    def parse(self):
        while self.status_code == 200:
            print(f'page # {self.avito_page}, status code {self.status_code}')
            response = requests.get(self.url, headers={'User-Agent': self.USER_AGENT}, proxies={'p': self.avito_page})
            soup = BeautifulSoup(response.text, 'lxml')
            body = soup.html.body
            ads = body.find_all('a', attrs={'class': 'item-description-title-link'})
            urls = [f'{self.base_url}{itm.attrs["href"]}' for itm in ads]
            self.status_code = response.status_code
            self.avito_page += 1
            collection = self.database.avito
            time.sleep(random.randint(1, 5))
            for itm in urls:
                time.sleep(random.randint(1, 5))
                result = self.req_ads(itm)
                collection.insert_one(result)

    def req_ads(self, url):
        response = requests.get(url, headers={'User-Agent': self.USER_AGENT})
        soup = BeautifulSoup(response.text, 'lxml')
        user_element = soup.html.body.find('a', attrs={'title': 'Нажмите, чтобы перейти в профиль'})
        try:
            price = soup.body.findAll('span', attrs={'class': 'js-item-price', 'itemprop': 'price'})[0].attrs.get(
                'content')
        except IndexError:
            price = None
        result = {'title': soup.head.title.text,
                  'price': int(price) if price and price.isdigit else None,
                  'url': response.url,
                  'params': [tuple(itm.text.split(':')) for itm in
                             soup.body.findAll('li', attrs={'class': 'item-params-list-item'})],
                  'user_name': user_element.text if user_element else None,
                  'user_profile': f'{self.base_url}{user_element.attrs["href"]}' if user_element else None
                  }
        return result


if __name__ == '__main__':
    testing = AvitoParser()
    testing.parse()
