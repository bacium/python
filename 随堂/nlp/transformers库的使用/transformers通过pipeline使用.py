from transformers import pipeline
import torch
import numpy as np
import os


def dm1():
    # 1 使用中文预训练模型chinese_sentiment
    # 模型下载地址 git clone https://huggingface.co/techthiyanes/chinese_sentiment
    # 2 实例化pipeline对象
    # path = os.getcwd()
    # print(path)
    # 检查模型路径是否存在
    model_dir = "../../../models/chinese_sentiment"
    if os.path.exists(model_dir):
        print(f"✓ 模型路径存在: {os.path.abspath(model_dir)}")
        print(f"✓ 模型文件夹内容: {os.listdir(model_dir)}")
    else:
        print(f"✗ 模型路径不存在: {os.path.abspath(model_dir)}")
    my_model = pipeline(task='sentiment-analysis', model=model_dir)
    # print(my_model)
    result = my_model.predict("测试数据，你是谁")
    print(result)


# # 3 文本送给模型 进行文本分类
# output = my_model('我爱北京天安门，天安门上太阳升。')
# print('output--->', output)


if __name__ == '__main__':
    dm1()
    # pass
