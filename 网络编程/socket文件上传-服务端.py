import socket

service_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
service_socket.bind(("localhost", 10000))
service_socket.listen(5)
client_socket, client_address = service_socket.accept()
with open("data/test.txt", "wb") as def_file:
    while True:
        res_file_content = client_socket.recv(8092)
        if len(res_file_content) == 0:
            break
        def_file.write(res_file_content)
print("上传完成！")
client_socket.close()
