import re

str1 = "联系我手机号码是 123-4567-8901，还有一个备用号码是 987-6543-2109。"

reg = r'\b\d{3}-\d{4}-\d{4}\b'

result = re.findall(reg, str1)
print(result)

for i in result:
    print(f"提取到的电话为:{i}")
