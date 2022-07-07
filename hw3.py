import re
from pprint import pprint
from bs4 import BeautifulSoup
import requests
from pymongo import MongoClient
from pymongo import errors

from hw2_utils import salaryMaker
from hw3_utils import salaryAnalizer

client = MongoClient('mongodb://localhost:27017')
db = client['vacancies']
vacancies_hh = db.hh
# vacancies_hh.drop()
# vacs = list(vacancies_hh.find())
# pprint(vacs)

session = requests.Session()
url = 'https://hh.ru'
searchString = 'react nest'
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
    'Charset': 'utf-8'
}
params = {'search_field': 'name+description', 'text': searchString, 'items_on_page': '20'}

response = session.get(url=url + '/search/vacancy', headers=headers, params=params)
dom = BeautifulSoup(response.text, 'html.parser')
vacancies = dom.select('div.vacancy-serp-item')

pages = dom.findAll('a', {'data-qa': "pager-page"})
last_page = (list(pages)[-1]).find('span').text
print('Pages count=' + last_page)
count_added = 0
count_skipped = 0

vacancies_data = []
for page in range(0, int(last_page)):
    params['page'] = str(page)
    print(f'Handling page # {page}')
    response = session.get(url=url + '/search/vacancy', headers=headers, params=params)
    dom = BeautifulSoup(response.text, 'html.parser')
    vacancies = dom.select('div.vacancy-serp-item')
    for vacancy in vacancies:
        vacancy_data = {}
        title_href = vacancy.find('a', {'data-qa': "vacancy-serp__vacancy-title"})
        vacancy_data['title'] = title_href.text
        vacancy_data['link'] = title_href.get('href')
        company_href = vacancy.find('a', {'data-qa': "vacancy-serp__vacancy-employer"})
        vacancy_data['company'] = company_href.text
        vacancy_data['company_link'] = company_href.get('href')
        vacancy_data['salary'] = salaryMaker(vacancy.find('span', {'data-qa': "vacancy-serp__vacancy-compensation"}))
        vacancy_data['site_from'] = url
        vacancy_data['_id'] = int(re.search('vacancy/(\d+)', vacancy_data['link']).group(1))
        vacancies_data.append(vacancy_data)
        try:
            vacancies_hh.insert_one(vacancy_data)
            count_added += 1
        except errors.DuplicateKeyError:
            count_skipped += 1

print('Found : ' + str(len(vacancies_data)))
print('New Added : ' + str(count_added))
print('Skipped : ' + str(count_skipped))

# pprint(list(vacancies_hh.find()))

vacs = list(vacancies_hh.find())
salary = 120000
print('Relevant vacancies : (>' + str(salary) + ')')
salaryAnalizer(salary, vacs)
