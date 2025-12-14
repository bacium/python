"""
1 导包 从sklearn导入线性回归的包
2 准备数据集(包括:训练集特征,训练集标签,测试集特征)
3 创建模型对象
4 模型训练
5 使用模型预测测试集标签,
6 查看训练结果

"""

# 1 导包
from sklearn.neighbors import KNeighborsRegressor

# 2 准备数据集(包括:训练集特征,训练集标签,测试集特征)
x_train = [[0, 1, 2], [1, 0, 1], [2, 1, 0], [0, 2, 1], [1, 2, 0], [2, 0, 1]]
y_train = [0, 1, 1, 1, 0, 1]
x_test = [[1, 1, 1]]

# 3 创建模型对象
model = KNeighborsRegressor(n_neighbors=3)

# 4 模型训练
model.fit(x_train, y_train)

# 5 使用模型预测测试集标签,
y_pre = model.predict(x_test)
print("预测结果:", y_pre)
