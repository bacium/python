import torch

# 初始化参数w，设置requires_grad=True以启用自动微分
w = torch.tensor(10, requires_grad=True, dtype=torch.float32)
print(f"初始值w:{w}")


# 梯度下降迭代优化过程
# 使用简单的二次函数 loss = 2*w^2 进行100次梯度下降
for i in range(1, 101):
    # 计算损失函数
    loss = 2 * w**2
    # 清零梯度累积
    if w.grad is not None:
        w.grad.zero_()
    # 反向传播计算梯度
    loss.mean().backward()
    # 更新参数w（学习率为0.01）
    w.data = w.data - 0.01 * w.grad
    print(f"梯度:{w.grad},w的值{w},损失函数:{loss.mean():.5f}")
# 输出最终优化结果
print(f"新值w:{w:.5f}")