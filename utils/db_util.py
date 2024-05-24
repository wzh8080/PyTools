import os
from configparser import ConfigParser
from pathlib import Path
import mysql.connector
from mysql.connector import Error

# 使用环境变量或配置文件来获取配置
# DB_CONFIG_PATH = os.getenv('DB_CONFIG_PATH', 'etc/db_config.ini')
DB_CONFIG_PATH = 'etc/db_config.ini'


# 数据库连接类
class DatabaseManager:
    def __init__(self):
        self.conn = None
        self.load_db_config()

    def load_db_config(self):
        """
        读取并返回数据库配置信息。
        """
        # config_path = Path(DB_CONFIG_PATH)
        config_path = get_config_path(DB_CONFIG_PATH)

        config = ConfigParser()
        config.read(str(config_path))

        try:
            db_config = config['Database']
            print("加载数据库配置成功..")
        except KeyError:
            print(f"异常 Error : 'Database' section not found in the configuration file at {config_path}")
            raise

        self.conn = mysql.connector.connect(
            host=db_config['host'],  # 数据库主机地址，例如 'localhost' 或 '127.0.0.1'
            database=db_config['database'],  # 数据库名称
            user=db_config['user'],  # 数据库用户名
            password=db_config['password'],  # 数据库密码
            autocommit=False  # 禁用自动提交
        )

    def get_conn(self):
        if self.conn is None:
            print('新建数据源...')
            self.load_db_config()
        return self.conn

    def close_conn(self):
        if self.conn is not None:
            self.conn.close()
            print('数据源已关闭')



def get_config_path(relative_path):
    # 获取当前脚本所在的目录
    current_dir = Path(__file__).resolve().parent.parent
    # 结合相对路径得到配置文件的完整路径
    return current_dir / relative_path


def batch_insert_once(db, table_name, columns, values):
    """
    批量插入数据到数据库。
    """
    try:
        with db.get_conn() as conn, conn.cursor() as cursor:
            placeholders = ', '.join(['%s'] * len(columns))
            query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"
            cursor.executemany(query, values)
            conn.commit()
            print(f"{len(values)} rows inserted into {table_name} successfully.")
    except Error as e:
        print(f"Error: {e}")
        if conn:
            conn.rollback()


def batch_insert(conn, table_name, columns, values):
    """
    批量插入数据到数据库。
    """
    try:
        cursor = conn.cursor()
        # with db.get_conn() as conn, conn.cursor() as cursor:
        placeholders = ', '.join(['%s'] * len(columns))
        query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"
        cursor.executemany(query, values)
        conn.commit()
        print(f"{len(values)} rows inserted into {table_name} successfully.")
    except Error as e:
        print(f"Error: {e}")
        if conn:
            conn.rollback()
# 示例使用
# db_manager = DatabaseManager()
# batch_insert('your_table_name', ['column1', 'column2'], [(value1, value2), (value3, value4)])
