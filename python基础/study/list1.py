# 列表操作

list1 = [1, 2, 3, 4, 5, 6, 17, 8, 9]
# print(len(list1))
# print(max(list1))
# print(min(list1))

# 元组转化为列表list
tuple1 = (1, 2, 3, 4, 5, 6, 17, 8, 9)
# print(list(tuple1))

# 列表后追加元素
list2 = [11, 23, 34, 312]
list1.append(19)
# print(list1)

# 合并列表
list3=[34,546,23]
# list1.extend(list3)
# print(list1)

# 删除元素
list1.remove(17)
# print(list1)


# 反转列表
# list1.reverse()
# print(list1)

# 排序
# sort()直接调用是正序从小到大排序
# sort(reverse=True) 是从大到小排序
list1.sort()
print(list1)



