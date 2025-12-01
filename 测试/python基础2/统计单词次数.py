"""
统计单词次数
"""

str_ = "As your report on White Pollution indicates regulations on the use of plastic bags have not been implemented effectively in some areas. I am writing this letter to express my concern over the abuse of plastic bags and make some suggestions."


def count(string):
    temp = string.split(" ")
    str_list = []
    num = 1
    for word in temp:
        if word in str_list:
            num += 1
            dict_ = {word: num}
        else:
            dict_ = {word: num}
        str_list.append(dict_)
    print(str_list)


if __name__ == "__main__":
    count(str_)
