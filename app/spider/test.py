import requests


def fetch_download_url():
    # 目标URL
    ajax_url = 'https://www.zxcs.info/download1.php'

    # POST数据
    data = {'id': 14705}

    # 发送POST请求
    response = requests.post(ajax_url, data=data)

    # 检查请求是否成功
    if response.status_code == 200:
        # 假设服务器返回的是直接拼接后的完整下载URL
        download_url = "https://down.zxcs.info" + response.text.strip()
        return download_url
    else:
        print("请求失败，状态码:", response.status_code)
        return None


download_url = fetch_download_url()
if download_url:
    print("获取到的下载链接为:", download_url)
else:
    print("未能成功获取下载链接。")