# 1 导包
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor

# 2 准备数据
x_train = [[1, 2], [1, 3], [1, 4], [2, 1], [2, 2], [2, 3], [3, 1], [3, 2], [3, 3]]
y_train = [0, 0, 0, 1, 1, 1, 2, 2, 2]
x_test = [[2, 2]]
# 3 创建模型
classifier_model = KNeighborsClassifier(n_neighbors=3)
regressor_model = KNeighborsRegressor(n_neighbors=3)

# 4 训练模型
result_classifier = classifier_model.fit(x_train, y_train)
result_regress = regressor_model.fit(x_train, y_train)

# 5 预测结果
print("分类结果:", result_classifier.predict([[3, 4]]))
print("回归结果:", result_regress.predict([[3, 4]]))
