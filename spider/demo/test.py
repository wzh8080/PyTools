import time

from tqdm import tqdm

# 假设list_items是一个很大的列表
list_items = range(100)

for item in tqdm(list_items):
    # 对item进行某种处理
    time.sleep(0.01)  # 模拟耗时操作

