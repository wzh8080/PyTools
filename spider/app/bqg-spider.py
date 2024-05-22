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


def get_content(target):
    req = requests.get(url=target)
    req.encoding = 'utf-8'
    html = req.text
    bf = BeautifulSoup(html, 'lxml')
    texts = bf.find('div', id='content')
    content = texts.text.strip().split('\xa0' * 4)
    return content


def get_soup(url):
    response = requests.get(url=url, headers=headers)
    if response.status_code == 200:
        response.encoding = encoding
        html = response.text
        return BeautifulSoup(html, 'lxml')


def test1():
    print('test1')
    # chapter_bs = BeautifulSoup(html, 'lxml')
    # chapters = chapter_bs.find('div', id='list')
    # chapters = chapters.find_all('a')
    # for chapter in tqdm(chapters):
    #     chapter_name = chapter.string
    #     url = server + chapter.get('href')
    #     content = get_content(url)
    #     with open(book_name, 'a', encoding='utf-8') as f:
    #         f.write(chapter_name)
    #         f.write('\n')
    #         f.write('\n'.join(content))
    #         f.write('\n')

def test():
    soup = get_soup(url=main_url)
    div_blocks = soup.find_all('div', class_='blocks')

    # 遍历每个div块，提取h2标签的文本
    for block in div_blocks:
        h2_text = block.h2.text
        print(h2_text)
        a_tags = block.find_all('a')
        for a_tag in a_tags:
            print(a_tag.text)
            print(a_tag.get('href'))


if __name__ == '__main__':
    test()
    print('end')
