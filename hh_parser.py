import requests
from bs4 import BeautifulSoup

hh_search_url = 'https://hh.ru/search/vacancy?area=1&st=searchVacancy&from=suggest_post'
hh_page = 0
superjob_base_url = 'https://www.superjob.ru'
superjob_search_url = 'https://www.superjob.ru/vacancy/search/'
superjob_page = 1
user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'

vacancy_name = input('input vacancy name: ')
number_of_pages = int(input('input number of pages: '))
vacansy_list = []


def parse_hh_vacancies():
    hh_response = requests.get(hh_search_url, headers={'User-Agent': user_agent},
                               params={'text': vacancy_name, 'page': hh_page})
    hh_soup = BeautifulSoup(hh_response.text, 'lxml')
    hh_serp = hh_soup.html.body.find_all('div', attrs={'class': 'vacancy-serp-item'})
    for item in hh_serp:
        salary_element = item.find('div', attrs={'data-qa': 'vacancy-serp__vacancy-compensation'})
        if salary_element:
            salary = salary_element.text
            if salary.startswith('от'):
                salary = {
                    'from': salary,
                    'to': None
                }
            elif salary.startswith('до'):
                salary = {
                    'from': None,
                    'to': salary
                }
            else:
                salary = {
                    'from': salary.split('-')[0],
                    'to': salary.split('-')[1]
                }
        vacancy = {
            'title': item.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'}).text,
            'salary': salary,
            'vacancy_link': item.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'}).attrs['href'],
            'site': 'hh'
        }
        vacansy_list.append(vacancy)


def parse_superjob_vacancies():
    response = requests.get(superjob_search_url, headers={'User-Agent': user_agent},
                            params={'keywords': vacancy_name, 'page': superjob_page})
    soup = BeautifulSoup(response.text, 'lxml')

    serp = soup.html.body.find_all('div', attrs={'class': '_3zucV _2GPIV i6-sc _3VcZr'})
    for item in serp:
        salary_element = item.find('span', attrs={'class': '_3mfro _2Wp8I f-test-text-company-item-salary PlM3e '
                                                           '_2JVkc _2VHxz'})
        if salary_element:
            salary = salary_element.text
            if salary == 'По договорённости':
                salary = {
                    'from': 'По договорённости',
                    'to': 'По договорённости'
                }
            elif salary.startswith('от'):
                salary = {
                    'from': salary,
                    'to': None
                }
            elif salary.startswith('до'):
                salary = {
                    'from': None,
                    'to': salary
                }
            else:
                salary_range = salary.split('—')
                salary = {
                    'from': salary_range[0],
                    'to': salary_range[1] if len(salary_range) > 1 else None
                }
        vacancy = {
            'title': item.find('a', attrs={'target': '_blank'}).text,
            'salary': salary,
            'vacancy_link': F"{superjob_base_url}{item.find('a', attrs={'target': '_blank'}).attrs['href']}",
            'site': 'superjob'
        }
        vacansy_list.append(vacancy)


for i in range(number_of_pages):
    parse_hh_vacancies()
    parse_superjob_vacancies()

    hh_page += 1
    superjob_page += 1

print(vacansy_list)
