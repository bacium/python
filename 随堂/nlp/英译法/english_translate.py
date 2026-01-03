# 用于正则表达式
import re

# 用于构建网络结构和函数的torch工具包
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader

# torch中预定义的优化方法工具包
# 用于随机生成数据
# import matplotlib.pyplot as plt


# 设备选择
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# 起始标志
SOS_TOKEN = 0
# 结束标志
EOS_TOKEN = 1
# 最大句子长度不能超过10个,用于设置每个句子样本中间语义张量c的长度都为10
MAX_LENGTH = 10
# 数据文件路径
dataPath = './data/eng-fra-v2.txt'


def normaliserString(s):
    # 字符转小写,去除两边的空白符
    s = s.lower().strip()  # 修正：使用 strip() 并将结果赋值回 s
    # print(f"s====>:{s}")
    # 将句子中的标点符号和词用空格隔开, 标点符号也作为一个词处理
    s = re.sub(r"([.!?])", r" \1", s)
    # print(f"s====>:{s}")
    # 将句子中其他的符号替换成空格
    s = re.sub(r"[^a-z.!?]+", r" ", s)
    # print(f"s====>:{s}")
    return s


def load_data(file_path):
    # my_getdata() 清洗文本构建字典思路分析
    # 1 按行读文件 open().read().strip().split(\n) my_lines
    with open(file_path, "r") as fr:
        line_data = fr.read().strip().split("\n")
        # print(line_data[:5])
        # 2 按行清洗文本 构建语言对 my_pairs[] tmppair[]
        temp_pair, my_pair = [], []
    # 2-1格式 [['英文', '法文'], ['英文', '法文'], ['英文', '法文'], ['英文', '法文']....]
    for line in line_data:
        # 2-2调用清洗文本工具函数normalizeString(s)
        for s in line.split("\t"):
            # print(s)
            temp_pair.append(normaliserString(s))
        my_pair.append(temp_pair)
        temp_pair = []
    # print(my_pair[:5],len(my_pair))
    # 3构建词表
    # 3-1 词对下标词表构建
    english_word2index = {"SOS": SOS_TOKEN, "EOS": EOS_TOKEN}
    english_word2index_n = 2
    frence_word2index = {"SOS": SOS_TOKEN, "EOS": EOS_TOKEN}
    frence_word2index_n = 2
    for seq in my_pair:
        # 英文词对下标
        for word in seq[0].split(" "):
            if word not in english_word2index:
                english_word2index[word] = english_word2index_n
                english_word2index_n += 1
        # 法文词对下标
        for word in seq[1].split(" "):
            if word not in frence_word2index:
                frence_word2index[word] = frence_word2index_n
                frence_word2index_n += 1
    # print(english_word2index,english_word2index_n)
    # print(frence_word2index,frence_word2index_n)
    english_index2word = {v: k for k, v in english_word2index.items()}
    frence_index2word = {v: k for k, v in frence_word2index.items()}
    # print(english_index2word,frence_index2word)
    return english_word2index, english_index2word, english_word2index_n, frence_word2index, frence_index2word, frence_word2index_n, my_pair


# 构建数据加载器对象
class DatasetMyPairs(Dataset):
    def __init__(self, my_pair, english_word2index, frence_word2index):
        """
        my_pair: 数据集对象
        english_word2index: 英文词表
        frence_word2index: 法文词表
        """
        self.my_pair = my_pair
        self.english_word2index = english_word2index
        self.frence_word2index = frence_word2index
        self.samples_n = len(my_pair)

    def __len__(self):
        return self.samples_n

    def __getitem__(self, index):
        # 修正下标,防止下标越界
        index = min(max(index, 0), self.samples_n - 1)
        # print(index)
        # 从数据集中获取句子对象
        x = my_pair[index][0]
        y = my_pair[index][1]

        # 获取到对应句子之后将句子分词,
        x = [self.english_word2index[word] for word in x.split(" ")]
        x.append(EOS_TOKEN)
        y = [self.frence_word2index[word] for word in y.split(" ")]
        y.append(EOS_TOKEN)

        # 将获取的下标构建为张量形式
        tensor_x = torch.tensor(data=x, dtype=torch.long, device=device)
        tensor_y = torch.tensor(data=y, dtype=torch.long, device=device)
        return tensor_x, tensor_y


class Encoder(nn.Module):
    def __init__(self, input_size, hidden_size):
        """
        参数说明:
        input_size:词表大小
        hidden_size:初始隐藏值维度
        """
        super().__init__()
        self.input_size = input_size
        self.hidden_size = hidden_size

        self.embedding = nn.Embedding(num_embeddings=self.input_size, embedding_dim=self.hidden_size)
        self.gru = nn.GRU(input_size=self.hidden_size, hidden_size=self.hidden_size, batch_first=True)

    def forward(self, input, h0=None):
        """
        input: 输入句子的张量表示
        h0:初始化隐藏状值
        """
        # input转换成词向量表示 (句子数, 句子长度, 词维度)
        embeded = self.embedding(input)
        # gru层提取输入序列语义表示
        output, hn = self.gru(embeded, h0)
        return output, hn

    def inithidden(self):
        torch_zeros = torch.zeros(size=(1, 1, self.hidden_size), device=device)
        return torch_zeros


class Decoder(nn.Module):
    def __init__(self, output_size, hidden_size,dropout_p=0.1):
        super().__init__()
        self.output_size = output_size
        self.hidden_size = hidden_size
        self.dropout_p = dropout_p
        # 1.实例化attn1和attn2线性层对象, 用于计算q和k的相似分值
        # 1.1 attn1是用于对q和k融合的结果进行线性计算, q特征数+k特征数
        self.attn1 = nn.Linear(in_features=self.hidden_size * 2, out_features=self.hidden_size)
        # 1.2 attn2是对attn1的一维向量相似分映射为标量相似分(1个特征值)
        self.attn2 = nn.Linear(in_features=self.hidden_size, out_features=1)
        self.attn_combine = nn.Linear(in_features=self.hidden_size * 2, out_features=self.hidden_size)
        # 3.实例化embedding层, droput层, gru层, 全连接层(线性层+logsoftmax层)
        # num_embeddings: 法文词表大小
        self.embedding = nn.Embedding(num_embeddings=self.output_size, embedding_dim=self.hidden_size)
        self.dropout = nn.Dropout(p=self.dropout_p)
        self.gru = nn.GRU(input_size=self.hidden_size, hidden_size=self.hidden_size, batch_first=True)
        # out_features: 法文词表大小/预测的类别数
        self.out = nn.Linear(in_features=self.hidden_size, out_features=self.output_size)
        self.softmax = nn.LogSoftmax(dim=-1)

    def forward(self, input, hidden, encoder_output):
        """
        前向传播计算
        :param input: 当前时间步的输入 (句子数, 词数) -> (1, 1)
        :param hidden: 当前时间步的输入隐藏状态值 s0=编码器的hn q
        :param encoder_outputs: 编码 器的output k/v
        :return: 法文预测结果 输出隐藏状态值(作为下一个时间步的输入隐藏状态值 q) 注意力权重分布attn_weights
        """
        embedded = self.dropout(self.embedding(input))
        expand_hidden = hidden.transpose(0, 1).expand(-1, encoder_output.shape[1], -1)
        attn_score = self.attn2(
            torch.tanh(self.attn1(torch.cat(tensors=[expand_hidden, encoder_output], dim=-1)))).squeeze(dim=2)
        attn_wights = torch.softmax(attn_score, dim=-1)
        c = torch.bmm(input=attn_wights.unsqueeze(dim=1), mat2=encoder_output)
        attn_applied = self.attn_combine(torch.cat(tensors=[embedded, c], dim=-1))
        output, hidden = self.gru(torch.relu(attn_applied), hidden)
        output = self.softmax(self.out(output[:, -1, :]))
        return output, hidden, attn_wights


if __name__ == "__main__":
    # data= normaliserString("I'm fine, thank you@.\n")
    english_word2index, english_index2word, english_word2index_n, frence_word2index, frence_index2word, frence_word2index_n, my_pair = load_data(
        dataPath)
    # print(english_word2index_n,frence_word2index_n)
    dataset = DatasetMyPairs(my_pair, english_word2index, frence_word2index)
    # print(dataset[0])
    dataLoader = DataLoader(dataset=dataset, batch_size=1, shuffle=True)
    encoder = Encoder(input_size=english_word2index_n, hidden_size=256)
    print(f"encoder:{encoder}")
    decoder=Decoder(output_size=frence_word2index_n,hidden_size=256)
    for train_x, train_y in dataLoader:
        encoder_output, hidden = encoder(train_x, encoder.inithidden())
        for i in range(train_y.shape[1]):
            input = train_y[:, i].view(-1, 1)
            output, hidden, attn_weight = decoder(input=input, hidden=hidden, encoder_output=encoder_output)
            print("output--->", output.shape, output)
            print("hidden--->", hidden.shape, hidden)
            print("attn_weights--->", attn_weight.shape, attn_weight)
            exit()
