"""
假设你正在开发一个学生成绩管理系统，需要编写 Python 代码来计算学生的总成绩和平均成绩。
请完成以下要求:已知一个学生的成绩列表scores=[88，90，85，95，70]，其中每个元素表示学生的一门成绩。
请使用函数嵌套调用的方式编写代码，实现以下功能:
创建一个函数 calculate_total(scores)，计算学生的总成绩，并返回结果。
创建一个函数 calculate_average(scores)，计算学生的平均成绩，并返回结果。
在 calculate_average(scores)函数内部，通过调用 calculate_total(scores)函数来获取学生的总成绩，
并计算平均成绩在主程序中调用 calculate_average(scores) 函数，并输出学生的总成绩和平均成绩。
"""

scores = [88, 90, 85, 95, 70]


# 求总分
def calculate_total(scores):
    total = 0
    for item in scores:
        total += item
    print(f"总分:{total}")
    return total


def calculate_average(scores):
    average = calculate_total(scores) / len(scores)
    print(f"平均分:{average}")
    return average


if __name__ == "__main__":
    calculate_total(scores)
    calculate_average(scores)
