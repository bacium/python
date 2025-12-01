"""
【征兵标准】
性别要求:征收男兵
身高标准:男性160cm以上，女性158cm以上。
男性体重:男性不超过90kg，不低于60kg。
视力标准:右眼裸眼视力不低于4.6，左眼裸眼视力不低于4.5
"""


class Army(object):
    def __init__(self, gender, height, weight, right_eye, left_eye):
        self.gender = gender
        self.height = height
        self.weight = weight
        self.right_eye = right_eye
        self.left_eye = left_eye

    def check_height(self):
        if self.height < 160:
            print("身高不符合征兵标准!")
        else:
            print("身高符合征兵标准!")

    def check_weight(self):
        if 60 <= self.weight < 90:
            print("体重符合征兵标准!")
        else:
            print("体重不符合标准")

    def check_eyes(self):
        if self.right_eye < 4.6:
            print("右眼视力不符合标准")
        elif self.left_eye < 4.5:
            print("左眼视力不符合标准")
        else:
            print("双眼视力符合标准")


if __name__ == "__main__":
    a1 = Army("男", 170, 69, 4.6, 4.3)
    a1.check_eyes()  # 左眼视力不符合标准
    a1.check_height()  # 身高符合征兵标准!
    a1.check_weight()  # 体重符合征兵标准!
