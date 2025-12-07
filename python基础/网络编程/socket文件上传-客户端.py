import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 10000)
client_socket.connect(server_address)

with open('data/uploadFile.txt', "rb") as read_stream:
    while True:
        bys = read_stream.read(8192)
        client_socket.send(bys)
        if len(bys) == 0:
            break

print("发送完成！")
client_socket.close()
