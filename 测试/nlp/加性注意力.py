import torch
import torch.nn as nn
import torch.nn.functional as fc


class AdditiveAttention(nn.Module):
    def __init__(self, query_dim, key_dim, hidden_dim):
        super().__init__()
        self.W_q = nn.Linear(query_dim, hidden_dim, bias=False)
        self.W_k = nn.Linear(key_dim, hidden_dim, bias=False)
        self.v = nn.Linear(hidden_dim, 1, bias=False)

        self.fc = nn.Linear(query_dim + key_dim, query_dim)

    def forward(self, query, keys, values):
        batch_size, le, _ = keys.size()

        q_proj = self.W_q(query).unsqueeze(1)

        k_proj = self.W_k(keys)

        scores = self.v(torch.tanh(q_proj + k_proj)).squeeze(-1)

        # softmax 得到注意力权重
        attn_weights = fc.softmax(scores, dim=1)

        context = torch.bmm(attn_weights.unsqueeze(1), values)
        context = context.squeeze(1)

        fused = torch.cat([query, context], dim=-1)
        output = self.fc(fused)

        return output, attn_weights


if __name__ == '__main__':
    query = torch.randn(5, 10)
    keys = torch.randn(5, 20, 10)
    values = torch.randn(5, 20, 10)

    attn = AdditiveAttention(10, 10, 10)
    output, attn_weights = attn(query, keys, values)

    print(output.size())
    print(attn_weights.size())