class Account(object):
    def __init__(self, name, balance):
        self.name = name
        self.balance = balance

    #     取款方法
    def deposit(self, amount):
        if (self.balance - amount) < 0:
            print("老铁,余额不足,晚上带斧头去银行提款啊")
        else:
            self.balance -= amount
            print("走,抽烟喝酒烫头")

    # 存款
    def withhdraw(self, amount):
        self.balance += amount

    def __str__(self):
        print(f"当前用户:{self.name}的余额为:{self.balance}")


if __name__ == "__main__":
    coast = Account("张三", 1000)
    # 存10000
    coast.withhdraw(10000)
    # 取1000
    coast.deposit(1001)
