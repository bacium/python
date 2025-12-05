import socket

"""
@params:{socket.AF_INET}: Address Family 表示地址簇，Inet代表使用Ipv4地址进行连接
@params:{socket.SOCK_STREAM} SOCK_STREAM表示使用字节流的形式进行通信
"""
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


print(client_socket)
client_socket.close()
