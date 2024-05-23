from utils.http_util import get_soup
import time
from tqdm import tqdm
from urllib.parse import urljoin
from utils.db_util import *
from bs4 import BeautifulSoup
import asyncio
from pyppeteer import launch

"""
    Describe:
        通过搜索，爬取指定小说
    Address:
        https://www.bg60.cc/
        
"""
main_url = 'https://www.bg60.cc/'


async def main(search_url):
    # 异步函数，获取动态加载后的页面
    browser = await launch({
        'headless': True,
        # 'executablePath': r'D:\Tools\chrome-win\chrome.exe',
        'autoDownload': False,  # 禁止自动下载Chromium
        'args': ['--no-sandbox', '--disable-setuid-sandbox']
    })
    page = await browser.newPage()  # 新建一个页面
    # 设置页面视口大小，模拟真实用户环境
    await page.setViewport({'width': 1920, 'height': 1080})

    try:
        return await get_page_content(page, search_url)
    finally:
        await browser.close()


async def get_page_content(page, url):
    # 获取页面
    await page.goto(url)
    try:
        await page.waitForSelector('.bookbox', {'visible': True, 'timeout': 8000})
    except asyncio.TimeoutError:
        print("等待元素超时，未找到'.bookbox'")
    cont = await page.content()
    cont.encode('utf-8')
    # 使用BeautifulSoup解析HTML
    soup = BeautifulSoup(cont, 'html.parser')
    book_list = soup.find_all('div', class_='bookbox')
    arr = []
    for book in book_list:
        author = book.find('div', class_='author').get_text(strip=True)
        describe = book.find('div', class_='uptime').get_text(strip=True)
        # 获取 div(.bookname) 元素中的 a 元素的 href 属性值
        book_href = book.find('h4', class_='bookname').find('a')['href']
        if book_href.startswith('/'):
            book_href = book_href[1:]
        book_url = main_url + book_href
        book_name = book.find('h4', class_='bookname').text
        img_url = book.find('div', class_='bookimg').find('img')['src']
        arr.append([book_name, author, describe, book_url, img_url])
        break
    return arr

if __name__ == '__main__':
    book_arr = asyncio.run(main("https://www.bg60.cc/s?q=%E7%9B%97%E5%A2%93%E7%AC%94%E8%AE%B0"))
    batch_insert(get_conn(), 'book_list', ['title', 'author', 'description', 'book_url', 'img_url'], book_arr)
