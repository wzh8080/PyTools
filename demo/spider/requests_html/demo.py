from requests_html import HTMLSession


def fetch_dynamic_content(url):
    """
    抓取动态加载页面
    pip install requests-html

    pip install lxml[html_clean]  或者  pip install lxml_html_clean
    添加：from lxml_html_clean import clean

    https://storage.googleapis.com/chromium-browser-snapshots/Win_x64/1181205/chrome-win.zip
    https://registry.npmmirror.com/binary.html?path=chromium-browser-snapshots/Win_x64/

    使用requests-html库获取并解析一个网页的动态内容。

    参数:
    url (str): 要访问的网页URL

    返回:
    str: 提取到的动态生成的内容（示例中为页面标题）

    注意：
    requests_html库并不直接支持指定Chrome浏览器的路径，因为它底层使用pyppeteer来处理JavaScript渲染，
    而pyppeteer会自动管理Chromium的下载和使用。当你调用response.html.render()方法时，
    它会自动在后台使用Chromium来渲染页面，无需手动指定Chromium或Chrome的路径。
    """

    # 创建一个HTMLSession实例，用于维持会话和浏览器上下文
    session = HTMLSession()

    try:
        # 使用Session实例发送请求，它会自动处理JavaScript渲染
        response = session.get(url, timeout=20)

        # 确保页面完全加载，等待JavaScript执行完成
        response.html.render(sleep=2)  # sleep 参数让程序暂停指定秒数，等待页面加载

        # 提取页面标题作为示例，你可以根据需要提取其他元素
        # 提取并打印页面内容
        content = response.html.html
        print("页面内容：")
        print(content)
        return content

    except Exception as e:
        print(f"发生错误: {e}")
    finally:
        # 关闭会话以释放资源
        session.close()


# 主程序
if __name__ == "__main__":
    url = 'https://www.bg60.cc/s?q=%E7%9B%97%E5%A2%93%E7%AC%94%E8%AE%B0'  # 请替换为你想要抓取的动态加载内容的网址
    fetch_dynamic_content(url)

