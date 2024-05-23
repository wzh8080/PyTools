from utils.http_util import *
from requests_html import HTMLSession

a = get_soup('https://www.bg60.cc/s?q=%E7%9B%97%E5%A2%93%E7%AC%94%E8%AE%B0')
b = a.find_all('div', class_='bookinfo')

print(b)
# with open('aaa', 'a', encoding='utf-8') as f:
#     f.write(a.)
