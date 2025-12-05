class Student(object):
    # 定义学生属性的魔术方法
    def __init__(self, name, gender, age, phone, memo):
        """
        :param name:姓名
        :param gender: 性别
        :param age: 年龄
        :param phone: 电话
        :param memo: 备注（描述信息）
        """
        self.name = name
        self.gender = gender
        self.age = age
        self.phone = phone
        self.memo = memo

    def __str__(self):
        return f"姓名：{self.name},性别：{self.gender},年龄：{self.age},电话：{self.phone},备注：{self.memo}"


if __name__ == "__main__":
    student = Student("张飞", "男", "25", "13621109595", "黑旋风，大板斧！")
    print(student)
