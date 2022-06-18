#实验python的字典

def sing():
    print("唱支山歌给党听")

dt ={
    'name':'jay',
    'age':10,
    'hobby':sing,
    'heigin':171,
    'weight':65
    }

try:
    print(dt['name'])
    dt['hobby']()
except KeyError as e:
    print("没有找到键值！%s " % e)
