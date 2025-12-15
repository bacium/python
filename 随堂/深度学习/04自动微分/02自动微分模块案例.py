"""
随堂.深度学习.04自动微分.02自动微分模块案例 的 Docstring
"""

import torch

# 初始化参数w，设置requires_grad=True以启用自动微分
w = torch.tensor(10, requires_grad=True, dtype=torch.float32)

# 计算损失函数值，这里使用的是二次函数 loss = w^2 + 20
loss = w**2 + 20

# 使用梯度下降法进行100次迭代优化
for i in range(1,101):
    # 重新计算损失函数值
    loss = w**2 + 20
    # 如果存在梯度，则清零梯度缓存
    if w.grad is not None:
        w.grad.zero_()
    # 反向传播计算梯度
    loss.sum().backward()
    # 使用梯度下降更新参数，学习率为0.01
    w.data = w.data - 0.01 * w.grad
    # 打印当前迭代次数、参数值、梯度和损失值
    print(f"数据{i}：{w.data:.5f},梯度{w.grad:.5f},损失值{loss.sum():.5f}")
# 输出最终优化结果
print(f"结果：{w.data:.5f}")