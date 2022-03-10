# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from pymongo import MongoClient
from pprint import pprint
import re


class JobparserPipeline:

    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase = client.vacancies0903

    def process_item(self, item, spider):
        if spider.name == 'hhru':
            self.process_item_hhru(item, spider)
        elif spider.name == 'sjru':
            self.process_item_sjru(item, spider)
        else:
            raise AssertionError('unknown spider found')

    # ==========  hhru  ========== #
    def process_item_hhru(self, item, spider):
        item['min'], item['max'], item['cur'] = self.process_salary_hhru(item['salary'])
        del item['salary']

        p = re.compile(r'vacancy\/(\d+)')
        m = p.search(item['url'])

        id_ = m.group(1)
        print('id = ', id_)
        item['_id'] = id_
        print()

        collection = self.mongobase[spider.name]  # чтобы не делать проверку if else при раскладывании по коллекциям - используем имя паука
        collection.insert_one(item)
        return item

    # метод обработки зарплаты hhru
    def process_salary_hhru(self, salary):
        if 'з/п не указана' in salary:
            return -1, -1, None
        elif len(salary) == 5:
            if salary[0] == 'от ':
                # ['от ', '150\xa0000', ' ', 'руб.', ' на руки']
                return self.to_int(salary[1]), None, salary[3]
            elif salary[0] == 'до ':
                # ['до ', '260\xa0000', ' ', 'руб.', ' на руки']
                return None, self.to_int(salary[1]), salary[3]
        elif len(salary) == 7:
            # ['от ', '150\xa0000', ' до ', '200\xa0000', ' ', 'руб.', ' на руки']
            return self.to_int(salary[1]), self.to_int(salary[3]), salary[5]
        else:
            return None, None, None




    # ==========  sjru  ========== #
    def process_item_sjru(self, item, spider):
        item['min'], item['max'], item['cur'] = self.process_salary_sjru(item['salary'])
        del item['salary']

        p = re.compile(r'(\d+).html$')
        m = p.search(item['url'])

        id_ = m.group(1)
        print('id = ', id_)
        item['_id'] = id_

        collection = self.mongobase[spider.name]  # чтобы не делать проверку if else при раскладывании по коллекциям - используем имя паука
        collection.insert_one(item)
        return item

    # метод обработки зарплаты sjru
    def process_salary_sjru(self, salary):

        # ['По договорённости']
        if 'По договорённости' in salary:
            return 'По договорённости', 'По договорённости', None

        elif len(salary) == 3:
            # ['от', '\xa0', '90\xa0000\xa0руб.']
            if salary[0] == 'от':
                min_, cur = self.to_int_and_curr(salary[2])
                return min_, None, cur
            # ['до', '\xa0', '150\xa0000\xa0руб.']
            elif salary[0] == 'до':
                max_, cur = self.to_int_and_curr(salary[2])
                return None, max_, cur


        # ['120\xa0000', '130\xa0000', '\xa0', 'руб.']
        elif len(salary) == 4:
            return self.to_int(salary[0]), self.to_int(salary[1]), salary[3]
        else:
            return '_'.join(salary), None, None

    # ==========  общие методы  ========== #
    def to_int(self, s):
        try:
            return int(s.replace('\xa0', ''))
        except ValueError:
            return s

    def to_int_and_curr(self, s):
        try:
            s = s.replace('\xa0', '')
            p = re.compile(r'(\d+)(.+)')
            m = p.search(s)
            res = int(m.group(1)), m.group(2)
            return res

        except ValueError:
            return s
