from tensorflow.keras.preprocessing import sequence
import torch
from torch.nn.utils.rnn import pad_sequence


def dm1():
    x_train = [[1, 3, 5, 2, 4, 6, 7, 8, 9, 10], [8, 5, 2, 3, 4]]
    cutlen = 8

    result = sequence.pad_sequences(x_train, maxlen=cutlen, truncating='post', padding='post')

    print(result)


def dm2():
    a = torch.ones(5)
    b = torch.ones(6)
    c = torch.ones(9)
    # pad_sequence 当前批次中最长的句子进行填充
    resulr = pad_sequence([a, b, c], batch_first=True)
    print(resulr)
    


if __name__ == '__main__':
    # dm1()
    dm2()
