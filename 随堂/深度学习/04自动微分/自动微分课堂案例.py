import torch

# 创建一个可求导的张量w，初始值为10
w=torch.tensor(10,requires_grad=True,dtype=torch.float32)
print(f"初始值w:{w}")
# 计算损失函数，这里是w的平方
loss=w**2

# 对损失函数求导，并计算梯度
loss.mean().backward()
print(f"w.grad:{w.grad}")


# 使用梯度下降法更新参数w，学习率为0.01
w=w-0.01*w.grad

print(f"新值w:{w:.5f}")














