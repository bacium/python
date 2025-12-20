"""
    Mobile Price Prediction

"""
import time

import numpy as np
import pandas as pd
import torch
from sklearn.model_selection import train_test_split
from torch.utils.data import TensorDataset, DataLoader


# 加载数据集对象
def load_data_source(batch_size):
    """
    加载数据集对象
    :param batch_size: 批次大小
    :return:
    """
    dataSource = pd.read_csv("./data/手机价格预测.csv")
    # print(dataSource.head())
    x = dataSource.iloc[:, :-1]
    y = dataSource.iloc[:, -1]
    # print(x_train,y_train)
    # print("前面", x_train.dtypes, y_train.dtypes)
    x = x.astype(np.float32)
    y = y.astype(np.int64)
    # print("后面", x_train.dtypes, y_train.dtypes)
    # 分割数据
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
    # 转换为张量, 并创建数据集对象
    trainDataSet = TensorDataset(torch.from_numpy(x_train.values), torch.from_numpy(y_train.values))
    testDataSet = TensorDataset(torch.from_numpy(x_test.values), torch.from_numpy(y_test.values))
    # print(trainDataSet)
    # print(trainDataSet[0])
    trainDataLoder = DataLoader(dataset=trainDataSet, batch_size=batch_size, shuffle=True)
    testDataLoder = DataLoader(dataset=testDataSet, batch_size=batch_size, shuffle=True)
    return trainDataLoder, testDataLoder, x_train.shape[1], len(y_train.unique())


# 构建神经网络
class MobilePricePrediction(torch.nn.Module):
    def __init__(self, input_size, output_size):
        # 调用父级对象的初始化方法
        super().__init__()
        # 构建隐藏层
        self.linear1 = torch.nn.Linear(input_size, 128)
        self.linear2 = torch.nn.Linear(128, 256)
        # 输出层
        self.out = torch.nn.Linear(256, output_size)

        # 实例化dropout层
        self.Dropout = torch.nn.Dropout(p=0.2)
        # 初始化参数
        # torch.nn.init.xavier_uniform_(self.linear1.weight)
        # torch.nn.init.xavier_uniform_(self.linear2.weight)
        torch.nn.init.kaiming_normal_(self.linear1.weight)
        torch.nn.init.kaiming_uniform_(self.linear2.weight)
    def forward(self, x):
        x = torch.relu(self.linear1(x))
        x = torch.relu(self.linear2(x))
        x = self.out(x)
        return x


def train_model(train_dataloader, model, epochs):
    """
    训练模型
    :param train_dataloader: 训练数据集对象
    :param model: 模型对象
    :param epochs: 训练轮次
    :return:
    """
    model.train()  # 训练模式
    # 创建损失函数对象
    criterion = torch.nn.CrossEntropyLoss()
    # 创建优化器对象
    #optimazer = torch.optim.SGD(model.parameters(), lr=0.01)
    optimazer = torch.optim.Adam(model.parameters(), lr=0.001)
    # 循环轮次
    for epoch in range(epochs):
        # 定义初始参数(取日志)
        total_loss, batch_cnt, start = 0.0, 0, time.time()
        # 循环数据集,此处是批次数据
        for batch_x, batch_y in train_dataloader:
            # 正向传播,计算预测值
            y_pred = model(batch_x)
            # 计算损失值
            loss = criterion(y_pred, batch_y)
            total_loss += loss.item()
            batch_cnt += 1
            # 总损失
            total_loss += loss.item()
            # 梯度清零
            optimazer.zero_grad()
            # 反向传播,计算梯度
            loss.backward()
            # 参数更新
            optimazer.step()
        # 单轮平均损失
        epoch_loss = total_loss / batch_cnt
        print("轮次: {}, 损失值: {:.4f}, 时间: {:.4f}".format(epoch + 1, epoch_loss, time.time() - start))
    # 确保保存目录存在
    import os
    save_dir = "model"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    torch.save(model.state_dict(), os.path.join(save_dir, "手机价格预测模型.pth"))


def exal_model(testDataLoder, input_size, output_size):
    """
    模型评估
    :param testDataLoder: 测试数据集对象
    :param input_size: 输入特征维度
    :param output_size: 输出特征维度
    :return:
    """
    # 加载模型
    model = MobilePricePrediction(input_size, output_size)
    # 加载训练好的模型
    model.load_state_dict(torch.load("model/手机价格预测模型.pth"))
    model.eval()  # 切换推理模式
    correct = 0  # 记录正确的数据
    for batch_x, batch_y in testDataLoder:
        with torch.no_grad():  # 上下文管理器, 推理阶段自动关闭梯度计算
            # 模型预测值
            y = model(batch_x)
            # 预测最大值的下标
            y_pred = torch.argmax(y, dim=1)
            correct += (y_pred == batch_y).sum()
    print(f'Acc: {(correct / len(testDataLoder.dataset)):.4f}')


if __name__ == '__main__':
    batch_size = 4
    # 1 加载数据集对象
    trainDataLoder, testDataLoder, input_size, output_size = load_data_source(batch_size)
    # print(trainDataLoder, testDataLoder, input_size, output_size)
    # for item in trainDataLoder:
    #     print(item)
    #     break
    # 2 定义损失函数和优化器
    model = MobilePricePrediction(input_size, output_size)
    # print(model)
    # 3 训练模型
    epochs =100  # 训练轮次
    train_model(trainDataLoder, model, epochs)
    # 4 模型评估
    exal_model(testDataLoder, input_size, output_size)
