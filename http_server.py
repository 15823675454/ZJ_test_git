"""
主要功能 ：
【1】 接收客户端（浏览器）请求
【2】 解析客户端发送的请求
【3】 根据请求组织数据内容
【4】 将数据内容形成http响应格式返回给浏览器

升级点 ：
【1】 采用IO并发，可以满足多个客户端同时发起请求情况
【2】 做基本的请求解析，根据具体请求返回具体内容，同时满足客户端简单的非网页请求情况
【3】 通过类接口形式进行功能封装
httpserver 2.0
env: python3.6
io多路复用 http练习
"""
from socket import *
from select import select
class HttpServer:
    def __init__(self, host='0.0.0.0', port=80, dir=None):
        self.host = host
        self.port = port
        self.dir = dir
        self.address = (host, port)
        self.creat_sock()
        self.bind()
        # select 监控列表
        self.rlist = []
        self.wlist = []
        self.xlist = []

    def server_forever(self):
        self.sockfd.listen(5)
        print('Listen the port %d' % self.port)
        # 设置关注的IO
        self.rlist.append(self.sockfd)
        while True:
            rs, ws, xs = select(self.rlist, self.wlist, self.wlist)
            for r in rs:
                if r is self.sockfd:
                    c, addr = r.accept()
                    self.rlist.append(c)
                else:
                    # 有客户端发请求
                    self.handle(r)
    # 创建套接字
    def creat_sock(self):
        self.sockfd = socket()
        self.sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    # 绑定地址
    def bind(self):
        self.sockfd.bind(self.address)

    # 处理客户端请求
    def handle(self, connfd):
        # 接受请求
        request = connfd.recv(4096)
        # 客户端断开处理
        if not request:
            self.rlist.remove(connfd)
            connfd.close()
            return
        # 提取请求内容
        request_line = request.splitlines()[0]
        info = request_line.decode().split()[1]
        print("info:", info)
        # 根据info情况分类
        if info == '/' or info[-5:] == '.html':
            self.get_html(connfd, info)
        else:
            self.get_data(connfd, info)

    def get_html(self, connfd, info):
        if info == '/':
            # 主页
            filename = self.dir + 'net2.html'
        else:
            filename = self.dir + info
        try:
            f = open(filename, 'rb')
        except Exception:
            # 没有网页
            response = """HTTP/1.1 404 Not Found
            Conten-Type:text/html
            
            
            <h1>Sorry...</h1>
            """

        else:
            # 有网页
            response = """HTTP/1.1 200 OK
            Conten-Type:text/html
            
            %s""" % f.read()
        finally:
            connfd.send(response.encode())
    def get_data(self, connfd, info):
        f = open(self.dir+'re1.png', 'rb')
        response = "HTTP/1.1 200 OK\r\n"
        response += "Content-Type:image/jpeg\r\n"
        response += "\r\n"
        response = response.encode() + f.read()
        connfd.send(response)


if __name__ == '__main__':
    HOST = '0.0.0.0'
    PORT = 8000
    DIR = './static/'
    http = HttpServer(HOST, PORT, DIR) # 实例化对象
    http.server_forever()


