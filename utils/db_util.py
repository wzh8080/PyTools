import os
from configparser import ConfigParser
from pathlib import Path


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
    config_path = get_config_path('config/db_config.ini')

    config = ConfigParser()
    config.read(str(config_path))

    try:
        db_config = config['Database']
        print("Database configuration loaded successfully.")
        return db_config
    except KeyError:
        print(f"Error: 'Database' section not found in the configuration file at {config_path}")
        return None


# 调用公共方法来加载数据库配置
# db_conf = load_db_config()
# if db_conf:
#     # 进一步操作，比如使用db_config连接数据库...
#     pass
