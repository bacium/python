import torch
import torch.nn as nn
import torch.nn.functional as F
import math


# ---------------------- 1. 位置编码（正弦余弦）----------------------
class PositionalEncoding(nn.Module):
    def __init__(self, embedding_dim, max_seq_len=512):
        super(PositionalEncoding, self).__init__()
        self.embedding_dim = embedding_dim

        # 初始化位置编码矩阵，shape: [max_seq_len, embedding_dim]
        pe = torch.zeros(max_seq_len, embedding_dim)
        # 生成位置索引，shape: [max_seq_len, 1]
        pos = torch.arange(0, max_seq_len, dtype=torch.float).unsqueeze(1)

        # 计算分母项（避免重复计算）
        div_term = torch.exp(torch.arange(0, embedding_dim, 2).float() * (-math.log(10000.0) / embedding_dim))

        # 填充偶数维（sin）和奇数维（cos）
        pe[:, 0::2] = torch.sin(pos * div_term)  # 0::2 表示从0开始，步长2（偶数索引）
        pe[:, 1::2] = torch.cos(pos * div_term)  # 1::2 表示从1开始，步长2（奇数索引）

        # 增加batch维度，shape: [1, max_seq_len, embedding_dim]（方便后续与批次数据相加）
        self.register_buffer('pe', pe.unsqueeze(0))

    def forward(self, x):
        """
        输入x: 词嵌入序列，shape: [batch_size, seq_len, embedding_dim]
        输出: 带位置信息的嵌入序列，shape与x一致
        """
        # 只取与输入序列长度匹配的位置编码
        x = x + self.pe[:, :x.size(1), :]
        return x


# ---------------------- 2. 多头自注意力模块 ----------------------
class MultiHeadAttention(nn.Module):
    def __init__(self, embedding_dim, num_heads):
        super(MultiHeadAttention, self).__init__()
        # 断言：embedding_dim必须能被num_heads整除（保证每个头的维度相等）
        assert embedding_dim % num_heads == 0, "embedding_dim must be divisible by num_heads"

        self.embedding_dim = embedding_dim  # 整体维度D
        self.num_heads = num_heads  # 头数h
        self.d_k = embedding_dim // num_heads  # 每个头的维度d_k=D/h

        # 定义Q、K、V、输出的线性变换矩阵（全连接层，无激活函数）
        self.W_q = nn.Linear(embedding_dim, embedding_dim)
        self.W_k = nn.Linear(embedding_dim, embedding_dim)
        self.W_v = nn.Linear(embedding_dim, embedding_dim)
        self.W_o = nn.Linear(embedding_dim, embedding_dim)

    def scaled_dot_product_attention(self, Q, K, V, mask=None):
        """
        单头自注意力的核心计算（批量处理，支持多头）
        Q/K/V shape: [batch_size, num_heads, seq_len, d_k]
        mask shape: [batch_size, 1, seq_len, seq_len]（可选）
        返回: 注意力输出，注意力权重
        """
        # 步骤1：计算Q与K^T的得分，shape: [batch_size, num_heads, seq_len, seq_len]
        scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(self.d_k)

        # 步骤2：应用掩码（如果有）
        if mask is not None:
            # 掩码位置填充为-1e9（近似-∞），softmax后权重趋近于0
            scores = scores.masked_fill(mask == 0, -1e9)

        # 步骤3：softmax归一化得到注意力权重
        attn_weights = F.softmax(scores, dim=-1)

        # 步骤4：加权求和得到输出
        output = torch.matmul(attn_weights, V)

        return output, attn_weights

    def split_heads(self, x):
        """
        将输入x拆分为多个头，方便并行计算
        输入x shape: [batch_size, seq_len, embedding_dim]
        输出 shape: [batch_size, num_heads, seq_len, d_k]
        """
        batch_size, seq_len, embedding_dim = x.size()
        # 先reshape：[batch_size, seq_len, num_heads, d_k]
        x = x.view(batch_size, seq_len, self.num_heads, self.d_k)
        # 转置：将num_heads提到第二维，方便后续计算
        return x.transpose(1, 2)

    def combine_heads(self, x):
        """
        将多个头的输出拼接回原来的维度
        输入x shape: [batch_size, num_heads, seq_len, d_k]
        输出 shape: [batch_size, seq_len, embedding_dim]
        """
        batch_size, num_heads, seq_len, d_k = x.size()
        # 先转置：[batch_size, seq_len, num_heads, d_k]
        x = x.transpose(1, 2).contiguous()
        # 再reshape拼接：[batch_size, seq_len, embedding_dim]
        return x.view(batch_size, seq_len, self.embedding_dim)

    def forward(self, Q, K, V, mask=None):
        """
        多头自注意力前向传播
        Q/K/V: 输入向量（自注意力时三者相同，交叉注意力时Q不同）
        mask: 掩码矩阵（可选）
        """
        # 步骤1：线性变换生成Q、K、V，shape: [batch_size, seq_len, embedding_dim]
        Q_linear = self.W_q(Q)
        K_linear = self.W_k(K)
        V_linear = self.W_v(V)

        # 步骤2：拆分为多个头，shape: [batch_size, num_heads, seq_len, d_k]
        Q_split = self.split_heads(Q_linear)
        K_split = self.split_heads(K_linear)
        V_split = self.split_heads(V_linear)

        # 步骤3：执行缩放点积注意力，得到输出和权重
        attn_output, attn_weights = self.scaled_dot_product_attention(Q_split, K_split, V_split, mask)

        # 步骤4：拼接多个头的输出，shape: [batch_size, seq_len, embedding_dim]
        attn_output_concat = self.combine_heads(attn_output)

        # 步骤5：最终线性变换，融合多头信息
        final_output = self.W_o(attn_output_concat)

        return final_output, attn_weights


# ---------------------- 3. 前馈神经网络模块 ----------------------
class FeedForwardNetwork(nn.Module):
    def __init__(self, embedding_dim, ff_dim=2048):
        super(FeedForwardNetwork, self).__init__()
        # 两层全连接层
        self.fc1 = nn.Linear(embedding_dim, ff_dim)
        self.fc2 = nn.Linear(ff_dim, embedding_dim)
        # 激活函数（GELU比ReLU效果更好，常用在大模型中）
        self.gelu = nn.GELU()

    def forward(self, x):
        """
        前向传播
        输入x shape: [batch_size, seq_len, embedding_dim]
        输出 shape: 与输入一致
        """
        # 第一层：线性变换+GELU激活
        x = self.gelu(self.fc1(x))
        # 第二层：线性变换（无激活）
        x = self.fc2(x)
        return x


# ---------------------- 4. 编码器单层 ----------------------
class EncoderLayer(nn.Module):
    def __init__(self, embedding_dim, num_heads, ff_dim=2048, dropout=0.1):
        super(EncoderLayer, self).__init__()
        # 核心模块
        self.self_attn = MultiHeadAttention(embedding_dim, num_heads)
        self.ffn = FeedForwardNetwork(embedding_dim, ff_dim)

        # 层归一化
        self.norm1 = nn.LayerNorm(embedding_dim)
        self.norm2 = nn.LayerNorm(embedding_dim)

        # Dropout（防止过拟合）
        self.dropout1 = nn.Dropout(dropout)
        self.dropout2 = nn.Dropout(dropout)

    def forward(self, x, mask=None):
        """
        编码器单层前向传播
        输入x shape: [batch_size, seq_len, embedding_dim]
        输出 shape: 与输入一致
        """
        # 子层1：多头自注意力（自注意力时Q=K=V=x）
        attn_output, _ = self.self_attn(x, x, x, mask)
        # Dropout+残差连接+层归一化（注意：先Dropout，再残差，再归一化）
        x = self.norm1(x + self.dropout1(attn_output))

        # 子层2：前馈神经网络
        ffn_output = self.ffn(x)
        # Dropout+残差连接+层归一化
        x = self.norm2(x + self.dropout2(ffn_output))

        return x


# ---------------------- 5. 解码器单层 ----------------------
class DecoderLayer(nn.Module):
    def __init__(self, embedding_dim, num_heads, ff_dim=2048, dropout=0.1):
        super(DecoderLayer, self).__init__()
        # 核心模块
        self.masked_self_attn = MultiHeadAttention(embedding_dim, num_heads)
        self.cross_attn = MultiHeadAttention(embedding_dim, num_heads)
        self.ffn = FeedForwardNetwork(embedding_dim, ff_dim)

        # 层归一化
        self.norm1 = nn.LayerNorm(embedding_dim)
        self.norm2 = nn.LayerNorm(embedding_dim)
        self.norm3 = nn.LayerNorm(embedding_dim)

        # Dropout
        self.dropout1 = nn.Dropout(dropout)
        self.dropout2 = nn.Dropout(dropout)
        self.dropout3 = nn.Dropout(dropout)

    def forward(self, x, enc_output, src_mask=None, tgt_mask=None):
        """
        解码器单层前向传播
        x: 解码器输入，shape: [batch_size, tgt_seq_len, embedding_dim]
        enc_output: 编码器输出，shape: [batch_size, src_seq_len, embedding_dim]
        src_mask: 源序列掩码（可选）
        tgt_mask: 目标序列掩码（未来掩码，必选）
        """
        # 子层1：掩码多头自注意力
        masked_attn_output, _ = self.masked_self_attn(x, x, x, tgt_mask)
        x = self.norm1(x + self.dropout1(masked_attn_output))

        # 子层2：编码器-解码器交叉注意力（Q=x, K=V=enc_output）
        cross_attn_output, _ = self.cross_attn(x, enc_output, enc_output, src_mask)
        x = self.norm2(x + self.dropout2(cross_attn_output))

        # 子层3：前馈神经网络
        ffn_output = self.ffn(x)
        x = self.norm3(x + self.dropout3(ffn_output))

        return x


# ---------------------- 6. 完整Transformer模型 ----------------------
class Transformer(nn.Module):
    def __init__(self, src_vocab_size, tgt_vocab_size, embedding_dim=512, num_heads=8,
                 num_layers=6, ff_dim=2048, max_seq_len=512, dropout=0.1):
        super(Transformer, self).__init__()
        self.embedding_dim = embedding_dim
        self.num_layers = num_layers

        # 输入/输出嵌入层
        self.src_embedding = nn.Embedding(src_vocab_size, embedding_dim)
        self.tgt_embedding = nn.Embedding(tgt_vocab_size, embedding_dim)

        # 位置编码
        self.positional_encoding = PositionalEncoding(embedding_dim, max_seq_len)

        # 编码器栈（堆叠num_layers层EncoderLayer）
        self.encoder_layers = nn.ModuleList([
            EncoderLayer(embedding_dim, num_heads, ff_dim, dropout)
            for _ in range(num_layers)
        ])

        # 解码器栈（堆叠num_layers层DecoderLayer）
        self.decoder_layers = nn.ModuleList([
            DecoderLayer(embedding_dim, num_heads, ff_dim, dropout)
            for _ in range(num_layers)
        ])

        # 最终输出层（线性变换+softmax，这里只做线性变换，softmax在计算损失时做）
        self.final_linear = nn.Linear(embedding_dim, tgt_vocab_size)

        # Dropout
        self.dropout = nn.Dropout(dropout)

    def generate_mask(self, src_seq, tgt_seq):
        """
        生成源序列掩码和目标序列掩码（简化版，仅处理未来掩码，忽略padding掩码）
        src_seq: 输入序列，shape: [batch_size, src_seq_len]
        tgt_seq: 输出序列，shape: [batch_size, tgt_seq_len]
        """
        batch_size, src_seq_len = src_seq.size()
        batch_size, tgt_seq_len = tgt_seq.size()

        # 目标序列的未来掩码（下三角矩阵），shape: [1, tgt_seq_len, tgt_seq_len]
        tgt_mask = torch.tril(torch.ones((tgt_seq_len, tgt_seq_len))).unsqueeze(0)

        # 源序列掩码（这里简化为None，实际应用中需要处理padding token）
        src_mask = None

        return src_mask, tgt_mask

    def forward(self, src_seq, tgt_seq):
        """
        完整Transformer前向传播
        src_seq: 输入序列（Token ID），shape: [batch_size, src_seq_len]
        tgt_seq: 输出序列（Token ID），shape: [batch_size, tgt_seq_len]
        """
        # 步骤1：生成掩码
        src_mask, tgt_mask = self.generate_mask(src_seq, tgt_seq)

        # 步骤2：输入序列处理（嵌入+位置编码+Dropout）
        src_emb = self.src_embedding(src_seq)  # [batch_size, src_seq_len, embedding_dim]
        src_emb = self.positional_encoding(src_emb)  # 加位置编码
        src_emb = self.dropout(src_emb)  # Dropout

        # 步骤3：编码器栈前向传播
        enc_output = src_emb
        for encoder_layer in self.encoder_layers:
            enc_output = encoder_layer(enc_output, src_mask)

        # 步骤4：输出序列处理（嵌入+位置编码+Dropout）
        tgt_emb = self.tgt_embedding(tgt_seq)  # [batch_size, tgt_seq_len, embedding_dim]
        tgt_emb = self.positional_encoding(tgt_emb)  # 加位置编码
        tgt_emb = self.dropout(tgt_emb)  # Dropout

        # 步骤5：解码器栈前向传播
        dec_output = tgt_emb
        for decoder_layer in self.decoder_layers:
            dec_output = decoder_layer(dec_output, enc_output, src_mask, tgt_mask)

        # 步骤6：最终线性变换，得到词表得分
        logits = self.final_linear(dec_output)  # [batch_size, tgt_seq_len, tgt_vocab_size]

        return logits


# ---------------------- 7. 测试模型（观察各模块输出形状）----------------------
if __name__ == "__main__":
    # 超参数设置（简化版，小批量小维度，方便测试）
    src_vocab_size = 1000  # 输入词表大小
    tgt_vocab_size = 1000  # 输出词表大小
    embedding_dim = 128  # 嵌入维度（简化为128，方便计算）
    num_heads = 4  # 多头数（4，128/4=32，符合要求）
    num_layers = 2  # 编码器/解码器层数（2，简化训练）
    batch_size = 2  # 批次大小
    src_seq_len = 10  # 输入序列长度
    tgt_seq_len = 8  # 输出序列长度

    # 1. 初始化模型
    model = Transformer(src_vocab_size, tgt_vocab_size, embedding_dim, num_heads, num_layers)

    # 2. 生成随机输入/输出序列（Token ID，范围0~vocab_size-1）
    src_seq = torch.randint(0, src_vocab_size, (batch_size, src_seq_len))
    tgt_seq = torch.randint(0, tgt_vocab_size, (batch_size, tgt_seq_len))

    # 3. 前向传播
    logits = model(src_seq, tgt_seq)

    # 4. 打印各部分形状，观察流程
    print("=" * 50)
    print("输入序列形状：", src_seq.shape)
    print("输出序列形状：", tgt_seq.shape)
    print("模型最终输出形状：", logits.shape)
    print("=" * 50)
    print("模型初始化成功，各模块流程正常！")