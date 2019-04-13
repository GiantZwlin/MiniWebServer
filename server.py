from socket import *
import threading


class Server:
    def __init__(self, ip, port):
        self.open = False
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.bind((ip, port))
        self.sock.listen(10)
        self.response_headers = "HTTP/1.1 200 OK\r\n"  # 200 表示找到这个资源
        self.response_headers += "\r\n"  # 空一行与body隔开

    @property
    def status(self):
        return self.open

    def tcp_link(self, sock, addr):
        print("Accept new connection from {}".format(addr))
        recv_data = sock.recv(1024).decode("utf-8")  # 1024表示本次接收的最大字节数
        # request_header_lines = recv_data.splitlines()
        # for line in request_header_lines:
        #     print(line)
        file_name = "./index.html"  # 设置读取的文件路径
        with open(file_name, "rb") as f:  # 以二进制读取文件内容
            response_body = f.read()

        sock.send(self.response_headers.encode("utf-8"))  # 转码utf-8并send数据到浏览器
        sock.send(response_body)  # 转码utf-8并send数据到浏览器
        sock.close()

        print("Connection from {} closed.".format(addr))

    def start(self):
        print("Server start!")
        self.open = True
        self.sock.settimeout(2)
        while self.open:
            try:
                sock, addr = self.sock.accept()
                thread = threading.Thread(target=self.tcp_link, args=(sock, addr))
                thread.start()
            except:
                continue
        print("Server close!")

    def close(self):
        self.open = False


if __name__ == '__main__':
    server = Server("10.23.97.98", 8080)
    server.start()
