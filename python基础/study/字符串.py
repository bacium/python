str1 = "abcdefghijk"

print(str1[0])

print(str1[:5:2])

# 从后往前取所有值
print(str1[::-1])

print(str1[1:3])

# 从后往前,每隔一个字符取一个值
print(str1[::-2])

print("个数", str1.count("a"))

print("字符的位置", str1.index("f"))

print("分割字符串", str1.split(","))

print([i for i in str1])

print(str1.startswith("a"))

# 替换字符串
print(str1.replace("a", "b"))
