import torch
import torch.nn as nn
from transformers import BertTokenizer, BertModel, BertConfig
from torch.utils.data import Dataset, DataLoader
from datasets import load_dataset
import time

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# print("device==========>",device)
model = BertModel.from_pretrained("../../../models/bert-base-chinese").to(device)
tokenizer = BertTokenizer.from_pretrained("../../../models/bert-base-chinese")
bert_config = BertConfig.from_pretrained("../../../models/bert-base-chinese")

hidden_size = model.config.hidden_size


# print("hidden_size==========>", hidden_size)
def load_data():
    train_dataset = load_dataset(path="csv", data_files={
        "train": "./data/train.csv",
        "test": "./data/test.csv",
        "valid": "./data/validation.csv"
    })
    # print(train_dataset)
    return train_dataset


class MyModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc = nn.Linear(hidden_size, 2)

    def forward(self, input_ids, attention_mask, token_type_ids):
        with torch.no_grad():
            # 预训练模型结果
            output = model(input_ids, attention_mask, token_type_ids)
        # 池化层结果
        output = self.fc(output.pooler_output)
        return output


def collate_fn(batch):
    # print("batch==========>", batch)
    texts = [dict1['text'] for dict1 in batch]
    # print('texts--->', len(texts), texts)
    labels = [dict1['label'] for dict1 in batch]
    input = tokenizer(text=texts, padding=True, truncation=True, return_tensors="pt", max_length=500)
    return input['input_ids'].to(device), input['attention_mask'].to(device), input['token_type_ids'].to(
        device), torch.tensor(labels).to(device)


def train():
    datasets = load_data()
    train_dataset = datasets["train"]
    test_dataset = datasets["test"]
    valid_dataset = datasets["valid"]
    train_dataloader = DataLoader(dataset=train_dataset, batch_size=8, shuffle=True, drop_last=True,
                                  collate_fn=collate_fn)
    # print("train_dataloader====>", train_dataloader)
    # 模型调用
    my_model = MyModel().to(device)
    # 切换模型为训练模式
    my_model.train()
    # 冻结预训练模型参数
    for params in model.parameters():
        params.requires_grad = False
    # 定义优化器对象
    optimizer = torch.optim.AdamW(my_model.parameters(), lr=5e-4)
    # 定义损失函数
    criterion = nn.CrossEntropyLoss()
    epochs = 3
    for epoch in range(epochs):
        for i, (input_ids, attention_mask, token_type_ids, labels) in enumerate(train_dataloader, start=1):
            starttime = time.time()
            pred_y = my_model(input_ids, attention_mask, token_type_ids)
            loss = criterion(pred_y, labels)
            # print("loss==========>", loss.item())
            # 梯度清零
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            # 4.6.4 打印训练日志
            if i % 5 == 0:  # 每5个batch打印一次训练日志
                y_pred_index = pred_y.argmax(dim=-1)
                # print('y_pred_index--->', y_pred_index)
                acc = (y_pred_index == labels).sum().item() / len(labels)
                print(f'轮次:{epoch} 迭代数:{i}, 损失:{loss.item()} 准确率{acc} 时间{time.time() - starttime}')
            torch.save(my_model.state_dict(), f'model/my_model{epoch + 1}.bin')


if __name__ == '__main__':
    # datasets = load_data()
    # print(datasets)
    # MyModel()
    train()
