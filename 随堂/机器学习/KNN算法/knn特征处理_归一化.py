from sklearn.preprocessing import MinMaxScaler

data = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

model = MinMaxScaler(feature_range=(0, 1))

model = model.fit_transform(data)
print(model)
