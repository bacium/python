from sklearn.neighbors import KNeighborsClassifier

"""
        1 导包 从sklearn导入近邻分类算法的包
        2 准备数据集(包括:训练集特征,训练集标签,测试集特征)
        3 创建模型对象
        4 模型训练 使用训练集特征和标签
        5 使用模型预测测试集标签,
        6 查看训练结果
"""

# 2 准备数据集(包括:训练集特征,训练集标签,测试集特征)
x_train = [
    [1],
    [2],
    [1],
    [5],
]
y_train = [0, 1, 1, 1]
x_test = [[3]]


# 创建模型对象
model = KNeighborsClassifier(n_neighbors=3)
# 模型训练

model.fit(x_train, y_train)

# 使用模型预测测试集标签,
y_pre = model.predict(x_test)


# 查看训练结果
print("预测结果:", y_pre) # [1]
