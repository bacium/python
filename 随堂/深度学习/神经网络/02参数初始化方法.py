"""
随堂.深度学习.神经网络.02参数初始化方法 的 Docstring
"""

"""
  1.随机均匀初始化
  2.随机正态初始化
  3.全0初始化
  4.全1初始化
  5.Xavier初始化
  6.Kaiming初始化
  7.固定值初始化
"""

import torch


# 随机均匀初始化
def uniform_init():
    # 创建一个全连接层
    linear = torch.nn.Linear(in_features=5, out_features=3, bias=True)
    # 均匀分布初始化
    torch.nn.init.uniform_(linear.weight)
    print(f"均匀分布初始化权重:{linear.weight}")
    print(f"均匀分布初始化截距:{linear.bias}")


# 正态分布初始化
def normal_init():
    # 创建一个全连接层
    linear = torch.nn.Linear(in_features=5, out_features=3, bias=True)
    # 正态分布初始化
    torch.nn.init.normal_(linear.weight)
    print(f"正态分布初始化权重:{linear.weight}")
    print(f"正态分布初始化截距:{linear.bias}")


# 全0初始化
def allZero_init():
    # 创建一个全连接层
    linear = torch.nn.Linear(
        in_features=5,
        out_features=3,
    )
    # 全0初始化
    torch.nn.init.zeros_(linear.weight)
    print(f"全0初始化的权重:{linear.weight}")
    print(f"全0初始化的截距:{linear.bias}")


# 全1初始化
def allOne_init():
    # 创建一个全连接层
    linear = torch.nn.Linear(in_features=5, out_features=3)
    # 全1初始化
    torch.nn.init.ones_(linear.weight)
    print(f"全1初始化的权重:{linear.weight}")
    print(f"全1初始化的截距:{linear.bias}")


# Xavier初始化
def xavier_init():
    # 创建一个全连接层
    linear1 = torch.nn.Linear(5, 3)
    linear2 = torch.nn.Linear(5, 3)
    # xavier正态分布初始化
    torch.nn.init.xavier_normal_(linear1.weight)
    # xavier均匀分布初始化
    torch.nn.init.xavier_uniform_(linear2.weight)
    print(f"xavier正态分布初始化权重:{linear1.weight}")
    print(f"xavier正态分布初始化截距:{linear1.bias}")
    print(f"xavier均匀分布初始化权重:{linear2.weight}")
    print(f"xavier均匀分布初始化截距:{linear2.bias}")


# kaiming初始化
def kaiming_init():
    linear1 = torch.nn.Linear(5, 3)
    linear2 = torch.nn.Linear(5, 3)
    # kaiming正态分布初始化
    torch.nn.init.kaiming_normal_(linear1.weight)
    # kaiming均匀分布初始化
    torch.nn.init.kaiming_uniform_(linear2.weight)
    print(f"kaiming正态分布初始化权重:{linear1.weight}")
    print(f"kaiming正态分布初始化截距:{linear1.bias}")
    print(f"kaiming均匀分布初始化权重:{linear2.weight}")
    print(f"kaiming均匀分布初始化截距:{linear2.bias}")


# 固定值初始化
def constant_init():
    # 创建一个全连接层
    linear = torch.nn.Linear(5, 3)
    # 固定值初始化 权重 固定值
    torch.nn.init.constant_(linear.weight, 1.6)
    print(f"固定值初始化权重:{linear.weight}")
    print(f"固定值初始化截距:{linear.bias}")


if __name__ == "__main__":
    # uniform_init()
    # normal_init()
    # allZero_init()
    # allOne_init()
    # xavier_init()
    # kaiming_init()
    constant_init()
