"""
poll 方法实现IO多路复用
【1】 创建套接字
【2】 将套接字register
【3】 创建查找字典，并维护
【4】 循环监控IO发生
【5】 处理发生的IO
"""
from socket import *
from select import *
# 创建套接字作为关注IO
s = socket()
s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
s.bind(('0.0.0.0', 8888))
s.listen(5)
# 创建poll对象
p = poll()
# 建立查找字典，通过IO对象的fileno找到对象
# 字典内容与关注IO保持一致
fdmap = {s.fileno(): s}
# 关注s
p.register(s, POLLIN | POLLERR | POLLOUT)
print(fdmap)
# 循环监控IO的发生
while True:
    events = p.poll()
    print(events)
    for fd, event in events:
        if fd == s.fileno():
            c, addr = fdmap[fd].accept()
            print('connect from', addr)
            # 添加新的关注对象，同时维护字典
            p.register(c, POLLIN)
            # 维护字典
            fdmap[c.fileno()] = c
        elif event & POLLIN:
            data = fdmap[fd].recv(1024).decode()
            # 客户端退出
            if not data:
                # 取消关注
                p.unregister(fd)
                fdmap[fd].close()
                del fdmap[fd]
                continue
            print(data)
            p.register(fd, POLLOUT)
            # fdmap[fd].send("OK".encode())
        elif event & POLLOUT:
            fdmap[fd].send(b"OK")
            p.register(fd, POLLIN)





