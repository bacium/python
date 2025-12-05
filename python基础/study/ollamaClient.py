
import ollama
client=ollama.Client(host="127.0.0.1:11434")
#显示模型列表
client.list()
#print(client.list())

# 显示模型的详细信息
print(client.show("deepseek-r1:8b"))
print("<================================================>")
print(client.ps())