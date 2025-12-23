import torch
import torch.nn as nn


class RNNModel(nn.Module):

    def __init__(self):
        super().__init__()
        # 嵌入层
        # num_embeddings 词表大小
        self.embedding = nn.Embedding(num_embeddings=10, embedding_dim=10)
        self.rnn = nn.RNN(
            input_size=10,
            hidden_size=20,
            num_layers=1,
            batch_first=True,
            bidirectional=False,
        )
        self.out = nn.Linear(20, 4)

    def forward(self, x,h0=None):
        embeded = self.embedding(x)
        print("嵌入层处理结果:", embeded.shape, embeded)
        output, hn = self.rnn(embeded,h0)
        print("RNN处理结果:", output.shape, output)
        result = self.out(hn[-1])
        print("输出结果:", result.shape, result)


if __name__ == "__main__":
    input = torch.tensor([[1, 3, 4], [3, 1, 5]])
    model = RNNModel()
    h0 = torch.zeros(size=(1, 2, 20))
    model(input, h0)
