date1=int(input('请输入数字：'))

if date1 in range(1,8):
  if date1 ==6 or date1 ==7:
    print('是周末')
  else:
    print('工作日')
else:
    print("输入有误,请输入1-7的数字")