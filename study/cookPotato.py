class CookPotato():
    def __init__(self):
        self.cook_time = 0
        self.cook_state = "生的"
        self.condiment = []

    def cook(self, cook_time):
        if cook_time < 0:
            return print("禁止时间倒流")
        else:
            self.cook_time = self.cook_time + cook_time
        if 0 < self.cook_time < 3:
            self.cook_state = "生的"
        elif 3 <= self.cook_time <= 5:
            self.cook_state = "半生不熟"
        elif 5 < self.cook_time <= 10:
            self.cook_state = "熟了"
        else:
            self.cook_state = "焦了……"

    def add_condiment(self, condiment):
        self.condiment.append(condiment)

    def __str__(self):
        return f"老铁,已经烤了{self.cook_time}分钟,现在的状态是{self.cook_state},添加的调料是{self.condiment}"


if __name__ == "__main__":
    digua = CookPotato()
    digua.cook(5)
    digua.cook(7)
    digua.add_condiment("大蒜")
    digua.add_condiment("辣条")
    print(digua)
