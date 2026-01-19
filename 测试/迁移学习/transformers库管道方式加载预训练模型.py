"""
    使用Hugging Face 管道方式加载预训练Bert模型进行文本分类任务
"""
from transformers import pipeline


def dm():
    model = pipeline(task='text-classification', model='../../models/chinese_sentiment')
    print("model==========>", model)
    message = "人生得意须尽欢！"
    output = model(message)
    print("output==========>", output)

if __name__ == '__main__':
    dm()
