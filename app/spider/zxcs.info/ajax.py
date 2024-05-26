import logging
import os
from tqdm import tqdm
import requests
from utils.db_util import *

"""
zxcs 通过ajax获取文件
"""

logging.basicConfig(
    filename='log/zxcs_ajax.log',
    filemode='w',
    # stream=sys.stdout,
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(module)s:%(funcName)s:%(lineno)d - %(message)s'
    , encoding='utf-8'
)


def fetch_download_url(book_id):
    """
    ajax 请求 获取下载地址
    """
    # 目标URL
    ajax_url = 'https://www.zxcs.info/download1.php'
    # POST数据
    data = {'id': book_id}
    # 发送POST请求
    response = requests.post(ajax_url, data=data)
    # 检查请求是否成功
    if response.status_code == 200:
        # 假设服务器返回的是直接拼接后的完整下载URL
        download_url = "https://down.zxcs.info" + response.text.strip().replace("\\", "/")
        # https://down.zxcs.info/upload/2024/04/wltygjn,mjle.zip
        # https://down2.zxcs.info/upload/2024/04/wltygjn,mjle.zip
        return response.text.strip(), download_url
    else:
        logging.debug(f"请求失败，状态码:{response.status_code}")
        return None, None


def download_file(book_id, book_path):
    # 创建目录，exist_ok=True避免异常
    os.makedirs(book_path, exist_ok=True)
    file_name, url = fetch_download_url(book_id)
    if not file_name:
        logging.debug(f"{book_id} 获取下载地址异常！！")
        cursor.execute(
            "update book_list_zxcs set down_type='99' where book_id=%s", book_id)
        conn.commit()
    r = to_download(url, file_name, book_path, book_id)
    if not r:
        # down.zxcs.info
        r = to_download(url.replace("down.zxcs.info", "down2.zxcs.info"), file_name, book_path, book_id)
        if not r:
            logging.debug(f"{book_id} 无普通下载~~")
            cursor.execute(
                "update book_list_zxcs set down_type='02' where book_id=%s", (book_id,))
            conn.commit()


def to_download(url, file_name, book_path, book_id):
    file_name = file_name.replace("\\", "_").replace("/", "_")
    file_path_name = os.path.join(book_path, file_name)
    logging.debug(f"正在下载文件 {file_path_name}，url={url}")
    with requests.get(url, stream=True) as r:
        # r.raise_for_status()  # 如果响应状态码不是200，将抛出异常
        if r.status_code == 200:
            with open(file_path_name, 'wb') as f:
                logging.debug(f"开始下载：{file_path_name}")
                for chunk in r.iter_content(chunk_size=1024 * 1024 * 2):
                    logging.debug(f"下载片段开始：{file_path_name}")
                    # 使用iter_content逐步下载文件，适合大文件
                    if chunk:  # filter out keep-alive new chunks
                        f.write(chunk)
                    logging.debug(f"下载片段结束：{file_path_name}")
                logging.debug(f"下载完成：{file_path_name}")
                cursor.execute(
                    "update book_list_zxcs set down_url=%s,down_flag=1,"
                    "finish_flag=2,down_type='01',file_name=%s,file_path=%s where book_id=%s",
                    (url, file_name, book_path, book_id))
                conn.commit()
                return True
        else:
            # 直接下载连接不存在，需使用网盘下载
            # 更新数据库
            return False


if __name__ == '__main__':
    db_manager = DatabaseManager()
    conn = db_manager.get_conn()
    cursor = conn.cursor()
    try:
        cursor.execute("select book_id from book_list_zxcs where down_type='00' order by book_id ")
        rows = cursor.fetchall()
        # i = 0  # 测试
        for row in tqdm(rows):
            # if i >= 2:
            #     break
            # i += 1
            bid = row[0]
            logging.debug(f"开始下载数据编号： {bid}")
            download_file(bid, 'D:/temp/zxcs')
            conn.commit()
    except Exception as e:
        logging.debug(e, exc_info=True)
    finally:
        db_manager.close_conn()
    logging.debug("任务完成！")
    print("任务完成！")
