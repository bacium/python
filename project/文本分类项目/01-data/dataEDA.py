import pandas as pd
from config import Config
from collections import Counter  # 聚合
import seaborn as sns
import matplotlib.pyplot as plt

# todo:1-实例config类对象, 获取文件路径属性
config = Config()


def dataEDA(path):
    # todo:2-加载数据集
    data = pd.read_csv(path, sep='\t', names=['text', 'label'])
    print('查看前5条数据--->\n', data.head())
    # todo:3-探索性数据分析 EDA
    # 数据集行列数
    print('查看数据集的行列数--->\n', data.shape)
    # 数据集基本信息
    data.info()
    print('=' * 80)

    # 不同标签的样本数/占比
    label_counts = Counter(data['label'])  # 分组聚合
    print('不同标签的样本数--->\n', type(label_counts), label_counts)
    for label, count in label_counts.items():
        print(f'标签{label}的样本数是{count}')

    data_len = len(data)
    for label, count in label_counts.items():
        ratio = (count / data_len) * 100
        print(f'标签{label}的样本占比是{ratio:.2f}%')

    plt.figure(figsize=(16, 8))
    sns.countplot(data=data, x='label')
    plt.show()

    print('=' * 80)
    # 文本长度统计 平均值/标准差/最大值/最小值
    # 增加一列文本字符长度列
    data['text_length'] = data['text'].str.len()
    print(data.head())
    plt.figure(figsize=(16, 8))
    sns.countplot(data=data, x='text_length')
    plt.show()
    print('文本平均长度--->\n', data['text_length'].mean())
    print('文本长度标准差--->\n', data['text_length'].std())
    print('文本最大长度--->\n', data['text_length'].max())
    print('文本最小长度--->\n', data['text_length'].min())


if __name__ == '__main__':
    train_datapath = config.train_datapath
    test_datapath = config.test_datapath
    dataEDA(train_datapath)
    dataEDA(test_datapath)
