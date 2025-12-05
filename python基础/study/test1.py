import random

str1 = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

verify_code_list = []

while (True):
    index = random.randint(0, len(str1)-1)
    if len(verify_code_list) > 3:
        break
    else:
        verify_code_list.append(str1[index])

print("".join(verify_code_list))


