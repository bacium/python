count = 0
while (True):
    username = input("请输入用户名:")
    password = input("请输入密码:")
    if username == "admin" and password == "admin888":
        print("登录成功!")
        break
    else:
        count += 1
        if count >= 3:
            print("3次密码输入错误,账户已被锁定,请联系管理员")
            break
        print("用户名或密码输入错误,请重新输入")