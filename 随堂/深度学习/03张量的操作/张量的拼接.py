"""
拼接张量:
  torch.cat(tensors, dim=0)
  在指定维度上作拼接,不改变维度数,除了拼接的维度,其他维度必须保持一致
    **tensors**:张量列表
    **dim**:拼接的维度
    返回拼接后的张量
  torch.stack(tensors, dim=0)
  在新维度上做拼接,会改变维度数,所有维度必须保持一致
    **tensors**:张量列表

"""

import torch


t1 = torch.randint(1, 10, size=(2, 3))
t2 = torch.randint(1, 10, size=(2, 3))
print(f"t1:{t1}")
print(f"t2:{t2}")

"""
    dim=0:拼接在维度0上 即拼接在列上
    dim=1:拼接在维度1上 即拼接在行上
"""

t3 = torch.cat([t1, t2], dim=0)
print(f"t3:{t3}")
print(f"t3.shape:{t3.shape},t3.size():{t3.size()}")  # (2,3)+(2,3)=(4,3)


t4 = torch.cat([t1, t2], dim=1)
print(f"t4:{t4}")
print(f"t4.shape:{t4.shape},t4.size():{t4.size()}")  # (2,3)+(2,3)=(2,6)


"""
  torch.stack(tensors, dim=0)
  **tensors**:张量列表
  **dim**:拼接的维度
"""
t5 = torch.stack([t1, t2], dim=0)  # 在新维度上做拼接
print(f"t5:{t5}")
print(f"t5.shape:{t5.shape},t5.size():{t5.size()}")

t6 = torch.stack([t1, t2], dim=1)
print(f"t6:{t6}")
print(f"t6.shape:{t6.shape},t6.size():{t6.size()}")


t7 = torch.stack([t1, t2], dim=2)
print(f"t7:{t7}")
print(f"t7.shape:{t7.shape},t7.size():{t7.size()}")
