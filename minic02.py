from enum import Enum
#import pdb
#重要参考下面链接：
#https://www.geeksforgeeks.org/expression-evaluation/
#因为python没有一个字符一个字符拼接的函数，我尝试用getch同时返回字符和索引
#但这样写了以后，发现操作起来非常繁琐；后来，发现有python的字符串有join方法
#可以用''.join([])拼接字符成为字符串，所以又改回了原来的getch
input_src = "(10+20) * 5-30*(3-2*(2-1))"    #输入字符串
caret = 0

#优先级 priority    precede
#分析   每次得到一个新的操作符都要和栈顶的操作符比较优先级
#如果 新的操作符优先级比栈顶的操作符高 就把这个新的操作符push堆栈中
dict_precede = {'+':2,'-':2,'*':3,'/':3,'(':0,')':0}
opr =['+','-','*','/','(',')']

def func_add(a,b):
    return a+b
def func_minus(a,b):
    return a-b
def func_mul(a,b):
    return a*b
def func_div(a,b):
    return a/b
#计算函数字典
dict_func = {'+':func_add,'-':func_minus,'*':func_mul,'/':func_div}

#enum   operator operand
class TokenTpye(Enum):
    tk_EOF = 0
    tk_digit = 1
    tk_id = 2
    tk_operator = 3
    tk_lb=4                     #left brackets
    tk_rb=5                     #right brackets

#存储token类型和值的类
class Token:
    def __init__(self,t,v):
        self.type = t
        self.value = v


#从原文件中读取一个字符
def getch():
    global input_src
    global caret

    if(caret < len(input_src)):
        c = input_src[caret]
        caret += 1
        return c
    else:
        return 0
#回退一个字符
def back():
    global caret
    caret -= 1
def isoperator(pch):
    if pch in opr:
        return True
    else:
        return False

#parameter
def getdigit(pch):
    rlt =[pch]
    while True:
        ch = getch()
        if ch == 0: #如果到达字符串缓冲区的末尾就退出循环
            break
        if ch.isdigit():
            rlt.append(ch)
        else:
            back()
            break
    #print("rlt->",''.join(rlt))
    return ''.join(rlt)
#返回
def gettoken():
    while True:
        ch= getch()
        if ch == 0: #如果到达字符串末尾就退出循环
            return Token(TokenTpye.tk_EOF,ch)
        elif ch=='(':
            return Token(TokenTpye.tk_lb,ch)
        elif ch==')':
            return Token(TokenTpye.tk_rb,ch)
        elif ch.isdigit():
            v = getdigit(ch)
            return Token(TokenTpye.tk_digit,int(v))
        elif isoperator(ch):
            return Token(TokenTpye.tk_operator,ch)

#表达式处理 expression
def do_expression():
    #btm = Token(TokenTpye.tk_EOF,0)
    st_operator = []    #存储操作符的栈
    st_operand = []     #存储操作数的栈
    
    while True:
        #pdb.set_trace()
        tk = gettoken()
        if tk.type == TokenTpye.tk_EOF:
            break
        elif tk.type == TokenTpye.tk_lb:
            st_operator.append(tk)
        elif tk.type == TokenTpye.tk_rb:
            while len(st_operator)>0 and st_operator[-1].value != '(':
                b = st_operand.pop()
                a = st_operand.pop()
                c = st_operator.pop()
                d = dict_func[c.value](a.value,b.value)
                st_operand.append(Token(TokenTpye.tk_digit,d))  #将计算结果存入栈中
            if len(st_operator)>0:
                st_operator.pop()       #消除左括号
        elif tk.type == TokenTpye.tk_digit:
            st_operand.append(tk)
        elif tk.type == TokenTpye.tk_operator:
            while len(st_operator)>0 and dict_precede[tk.value] <= dict_precede[st_operator[-1].value]:
                b = st_operand.pop()
                a = st_operand.pop()
                c = st_operator.pop()
                d = dict_func[c.value](a.value,b.value)
                st_operand.append(Token(TokenTpye.tk_digit,d))
                
            st_operator.append(tk)          #当前操作符入栈
            #print("precede:",p1,p2,"栈顶符号:",st_operator[-1].value," 新操作符：",tk.value)
    
    while len(st_operator)>0:
        b = st_operand.pop()
        a = st_operand.pop()
        c = st_operator.pop()
        d = dict_func[c.value](a.value,b.value)
        st_operand.append(Token(TokenTpye.tk_digit,d))    
    #print("operand:")
    # for x in st_operand:
    #    print(x.value,end=',')
    # print("\noperator:")
    # for y in st_operator:
    #     print(y.value,end=',')
    return st_operand[-1].value

print(input_src,end=' = ')
print(do_expression())