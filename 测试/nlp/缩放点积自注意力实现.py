import torch
import torch.nn as nn


def scaled_dot_product_attention(q, k, v, mask=None):
    scores = torch.matmul(q, k.transpose(-2, -1))
    d_k = q.size(-1)
    # 计算得分
    scores = scores / torch.sqrt(torch.tensor(d_k))
    print(f"注意力得分：{scores}, {scores.shape}")
    if mask is not None:
        scores = scores.masked_fill(mask == 0, -1e9)
        print(f"带掩码的注意力得分：{scores}, {scores.shape}")
    attn_weight = nn.softmax(scores, dim=-1)
    # print(attn_weight, attn_weight.shape)
    output = torch.matmul(attn_weight, v)
    return output, attn_weight


if __name__ == '__main__':
    q = torch.randn(10, 3, 64)
    k = torch.randn(10, 3, 64)
    v = torch.randn(10, 3, 64)
    seq_mask = torch.randint(0, 2, (10, 3, 3))
    # 计算缩放点积注意力(无掩码的)
    output,attn_weight = scaled_dot_product_attention(q, k, v,seq_mask)
