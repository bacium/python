# 生成器
import math

"""
    使用生成器返回批量歌词数据
"""


def generate_self(batch_size):
    with open('./data/lrc.txt', "r", encoding="utf-8") as def_lrc:
        lines = def_lrc.readlines()
        rows = math.ceil(len(lines) / batch_size)  # 越看越像分页
        for i in range(rows):
            # 生成器,调用一次返回对应数据及后续批量数据
            yield lines[i * batch_size:(i + 1) * batch_size]


result = generate_self(3)
print(next(result))  # 调用一次返回对应条数
print(next(result))  # 调用一次返回对应条数
print(next(result))  # 调用一次返回对应条数
