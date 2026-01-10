import torch
import torch.nn as nn
import math

# 使用三角函数生成位置编码
class Encoding(nn.Module):
    def __init__(self, d_model, seq_len, dropout):
        super().__init__()
        self.dropout = nn.Dropout(dropout)
        self.pe = torch.zeros(seq_len, d_model)
        self.position = torch.arange(0, seq_len).unsqueeze(1)
        # 位置信息分母
        self.div_term = torch.exp(torch.arange(0, d_model, 2) * -math.log(10000) / d_model)
        # 奇数和偶数计算
        self.pe[:, 0::2] = torch.sin(self.position * self.div_term)
        self.pe[:, 1::2] = torch.cos(self.position * self.div_term)

    def forward(self, x):
        # 加入位置信息
        x = x + self.pe
        return self.dropout(x)


if __name__ == '__main__':
    # 创建位置编码
    pe = Encoding(d_model=512, seq_len=100, dropout=0.1)
    x = torch.rand(1, 100, 512)
    out = pe(x)
    print(out.shape)