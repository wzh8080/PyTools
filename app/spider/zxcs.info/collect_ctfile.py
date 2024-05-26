"""
收集 zxcs.info（知轩藏书）的 网盘下载连接

https://zxcs.info/sort/3/page/1 都市·娱乐
https://zxcs.info/sort/4/page/1 武侠·仙侠
https://zxcs.info/sort/6/page/1 精校武侠
https://zxcs.info/sort/7/page/1 精校仙侠
https://zxcs.info/sort/8/page/1 奇幻·玄幻

获取：
    1. 书籍详情地址，<a href="https://zxcs.info/post/15521"
    2. 详情，<dd class="des"> 一个神奇的‘万能工具箱’
    3. 内容分类，<a href="/tag/金手指" />金手指
"""
import logging
import random
import time
from urllib.parse import urljoin
from utils.db_util import *
from utils.http_util import *
import sys

logging.basicConfig(
    # filename='log/collect_ctfile.log',
    # filemode='w',
    # stream=sys.stdout,
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(module)s:%(funcName)s:%(lineno)d - %(message)s'
    # ,encoding='utf-8'
    )


def collect_books_list(url):
    time.sleep(random.uniform(1, 5))
    logging.debug(f"开始收集书籍列表:[{url}]")
    soup = get_soup(url)
    logging.debug("HTML解析完毕..")
    if soup is None:
        logging.warning(f"无法获取soup对象，可能的网络问题或HTML解析错误，url={url}")
        return []  # 如果获取soup失败，则返回空列表

    block_list = soup.find_all('dl', id='plist')
    logging.debug("开始循环 block 块...")
    book_list = []
    # 遍历每个div块，提取h2标签的文本
    for block in block_list:
        #     1. 书籍详情地址，<a href="https://zxcs.info/post/15521"
        #     2. 详情，<dd class="des"> 一个神奇的‘万能工具箱’
        tag_a = block.dt.a
        book_name = tag_a.text.strip()
        book_url = tag_a.get('href').strip()
        des = block.find('dd', class_='des').text.strip()
        book_list.append([url, book_url, des, book_name])
    return book_list


def update_catalog(p_type, p_page):
    cursor.execute('update book_catalog set next_page=%s where book_type=%s', (p_page, p_type))
    conn.commit()
    logging.debug(f"更新目录表成功，[{p_type}]类型")


def main():
    # 获取查询结果
    cursor.execute(
        'select catalog_url ,total_page ,next_page, book_type from book_catalog bc where total_page>next_page')
    rows = cursor.fetchall()
    print("查询结果条数：", len(rows))
    temp_i = 0
    book_type = ''
    try:
        for row in rows:
            # if temp_i > 2:    # 测试
            #     break
            catalog_url, total_page, next_page, temp_type = row
            book_type = temp_type
            logging.info(f"开始爬取[{book_type}]类型书籍 的第[{next_page}]到[{total_page}]页数据")
            # 开始爬虫
            for i in range(next_page, total_page + 1):
                temp_i = i
                # 当前准备爬取的 url
                current_url = catalog_url.format(i)
                # 爬取该网页的所有书籍列表
                logging.debug(f"开始爬取[{book_type}]类型共[{total_page}]页的第[{i}]页数据 [{current_url}]")
                book_list = collect_books_list(current_url)
                db_batch_insert(cursor, 'book_list_zxcs', ['catalog_url', 'book_url', 'description', 'title'], book_list)
            conn.commit()
            update_catalog(book_type, temp_i)
    except Exception as e:
        logging.error(f"爬取[{book_type}]类型 的第[{temp_i}]页数据时失败，原因：[{e}]", exc_info=True)
        update_catalog(book_type, temp_i)
    finally:
        logging.info('关闭数据库连接')
        cursor.close()
        conn.close()
        logging.info('结束任务！')


if __name__ == '__main__':
    # 获取数据源及游标
    manager = DatabaseManager()
    conn = manager.get_conn()
    cursor = conn.cursor()
    main()

