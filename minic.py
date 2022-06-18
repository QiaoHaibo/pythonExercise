from enum import Enum
import pdb
#添加流程控制语句 if else while for
#想要控制流程，必须实现一个“codetable”的数组，或者叫“inctable”(instruction)，数组的每一项是：
#1  参数 2 个
#2  要执行的指令或函数地址
#3  返回值
#现在想到的问题 表达式翻译成两个参数的指令集 该怎么传递参数，让指令连续的执行，比如“add p1 p2”
#暂时的解决方案 约定两个寄存器  常量和变量怎么区分 原来的执行函数返回值都得改？
input_src = '''
    int a =3*(5-3);
    int b =10/2;
    int c = a +b*2;
    int d = a>=b && a > c ;
'''
caret = 0

#优先级 priority    precede
#分析   每次得到一个新的操作符都要和栈顶的操作符比较优先级
#如果 新的操作符优先级比栈顶的操作符高 就把这个新的操作符push堆栈中
dict_precede = {'+':12,'-':12,'*':13,'/':13,'%':13,'>':10,'<':10,'>=':10,'<=':10,'==':9,'!=':9,'&&':5,'||':4,'=':2,'(':0,')':0}
opr =['+','-','*','/','%','(',')','=','>','<']

#enum   operator operand
class TokenType(Enum):
    tk_EOF = 0
    tk_digit = 1
    tk_id = 2
    tk_operator = 3
    tk_lb=4                     #left brackets
    tk_rb=5                     #right brackets
    tk_if=6                     #条件分支控制关键字
    tk_else=7
    tk_for=8
    tk_while=9
    tk_break=10
    tk_continue=11
    tk_int = 12                 #定义变量的关键字
    tk_var_int = 13
    tk_semicolon =14            #英语中分号(Semicolon,“;”)
    tk_error = 20

#加法的实现
def func_add(a,b):
    if a.type == TokenType.tk_var_int: #如是变量要先取得对应内存再计算
        c = dict_vardata[a.value]
    else:
        c = a.value
    if b.type == TokenType.tk_var_int:
        d = dict_vardata[b.value]
    else:
        d = b.value
    return c+d
#减法实现
def func_minus(a,b):
    if a.type == TokenType.tk_var_int: #如是变量要先取得对应内存再计算
        c = dict_vardata[a.value]
    else:
        c = a.value
    if b.type == TokenType.tk_var_int:
        d = dict_vardata[b.value]
    else:
        d = b.value
    return c-d
#乘法实现
def func_mul(a,b):
    if a.type == TokenType.tk_var_int: #如是变量要先取得对应内存再计算
        c = dict_vardata[a.value]
    else:
        c = a.value
    if b.type == TokenType.tk_var_int:
        d = dict_vardata[b.value]
    else:
        d = b.value
    return c*d
#除法实现
def func_div(a,b):
    if a.type == TokenType.tk_var_int: #如是变量要先取得对应内存再计算
        c = dict_vardata[a.value]
    else:
        c = a.value
    if b.type == TokenType.tk_var_int:
        d = dict_vardata[b.value]
    else:
        d = b.value
    return c//d
def func_mod(a,b):      #取余运算
    if a.type == TokenType.tk_var_int: #如是变量要先取得对应内存再计算
        c = dict_vardata[a.value]
    else:
        c = a.value
    if b.type == TokenType.tk_var_int:
        d = dict_vardata[b.value]
    else:
        d = b.value
    return c % d
def func_as(a,b):      #赋值运算
    #pdb.set_trace()
    if b.type == TokenType.tk_var_int:
        d = dict_vardata[b.value]
    else:
        d = b.value

    if a.type == TokenType.tk_var_int: #如是变量要先取得对应内存再计算
        dict_vardata[a.value] = d
        return d
    else:                               #被赋值的不是变量，此处应该发出异常
        print("语法错误：被赋值的对象不是变量，无效的操作")
#关系运算符和逻辑运算符
#   "<"
def func_less(a,b):
    if a.type == TokenType.tk_var_int: #如是变量要先取得对应内存再计算
        c = dict_vardata[a.value]
    else:
        c = a.value
    if b.type == TokenType.tk_var_int:
        d = dict_vardata[b.value]
    else:
        d = b.value
    return c < d
#   ">"
def func_great(a,b):
    if a.type == TokenType.tk_var_int: #如是变量要先取得对应内存再计算
        c = dict_vardata[a.value]
    else:
        c = a.value
    if b.type == TokenType.tk_var_int:
        d = dict_vardata[b.value]
    else:
        d = b.value
    return c > d
#   "<="
def func_LEQ(a,b):
    if a.type == TokenType.tk_var_int: #如是变量要先取得对应内存再计算
        c = dict_vardata[a.value]
    else:
        c = a.value
    if b.type == TokenType.tk_var_int:
        d = dict_vardata[b.value]
    else:
        d = b.value
    return c <= d
#   ">="
def func_GEQ(a,b):
    if a.type == TokenType.tk_var_int: #如是变量要先取得对应内存再计算
        c = dict_vardata[a.value]
    else:
        c = a.value
    if b.type == TokenType.tk_var_int:
        d = dict_vardata[b.value]
    else:
        d = b.value
    return c >= d
#   "=="
def func_equal(a,b):
    if a.type == TokenType.tk_var_int: #如是变量要先取得对应内存再计算
        c = dict_vardata[a.value]
    else:
        c = a.value
    if b.type == TokenType.tk_var_int:
        d = dict_vardata[b.value]
    else:
        d = b.value
    return c == d
#   "!="
def func_notequal(a,b):
    if a.type == TokenType.tk_var_int: #如是变量要先取得对应内存再计算
        c = dict_vardata[a.value]
    else:
        c = a.value
    if b.type == TokenType.tk_var_int:
        d = dict_vardata[b.value]
    else:
        d = b.value
    return c != d
#   "&&"
def func_and(a,b):
    if a.type == TokenType.tk_var_int: #如是变量要先取得对应内存再计算
        c = dict_vardata[a.value]
    else:
        c = a.value
    if b.type == TokenType.tk_var_int:
        d = dict_vardata[b.value]
    else:
        d = b.value
    return c and d
#   "||"
def func_or(a,b):
    if a.type == TokenType.tk_var_int: #如是变量要先取得对应内存再计算
        c = dict_vardata[a.value]
    else:
        c = a.value
    if b.type == TokenType.tk_var_int:
        d = dict_vardata[b.value]
    else:
        d = b.value
    return c or d
#运算执行功能字典
dict_func = {'+':func_add,'-':func_minus,'*':func_mul,'%':func_mod,'/':func_div,'=':func_as,'>':func_great,'<':func_less,'>=':func_GEQ,'<=':func_LEQ,'==':func_equal,'!=':func_notequal,'&&':func_and,'||':func_or}
#关键字字典
dict_keyword = {'if':TokenType.tk_if,'for':TokenType.tk_for,'while':TokenType.tk_while,'else':TokenType.tk_else,'break':TokenType.tk_break,'continue':TokenType.tk_continue,'int':TokenType.tk_int}
#存储token类型和值的类
class Token:
    def __init__(self,t,v):
        self.type = t
        self.value = v

#Token缓冲区，句子用户发现Token不是自己的退货到此处
token_buf = []

#程序存储数据的区域vardata
dict_vardata ={}

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
def backch():
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
            backch()
            break
    #print("rlt->",''.join(rlt))
    return ''.join(rlt)
    
def getid(pch):
    rlt = [pch]
    while True:
        ch = getch()
        if ch == 0:
            break
        if ch.isalpha() or ch.isdigit() or ch == '_':
            rlt.append(ch)
        else:
            backch()
            break
    return ''.join(rlt)
#返回
def gettoken():
    #如果暂存区有token就要先用光暂存区的token
    if len(token_buf) > 0:
        return token_buf.pop()
    
    while True:
        ch= getch()
        if ch == 0: #如果到达字符串末尾就退出循环
            return Token(TokenType.tk_EOF,ch)
        elif ch==';':
            return Token(TokenType.tk_semicolon,ch)
        elif ch=='(':
            return Token(TokenType.tk_lb,ch)
        elif ch==')':
            return Token(TokenType.tk_rb,ch)
        elif ch.isidentifier():
            n = getid(ch)
            #查询标识符是否是变量
            try:
                v = dict_keyword[n]     #查询标识符是否是'关键字'
                return Token(v,n)
            except KeyError:
                try:
                    v = dict_vardata[n] #查询标识符是否是一个变量
                    return Token(TokenType.tk_var_int,n)
                except KeyError:
                    return Token(TokenType.tk_id,n)
        elif ch.isdigit():
            v = getdigit(ch)
            return Token(TokenType.tk_digit,int(v))
        elif ch in ['>','<','!','=','&','|']:
            #pdb.set_trace()
            ch1 = getch()
            cc = ch +ch1
            if cc in ['>=','<=','==','!=','&&','||']:
                return Token(TokenType.tk_operator,cc)
            else:
                backch()
        if isoperator(ch):
            return Token(TokenType.tk_operator,ch)

def backtoken(t):
    global token_buf
    token_buf.append(t)

#表达式处理 expression
def do_expression():
    #btm = Token(TokenType.tk_EOF,0)
    st_operator = []    #存储操作符的栈
    st_operand = []     #存储操作数的栈
    
    while True:
        tk = gettoken()
        #pdb.set_trace()
        if tk.type == TokenType.tk_EOF:
            break
        elif tk.type == TokenType.tk_semicolon:
            break
        elif tk.type == TokenType.tk_lb:
            st_operator.append(tk)
        elif tk.type == TokenType.tk_rb:
            while len(st_operator)>0 and st_operator[-1].value != '(':
                b = st_operand.pop()
                a = st_operand.pop()
                c = st_operator.pop()
                d = dict_func[c.value](a,b)
                st_operand.append(Token(TokenType.tk_digit,d))  #将计算结果存入栈中
            if len(st_operator)>0:
                st_operator.pop()       #消除左括号
        elif tk.type == TokenType.tk_digit:
            st_operand.append(tk)
        elif tk.type == TokenType.tk_var_int:
            st_operand.append(tk)
        elif tk.type == TokenType.tk_operator:
            while len(st_operator)>0 and dict_precede[tk.value] <= dict_precede[st_operator[-1].value]:
                b = st_operand.pop()
                a = st_operand.pop()
                c = st_operator.pop()
                d = dict_func[c.value](a,b)
                st_operand.append(Token(TokenType.tk_digit,d))
                
            st_operator.append(tk)          #当前操作符入栈
            #print("precede:",p1,p2,"栈顶符号:",st_operator[-1].value," 新操作符：",tk.value)

    while len(st_operator)>0:
        #pdb.set_trace()
        b = st_operand.pop()
        a = st_operand.pop()
        c = st_operator.pop()
        d = dict_func[c.value](a,b)
        st_operand.append(Token(TokenType.tk_digit,d))    
    #print("operand:")
    # for x in st_operand:
    #    print(x.value,end=',')
    # print("\noperator:")
    # for y in st_operator:
    #     print(y.value,end=',')
    return st_operand[-1].value


#变量定义statement_vardef
def stm_vardef():
    tk1 = gettoken()
    #pdb.set_trace()
    if tk1.type != TokenType.tk_int:
        backtoken(tk1)
        return False
    tk2 = gettoken()
    if tk2.type != TokenType.tk_id:
        backtoken(tk2)
        backtoken(tk1)
        return False
    tk3 = gettoken()
    if  tk3.value !='=': #语法错误
        return False
    #开一块内存给ID
    dict_vardata[tk2.value] = 0     #暂时让它等于0，真实环境中应该是未初始化的值
    tk2.type =TokenType.tk_var_int
    backtoken(tk3)                  #把‘=’和‘ID’再放回去
    backtoken(tk2)
    #调用表达式模块
    do_expression()
#pdb.set_trace()


stm_vardef()  
stm_vardef()  
stm_vardef()  
stm_vardef()  
print(dict_vardata)
#print(input_src,end=' = ')
#print(do_expression())