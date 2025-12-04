from sklearn.linear_model import LinearRegression

# 训练数据集
x_train = [[160], [180], [170], [190], [165]]
# 训练标签
y_train = [[60.2], [80.1], [70.7], [90.3], [65.9]]
# 测试集数据
x_test = [[186]]
# 创建模型对象
model = LinearRegression()

# 模型训练
model.fit(x_train, y_train)

# 使用模型预测测试集标签,
y_pre = model.predict(x_test)
print("预测结果:", y_pre)
print(f"模型斜率 :{model.coef_}")
print(f"模型截距 :{model.intercept_}")
