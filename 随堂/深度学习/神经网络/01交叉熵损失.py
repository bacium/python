import torch

# 创建一个张量，表示真实值
y_true = torch.tensor([[1, 0, 0], [0, 1, 0], [1, 0, 0]], dtype=torch.float32)

# 创建一个张量，表示预测值
y_pred = torch.tensor(
    [[0.9, 0.1, 0.1], [0.1, 0.9, 0.1], [0.1, 0.1, 0.9]], dtype=torch.float32
)
# 创建一个交叉熵损失函数
loss_fn = torch.nn.CrossEntropyLoss(reduction="sum")

# 计算损失
loss = loss_fn(y_pred, y_true)
print(f"损失值loss:{loss}")
