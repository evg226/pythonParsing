from pprint import pprint
from bs4 import BeautifulSoup
import requests

from hw2_utils import salaryMaker

session = requests.Session()
url = 'https://hh.ru'
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
    'Charset': 'utf-8'
}
params = {'search_field': 'name+description','text': 'react laravel'}

response = session.get(url=url + '/search/vacancy', headers=headers, params=params)
dom = BeautifulSoup(response.text, 'html.parser')
vacancies = dom.select('div.vacancy-serp-item')

pages = dom.findAll('a', {'data-qa': "pager-page"})
last_page = (list(pages)[-1]).find('span').text
print('Pages count=' + last_page)

vacancies_data = []
for page in range(1, int(last_page) + 1):
    params['page'] = page
    print(f'Handling page # {page}')
    response = session.get(url=url + '/search/vacancy', headers=headers, params=params)
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
        vacancies_data.append(vacancy_data)

pprint(vacancies_data)
print('Vacancies count:' + str(len(vacancies_data)))
