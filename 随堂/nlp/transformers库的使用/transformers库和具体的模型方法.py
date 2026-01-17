import torch
import os


def dm0(model_name):
    model_dir = "../../../models/" + model_name
    if os.path.exists(model_dir):
        print(f"✓ 模型路径存在: {os.path.abspath(model_dir)}")
        print(f"✓ 模型文件夹内容: {os.listdir(model_dir)}")
    else:
        print(f"✗ 模型路径不存在: {os.path.abspath(model_dir)}")


# 情感分类任务
def dm01():
    # dm0("chinese_sentiment")
    from transformers import BertTokenizer  # 分词器
    from transformers import BertForSequenceClassification  # 模型
    from transformers import BertConfig
    # 1自动加载分词器
    tokenizers = BertTokenizer.from_pretrained("../../../models/chinese_sentiment")
    # print("tokenizers==========>", tokenizers)
    # 2自动加载模型
    my_model = BertForSequenceClassification.from_pretrained("../../../models/chinese_sentiment")
    # print("my_model======>", my_model)
    # 3 模型配置信息
    configparser = BertConfig.from_pretrained("../../../models/chinese_sentiment")
    # print("configparser==========>", configparser)

    # 4 模型输入
    message = "人生何处不春风"
    input_ids = tokenizers.encode(text=message, return_tensors="pt", max_length=50, add_special_tokens=True)
    print("input_ids==========>", input_ids)

    # 5切换模型模式为评估模式
    my_model.eval()

    # 6获得模型预测结果
    output = my_model(input_ids, return_dict=True)
    print("output==========>", output)

    # 7 线性计算结果转化为随机概率
    probs = torch.softmax(output.logits, dim=-1)
    print("probs==========>", probs)
    # 获取概率最大值对应的索引(类别编号0,1,2,3,4)
    class_id = torch.argmax(probs, dim=-1).item()
    print('分类idclass_id--->', class_id)

    print(my_model.config.id2label[class_id])
    print(configparser.id2label[class_id])


# 特征提取任务
def dm02():
    # dm0("bert-base-chinese")
    from transformers import BertTokenizer
    from transformers import BertModel
    tokenizers = BertTokenizer.from_pretrained("../../../models/bert-base-chinese")
    # print("tokenizers==========>", tokenizers)
    model = BertModel.from_pretrained("../../../models/bert-base-chinese")
    # print("model==========>", model)
    message = ["你是哪位", "春风得意马蹄疾"]
    # encode_plus() 的主要功能是将原始文本转换为模型所需的输入格式(字典类型)，包括：
    # input_ids: 输入文本的词下标表示
    # token_type_ids: 句子的标记，0表示第一个句子，1表示第二个句子  1后续的0是填充的  不是必须返回的(跟模型相关)
    # attention_mask: 表示哪些是需要计算注意力的，1表示需要计算，0表示不需要计算
    input_ids = tokenizers.encode_plus(message, return_tensors="pt", max_length=50, truncation=True)
    # print("input_ids==========>", input_ids)
    # 切换模型推理模式
    model.eval()
    output = model(**input_ids)
    # print("output==========>", output)
    # last_hidden_state表示所有词最后一层隐藏层的输出
    print("last_hidden_state==========>", output.last_hidden_state)
    # pooler_output表示所有词最后一层隐藏层的输出的池化结果
    print("pooler_output==========>", output.pooler_output)


# 完型填空任务
def dm03():
    from transformers import BertTokenizer
    from transformers import AutoModelForMaskedLM
    tokenizers = BertTokenizer.from_pretrained("../../../models/chinese-bert-wwm")
    model = AutoModelForMaskedLM.from_pretrained("../../../models/chinese-bert-wwm")
    # print("model==========>", model)
    input = tokenizers.encode_plus("我今天学习了大模型，我想写一个关于[MASK]的博客", return_tensors="pt")
    print("input==========>", input)
    # print("input.input_ids==========>", input)
    model.eval()
    output = model(**input)
    # print("output==========>", output)
    print("output.logits=========>", output.logits)
    # 取概率最高的
    mask_print_idx = torch.argmax(output.logits[0][18]).item()
    print("mask_print_idx==========>", mask_print_idx)
    print("预测结果==========>", tokenizers.convert_ids_to_tokens([mask_print_idx]))


#  文本摘要任务
def dm04():
    from transformers import BartTokenizer
    from transformers import BartModel
    text = "BERT is a transformers model pretrained on a large corpus of English data " \
           "in a self-supervised fashion. This means it was pretrained on the raw texts " \
           "only, with no humans labelling them in any way (which is why it can use lots " \
           "of publicly available data) with an automatic process to generate inputs and " \
           "labels from those texts. More precisely, it was pretrained with two objectives:Masked " \
           "language modeling (MLM): taking a sentence, the model randomly masks 15% of the " \
           "words in the input then run the entire masked sentence through the model and has " \
           "to predict the masked words. This is different from traditional recurrent neural " \
           "networks (RNNs) that usually see the words one after the other, or from autoregressive " \
           "models like GPT which internally mask the future tokens. It allows the model to learn " \
           "a bidirectional representation of the sentence.Next sentence prediction (NSP): the models" \
           " concatenates two masked sentences as inputs during pretraining. Sometimes they correspond to " \
           "sentences that were next to each other in the original text, sometimes not. The model then " \
           "has to predict if the two sentences were following each other or not."
    # dm0("distilbart-cnn-12-6")
    tokenizers = BartTokenizer.from_pretrained("../../../models/distilbart-cnn-12-6")
    model = BartModel.from_pretrained("../../../models/distilbart-cnn-12-6")
    input = tokenizers([text], return_tensors="pt")
    print("input==========>", input)
    model.eval()
    output = model(input.input_ids)
    print("output==========>", output)

if __name__ == '__main__':
    # dm01()
    # dm02()
    # dm03()
    dm04()
