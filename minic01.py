from enum import Enum
#因为python没有一个字符一个字符拼接的函数，我尝试用getch同时返回字符和索引
#但这样写了以后，发现操作起来非常繁琐；后来，发现有python的字符串有join方法
#可以用''.join([])拼接字符成为字符串，所以又改回了原来的getch
input_src = "12"    #输入字符串
caret = 0

#enum   Operator operand
class Token(Enum):
    tk_digit = 1
    tk_id = 2
    tk_operator = 3
#提取由a b作为区间的字符串
def getstr(a,b):
    global input_src
    return input_src[a:b]

#从原文件中读取一个字符
def getch():
    global input_src
    global caret
    print('getch:',caret)
    if(caret < len(input_src)):
        c = input_src[caret]
        caret += 1
        return c,caret-1
    else:
        return 0,caret-1
#parameter
def getdigit(pch,pi):
    end = pi
    print("getdigit:",pi)
    while True:
        ch,end = getch()
        print("ch end:",ch,",",end)
        if ch == 0: #如果到达字符串缓冲区的末尾就退出循环
            break
        if not ch.isdigit():
            break
    s = getstr(pi,end)
    print("getstr(",pi,",",end,"):",s)
#返回
def gettoken():
    while True:
        ch,i = getch()
        if ch == 0: #如果到达字符串末尾就退出循环
            break
        if ch.isdigit():
            getdigit(ch,i)

gettoken()
