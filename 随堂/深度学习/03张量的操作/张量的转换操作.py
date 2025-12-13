"""
随堂.深度学习.03张量的操作.张量的转换操作 的 Docstring
"""

"""
  张量的转换操作:
        torch.view(input, *shape)
        **input**:输入张量
        **shape**:转换后的张量形状
        返回转换后的张量
    torch.contiguous(input)
        **input**:输入张量
        返回一个连续的张量
    torch.is_contiguous(input)
        **input**:输入张量
        返回一个布尔值,判断张量是否连续


"""

import torch

torch.manual_seed(100)

t1 = torch.randint(1, 10, size=(2, 3, 4))
print(t1)
print(f"t1.shape:{t1.shape},t1.size():{t1.size()}")
print(f"t1是否连续:{t1.is_contiguous()}")

# 使用view转换维度
"""
  view函数:
    **input**:输入张量
    **shape**:转换后的张量形状
    返回转换后的张量

"""
# 写法一

# t2 =torch.view(t1, 4, 6) 报错
# print(t2)
# print(f"t2.shape:{t2.shape},t2.size():{t2.size()}")
# print(f"t2是否连续:{t2.is_contiguous()}")


# 写法二
t3 = t1.view(4, 6)
print(t3)
print(f"t3.shape:{t3.shape},t3.size():{t3.size()}")
print(f"t3是否连续:{t3.is_contiguous()}")


""""
  使用contiguous()函数
      **input**:输入张量
      返回一个连续的张量

"""
t4 = t1.transpose(1, 0)
print(f"t4{t4}")
print(f"t4.shape:{t4.shape},t4.size():{t4.size()}")
print(f"t4是否连续:{t4.is_contiguous()}")  # 此时t4不连续

print("*" * 70)

t5 = t4.contiguous().view(6, 4)
print(t5)
print(f"t5.shape:{t5.shape},t5.size():{t5.size()}")
print(f"t5是否连续:{t5.is_contiguous()}")  # 连续
