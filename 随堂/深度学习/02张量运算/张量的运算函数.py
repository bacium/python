"""
    张量的运算函数主要有:
    sum,mean,sqrt,pow,exp,log

    **dim**参数说明:取值0为列,1为行
"""
import torch

torch.manual_seed(100)

t1 = torch.randn(size=(2, 3))
print(t1)

# sum 求和:即将所有元素相加
print(torch.sum(t1))

# mean 求均值:
t2 = torch.mean(t1, dim=1)
print(f"行平均值:{t2}")
t3=torch.mean(t1, dim=0)
print(f"列平均值:{t3}")



# sqrt 平方根

t_init=torch.randint(0,10,(2,3))
print(f"平方根:{torch.sqrt(t_init)}")

print("="*70)
# pow 指数
print(f"指数1:{torch.pow(t_init,2)}")
print(f"指数2:{t_init**2}")
print("="*70)
# exp
print(f"指数:{torch.exp(t_init)}")

print("="*70)
# log
print(f"对数:{torch.log(t_init)}")




