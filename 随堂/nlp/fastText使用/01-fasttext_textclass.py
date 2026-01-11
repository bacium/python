# 导入fasttext
import fasttext


# 未清洗文本的默认参数训练
def dm01():
    # 使用fasttext的train_supervised方法进行文本分类模型的训练
    # train_supervised: 监督学习训练方法  文本分类使用人工标注的数据集
    # input: 训练集路径
    model = fasttext.train_supervised(input="data/cooking.train")
    print('model--->', model)
    # 模型预测
    print(model.predict("Which baking dish is best to bake a banana bread ?"))
    # 模型评估
    # 返回样本数/模型精确度/召回率
    print(model.test(path="data/cooking.valid"))


# 清洗文本的默认参数训练
# 清洗: 大写转换成小写  标点符号和词分隔开
def dm02():
    # 使用fasttext的train_supervised方法进行文本分类模型的训练
    # train_supervised: 监督学习训练方法  文本分类使用人工标注的数据集
    # input: 训练集路径
    model = fasttext.train_supervised(input="data/cooking.pre.train")
    print('model--->', model)
    # 模型预测
    print(model.predict("Which baking dish is best to bake a banana bread ?"))
    # 模型评估
    # 返回样本数/模型精确度/召回率
    print(model.test(path="data/cooking.pre.valid"))


# 增加训练轮次
def dm03():
    # 使用fasttext的train_supervised方法进行文本分类模型的训练
    # train_supervised: 监督学习训练方法  文本分类使用人工标注的数据集
    # input: 训练集路径
    model = fasttext.train_supervised(input="data/cooking.pre.train", epoch=25)
    print('model--->', model)
    # 模型预测
    print(model.predict("Which baking dish is best to bake a banana bread ?"))
    # 模型评估
    # 返回样本数/模型精确度/召回率
    print(model.test(path="data/cooking.pre.valid"))


# 调整学习率
def dm04():
    # 使用fasttext的train_supervised方法进行文本分类模型的训练
    # train_supervised: 监督学习训练方法  文本分类使用人工标注的数据集
    # input: 训练集路径
    model = fasttext.train_supervised(input="data/cooking.pre.train", epoch=25, lr=1.0)
    print('model--->', model)
    # 模型预测
    print(model.predict("Which baking dish is best to bake a banana bread ?"))
    # 模型评估
    # 返回样本数/模型精确度/召回率
    print(model.test(path="data/cooking.pre.valid"))


# 增加n-gram特征
def dm05():
    # 使用fasttext的train_supervised方法进行文本分类模型的训练
    # train_supervised: 监督学习训练方法  文本分类使用人工标注的数据集
    # input: 训练集路径
    # wordNgrams: 词级别, 连续的n个词组合到一起生成一个新词
    # minn/maxn: 字符级别, 词中连续的n个字符组合到一起生成一个子词
    model = fasttext.train_supervised(input="data/cooking.pre.train", epoch=25, lr=1.0, wordNgrams=2)
    print('model--->', model)
    # 模型预测
    print(model.predict("Which baking dish is best to bake a banana bread ?"))
    # 模型评估
    # 返回样本数/模型精确度/召回率
    print(model.test(path="data/cooking.pre.valid"))

# 修改损失计算方式
def dm06():
    # loss='hs': 层次softmax
    # neg=0: 0个负样本 不使用负采样
    model = fasttext.train_supervised(input="data/cooking.pre.train", lr=1.0, epoch=25, wordNgrams=2, loss='hs', neg=0)
    # 模型预测
    print(model.predict("Which baking dish is best to bake a banana bread ?"))
    # 模型评估
    # 返回样本数/模型精确度/召回率
    print(model.test(path="data/cooking.pre.valid"))

# 自动超参数调优
def dm07():
    # autotuneValidationFile: 自动验证的数据集路径
    # autotuneDuration: 自动调优时间
    model = fasttext.train_supervised(input='data/cooking.pre.train',
                                      autotuneValidationFile='data/cooking.pre.valid',
                                      autotuneDuration=600)
    # 模型预测
    print(model.predict("Which baking dish is best to bake a banana bread ?"))
    # 模型评估
    # 返回样本数/模型精确度/召回率
    print(model.test(path="data/cooking.pre.valid"))

# 多标签多分类损失计算方式调整
def dm08():
    # loss='ova': one vs all  预测结果和所有类别进行损失计算 -> 将多分类问题转换成多个二分类问题
    model = fasttext.train_supervised(input="data/cooking.pre.train", lr=0.2, epoch=25, wordNgrams=2, loss='ova')
    # 模型预测
    print(model.predict("Which baking dish is best to bake a banana bread ?"))
    # 模型评估
    # 返回样本数/模型精确度/召回率
    print(model.test(path="data/cooking.pre.valid"))

    # 模型保存
    model.save_model("model/model_cooking.bin")

    # 模型加载
    model = fasttext.load_model("model/model_cooking.bin")
    print(model)

if __name__ == '__main__':
    # dm01()
    # dm02()
    # dm03()
    # dm04()
    # dm05()
    # dm06()
    # dm07()
    dm08()