import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler


# 生成数据
def generate_data():
    iris = load_iris()
    x = iris.data
    y = iris.target
    print("特征数据形状:", iris)
    print("样本特征数据:\n", x)
    print("样本标签数据:\n", y)








if __name__ == '__main__':
    generate_data()





