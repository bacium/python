"""
    使用Hugging Face 的transformer库具体模型加载预训练模型
"""
from transformers import BertTokenizer, BertForSequenceClassification, BertConfig
import torch


def dm():
    tokenizers = BertTokenizer.from_pretrained("../../models/chinese_sentiment")
    # print("tokenizers==========>", tokenizers)
    model = BertForSequenceClassification.from_pretrained("../../models/chinese_sentiment")
    # print("model==========>", model)
    config = BertConfig.from_pretrained("../../models/chinese_sentiment")
    # print("config==========>", config)
    message = "人生得意须尽欢！"
    input = tokenizers(text=message, return_tensors="pt", max_length=30, padding="max_length", truncation=True)
    # print("input_ids==========>", input)
    # 切换模型为推理模式
    model.eval()
    output = model(input_ids=input.input_ids, return_dict=True)
    print("output==========>", output)
    temp = torch.softmax(output.logits, dim=-1)
    result = torch.argmax(temp, dim=-1).item()
    print("result==========>", config.id2label[result])


if __name__ == '__main__':
    dm()
