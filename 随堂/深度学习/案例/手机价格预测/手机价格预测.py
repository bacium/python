import time

import numpy as np
import pandas as pd
import torch
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from torch.utils.data import TensorDataset, DataLoader


def load_data_source(batch_size):
    """
    加载数据集对象
    :param batch_size: 批次大小
    :return:
    """
    data = pd.read_csv("./data/手机价格预测.csv")
    x = data.iloc[:, :-1]
    y = data.iloc[:, -1]
    x = x.astype(np.float32)
    y = y.astype(np.int64)
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
    astmater = StandardScaler()
    x_train = astmater.fit_transform(x_train)
    x_test = astmater.transform(x_test)

    trainDataSet = TensorDataset(torch.from_numpy(x_train), torch.from_numpy(y_train.values))
    testDataSet = TensorDataset(torch.from_numpy(x_test), torch.from_numpy(y_test.values))

    trainDataLoder = DataLoader(dataset=trainDataSet, batch_size=batch_size, shuffle=True)
    testDataLoder = DataLoader(dataset=testDataSet, batch_size=batch_size, shuffle=True)
    return trainDataLoder, testDataLoder, x_train.shape[1], len(y_train.unique())


class MobilePricePrediction(torch.nn.Module):
    def __init__(self, input_size, output_size):
        super().__init__()
        self.lear1 = torch.nn.Linear(input_size, 128)
        self.lear2 = torch.nn.Linear(128, 256)
        self.out = torch.nn.Linear(256, output_size)
        torch.nn.init.kaiming_normal_(self.lear1.weight)
        torch.nn.init.kaiming_uniform_(self.lear2.weight)

    def forward(self, x):
        x = torch.relu(self.lear1(x))
        x = torch.relu(self.lear2(x))
        x = self.out(x)
        return x


def train_model(train_dataloader, model, epochs):
    model.train()  # 训练模式
    # 创建损失函数对象
    criterion = torch.nn.CrossEntropyLoss()
    # 创建优化器对象
    optimazer = torch.optim.Adam(model.parameters(), lr=0.001)
    # 循环轮次
    for epoch in range(epochs):
        total_loss, batch_cnt, start = 0.0, 0, time.time()
        for batch_x, batch_y in train_dataloader:
            y_pred = model(batch_x)
            loss = criterion(y_pred, batch_y)
            total_loss += loss.item()
            batch_cnt += 1
            optimazer.zero_grad()
            loss.backward()
            optimazer.step()
        print("轮次: {}, 损失值: {:.4f}, 时间: {:.4f}".format(epoch + 1, total_loss / batch_cnt, time.time() - start))
    import os
    save_dir = "model"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    torch.save(model.state_dict(), "model/手机价格预测模型_新.pth")
    print("保存模型成功")


def exal_model(testDataLoder, input_size, output_size):
    model = MobilePricePrediction(input_size, output_size)
    model.load_state_dict(torch.load("model/手机价格预测模型_新.pth"))
    model.eval()
    correct = 0
    for batch_x, batch_y in testDataLoder:
        with torch.no_grad():
            y = model(batch_x)
            y_pred = torch.argmax(y, dim=1)
            correct += (y_pred == batch_y).sum()
    print(f'Acc: {(correct / len(testDataLoder.dataset)):.4f}')


if __name__ == '__main__':
    batch_size = 8
    # 1 加载数据集对象
    trainDataLoder, testDataLoder, input_size, output_size = load_data_source(batch_size)
    # print(trainDataLoder, testDataLoder, input_size, output_size)
    # for item in trainDataLoder:
    #     print(item)
    #     break
    # 2 创建模型
    model = MobilePricePrediction(input_size, output_size)
    # print( model)
    # 3 训练模型
    epochs = 34
    train_model(trainDataLoder, model, epochs)
    # 4 模型评估
    exal_model(testDataLoder, input_size, output_size)
