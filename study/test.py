height = float(input("请输入身高(m):"))
weight = float(input("请输入体重(Kg):"))

bmi = weight / height ** 2

if bmi < 18.5:
    print("细狗,经历过饥荒？")
elif 18.5 <= bmi < 25:
    print("猛男")
elif 25 <= bmi < 28:
    print("机车")
elif 28 <= bmi < 32:
    print("重卡")
elif bmi >= 32:
    print("饥荒制造者")

