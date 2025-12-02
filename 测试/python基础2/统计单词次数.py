"""
统计单词次数
"""

str_ = "As your report on White Pollution indicates regulations on the use of plastic bags have not been implemented effectively in some areas. I am writing this letter to express my concern over the abuse of plastic bags and make some suggestions."


def count(string):
    temp = string.split(" ")
    dict_ = {}
    for word in temp:
        if word in dict_:
            dict_[word] += 1
        else:
            dict_[word] = 1
    with open('./output.txt', "w", encoding="utf-8") as df_stream:
        for key, value in dict_.items():
            df_stream.write(f"{key}:{value}\n")


if __name__ == "__main__":
    count(str_)
