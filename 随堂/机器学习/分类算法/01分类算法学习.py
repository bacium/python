"""
随堂.机器学习.分类算法.01分类算法学习 的 Docstring
    描述:分类算法学习
      实现思路
        1.导包
        2.准备数据集(包括:训练集特征,训练集标签,测试集特征)
        3.创建模型对象
        4.模型训练
        5.使用模型预测测试集标签,
        6.打印模型预测结果
      分类算法默认使用欧式距离计算各样本特征之间的距离.
"""

# 1.导包
from sklearn.neighbors import KNeighborsClassifier

# 2. 准备数据集(包括:训练集特征,训练集标签,测试集特征)
x_train = [[1], [2], [3], [4], [5]]  # 训练集会有多个特征,所以一般使用数组嵌套数组的方式
y_train = [0, 1, 1, 1, 1]  # 训练集标签,标签只有一个,所以使用一维数组即可
x_test = [[6]]  # 测试集特征,和训练集特征保持一致.

# 3.创建模型对象
model = KNeighborsClassifier(n_neighbors=3)

# 4.模型训练
model.fit(x_train, y_train)


# 5.使用模型预测测试集标签,
y_pre = model.predict(x_test)

print("预测结果:", y_pre)
