from utils.http_util import get_soup
import time
import random
from tqdm import tqdm
from urllib.parse import urljoin
from utils.db_util import *

"""
    Describe:
        爬取笔趣阁小说网站地图
    Address:
        https://www.bg60.cc/map
        https://www.bg60.cc/map/367.html

"""


def collect_books_list(url):
    soup = get_soup(url)
    if soup is None:
        return []  # 如果获取soup失败，则返回空列表

    div_blocks = soup.find_all('div', class_='blocks')

    book_list = []
    # 遍历每个div块，提取h2标签的文本
    for block in div_blocks:
        # book_type = block.h2.text.strip()
        book_type = ''
        li_list = block.find_all('li')
        for li_tag in li_list:
            arr = li_tag.text.strip().split('/')
            href = li_tag.a.get('href')
            if not href.startswith('http'):  # 如果链接是相对路径，则转换为绝对路径
                href = urljoin(url, href)
            book_author = ''
            if len(arr) == 2:
                # book_name, author = arr
                book_author = arr[1]
            elif len(arr) == 1:
                book_author = ''
            else:
                continue
            book_list.append([main_url, book_type, arr[0], book_author, href])
    return book_list


def collect_books_list2():
    soup = get_soup(main_url)
    blocks = soup.find_all('div', class_='blocks')
    # 列用列表推导式和提前查找减少循环内的重复操作
    books = [[block.h2.text, li.text.split('/')[0], li.text.split('/')[1], li.a['href']]
             for block in blocks
             for li in block.find_all('li')]
    return books


# page_num = 2  331 已完成
# 10-14 有重复
page_num = 10
main_url = f'https://www.bg60.cc/map/{page_num}.html'

if __name__ == '__main__':
    # 循环到 page_num = 367 时停下  183,000 + 335  182705
    for page_num in range(10, 15):
        main_url = f'https://www.bg60.cc/map/{page_num}.html'
        a = collect_books_list(main_url)
        batch_insert(get_conn(), 'book_list', ['web_name','genre', 'title', 'author', 'book_url'], a)
        print(f'已完成第 {page_num} 页')
        # 暂停随机秒
        # time.sleep(random.uniform(1, 3.0))
    print('end')

