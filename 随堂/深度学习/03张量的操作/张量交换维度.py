"""
交换张量维度:
  1.torch.transpose(input, dim0, dim1)
    **input**:输入张量
    **dim0**:交换的维度0
    **dim1**:交换的维度1
    返回交换后的张量
  2.torch.permute(input, *dims)
    **input**:输入张量
    **dims**:交换的维度
    返回交换后的张量

"""

import torch

torch.manual_seed(100)

t1 = torch.randint(1,10,size=(2, 3,4))
print(t1)
print(f"t1.shape:{t1.shape},t1.size():{t1.size()}")

print("="*70 )


# 使用transpose交换位置
#写法1
t2 = torch.transpose(t1,0,1) # 将t1的维度0和1进行交换
print(t2)
print(f"t2.shape:{t2.shape},t2.size():{t2.size()}")
# 写法2
t3=t1.transpose(0,1) # 将t1的维度0和1进行交换
print(t3)
print(f"t3.shape:{t3.shape},t3.size():{t3.size()}")


# 使用permute交换位置
# 写法1
t4 = torch.permute(t1, (1,2,0))
print(t4)
print(f"t4.shape:{t4.shape},t4.size():{t4.size()}")


# 写法2
t5=t1.permute(1,2,0)
print(t5)
print(f"t5.shape:{t5.shape},t5.size():{t5.size()}")
