import torch
import torch.nn.functional as F


def scaled_dot_product_attention(
        q: torch.Tensor,
        k: torch.Tensor,
        v: torch.Tensor,
        mask: torch.Tensor = None
) -> tuple[torch.Tensor, torch.Tensor]:
    """
    实现带掩码的缩放点积注意力
    Args:
        q: 查询向量 [batch_size, num_heads, seq_len_q, d_k]
        k: 键向量 [batch_size, num_heads, seq_len_k, d_k]
        v: 值向量 [batch_size, num_heads, seq_len_v, d_v]
           注意：seq_len_k 必须等于 seq_len_v，d_k 通常等于 d_v
        mask: 掩码张量 [batch_size, 1, seq_len_q, seq_len_k] 或 [1, 1, seq_len_q, seq_len_k]
              True表示该位置需要被屏蔽（置为负无穷）
    Returns:
        output: 注意力加权后的输出 [batch_size, num_heads, seq_len_q, d_v]
        attn_weights: 注意力权重矩阵 [batch_size, num_heads, seq_len_q, seq_len_k]
    """
    # 获取d_k（查询/键向量的维度）
    d_k = q.size(-1)

    # 1. 计算Q和K的点积 -> 原始注意力分数
    # [batch_size, num_heads, seq_len_q, seq_len_k]
    scores = torch.matmul(q, k.transpose(-2, -1))

    # 2. 缩放：除以√d_k，避免分数过大导致Softmax梯度消失
    scores = scores / torch.sqrt(torch.tensor(d_k, dtype=torch.float32))

    # 3. 应用掩码：将掩码位置的分数置为负无穷（Softmax后权重趋近于0）
    if mask is not None:
        # 确保mask的dtype与scores一致，避免类型错误
        scores = scores.masked_fill(mask, -1e9)

    # 4. Softmax归一化，得到注意力权重
    attn_weights = F.softmax(scores, dim=-1)

    # 5. 注意力权重与V相乘，得到最终输出
    output = torch.matmul(attn_weights, v)

    return output, attn_weights


# ------------------- 测试代码 -------------------
if __name__ == "__main__":
    # 模拟输入：batch_size=2, num_heads=1, seq_len=4, d_k/d_v=64
    batch_size = 2
    num_heads = 1
    seq_len = 4
    d_k = d_v = 64

    # 生成随机的Q/K/V
    q = torch.randn(batch_size, num_heads, seq_len, d_k)
    k = torch.randn(batch_size, num_heads, seq_len, d_k)
    v = torch.randn(batch_size, num_heads, seq_len, d_v)

    # 1. 测试无掩码场景
    output, attn_weights = scaled_dot_product_attention(q, k, v)
    print("无掩码输出形状:", output.shape)  # [2, 1, 4, 64]
    print("无掩码注意力权重形状:", attn_weights.shape)  # [2, 1, 4, 4]
    print("无掩码注意力权重（第1个样本）:\n", attn_weights[0, 0].round(3), "\n")

    # 2. 测试序列掩码（未来掩码，模拟解码器自注意力）
    # 生成[1, 1, 4, 4]的未来掩码：上三角为True（屏蔽未来位置）
    seq_mask = torch.triu(torch.ones(1, 1, seq_len, seq_len), diagonal=1).bool()
    output_masked, attn_weights_masked = scaled_dot_product_attention(q, k, v, mask=seq_mask)
    print("序列掩码:\n", seq_mask[0, 0])
    print("带序列掩码的注意力权重（第1个样本）:\n", attn_weights_masked[0, 0].round(3))

    # 3. 测试填充掩码（模拟编码器/解码器屏蔽PAD）
    # 模拟输入序列：[batch_size, seq_len]，PAD token_id=0
    seq = torch.tensor([[1, 2, 0, 0], [3, 0, 4, 0]])  # 0是PAD
    pad_mask = (seq == 0).unsqueeze(1).unsqueeze(2)  # [2, 1, 1, 4]
    output_pad, attn_weights_pad = scaled_dot_product_attention(q, k, v, mask=pad_mask)
    print("\n填充掩码:\n", pad_mask[:, 0, 0])
    print("带填充掩码的注意力权重（第1个样本）:\n", attn_weights_pad[0, 0].round(3))