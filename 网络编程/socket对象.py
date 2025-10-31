import socket

'''
@params:{socket.AF_INET}: Address Family 表示地址簇，Inet代表使用Ipv4地址进行连接
@params:{socket.SOCK_STREAM} SOCK_STREAM表示使用字节流的形式进行通信

'''
ws = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# ws.bind(host="127.0.0.1:12344")
print(ws)
ws.close()