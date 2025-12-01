"""
假设我们有一个存储商品价格的列表 prices，每个元素代表一个商品的价格。现在需要完成以下任务:将价格列表按升序排序。
将价格列表反转，以得到降序排序的列表。
找到最高价格和最低价格。
计算所有商品的平均价格。
"""

prices = [23, 12, 34, 45, 321, 452, 23, 21, 89]


# 升序
def ascending(list):
    print(f"排序前:{list}")
    list.sort()
    print(f"排序后:{list}")
    return list


def de_ascending(list):
    temp = ascending(list)
    temp.sort(reverse=True)
    return f"降序结果{temp}"


def max_min(list):
    return f"最大值:{max(list)},最小值:{min(list)}"


def average(list):
    sum_ = 0
    for prices in list:
        sum_ += prices
    result = sum_ / len(list)
    return f"平均值是{result}"


if __name__ == "__main__":
    result = ascending(prices)
    de_ascending(prices)
    print("+" * 50)
    max_min_result = max_min(prices)
    print(max_min_result)
    print("=" * 50)
    average_value = average(prices)
    print(average_value)
