str1 = "helloworldhellopythonhelloc++hellojava"


def findall(all_string, target_string):
    positions = []
    start = 0
    length = len(target_string)
    while True:
        pos = all_string.find(target_string, start)
        if pos == -1:
            break
        positions.append(pos)
        start = pos + 1

    return tuple(positions)


result = findall(str1, "hello")
print(result)
