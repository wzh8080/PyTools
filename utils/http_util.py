import random
import time

import requests
from bs4 import BeautifulSoup

encoding = 'utf-8'
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
#                   'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'}
# headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.95 Safari/537.36 QIHU 360SE'}

header_list = [
    {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.95 Safari/537.36 QIHU 360SE'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win6.1; Win64; Win64; rv:8.1) Gecko/52.0 Firefox/52.0'},
    {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7_7) AppleWebKit/6537.3 (KHTML, like Gecko) Chrome/69.0 Safari/653.0'},
    {'User-Agent': 'Mozilla/5.0 (Linux; Android 8.1; Mobile; rv:8.1; SAMS-KR1) AppleWebkit/6537.35.0 (KHTML, like Gecko) Version/4.0 Chrome/67.0 Mobile Safari/65.1'},
    {'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 13_2_3 like Mac OS X) AppleWebKit/6537.3 (KHTML, like Gecko) Version/6.0 Mobile/6.0 Mobile/6.0 Safari/65.0'},
    {'User-Agent': 'Mozilla/5.0 (Linux; U; Android 9; Mobile; rv:8.1; AOSP-Redmi Note 6 Pro) AppleWebKit/6537.3 (KHTML, like Gecko) Chrome/69.0 Mobile Safari/69.0'},
    {'User-Agent': 'Mozilla/5.0 (iPhone; CPU 4_3_4 like Mac OS X) AppleWebKit/6537.3 (KHTML, like Gecko) Version/1.0 Mobile/6.0 Mobile/6.0 Safari/6.0'},
    {'User-Agent': 'Mozilla/5.0 (Linux x86_6; rv:10.1; rv:1) Gecko/201.0 Firefox/201.0'},
    {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS 10_15_15_7) AppleWebKit/6537.3 (KHTML, like Gecko) Chrome/69.0 Safari/65.0'},
    {'User-Agent': 'Mozilla/5.0 (Linux; U; Android 10; Razer Phone) AppleWebKit/6537.3 (KHTML, like Gecko) Chrome/69.0 Mobile Safari/69.0'},
    {'User-Agent': 'Mozilla/5.0 (iPad; CPU 4_4 like Mac OS X) AppleWebKit/6537.3 (KHTML, like Gecko) Version/6.0 Mobile/6.0 Mobile/6.0 Safari/6.0'}
]


def get_soup(url):
    # 随机等待一段时间
    time.sleep(random.uniform(1, 5))
    # 随机选取一个User-Agent
    headers = random.choice(header_list)
    print("随机选取一个User-Agent:",headers)
    response = requests.get(url=url, headers=headers)
    if response.status_code == 200:
        response.encoding = encoding
        html = response.text
        return BeautifulSoup(html, 'lxml')
    else:
        print('请求失败，响应码:', response.status_code)
        return None


def get_soup_from_url(url):
    """一个安全地从给定URL获取soup的函数，包含异常处理。"""
    try:
        response = requests.get(url)
        response.raise_for_status()  # 检查请求是否成功
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup
    except requests.exceptions.RequestException as e:
        print(f"获取页面时出错: {e}")
        return None
