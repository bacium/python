# 管理界面
import time

from student import Student


class StudentCMS:
    def __init__(self):
        # s1 = Student("张三", "男", 23, "133", "老六")
        # s2 = Student("李四", "男", 26, "138", "老大")
        # s3 = Student("王五", "女", 32, "139", "老四")
        self.studentList = []

    def show_view(self):
        print("*" * 40)
        print("\t欢迎使用学生管理系统")
        print("\t1.添加学员")
        print("\t2.修改学员")
        print("\t3.删除学员")
        print("\t4.查询")
        print("\t5.所有学员")
        print("\t6.保存信息")
        print("\t0.退出系统")
        print("*" * 40)

    #  添加学员
    def add_student(self):
        name = input("请输入学员姓名：")
        gender = input("请输入学员性别：")
        age = input("请输入学员年龄：")
        phone = input("请输入学员电话：")
        memo = input("请输入学员备注：")
        student = Student(name, gender, age, phone, memo)
        self.studentList.append(student)

    # 更新学员
    def update_student(self):
        update_name = input("请输入要更新学员的姓名！")
        for student in self.studentList:
            if student.name == update_name:
                student.gender = input("请输入学员性别：")
                student.age = input("请输入学员年龄：")
                student.phone = input("请输入学员电话：")
                student.memo = input("请输入学员备注：")
                print("更新成功！")
                break
        else:
            print("未查到相关信息，请确认后再操作！")

    # 删除学员
    def delete_student(self):
        select_name = input("请输入删除学员姓名：")
        for student in self.studentList:
            if student.name == select_name:
                self.studentList.remove(student)
                print("删除成功")
                break
        else:
            print("学员 不存在，请确认后再操作！")

    # 搜索个人
    def search_one_student(self):
        search_name = input("请输入学员姓名:")
        for student in self.studentList:
            if student.name == search_name:
                print(student)
                break
        else:
            print("查无此人，请确认后在操作！")

    # 搜索全部
    def search_all_student(self):
        if len(self.studentList) > 0:
            for student in self.studentList:
                print(student)
        else:
            return print("目前没有学员，请添加后再查看！")
        print()

    # 保存信息
    def save_student(self):
        # 把学员信息[Student,Student,Student]转化为[{学员信息},{学员信息},{学员信息}]形式！
        student_database = str([student.__dict__ for student in self.studentList])
        with open("./studentDatabase.txt", "w", encoding="utf-8") as outputStream_txt:
            outputStream_txt.write(student_database)
            print("学员信息保存成功！")
            print()

    # 加载学员信息
    def load_student(self):
        try:
            # 学员信息从文件中读取出来，然后转化为学员对象形式
            with open(
                    "./studentDatabase.txt", "r", encoding="utf-8"
            ) as inputStream_txt:
                student_database = inputStream_txt.read()
                if student_database == "":
                    student_database = "[]"
                studentList = eval(student_database)
                self.studentList = [
                    Student(
                        student["name"],
                        student["gender"],
                        student["age"],
                        student["phone"],
                        student["memo"],
                    )
                    for student in studentList
                ]
        except:
            outputStream = open("./studentDatabase.txt", "w", encoding="utf-8")
            outputStream.close()

    # 开始服务
    def start(self):
        # 先从文件中加载存储的学院信息
        self.load_student()
        while True:
            time.sleep(0.5)
            self.show_view()
            select_operate_num = input("请选择操作序号：")
            if select_operate_num == "1":
                # print("添加学员：")
                self.add_student()
            elif select_operate_num == "2":
                # print("更新学员信息：")
                self.update_student()
            elif select_operate_num == "3":
                # print("删除学员：")
                self.delete_student()
            elif select_operate_num == "4":
                # print("查询学员：")
                self.search_one_student()
            elif select_operate_num == "5":
                # print("查询所有：")
                self.search_all_student()
            elif select_operate_num == "6":
                # print("保存信息")
                self.save_student()
            elif select_operate_num == "0":
                exitRes = input("确认要退出吗？请输入Y或者N确认")
                if exitRes.upper() == "Y":
                    break

# if __name__ == "__main__":
#     stu = StudentCMS()
#     # stu.show_view()
#     stu.start()
