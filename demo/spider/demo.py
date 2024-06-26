import requests
import time
from tqdm import tqdm
from bs4 import BeautifulSoup
from utils.http_util import *

"""
    Author:
        Jack Cui
    Wechat:
        https://mp.weixin.qq.com/s/OCWwRVDFNslIuKyiCVUoTA
    Github:
        https://github.com/Jack-Cherish/python-spider/blob/master/2020/xbqg/xbqg_spider.py
"""


def get_content(target):
    req = requests.get(url=target)
    req.encoding = 'utf-8'
    html = req.text
    bf = BeautifulSoup(html, 'lxml')
    texts = bf.find('div', id='content')
    content = texts.text.strip().split('\xa0' * 4)
    return content


if __name__ == '__main__':
    server = 'https://www.xsbiquge.com'
    book_name = '诡秘之主.txt'
    # target = 'https://www.xsbiquge.com/15_15338/'

    target = 'https://url03.ctfile.com/f/41439203-1248721456-5a91ca?p=2657'
    req = requests.get(url=target)
    req.encoding = 'utf-8'
    html = req.text
    print(html)
    # soup = BeautifulSoup(html, 'lxml')
    # chapters = soup.find('div', id='list')
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
