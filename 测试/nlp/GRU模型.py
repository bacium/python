import torch
import torch.nn as nn


class MyGRU(nn.Module):
    def __init__(self, input_size, hidden_size, output_size, num_layers, droup_out):
        super().__init__()
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.num_layers = num_layers
        self.droup_out = droup_out
        # 定义GRU
        self.gru = nn.GRU(
            input_size=self.input_size,
            hidden_size=self.hidden_size,
            num_layers=self.num_layers,
            batch_first=True,
            dropout=self.droup_out,
        )
        # 全连接层
        self.out = nn.Linear(in_features=self.hidden_size, out_features=self.output_size)

    # 反向传播
    def forward(self, x):
        batch_size = x.size(0)
        # 初始状态值
        h0 = torch.zeros(self.num_layers, batch_size, self.hidden_size)
        output, hn = self.gru(x, h0)
        output = self.out(output)
        return output



def create_sample_data():
    batch_size = 32
    sequence_length = 20
    input_size = 5
    X = torch.randn(batch_size, sequence_length, input_size)
    y = X[:, :, 0].mean(dim=1, keepdim=True) + torch.randn(batch_size, 1) * 0.1

    return X, y
if __name__ == "__main__":
    input_size = 5
    hidden_size = 64
    output_size = 1
    num_layers = 2

    # 创建模型
    model = MyGRU(
        input_size=input_size,
        hidden_size=hidden_size,
        output_size=output_size,
        num_layers=num_layers,
        droup_out=0.2
    )
    # 测试数据 - 修正维度匹配
    batch_size = 32
    sequence_length = 20
    X = torch.randn(batch_size, sequence_length, input_size)  # 使用 input_size 而不是 10
    model(X)
    print(model)

