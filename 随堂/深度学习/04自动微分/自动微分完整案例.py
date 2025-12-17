import torch

# 准备数据
x = torch.randn(size=(2, 5), dtype=torch.float32)
print(f"x:{x}")

y = torch.randn(size=(2, 3), dtype=torch.float32)
print(f"y:{y}")
w = torch.randn(size=(5, 3), dtype=torch.float32, requires_grad=True)
print(f"w:{w}")
b = torch.tensor(3, dtype=torch.float32, requires_grad=True)
print(f"b:{b}")

# 矩阵相乘,使用z = x @ w + b
# 
z = x.matmul(w) + b
print(f"z:{z}")
# 定义损失函数
loss_fn = torch.nn.MSELoss()
# 计算损失值
loss = loss_fn(z, y)  # z预测值，y真实值=====>使用z和y计算两个值之间的差距

loss.mean().backward()  # 开启梯度下降,反向传播更新w和b

w.data = w.data - 0.01 * w.grad
print(f"w:{w}")
b.data = b.data - 0.01 * b.grad
print(f"b:{b},b.grad:{b.grad}")
print(f"w.grad:{w.grad}")
print(f"loss:{loss}")
