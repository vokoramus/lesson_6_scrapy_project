import re

href = '-sisteme-1s-37779814.html'

p = re.compile(r'(\d+).html$')
m = p.search(href)

id_ = m.group(1)
print(id_)
