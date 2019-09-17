"""
select tcp 服务
【1】 将关注的IO放入对应的监控类别列表
【2】通过select函数进行监控
【3】遍历select返回值列表，确定就绪IO事件
【4】处理发生的IO事件
"""
from socket import *
from select import select
# 创建监听套接字作为关注IO
s = socket()
s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
s.bind(('0.0.0.0', 8888))
s.listen(5)
# 设置关注列表
rlist = [s] # 等待客户端连接
wlist = []
xlist = []
while True:
    # 监控IO发生
    rs, ws, xs = select(rlist, wlist, xlist)
    for r in rs:
        if r is s:
            c, addr = r.accept()
            print('connect from', addr)
            rlist.append(c)
        else:
            data = r.recv(1024)
            if not data:
                rlist.remove(r) # 取消对他关注
                r.close()
                continue
            print(data)
            wlist.append(r)
    for w in ws:
        w.send(b"OK")
        wlist.remove(w) # 从写监控中移除



