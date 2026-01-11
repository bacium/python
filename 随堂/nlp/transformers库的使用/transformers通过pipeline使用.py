from transformers import pipeline
import torch
import numpy as np


def dm1():
    # 1 使用中文预训练模型chinese_sentiment
    # 模型下载地址 git clone https://huggingface.co/techthiyanes/chinese_sentiment

    # 2 实例化pipeline对象
    # techthiyanes/xxx 官网自动下载路径
    # my_model = pipeline(task='sentiment-analysis', model='techthiyanes/chinese_sentiment')
    my_model = pipeline(task='sentiment-analysis', model='model/chinese_sentiment')

    # 3 文本送给模型 进行文本分类
    output = my_model('我爱北京天安门，天安门上太阳升。')
    print('output--->', output)


if __name__ == '__main__':
    # dm1()
    pass

