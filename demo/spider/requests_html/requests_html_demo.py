from requests_html import HTMLSession
from lxml_html_clean import clean

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
    """

    # 创建一个HTMLSession实例，用于维持会话和浏览器上下文
    session = HTMLSession()

    try:
        # 使用Session实例发送请求，它会自动处理JavaScript渲染
        response = session.get(url)

        # 确保页面完全加载，等待JavaScript执行完成
        response.html.render(sleep=2)  # sleep参数让程序暂停指定秒数，等待页面加载

        # 提取页面标题作为示例，你可以根据需要提取其他元素
        title = response.html.find('title', first=True).text
        print(f"页面HTML为: {response.html}")
        print(f"页面标题为: {title}")
        return title

    except Exception as e:
        print(f"发生错误: {e}")
    finally:
        # 关闭会话以释放资源
        session.close()


# 示例URL，这里使用一个假设的页面，实际使用时替换为具体网址
example_url = 'https://www.bg60.cc/s?q=%E7%9B%97%E5%A2%93%E7%AC%94%E8%AE%B0'

# 调用函数并打印结果
fetch_dynamic_content(example_url)
