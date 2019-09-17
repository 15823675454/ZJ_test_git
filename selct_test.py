"""
select 演示
"""
from socket import *
from select import select
s = socket()
s.bind(('0.0.0.0', 8888))
s.listen(5)
print("监控io")
rs, ws, xs = select([s], [], [], 3)
print('rlist:', rs)
print('wlist:', ws)
print('xlist', xs)


