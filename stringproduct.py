#生成字符串
import pyperclip

txt = open(r"E:\temp\stringtest.txt","at")

print("开始替换：")
strsrc = pyperclip.paste()
txt.write(strsrc.replace(".c",".o").replace("\r\n"," "))
strarr = strsrc.split()
for i in strarr:
    fulln = i.split('.')
    filen = fulln[0]
    ext = fulln[-1]
    #print(filen,'---',ext)
    # xxx.o:xxx.c
    #   gcc $(INCLUDE_DIR) -c xxx.c
    strrlt = "{0}.o:{1}.c\n\tgcc $(INCLUDE_DIR) -c {2}.c\n".format(filen,filen,filen)
    txt.write(strrlt)
txt.close()