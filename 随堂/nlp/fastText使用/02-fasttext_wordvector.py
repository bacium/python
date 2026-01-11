# 代码运行在python解释器中
# 导入fasttext
import fasttext


def dm01():
    # 使用fasttext的train_unsupervised(无监督训练方法)进行词向量的训练
    # 它的参数是数据集的持久化文件路径'data/fil9'
    # 注意，该行代码执行耗时很长
    # model = fasttext.train_unsupervised('data/fil9')

    # 加载模型
    # 可以使用以下代码加载文本预处理章节已经训练好的模型
    model = fasttext.load_model("data/fil9.bin")

    # 获取词的词向量表示
    ret = model.get_word_vector('the')
    # ret = model.get_word_vector('好')
    print(type(ret), ret.shape, ret)

    # 获取句子的向量表示
    ret2 = model.get_sentence_vector('I love you !')
    print(type(ret2), ret2.shape, ret2)

    ret3 = model.get_nearest_neighbors(word='the', k=5)
    print(ret3)


# 调整超参数训练模型
def dm02():
    # model: 模式
    # dim: 词向量维度数
    # thread: 线程数
    model = fasttext.train_unsupervised('data/fil9', model="cbow", dim=300, epoch=1, lr=0.1, thread=8)
    print(model.get_nearest_neighbors('sport'))


if __name__ == '__main__':
    dm01()
    # dm02()