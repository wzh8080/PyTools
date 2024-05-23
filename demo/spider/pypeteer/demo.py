# 导入所需库
import asyncio
from pyppeteer import launch


async def fetch_dynamic_content(url):
    """
    使用Pyppeteer异步抓取动态加载的网页内容。

    参数:
    - url: 需要抓取的网页地址

    步骤概述:
    1. 启动一个无头浏览器实例。
    2. 打开指定的URL。
    3. 等待页面加载完成（可选：包括等待特定元素出现，以处理更复杂的动态页面）。
    4. 获取页面的HTML内容。
    5. 关闭浏览器实例。
    """
    # 启动浏览器
    # browser = await launch(headless=True)  # headless=True表示无头模式，不打开实际的浏览器窗口
    browser = await launch({
        'headless': True,
        'executablePath': r'D:\Tools\chrome-win\chrome.exe',
        'autoDownload': False,  # 禁止自动下载Chromium
        'args': ['--no-sandbox', '--disable-setuid-sandbox']
    })

    page = await browser.newPage()  # 新建一个页面

    # 设置页面视口大小，模拟真实用户环境
    await page.setViewport({'width': 1920, 'height': 1080})

    # 访问URL
    await page.goto(url)

    # 等待页面加载完成。这里以页面加载完成为例子，如果页面有异步加载内容，可能需要更复杂的等待条件
    # await page.waitForNavigation()
    # 增加等待特定元素的逻辑，以替代waitForNavigation
    try:
        await page.waitForSelector('.bookbox', {'visible': True, 'timeout': 8000})
    except asyncio.TimeoutError:
        print("等待元素超时，未找到'.bookbox'")

    # 获取页面内容
    content = await page.content()

    # 打印页面内容
    print("页面内容：")
    print(content)

    # 关闭浏览器
    await browser.close()


# 主函数，确保异步函数能够被执行
async def main():
    url = 'https://www.bg60.cc/s?q=%E7%9B%97%E5%A2%93%E7%AC%94%E8%AE%B0'  # 请替换为你想要抓取的动态加载内容的网址
    await fetch_dynamic_content(url)


# 运行主函数
asyncio.run(main())
