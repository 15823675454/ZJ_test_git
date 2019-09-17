from socket import *
s = socket()
s.connect(('127.0.0.1', 8888))
while True:
    msg = input('msg:')
    s.send(msg.encode())
    data = s.recv(1024)
    print(data.decode())
