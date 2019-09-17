"""
协程行为展示
"""
from greenlet import greenlet
def fun1():
    print("执行fun1")
    gr2.switch()
    print("结束fun1")
    gr2.switch()
def fun2():
    print("执行fun2")
    gr1.switch()
    print("结束fun2")
    gr1.switch()
# 将函数变为协程函数
gr1 = greenlet(fun1)
gr2 = greenlet(fun2)
gr1.switch()
gr2.switch()






