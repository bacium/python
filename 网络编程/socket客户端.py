import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('192.168.0.103', 9999))
response = client_socket.recv(1024).decode('utf-8')
print(response)
client_socket.send("来，中路对线".encode('utf-8'))
client_socket.send("顶顶顶".encode('utf-8'))
client_socket.close()
