# 用于正则表达式
import re
# 用于构建网络结构和函数的torch工具包
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
# torch中预定义的优化方法工具包
import torch.optim as optim
import time
# 用于随机生成数据
import random
import numpy as np
import matplotlib.pyplot as plt

# 设置全局变量
# 设备选择, 我们可以选择在cuda或者cpu上运行你的代码
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# 起始标志 SOS->Start Of Sequence
SOS_token = 0
# 结束标志 EOS->End Of Sequence
EOS_token = 1
# 最大句子长度不能超过10个(包含标点), 用于模型推理时处理最长长度限制
MAX_LENGTH = 10
# 数据文件路径
data_path = "./data/eng-fra-v2.txt"


# todo:0-文本清洗的工具函数
def normalizeString(s: str):
    # 0.1 将字母全部转换成小写, 然后删除两端的空白符
    s = s.lower().strip()
    # print('s--->', s)
    # 0.2 将句子中的标点符号和词用空格隔开, 标点符号也作为一个词处理
    # \1: 代表当前匹配到的字符
    s = re.sub(r"([.!?])", r" \1", s)
    # print('s--->', s)
    # 0.3 将句子中其他的符号替换成空格
    s = re.sub(r"[^a-z.!?]+", r" ", s)
    # print('s--->', s)
    return s


# todo:1-加载数据集, 并构建词表
def load_data(file_path: str):
    # 1.加载数据集借助工具函数进行清洗, 以[[英文句子1, 法文句子1],[英文句子2, 法文句子2],...]格式存储到内存中
    # 1.1 读取文件数据集, 使用\n进行分割, 将每行样本存储到列表中
    with open(file_path, 'r', encoding='utf-8') as f:
        my_lines = f.read().strip().split('\n')
        print('my_lines--->', my_lines[:3])

    # 1.2.0 创建两个空列表, 一个临时存储处理好的样本, 一个是持久存储的数据集
    tmp_pair, my_pairs = [], []
    # 1.2.1 循环遍历每行数据, 进行处理
    for line in my_lines:
        # print('line--->', line)
        # 1.2.2 循环遍历每行数据用\t分割后的列表, 使用工具函数进行清洗操作, 并保存到临时列表中, 将临时列表保存到最终列表中
        # print(line.split('\t'))
        for s in line.split('\t'):  # ['i m .', 'j ai ans .']
            tmp_pair.append(normalizeString(s))
        my_pairs.append(tmp_pair)
        tmp_pair = []
    print('my_paris--->', len(my_pairs), my_pairs[:3])

    # 2.构建英文和法文词表 word2index index2word
    # 2.1 将起始词和结束词添加到词表中
    english_word2index = {'SOS': SOS_token, 'EOS': EOS_token}
    english_word_n = 2  # 下一词的词下标表示
    french_word2index = {'SOS': SOS_token, 'EOS': EOS_token}
    french_word_n = 2  # 下一词的词下标表示

    # 2.2 循环遍历my_paris数据集列表
    for pair in my_pairs:
        # print('pair--->', pair)
        # 2.2.1 获取英文句子通过空格进行分词, 然后遍历词列表
        # print(pair[0].split(" "))
        for word in pair[0].split(" "):
            # 2.2.2 判断该词是否在词表中, 如果不在则添加
            if word not in english_word2index:
                english_word2index[word] = english_word_n
                english_word_n += 1  # 更新下一个词的下标表示

        # 法文
        for word in pair[1].split(" "):
            # 2.2.2 判断该词是否在词表中, 如果不在则添加
            if word not in french_word2index:
                french_word2index[word] = french_word_n
                french_word_n += 1  # 更新下一个词的下标表示
    print('english_word2index--->', len(english_word2index))
    print('english_word_n--->', english_word_n)
    print('french_word2index--->', len(french_word2index))
    print('french_word_n--->', french_word_n)

    # 2.3 字典推导式构建index2word词表
    english_index2word = {v: k for k, v in english_word2index.items()}
    french_index2word = {v: k for k, v in french_word2index.items()}
    print('english_index2word--->', len(english_index2word))
    print('french_index2word--->', len(french_index2word))
    return (english_word2index,
            english_index2word,
            english_word_n,
            french_word2index,
            french_index2word,
            french_word_n,
            my_pairs)


# todo:2-构建数据集类, 返回每条样本词下标张量表示形式
class MyParisDataset(Dataset):
    # 2.1 初始化属性
    def __init__(self, my_pairs, english_word2index, french_word2index):
        """
        实例化对象属性
        :param my_pairs: 清洗后的数据集列表
        :param english_word2index: 英文 词对下标的词表
        :param french_word2index: 法文 词对下标的词表
        """
        self.my_pairs = my_pairs
        self.english_word2index = english_word2index
        self.french_word2index = french_word2index
        # 统计样本数
        self.n_samples = len(self.my_pairs)

    # 2.2 获取数据集的样本数
    def __len__(self):
        return self.n_samples

    # 2.3 根据当前样本的index下标, 获取该样本的词下标张量表示形式
    def __getitem__(self, index):
        """
        :param item: 必传形参, 样本下标
        :return: 词下标组成的句子张量对象
        """
        # print('index--->', index)
        # 2.3.1 修正item下标值, 防止索引越界
        # self.n_samples - 1:最大下标值, 长度-1
        index = min(max(index, 0), self.n_samples - 1)
        # print('index--->', index)

        # 2.3.2 获取当前样本中的x和y
        # print(self.my_pairs[index])
        x = self.my_pairs[index][0]
        y = self.my_pairs[index][1]
        # print('x1--->', x)
        # print('y1--->', y)
        # 2.3.3 分别对x和y进行分词处理, 并转换成词下标张量对象
        x = [self.english_word2index[word] for word in x.split(" ")]
        # 添加结束词, 当前没有添加起始词(后续训练时手动传入起始词)
        x.append(EOS_token)
        # print('x2--->', x)
        tensor_x = torch.tensor(data=x, dtype=torch.long, device=device)
        # print('tensor_x--->', tensor_x)

        y = [self.french_word2index[word] for word in y.split(" ")]
        # 添加结束词, 当前没有添加起始词(后续训练时手动传入起始词)
        y.append(EOS_token)
        # print('y2--->', y)
        tensor_y = torch.tensor(data=y, dtype=torch.long, device=device)
        # print('tensor_y--->', tensor_y)
        return tensor_x, tensor_y


# todo:3-构建编码器解码器的神经网络模型
# 编码器
class Encoder(nn.Module):
    def __init__(self, input_size, hidden_size):
        """
        搭建网络模型结构
        :param input_size: 英文词表大小, 词数
        :param hidden_size: GRU层的维度/特征数
        """
        super().__init__()
        self.input_size = input_size
        self.hidden_size = hidden_size

        # 1.实例化embedding层对象
        # num_embeddings: 词表大小 词数
        # embedding_dim: 词嵌入维度 词向量特征数
        self.embedding = nn.Embedding(num_embeddings=self.input_size,
                                      embedding_dim=self.hidden_size)
        # 2.实例化gru层对象
        # input_size: 词向量的维度/特征数
        # hidden_size: 隐藏层的维度/特征数
        # batch_first: True->输入数据维度为(句子数, 句子长度, 词维度)
        self.gru = nn.GRU(input_size=self.hidden_size,
                          hidden_size=self.hidden_size,
                          batch_first=True)

    def forward(self, input, h0=None):
        """
        前向传播计算, 提取输入序列英文句子的语义表示
        :param input: 词下标表示的句子张量对象 (句子数, 句子长度)
        :param h0: 初始隐藏状态值 (层数*方法, 句子数, 隐层维度)
        :return: output hn
        """
        # 1.input转换成词向量表示 (句子数, 句子长度, 词维度)
        # print('input--->', input.shape, input)
        embedded = self.embedding(input)
        # print('embedded--->', embedded.shape, embedded)
        # 2.gru层提取输入序列语义表示
        output, hn = self.gru(embedded, h0)
        # print('output--->', output.shape, output)
        # print('hn--->', hn.shape, hn)
        return output, hn

    def inithidden(self):
        """
        初始化全0的h0隐藏状态值
        :return:
        """
        return torch.zeros(size=(1, 1, self.hidden_size), device=device)


# 解码器
class Decoder(nn.Module):
    def __init__(self, output_size, hidden_size, dropout_p=0.1):
        """
        构建解码器网络结构
        :param output_size: embedding层词数 & 输出层的输出特征个数(法文词表词数/预测的类别数)
        :param hidden_size: embedding层词维度 & gru层的隐层维度
        :param dropout_p: 置零概率
        """
        super().__init__()
        # 初始化属性
        self.output_size = output_size
        self.hidden_size = hidden_size
        self.dropout_p = dropout_p

        # 1.实例化attn1和attn2线性层对象, 用于计算q和k的相似分值
        # 1.1 attn1是用于对q和k融合的结果进行线性计算, q特征数+k特征数
        self.attn1 = nn.Linear(in_features=self.hidden_size * 2, out_features=self.hidden_size)
        # 1.2 attn2是对attn1的一维向量相似分映射为标量相似分(1个特征值)
        self.attn2 = nn.Linear(in_features=self.hidden_size, out_features=1)

        # 2.实例化attn_combine线性层对象, 用于将注意力表示c和输入input融合到一起, 得到加强的输入
        # c和input融合, c特征数+input特征数
        self.attn_combine = nn.Linear(in_features=self.hidden_size * 2, out_features=self.hidden_size)

        # 3.实例化embedding层, droput层, gru层, 全连接层(线性层+logsoftmax层)
        # num_embeddings: 法文词表大小
        self.embedding = nn.Embedding(num_embeddings=self.output_size, embedding_dim=self.hidden_size)
        self.dropout = nn.Dropout(p=self.dropout_p)
        self.gru = nn.GRU(input_size=self.hidden_size, hidden_size=self.hidden_size, batch_first=True)
        # out_features: 法文词表大小/预测的类别数
        self.out = nn.Linear(in_features=self.hidden_size, out_features=self.output_size)
        self.softmax = nn.LogSoftmax(dim=-1)

    def forward(self, input, hidden, encoder_outputs):
        """
        前向传播计算
        :param input: 当前时间步的输入 (句子数, 词数) -> (1, 1)
        :param hidden: 当前时间步的输入隐藏状态值 s0=编码器的hn q
        :param encoder_outputs: 编码器的output k/v
        :return: 法文预测结果 输出隐藏状态值(作为下一个时间步的输入隐藏状态值 q) 注意力权重分布attn_weights
        """
        # 1.input进行词向量转换+droput, 获取词向量表示
        # print('input--->', input.shape, input)
        embedded = self.dropout(self.embedding(input))
        # print('embedded--->', embedded.shape, embedded)

        # 2.计算当前时间步的注意力分布表示 c
        # 2.1 q和k计算相似分 attn_scores
        # print('hidden--->', hidden.shape, hidden)
        # print('encoder_outputs--->', encoder_outputs.shape, encoder_outputs)
        expand_hidden = hidden.transpose(0, 1).expand(-1, encoder_outputs.shape[1], -1)
        # print('expand_hidden--->', expand_hidden.shape, expand_hidden)
        attn_scores = self.attn2(
            torch.tanh(
                self.attn1(
                    torch.cat(tensors=[expand_hidden, encoder_outputs], dim=-1)))).squeeze(dim=2)
        # print('attn_scores--->', attn_scores.shape, attn_scores)
        # 2.2 softmax得到注意力权重分布 attn_weights
        attn_weights = torch.softmax(attn_scores, dim=-1)
        # print('attn_weights--->', attn_weights.shape, attn_weights)
        # 2.3 attn_weights和v进行bmm三维矩阵乘法得到注意力表示 c
        c = torch.bmm(input=attn_weights.unsqueeze(dim=1), mat2=encoder_outputs)
        # print('c--->', c.shape, c)

        # 3.词向量表示和c进行融合, 得到加强的输入表示
        attn_applied = self.attn_combine(torch.cat(tensors=[embedded, c], dim=-1))
        # print('attn_applied--->', attn_applied.shape, attn_applied)

        # 4.gru层计算得到语义表示, 输出隐藏状态值
        output, hidden = self.gru(torch.relu(attn_applied), hidden)
        # print('output--->', output.shape, output)
        # print('hidden--->', hidden.shape, hidden)

        # 5.全连接层计算得到预测的结果
        output = self.softmax(self.out(output[:, -1, :]))
        return output, hidden, attn_weights


def test_attn_decoder():
    # data = normalizeString("I'm fine, thank you@.\n")
    # print('data--->', data)

    # 1.加载数据集
    (english_word2index,
     english_index2word,
     english_word_n,
     french_word2index,
     french_index2word,
     french_word_n,
     my_pairs) = load_data(file_path=data_path)

    # 2.实例化数据集对象
    dataset = MyParisDataset(my_pairs=my_pairs, english_word2index=english_word2index,
                             french_word2index=french_word2index)
    # print("dataset--->", dataset.french_word2index)
    print("len(dataset)--->", len(dataset))
    print("dataset[0]--->", dataset[0])

    # 3.实例化数据加载器对象
    dataloader = DataLoader(dataset=dataset,
                            batch_size=1,
                            shuffle=True)

    # 4.实例化编码器模型对象
    # to(device=device): 将模型移动到指定设备上
    encoder = Encoder(input_size=english_word_n, hidden_size=256).to(device=device)
    print('encoder--->', encoder)

    # 5.实例化解码器模型对象
    decoder = Decoder(output_size=french_word_n, hidden_size=256).to(device=device)
    print('decoder--->', decoder)

    # 遍历数据加载器
    for train_x, train_y in dataloader:
        encoder_outputs, hidden = encoder(train_x, encoder.inithidden())
        # print("encoder_outputs--->", encoder_outputs.shape, encoder_outputs)
        # print("hidden--->", hidden.shape, hidden)

        # 解码器是一个词一个词处理
        # train_y -> (句子数, 词数)
        # print('train_y.shape--->', train_y.shape)
        for i in range(train_y.shape[1]):
            # 获取当前i对应词下标, 当前时间步的输入
            # train_y[:, i]: 一维向量表示 (句子数, )
            # print('train_y[:, i]--->', train_y[:, i])
            input = train_y[:, i].view(-1, 1)
            # print('input--->', input.shape, input)
            output, hidden, attn_weights = decoder(input=input, hidden=hidden, encoder_outputs=encoder_outputs)
            print("output--->", output.shape, output)
            print("hidden--->", hidden.shape, hidden)
            print("attn_weights--->", attn_weights.shape, attn_weights)
            exit()


# todo:4-模型训练
# 模型训练参数
mylr = 1e-4  # 学习率
epochs = 2  # 训练轮次
print_interval_num = 1000  # 1000个batch打印一次训练结果
plot_interval_num = 100  # 100个batch绘制一次损失曲线


# 模型训练的二次封装函数
def train_iters(x, y, encoder, decoder, encoder_optimizer, decoder_optimizer, criterion, total_steps, current_step):
    """
    内层循环的模型训练逻辑
    :param x: 真实x 英文句子
    :param y: 真实y 法文句子
    :param encoder: 编码器模型
    :param decoder: 解码器模型
    :param encoder_optimizer: 编码器优化器
    :param decoder_optimizer: 解码器优化器
    :param criterion: 损失函数对象
    :param total_steps: 总训练批次数
    :param current_step: 当前累计的训练批次数
    :return: 当前预测句子的平均损失值(句子所有词的总损失/词数)
    """
    # 1.切换模型的训练模式
    encoder.train()
    decoder.train()

    # 2.编码器对输入序列x进行编码, 得到output(作为k和v)和hn(解码器第1个时间步的输入隐藏状态值,第1个q)
    encoder_outputs, hn = encoder(x, encoder.inithidden())
    # print('encoder_outputs--->', encoder_outputs.shape, encoder_outputs)
    # print('hn--->', hn.shape, hn)

    # encoder_outputs-> k和v  hn->解码器第1个时间步的输入隐藏状态值(第1个q)
    # 3.解码器第1个时间步的输入词 SOS
    input_y = torch.tensor(data=[[SOS_token]], device=device)
    # print('input_y--->', input_y.shape, input_y)

    # 4.循环遍历真实y的词数进行预测
    # 4.1 初始化统计变量 句子总损失, 句子总词数, 句子长度, 教师强制机制
    myloss = 0.0  # 句子总损失
    total_word_num = 0  # 句子总词数
    y_len = y.shape[1]  # 句子长度

    # 教师强制机制 阈值线性衰减
    teacher_forcing_ratio = max(0.1, 1 - (current_step / total_steps))
    # print('teacher_forcing_ratio--->', teacher_forcing_ratio)
    use_teacher_forcing = True if random.random() < teacher_forcing_ratio else False
    # print('use_teacher_forcing--->', use_teacher_forcing)

    for idx in range(y_len):
        # 4.2 解码器进行预测, 返回预测法文词(logsoftmax), 输出隐藏状态值, 注意力权重分布
        output_y, hn, attn_weights = decoder(input=input_y, hidden=hn, encoder_outputs=encoder_outputs)
        # print("output_y--->", output_y.shape, output_y)
        # 4.3 计算损失值
        # 获取当前时间步的真实词
        target_y = y[:, idx]
        # print('target_y--->', target_y.shape, target_y)
        loss = criterion(output_y, target_y)
        # print("loss--->", loss)
        myloss += loss
        # print("myloss--->", myloss)
        # 统计训练总词数
        total_word_num += 1
        # 4.4 通过教师强制机制, 判断是使用真实y还是预测y作为下一个时间步的输入
        if use_teacher_forcing:
            # 使用真实y作为下一个时间步的输入
            input_y = y[:, idx].view(-1, 1)
            # print('input_y--->', input_y.shape, input_y)
        else:
            # 使用预测y作为下一个时间步的输入
            pred_y = torch.argmax(output_y, dim=-1).view(-1, 1)
            # print('pred_y--->', pred_y.shape, pred_y)
            if pred_y.item() == EOS_token:
                break
            input_y = pred_y.detach()
            # print('input_y--->', input_y.shape, input_y)
    # 5.梯度清零 反向传播 参数更新
    encoder_optimizer.zero_grad()
    decoder_optimizer.zero_grad()
    myloss.backward()
    encoder_optimizer.step()
    decoder_optimizer.step()
    # 6.返回句子平均损失
    return myloss.item() / total_word_num


# 主函数代码逻辑
def train():
    # 1.加载数据集
    (english_word2index,
     english_index2word,
     english_word_n,
     french_word2index,
     french_index2word,
     french_word_n,
     my_pairs) = load_data(file_path=data_path)

    # 2.构建数据集对象
    dataset = MyParisDataset(my_pairs=my_pairs, english_word2index=english_word2index,
                             french_word2index=french_word2index)

    # 3.构建数据加载器对象
    dataloader = DataLoader(dataset=dataset, batch_size=1, shuffle=True)

    # 4.实例化编码器和解码器模型对象
    encoder = Encoder(input_size=english_word_n, hidden_size=256).to(device=device)
    decoder = Decoder(output_size=french_word_n, hidden_size=256, dropout_p=0.1).to(device=device)

    # 5.实例化编码器和解码器优化器对象
    encoder_optimizer = optim.Adam(params=encoder.parameters(), lr=mylr)
    decoder_optimizer = optim.Adam(params=decoder.parameters(), lr=mylr)

    # 6.实例化损失函数对象
    criterion = nn.NLLLoss()

    # 7.模型训练
    # 7.1 初始化遍历存储统计信息 绘图损失列表 总批次数 当前累计的批次数
    plot_loss_list = []
    total_steps = epochs * len(dataloader)
    current_step = 0

    # 7.2 外层循环遍历训练轮次
    for epoch_idx in range(1, epochs + 1):
        print_loss_total, plot_loss_total = 0.0, 0.0
        starttime = time.time()
        # 7.3 内层循环遍历数据加载器
        for item, (train_x, train_y) in enumerate(dataloader, start=1):
            # 7.3.1 调用二次封装的训练函数进行训练, 返回训练损失值
            myloss = train_iters(train_x,
                                 train_y,
                                 encoder,
                                 decoder,
                                 encoder_optimizer,
                                 decoder_optimizer,
                                 criterion,
                                 total_steps,
                                 current_step)
            # print('myloss--->', myloss)
            # 7.3.2 统计训练信息 打印日志损失值 绘图损失值 累加的训练批次数
            print_loss_total += myloss
            plot_loss_total += myloss
            current_step += 1

            # 7.3.3 打印训练日志信息
            if item % print_interval_num == 0:
                print_loss_avg = print_loss_total / print_interval_num
                # 重置总损失为0
                print_loss_total = 0
                print('轮次%d  损失%.6f 时间:%d' % (epoch_idx, print_loss_avg, time.time() - starttime))
            # 7.3.4 保存绘图的损失值
            if item % plot_interval_num == 0:
                plot_loss_list.append(plot_loss_total / plot_interval_num)
                plot_loss_total = 0
        # 7.4 保存模型
        torch.save(encoder.state_dict(), 'model/my_encoderrnn_%d.pth' % epoch_idx)
        torch.save(decoder.state_dict(), 'model/my_attndecoderrnn_%d.pth' % epoch_idx)

    # 7.5 绘制损失图像
    plt.figure()
    plt.plot(plot_loss_list)
    plt.savefig('img/seq2seq_loss.png')
    plt.show()


# todo:5-模型推理
PATH1 = "model/my_encoderrnn_5.pth"
PATH2 = "model/my_attndecoderrnn_5.pth"


# 模型评估代码与模型预测代码类似，需要注意使用with torch.no_grad()
# 模型预测时，第一个时间步使用SOS_token作为输入 后续时间步采用预测值作为输入，也就是自回归机制
def seq2seq_evaluate(
        x, my_encoderrnn, my_attndecoderrnn, french_index2word
):
    with torch.no_grad():
        my_encoderrnn.eval()
        my_attndecoderrnn.eval()
        # 1 编码：一次性的送数据
        encode_hidden = my_encoderrnn.inithidden()
        encode_output, encode_hidden = my_encoderrnn(x, encode_hidden)

        # 2 解码参数准备
        # 解码参数1 k和v
        encoder_outputs_c = encode_output

        # 解码参数2 编码器最后1个隐藏状态值 作为 解码器的第1个时间步的输入隐藏状态值
        decode_hidden = encode_hidden

        # 解码参数3 解码器第一个时间步起始符
        input_y = torch.tensor([[SOS_token]], device=device)

        # 3 自回归方式解码
        # 初始化预测的词汇列表
        decoded_words = []
        for idx in range(MAX_LENGTH):  # note:MAX_LENGTH=10
            output_y, decode_hidden, attn_weights = my_attndecoderrnn(
                input_y, decode_hidden, encoder_outputs_c
            )
            # 预测值作为下一次时间步的输入值
            topv, topi = output_y.topk(1)

            # 如果输出值是终止符，则循环停止
            if topi.item() == EOS_token:
                decoded_words.append("<EOS>")
                break
            else:
                decoded_words.append(french_index2word[topi.item()])

            # 将本次预测的索引赋值给 input_y，进行下一个时间步预测
            input_y = topi.detach()

    return decoded_words


def inference():
    # 加载数据集
    (
        english_word2index,
        english_index2word,
        english_word_n,
        french_word2index,
        french_index2word,
        french_word_n,
        my_pairs,
    ) = load_data(data_path)

    # 实例化模型
    input_size = english_word_n
    hidden_size = 256  # 观察结果数据 可使用8
    my_encoderrnn = Encoder(input_size, hidden_size).to(device)

    """
    torch.load(map_location=)
    map_location: 指定如何重映射模型权重的存储设备（如 GPU → CPU 或 GPU → 其他 GPU）。
    # 加载到 CPU：map_location=torch.device('cpu') 或 map_location='cpu'。
    自动选择可用设备：map_location=torch.device('cuda')。
    自定义映射逻辑：通过函数定义设备映射规则。
    map_location=lambda storage, loc: storage -> 该lambda函数直接返回原始存储对象(storage)
    强制所有张量保留在保存时的设备上。当模型权重保存时的设备与当前环境一致时（例如均在CPU或同一GPU上），避免不必要的设备迁移。

    load_state_dict(strict=)
    strict:True（默认）:要求加载的权重键（keys）与当前模型的键完全匹配。如果存在不匹配（例如权重中缺少某些键，或模型有额外键），抛出RuntimeError。
    """
    my_encoderrnn.load_state_dict(
        torch.load(PATH1, map_location=lambda storage, loc: storage), strict=False
    )
    print("my_encoderrnn模型结构--->", my_encoderrnn)

    # 实例化模型
    input_size = french_word_n
    hidden_size = 256  # 观察结果数据 可使用8
    my_attndecoderrnn = Decoder(input_size, hidden_size).to(device)
    # my_attndecoderrnn.load_state_dict(torch.load(PATH2))
    my_attndecoderrnn.load_state_dict(
        torch.load(PATH2, map_location=lambda storage, loc: storage), False
    )
    print("my_decoderrnn模型结构--->", my_attndecoderrnn)

    my_samplepairs = [
        [
            "i m impressed with your french .",
            "je suis impressionne par votre francais .",
        ],
        ["i m more than a friend .", "je suis plus qu une amie ."],
        ["she is beautiful like her mother .", "elle est belle comme sa mere ."],
    ]
    print("my_samplepairs--->", len(my_samplepairs))

    for index, pair in enumerate(my_samplepairs):
        x = pair[0]
        y = pair[1]

        # 样本x 文本数值化
        tmpx = [english_word2index[word] for word in x.split(" ")]
        tmpx.append(EOS_token)
        print("tmpx--->", tmpx)
        tensor_x = torch.tensor(tmpx, dtype=torch.long, device=device).view(1, -1)
        print("tensor_x--->", tensor_x)

        # 模型预测
        decoded_words = seq2seq_evaluate(
            tensor_x, my_encoderrnn, my_attndecoderrnn, french_index2word
        )
        print('decoded_words->', decoded_words)
        output_sentence = " ".join(decoded_words)

        print("\n")
        print(">", x)
        print("=", y)
        print("<", output_sentence)


if __name__ == '__main__':
    # train()
    inference()
