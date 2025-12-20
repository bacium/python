"""
使用Pytorch完成以下操作：
"""
# 1.导入pytorch包（__）
import torch

# 2.创建一个空的5x3张量 （__）
t1 = torch.zeros([5, 3])
print(f"t1{t1}")
# 3.创建一个随机初始化的5x3张量（__）
t2 = torch.randint(0, 10, [5, 3])
print(f"t2{t2}")
# 4.创建一个5x3的0张量，类型为long（__）
t3 = torch.zeros([5, 3], dtype=torch.long)
print(f"t3{t3.dtype}")
# 5.直接从数组创建张量（__）
t4 = torch.tensor([[1, 2, 3], [4, 5, 6]])
print(f"t4{t4}")
# 6.创建一个5x3的单位张量，类型为double（__）
t5 = torch.ones([5, 3],dtype=torch.double)
print(f"t5{t5}")
# 7.从已有的张量创建相同维度的新张量，并且重新定义类型为float（__）
t6 = t4.float()
print(f"t6{t6}")
# 8.打印一个张量的维度（__）
print(f"t4.shape:{t4.shape}")
# 9.将两个张量相加（__）
t7 = t1 + t2
print(f"t7{t7}")
# 10.取张量的第一列（__）
print(f"第一列:{t4[:, 0]}")
# 11.将一个4x4的张量resize成一个一维张量（__）
t_1 = torch.tensor([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]])
t_2 = t_1.view(-1)
print(f"t_2{t_2}")

# 12.将一个4x4的张量，resize成一个2x8的张量（__）
t_3 = torch.tensor([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]])
t_4 = t_3.view(2, 8)
print(f"t_4{t_4}")
