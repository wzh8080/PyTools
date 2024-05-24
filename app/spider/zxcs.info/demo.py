import random
import urllib.parse
import requests

"""

"""

def get_file_url(file_id, folder_id, file_chk, mb, app):
    api_server = 'https://webapi.ctfile.com'  # 替换为目标API服务器地址
    params = {
        'uid': '41439203',  # 替换为实际用户ID
        'fid': file_id,
        'folder_id': folder_id,
        'file_chk': file_chk,
        'mb': mb,
        'token': '0',   # 通过getTokenId()获取的token
        'app': app,
        'acheck': '1',  # 实际值需根据页面元素判断
        'verifycode': '',
        'rd': str(random.random())
    }
    # 使用urlencode函数将参数字典转换为URL编码的查询字符串
    query_string = urllib.parse.urlencode(params)
    # 将查询字符串添加到API服务器地址
    url = f"{api_server}/get_file_url.php?{query_string}"

    cookie_str = 'pass_f1244466878=2657; sessionid=1716530008570; PHPSESSID=t033h89c3e2djrcg1dorj5o938; ua_checkmutilogin=zGYxPnGJNv; pubcookie=Xj0DNA05AWxTYQZmAWQFbVYNATUAXFAOVHNcdgdsUz1fbg4-AT0FYgIyAF0EJAUkUWtVbQZjAW5UNFdEAzgHNV4-AywNYgE7UzsGWwFnBWlWNQE3AGBQNFQ0XDcHPFNjXwAOagE0BWYCNQAwBGMFbFEyVWMGMAE1VGVXZQNoBzVebQNnDTcBYVNlBmIBYAVuVmIBOABmUDJUN1w8Bz9TMV8-; ct_uid=bc53f479ebc63f1cbee8caae0bcf554e'
    # 使用分号和等号将字符串分割为键值对
    cookie_pairs = [pair.strip().split("=", 1) for pair in cookie_str.split(";")]
    # 将键值对转换为字典
    cookies = {pair[0]: pair[1] for pair in cookie_pairs}

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.95 Safari/537.36 QIHU 360SE'}

    response = requests.get(url, headers=headers, cookies=cookies)
    data = response.json()

    # 根据data.code处理不同情况
    if data['code'] == 200:
        # 下载文件
        download_url = data['downurl']
        file_name = data['file_name']
        print("download_url", download_url)
        print("file_name", file_name)
        file_name = 'aaass.zip'

        with requests.get(download_url, stream=True) as r:
            r.raise_for_status()  # 如果响应状态码不是200，将抛出异常
            with open(file_name, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    # 使用iter_content逐步下载文件，适合大文件
                    if chunk:  # filter out keep-alive new chunks
                        f.write(chunk)


if __name__ == '__main__':
    # 调用示例
    get_file_url(1244466878, 0, 'ffe60dd8d9a079fd9e92b3e9d2e648ca', '0', '0')

