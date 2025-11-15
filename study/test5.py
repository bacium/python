str1 = "hello world"
temp = "".join(str1.split(" "))
print(temp)

dict1 = {}
for i in temp:
    if i in dict1:
        dict1[i] += 1
    else:
        dict1[i] = 1

print(dict1)
print("abcdefgh"[3::-2])