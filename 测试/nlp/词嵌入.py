import torch

data = torch.tensor(data=[[1, 2, 3, 4, 5], [4, 10, 8, 5, 6]])

embedding = torch.nn.Embedding(num_embeddings=500, embedding_dim=100)

embedd = embedding(data)
print(embedd)
