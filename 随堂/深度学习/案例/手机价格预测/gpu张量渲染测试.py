import torch

# 1. 打印PyTorch版本，确认安装成功
print(f"PyTorch版本: {torch.__version__}")

# 2. 这是最关键的检查！返回True才说明GPU支持已启用
print(f"GPU是否可用: {torch.cuda.is_available()}")

# 3. 查看可用GPU数量
print(f"可用GPU数量: {torch.cuda.device_count()}")

# 4. 如果GPU可用，打印当前GPU的名称
if torch.cuda.is_available():
    print(f"当前GPU名称: {torch.cuda.get_device_name(0)}")
    # (可选) 尝试在GPU上创建一个张量来进一步验证
    x = torch.tensor([1.0, 2.0]).cuda()
    print(f"已创建GPU张量: {x}")
    print(f"张量所在设备: {x.device}")