# 输入输出

name = input("plase input you name:")

print(name)

age = input("plase input you age:")
print(age)

print("姓名", name, age, sep="\n", end=";")


# print 占位符: %s 字符串类型, %d:数字类型,%f:浮点类型
print("姓名:%s,年龄:%d,成绩:%f" % ("李四", 29, 23.8))
