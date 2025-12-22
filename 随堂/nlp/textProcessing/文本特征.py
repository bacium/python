def crate_ngram_set():
    # 构造文本数据
    input_list = [1, 4, 3, 6, 8, 2]
    # 一般ngram取2或者3
    ngram_range = 2
    # 创建临时列表，用于保存ngram
    temp_list = []
    for i in range(ngram_range):
        temp_list.append(input_list[i:])

    print(temp_list)
    print(set(zip(*temp_list)))


if __name__ == '__main__':
    crate_ngram_set()
