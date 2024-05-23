import requests
from bs4 import BeautifulSoup

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