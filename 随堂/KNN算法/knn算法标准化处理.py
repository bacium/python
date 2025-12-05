from sklearn.preprocessing import StandardScaler


data = [[1, 2, 5], [6, 5, 6], [7, 10, 9]]


transformer = StandardScaler()
target_data = transformer.fit_transform(data)

print(target_data)
"""
  [[-1.3970014  -1.1111678  -0.98058068]
  [ 0.50800051 -0.20203051 -0.39223227]
  [ 0.88900089  1.31319831  1.37281295]]
"""
