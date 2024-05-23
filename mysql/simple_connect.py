import mysql.connector
from mysql.connector import Error
from utils.db_util import load_db_config

# 从配置文件中获取数据库连接信息
db_config = load_db_config()
host = db_config['host']
database = db_config['database']
user = db_config['user']
password = db_config['password']

connection = None  # 先初始化connection为None

try:
    # 创建数据库连接
    connection = mysql.connector.connect(
        host=host,  # 数据库主机地址，例如 'localhost' 或 '127.0.0.1'
        database=database,  # 数据库名称
        user=user,  # 数据库用户名
        password=password  # 数据库密码
    )

    if connection.is_connected():
        db_info = connection.get_server_info()
        print(f"成功连接到MySQL Server，版本：{db_info}")
        cursor = connection.cursor()

        # 执行SQL查询，例如：
        cursor.execute("SELECT DATABASE();")
        record = cursor.fetchone()
        print(f"当前数据库：{record}")

        # 记得关闭游标和连接
        cursor.close()
except Error as e:
    print(f"连接失败：{e}")
finally:
    if connection.is_connected():
        connection.close()
        print("MySQL连接已关闭")
