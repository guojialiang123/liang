
from socket import *
import sys,os


def do_login(s,user,name,addr):
    if (name in user) or name == "管理员":
        s.sendto("该用户已存在".encode(),addr)
        return
    s.sendto(b'OK',addr)

    msg = '\n欢迎进入%s聊天室' % name
    for i in user:
        s.sendto(msg.encode(),user[i])
    user[name] = addr
def do_chat(s,user,name,text):

    msg = "\n%s 说 %s"%(name,text)
    for i in user:
        if i!=name:
            s.sendto(msg.encode(),user[i])

def do_quit(s,user,name):
    msg = '\n' + name + '退出了聊天室'
    for i in user:
        if i == name:
            s.sendto(b'EXIT',user[i])
        else:
            s.sendto(msg.encode(),user[i])
    del user[name]
def do_parent(s):
    user = {}
    while True:
        msg,addr = s.recvfrom(1024)
        msgList = msg.decode().split(' ')

        if msgList[0] == 'L':
            do_login(s,user,msgList[1],addr)
        elif msgList[0] == 'C':
            do_chat(s,user,msgList[1],' '.join(msgList[2:]))
        elif msgList[0] == 'Q':
            do_quit(s,user,msgList[1])

    s.recvfrom()
def do_child(s,addr):
    while True:
       msg = input("管理员消息:")
       msg = 'C 管理员 ' + msg
       s.sendto(msg.encode(),addr) 
    
def main():
    HOST = '127.0.0.1'
    PORT = 8888
    ADDR = (HOST,PORT)
    s = socket(AF_INET,SOCK_DGRAM)
    s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    s.bind(ADDR)
    pid = os.fork()
    if pid < 0:
        sys.exit("创建进程失败")
    elif pid == 0:
        do_child(s,ADDR)
    else:
        do_parent(s)




if __name__ == '__main__':
    main()