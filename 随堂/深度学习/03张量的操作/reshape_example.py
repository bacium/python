import numpy as np

# 创建一个示例数组
arr = np.array([[1, 2, 3],
                [4, 5, 6]])

print("原始数组:")
print(arr)
print("原始数组形状:", arr.shape)

# 使用 reshape(-1, 1)
reshaped_arr = arr.reshape(-1, 1)
print("\nreshape(-1, 1) 后的数组:")
print(reshaped_arr)
print("新数组形状:", reshaped_arr.shape)

# 对比 reshape(-1) 和 reshape(-1, 1)
flattened_arr = arr.reshape(-1)
print("\nreshape(-1) 后的数组 (展平为一维):")
print(flattened_arr)
print("展平后数组形状:", flattened_arr.shape)