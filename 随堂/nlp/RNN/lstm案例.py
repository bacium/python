import torch
import torch.nn as nn




def dm_lstm():
    def __init__(self):
        super().__init__()
        self.lstm = nn.LSTM(
            input_size=10,
            hidden_size=20,
            num_layers=2,
            batch_first=True,
            bidirectional=True,
        )
if __name__ == '__main__':
    dm_lstm()