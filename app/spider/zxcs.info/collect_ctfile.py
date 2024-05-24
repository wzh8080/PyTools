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
from urllib.parse import urljoin
from utils.db_util import *
from utils.http_util import *

logging.basicConfig(
    filename='log/bg60-map.log',
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
        logging.warning(f"无法获取soup对象，可能的网络问题或HTML解析错误，url={url}")
        return []  # 如果获取soup失败，则返回空列表

    block_list = soup.find_all('dl', id='plist')

    logging.debug("开始循环 block 块...")
    book_list = []
    # 遍历每个div块，提取h2标签的文本
    for block in block_list:
        #     1. 书籍详情地址，<a href="https://zxcs.info/post/15521"
        #     2. 详情，<dd class="des"> 一个神奇的‘万能工具箱’
        book_url = block.dt.a.get('href').strip()
        des = block.find('dd', class_='des').text.strip()
        book_list.append(url,book_url, des)
        break
        # for li_tag in li_list:
        #     book_name = li_tag.a.text.strip()
        #     book_author = li_tag.text.replace(book_name, '').strip()[1:]
        #     href = li_tag.a.get('href')
        #     if not href.startswith('http'):  # 如果链接是相对路径，则转换为绝对路径
        #         href = urljoin(url, href)
        #     book_list.append([main_url, book_type, book_name, book_author, href])
    return book_list


if __name__ == '__main__':
    collect_books_list('https://zxcs.info/sort/3/page/1')
