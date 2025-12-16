import torch

# 创建一个变量x，并设置requires_grad=True，表示x需要计算梯度
x = torch.ones([2, 5], requires_grad=True)
print(f"x:{x}")

# 创建一个变量y
y = torch.zeros(2, 3)
print(f"y:{y}")
# 创建一个变量w
w = torch.randn(5, 3, requires_grad=True, dtype=torch.float)
print(f"w:{w}")
# 创建一个变量b
b = torch.randn(3, requires_grad=True, dtype=torch.float)
print(f"b:{b}")

z = x @ w + b
print(f"z:{z}")

loss_fn = torch.nn.MSELoss()

loss = loss_fn(z, y)

loss.mean().backward()
print(f"w.grad:{w.grad}")

w.data = w.data - 0.01 * w.grad
b.data = b.data - 0.01 * b.grad
print(f"w:{w}")
print(f"b:{b}")


