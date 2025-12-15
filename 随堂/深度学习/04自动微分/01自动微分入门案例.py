"""
随堂.深度学习.04自动微分.01自动微分入门案例 的 Docstring
"""

import torch

"""
    创建一个变量w，并设置requires_grad=True，表示w需要计算梯度
        参数说明:
            参数1：数据
            参数2：是否需要计算梯度
            参数3：数据类型  
"""
w = torch.tensor(10, requires_grad=True, dtype=torch.float32)

# 损失函数
loss = 2 * w**2  # 导数:4w

# 计算梯度并反向传播
loss.sum().backward()

# 更新参数
w = w - 0.01 * w.grad
# 打印参数
print(w)
