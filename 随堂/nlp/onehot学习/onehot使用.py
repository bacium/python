from tensorflow.keras.preprocessing.text import Tokenizer # pyright: ignore[reportMissingImports]
import joblib


def dm1():
    """
    演示One-Hot编码的使用方法
    
    该函数通过Tokenizer对中文歌手姓名进行One-Hot编码，
    并展示如何保存和加载训练好的Tokenizer模型。
    """
    # 定义文本数据集，包含几位知名华语歌手姓名
    text = ["周杰伦", "陈奕迅", "王力宏", "李宗盛", "吴亦凡", "鹿晗"]
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(text)
    print(tokenizer.word_index)
    
    # 将文本转换为One-Hot编码矩阵，并去除第一列（索引从1开始）
    one_hot_matrix = tokenizer.texts_to_matrix(text, mode='binary')[:, 1:]
    # print('one_hot_matrix--->', one_hot_matrix)
    for word,idx in zip(text,one_hot_matrix):
        result = idx.astype(int).tolist()
        print(f"{word} 的one-hot编码是: {result}")
    
    # 保存训练好的Tokenizer模型到磁盘文件
    tokenizer_path = './onehot_tokenizer.joblib'
    joblib.dump(tokenizer, tokenizer_path)
    print(f"保存tokenizer模型成功,保存路径为: {tokenizer_path}")
    
    # 从磁盘加载保存的Tokenizer模型，并对新文本进行One-Hot编码
    tokenizer = joblib.load(tokenizer_path)
    result_ararry = tokenizer.texts_to_matrix(['王力宏'], mode='binary')[0, 1:]
    result_list = result_ararry.astype(int).tolist()
    print(f"'王力宏'的one-hot编码是: {result_list}")
    
if __name__ == '__main__':
    dm1()