import os
from configparser import ConfigParser
from pathlib import Path
import mysql.connector
from mysql.connector import Error

# 数据库连接
db_conn = None

def get_config_path(relative_path):
    # 获取当前脚本所在的目录
    current_dir = Path(__file__).resolve().parent.parent
    # 结合相对路径得到配置文件的完整路径
    return current_dir / relative_path


def load_db_config():
    """
    读取并返回数据库配置信息。
    """
    # 使用公共方法获取配置文件路径
    config_path = get_config_path('etc/db_config.ini')

    config = ConfigParser()
    config.read(str(config_path))

    try:
        db_config = config['Database']
        print("Database configuration loaded successfully.")
        return db_config
    except KeyError:
        print(f"Error: 'Database' section not found in the configuration file at {config_path}")
        return None


# 若数据库连接为空的话，返回新的连接
def get_conn():
    global db_conn
    if db_conn is None:
        db_conf = load_db_config()
        print("初始化数据库连接..自动提交(关闭)..")
        # 创建数据库连接
        return mysql.connector.connect(
            host=db_conf['host'],  # 数据库主机地址，例如 'localhost' 或 '127.0.0.1'
            database=db_conf['database'],  # 数据库名称
            user=db_conf['user'],  # 数据库用户名
            password=db_conf['password'],  # 数据库密码
            autocommit=False  # 禁用自动提交
        )
    else :
        return db_conn


def batch_insert(conn: mysql.connector.connect, table_name, columns, values):
    """
    批量插入数据到数据库。
    """
    try:
        cursor = conn.cursor()
        placeholders = ', '.join(['%s'] * len(columns))
        query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"
        cursor.executemany(query, values)
        conn.commit()
        print(f"{len(values)} rows inserted into {table_name} successfully.")
    except Error as e:
        print(f"Error: {e}")
        conn.rollback()

# 调用公共方法来加载数据库配置
# db_conf = load_db_config()
# if db_conf:
#     # 进一步操作，比如使用db_config连接数据库...
#     pass
