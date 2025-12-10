import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
# 设置显示中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
# 设置正常显示符号
plt.rcParams['axes.unicode_minus'] = False
# plt.switch_backend('TkAgg')
df = pd.read_csv('./data/car_sale.csv')
# print(df)
data = df["ad"].values.reshape(-1,1)
target = df["sale_num"]
# print(data, target)

x_train, x_test, y_train, y_test = train_test_split(data, target, test_size=0.2,random_state=23)
# print(f"训练集特征:{x_train}, 测试集特征 :{x_test}, 训练集标签:{y_train}, 测试集标签:{y_test}")
model = LinearRegression()
model.fit(x_train, y_train)
y_pred = model.predict(data)
print(y_pred)

print(f"准确度{model.coef_}")
print(f"截距{model.intercept_}")

plt.scatter(data, target)
plt.plot(data, y_pred)
plt.title("汽车销售预测")
plt.xlabel("汽车广告")
plt.ylabel("销售数量")
plt.show()




