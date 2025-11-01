import socket

'''
@params:{socket.AF_INET}: Address Family 表示地址簇，Inet代表使用Ipv4地址进行连接
@params:{socket.SOCK_STREAM} SOCK_STREAM表示使用字节流的形式进行通信

'''
# 创建socket对象
service_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 设置运行的IP地址和端口号
service_socket.bind(('192.168.0.103', 9999))
# 设置最大连接数
service_socket.listen(5)
# 开启监听收取消息的对象
while True:
    try:
        client_socket, client_info = service_socket.accept()
        # 发送消息
        client_socket.send(b"welcome to socket!")
        # 接收收到的消息对象
        response_message = client_socket.recv(1024).decode("utf-8")
        print(f"收到客户端{client_info}的消息：{response_message}")
        # 关闭消息服务对象
        client_socket.close()
    except:
       pass
