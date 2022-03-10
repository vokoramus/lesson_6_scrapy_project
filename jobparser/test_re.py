import re

href = '150\xa0000\xa0руб.'

href = href.replace('\xa0', '')
print(href)
p = re.compile(r'(\d+)(.+)')
m = p.search(href)
print(m.group(1), m.group(2))
