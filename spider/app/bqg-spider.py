import requests
import time
from tqdm import tqdm
from bs4 import BeautifulSoup

"""
    Author:
        Jack Cui
    Address:
        https://www.bg60.cc/top/
        
"""

main_url = 'https://www.bg60.cc/top/'
encoding = 'utf-8'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'}


def get_soup(url):
    response = requests.get(url=url, headers=headers)
    if response.status_code == 200:
        response.encoding = encoding
        html = response.text
        return BeautifulSoup(html, 'lxml')


def test():
    soup = get_soup(url=main_url)
    div_blocks = soup.find_all('div', class_='blocks')

    # 遍历每个div块，提取h2标签的文本
    for block in div_blocks:
        h2_text = block.h2.text
        print(h2_text)
        li_list = block.find_all('li')
        a_tags = block.find_all('a')
        for li_tag in li_list:
            print(li_tag.text)  # 老张的春天/姜晓雅张达明
            a_tag = li_tag.a
            print(a_tag.text)   # 老张的春天
            print(a_tag.get('href'))    # /book/37504/


if __name__ == '__main__':
    test()
    print('end')
