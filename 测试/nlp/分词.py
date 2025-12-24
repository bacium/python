"""
使用jieba模块对 "传智教育是一家上市公司" 内容实现精确模式/全模式/搜索引擎模式分词
"""
import jieba


content="传智教育是一家上市公司"

result1=jieba.lcut(sentence=content,cut_all=False)
print(f"精确模式{result1}")
result2=jieba.lcut(sentence=content,cut_all=True)
print(f"全模式{result2}")
result3=jieba.cut_for_search(sentence=content)
print(f"搜索引擎模式{list(result3)}")





