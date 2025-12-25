import torch
import torch.nn as nn


class MyAtt(nn.Module):
    def __init__(self, query_size, key_size, hidden_size, output_size):
        super().__init__()
        self.query_size = query_size
        self.key_size = key_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.linear1 = nn.Linear(in_features=self.query_size + self.key_size, out_features=self.hidden_size)
        self.linear2 = nn.Linear(in_features=self.hidden_size, out_features=1)
        self.combine = nn.Linear(in_features=self.key_size + self.hidden_size, out_features=self.output_size)
        self.gru = nn.GRU(input_size=self.output_size, hidden_size=128, batch_first=True)

    def forward(self, x, q, k, v):
        # 对q在1轴上进行复制, 1轴的维度值=K的1轴维度值
        expand_q = q.expand(-1, k.shape[1], -1)
        print(f"expand_q=====>{expand_q}")
        # q和v先在特征维度进行拼接 concat
        q_k_cat = torch.concat([expand_q, k], dim=-1)
        print(f"q_k_cat=====>{q_k_cat}")
        # 使用线性层1对q和k在特征维度进行相似度计算(线性层学习相似分)
        temp_attn_score = torch.tanh(self.linear1(q_k_cat))
        print(f"temp_attn_score========>形状{temp_attn_score.shape},值{temp_attn_score}")
        # 使用线性层2对线性层1的一维向量相似分进行映射, 得到标量相似分
        # squeeze(dim=2):删除2轴, 去掉第3个维度, 变成2维  ->  降维
        attn_score = self.linear2(temp_attn_score).squeeze(dim=2)
        print(f"attn_score=======>{attn_score.shape},值:{attn_score}")
        # 计算权重概率分布
        attn_weights = torch.softmax(attn_score, dim=-1)
        print('attn_weights--->', attn_weights.shape, attn_weights)
        c = torch.bmm(attn_weights.unsqueeze(dim=1), v)
        print('c--->', c.shape, c)
        # 将注意力表示c和输入x先在特征维度进行拼接, 然后进行线性映射, 获得当前时间步输入的新x表示
        new_x = self.combine(torch.concat([c, x], dim=-1))
        print(f"new_x=======>{new_x.shape},值{new_x}")

        output, hn = self.gru(new_x)
        print('output--->', output.shape, output)


if __name__ == "__main__":
    query_size = 32
    key_size = 32
    hidden_size = 32
    output_size = 32
    x = torch.randn(size=(1, 1, hidden_size))
    q = torch.randn(size=(1, 1, query_size))
    k = v = torch.randn(size=(1, 5, hidden_size))
    model = MyAtt(query_size=query_size, key_size=key_size, hidden_size=hidden_size, output_size=output_size)
    model(x, q, k, v)
