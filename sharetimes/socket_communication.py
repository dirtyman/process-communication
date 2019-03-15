# encoding: utf-8
#以太网套接字进程通信

# coding: utf-8

import os
import sys
import math
import socket


def slice(mink, maxk):
    s = 0.0
    for k in range(mink, maxk):
        s += 1.0/(2*k+1)/(2*k+1)
    return s


def pi(n):
    childs = []
    unit = n // 10
    servsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 注意这里的AF_INET表示普通套接字
    servsock.bind(("localhost", 0))  # 0表示随机端口
    server_address = servsock.getsockname()  # 拿到随机出来的地址，给后面的子进程使用
    servsock.listen(10)  # 监听子进程连接请求
    for i in range(10):  # 分10个子进程
        mink = unit * i
        maxk = mink + unit
        pid = os.fork()
        if pid > 0:
            childs.append(pid)
        else:
            servsock.close()  # 子进程要关闭servsock引用
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(server_address)  # 连接父进程套接字
            s = slice(mink, maxk)  # 子进程开始计算
            sock.sendall(str(s))
            sock.close()  # 关闭连接
            sys.exit(0)  # 子进程结束
    sums = []
    for pid in childs:
        conn, _ = servsock.accept()  # 接收子进程连接
        sums.append(float(conn.recv(1024)))
        conn.close()  # 关闭连接
    for pid in childs:
        os.waitpid(pid, 0)  # 等待子进程结束
    servsock.close()  # 关闭套接字
    return math.sqrt(sum(sums) * 8)


if __name__ == "__main__":
    print(pi(10000000))

