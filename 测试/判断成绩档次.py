score = int(input('请输入成绩：'))
if 90 <= score <= 100:
    print('你的成绩是优秀')
elif 80 <= score < 90:
    print('你的成绩是良好')
elif 70 <= score < 80:
    print('你的成绩是合格')
elif 60 <= score < 70:
    print('你的成绩是及格')
elif 0 <= score < 60:
    print('你的成绩是不及格')
else:
    print('输入有误')
