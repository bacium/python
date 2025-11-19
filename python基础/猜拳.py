import random

# 生成随机数
target_num = random.randint(1, 10)

# 猜数次数
count = 3
print("中奖号码:", target_num)
while True:
    if 1 <= count <= 3:
        count -= 1
        cust_num = int(input("老登,你猜多少?"))
        if cust_num == target_num:
            print("恭喜啊,老登!")
            break
    else:
        print("机会已用完,请打钱复活!")
        break
