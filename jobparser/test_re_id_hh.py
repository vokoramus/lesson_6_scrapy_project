import re

href = 'https://spb.hh.ru/vacancy/50573754?from=vacancy_search_list&hhtmFrom=vacancy_search_list&query=Python'


p = re.compile(r'vacancy\/(\d+)')
m = p.search(href)

id_ = m.group(1)
print(id_)
