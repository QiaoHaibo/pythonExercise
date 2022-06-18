#coding=utf-8
__author__ = 'zengqingming'

import urllib
import os
import sys

#default_encoding = 'utf-8'
#if sys.getdefaultencoding() != default_encoding:
#    reload(sys)
#    sys.setdefaultencoding(default_encoding)
#关键在206和416的状态处理
class myURLOpener(urllib.FancyURLopener):
    def http_error_206(self, url, fp, errcode, errmsg, headers, data=None):
        pass
#试验下载链接
#1  http://distro.ibiblio.org/puppylinux/puppy-fossa/fossapup64-9.5.iso
#2  http://ftp.nluug.nl/ftp/pub/os/Linux/distr/puppylinux/puppy-fossa/fossapup64-9.5.iso

def downloadFile():
    loop = 1
    dlFile = r"fossapup64-9.5.iso"
    existSize = 0
    myUrlclass = myURLOpener()
    if os.path.exists(dlFile):
        outputFile = open(dlFile,"ab")
        existSize = os.path.getsize(dlFile)
        #If the file exists, then only download the remainder
        myUrlclass.addheader("Range","bytes=%s-" % (existSize))
    else:
        outputFile = open(dlFile,"wb")

    url = "http://distro.ibiblio.org/puppylinux/puppy-fossa/%s" % dlFile
    print(url)
    webPage = myUrlclass.open(url)
    responsedCode = webPage.getcode()
    if responsedCode == 416:
        loop = 0
        print("Requested Range not satisfiable")

    contentLength = webPage.headers['Content-Length']
    print("contentLength:%s - existSize:%d " % (contentLength, existSize))
    #If the file exists, but we already have the whole thing, don't download again
    if int(contentLength) == existSize:
        loop = 0
        print("File already downloaded")

    numBytes = 0
    while loop:
        data = webPage.read(8192)
        if not data:
            break
        outputFile.write(data)
        numBytes = numBytes + len(data)
        #print "data:%s" % data
        print("read " , len(data) , " bytes")

    webPage.close()
    outputFile.close()

    for k,v in webPage.headers.items():
        print(k, "=",v)
    print("code:", webPage.getcode())
    print("copied", numBytes, "bytes from", webPage.url)


if __name__ == "__main__":
    downloadFile()
#————————————————
#版权声明：本文为CSDN博主「michaelzqm2」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
#原文链接：https://blog.csdn.net/michaelzqm2/article/details/84513290