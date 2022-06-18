from iptcinfo3 import IPTCInfo

info = IPTCInfo(r'E:\temp\misaki-yamamoto-11.jpg', inp_charset='utf-8')


print(type(info))
print(info['caption/abstract'])

#info['caption/abstract'] = r'E:\temp\misaki-yamamoto-11.jpg'
#info.save()

print('contact:',info['contact'])
print('keywords:',info['keywords'])

#error
#for i,j in info:
    #print(i,'=',j)
    
for i in range(len(info)):
    print(range[i])