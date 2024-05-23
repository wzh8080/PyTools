from utils.http_util import get_soup
import time
from tqdm import tqdm
from urllib.parse import urljoin
from utils.db_util import *

"""
    Describe:
        通过搜索，爬取指定小说
    Address:
        https://www.bg60.cc/s?q=
        
"""

main_url = 'https://www.bg60.cc/s?q='


def collect_books_list():
    soup = get_soup(main_url)
    if soup is None:
        return []  # 如果获取soup失败，则返回空列表

    div_blocks = soup.find_all('div', class_='blocks')

    book_list = []
    # 遍历每个div块，提取h2标签的文本
    for block in div_blocks:
        book_type = block.h2.text.strip()
        li_list = block.find_all('li')
        for li_tag in li_list:
            arr = li_tag.text.strip().split('/')
            href = li_tag.a.get('href')
            if not href.startswith('http'):  # 如果链接是相对路径，则转换为绝对路径
                href = urljoin(main_url, href)
            book_author = ''
            if len(arr) == 2:
                # book_name, author = arr
                book_author = arr[1]
            else:
                continue
            book_list.append([book_type, arr[0], book_author, href])
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
    a = collect_books_list()
    print(a)
    batch_insert(get_conn(), 'book_list', ['genre', 'title', 'author', 'book_url'], a)
    print('end')

