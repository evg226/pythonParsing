# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

from itemadapter import ItemAdapter
from pymongo import MongoClient
from pymongo import errors
import re


class JobparserPipeline:

    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongoBase = client.vacancies

    def process_item(self, item, spider):
        collection = self.mongoBase[spider.name]
        vacancy = {}
        vacancy['salary'] = self.salaryProccess(salary=item['salary'])
        vacancy['url'] = re.search('/vacancy/\d+', item['url']).group(0)
        vacancy['company'] = re.search('/employer/\d+', item['company']).group(0)
        vacancy['_id'] = re.search('\d+', vacancy['url']).group(0)
        print(vacancy)
        try:
            collection.insert_one(vacancy)
        except errors.DuplicateKeyError:
            pass
        return item

    def salaryProccess(self, salary):
        result = {}
        for i, el in enumerate(salary):
            if 'от' in el.lower():
                result['min'] = int(''.join(re.findall('\d+', salary[i + 1])))
            if ('до' in el.lower()) and ('до вычета' not in el.lower()):
                result['max'] = int(''.join(re.findall('\d+', salary[i + 1])))
        if len(salary) == 6:
            result['currency'] = salary[3]
        if len(salary) == 8:
            result['currency'] = salary[5]
        return result
