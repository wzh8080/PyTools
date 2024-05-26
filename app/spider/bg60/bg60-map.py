import sys

from utils.http_util import get_soup
import logging
import time
import random

from urllib.parse import urljoin
from utils.db_util import *

"""
    Describe:
        爬取笔趣阁小说网站地图
    Address:
        https://www.bg60.cc/map
        https://www.bg60.cc/map/367.html

"""


# 配置日志格式，添加 %(module)s（模块名）、%(funcName)s（函数名）、%(lineno)d（行号）到格式字符串


logging.basicConfig(
    filename='log/bg60-map1.log',
    filemode='w',
    # stream=sys.stdout,
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(module)s:%(funcName)s:%(lineno)d - %(message)s'
    )


def collect_books_list(url):
    logging.debug(f"开始收集书籍列表: {url}")
    soup = get_soup(url)
    logging.debug("HTML解析完毕..")
    if soup is None:
        logging.warning("无法获取soup对象，可能的网络问题或HTML解析错误")
        return []  # 如果获取soup失败，则返回空列表

    div_blocks = soup.find_all('div', class_='blocks')

    logging.debug("开始循环 block div 块...")
    book_list = []
    # 遍历每个div块，提取h2标签的文本
    for block in div_blocks:
        # book_type = block.h2.text.strip()
        book_type = ''
        li_list = block.find_all('li')
        for li_tag in li_list:
            book_name = li_tag.a.text.strip()
            book_author = li_tag.text.replace(book_name, '').strip()[1:]
            href = li_tag.a.get('href')
            if not href.startswith('http'):  # 如果链接是相对路径，则转换为绝对路径
                href = urljoin(url, href)
            book_list.append([main_url, book_type, book_name, book_author, href])
    return book_list


def collect_books_list2():
    soup = get_soup(main_url)
    blocks = soup.find_all('div', class_='blocks')
    # 列用列表推导式和提前查找减少循环内的重复操作
    books = [[block.h2.text, li.text.split('/')[0], li.text.split('/')[1], li.a['href']]
             for block in blocks
             for li in block.find_all('li')]
    return books


if __name__ == '__main__':
    # 循环到 page_num = 367 时停下  368
    manager = DatabaseManager()
    for page_num in range(35, 368):
        main_url = f'https://www.bg60.cc/map/{page_num}.html'
        print('开始任务...')
        a = collect_books_list(main_url)
        print('开始落库...')
        batch_insert(manager.get_conn(), 'book_list', ['web_name','genre', 'title', 'author', 'book_url'], a)
        print(f'已完成第 {page_num} 页')
        # 暂停随机秒
        # time.sleep(random.uniform(1, 3.0))
    print('end')
    manager.close_conn()
