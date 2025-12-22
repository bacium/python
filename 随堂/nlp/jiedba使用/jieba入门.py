import jieba
import os


def dm1():
    print(os.getcwd())
    # 出师表
    content = "今天下三分,益州疲敝,此诚危急存亡之秋也"
    """
        参数说明:
            sentence: 文本
            cut_all: 精确模式 True:按照词精确分词,默认Flase:按照人类正常理解进行分词;即:按所有可能出现组合进行分词
    """
    words = jieba.cut(sentence=content, cut_all=True)
    # print(list(words))
    # print(" ".join(list(words)))
    text=jieba.lcut(sentence=content,cut_all=False)
    # print(text)


    # 按搜索引擎进行拆分
    text = jieba.cut_for_search(sentence=content)
    print(" ".join(list(text)))
    # 繁体拆分
    content2="煩惱即是菩提，我暫且不提"
    text = jieba.lcut(sentence=content2)
    print(" ".join(list(text)))


    jieba.load_userdict("./dict/usedict.txt")
    result = jieba.lcut(sentence=content)
    print(f"result{result}")
    print("测试数据")
if __name__ == '__main__':
    dm1()
