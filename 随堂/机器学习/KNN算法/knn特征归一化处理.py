from sklearn.preprocessing import MinMaxScaler


# 特征数据
data = [[1, 2, 5], [6, 5, 6], [7, 10, 9]]


transformer = MinMaxScaler()

target_data = transformer.fit_transform(data)


print(target_data)

"""
  [[0.         0.         0.        ]
  [0.83333333 0.375      0.25      ]
  [1.         1.         1.        ]]
"""
