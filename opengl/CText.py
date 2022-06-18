import freetype
import numpy
from PIL import Image

class CText:
    image = None
    text = None
    def __init__(self,text = None,fontheight=18,fontpath=r'e:\font\AlibabaPuHuiTiAll\Alibaba-PuHuiTi-Bold.ttf'):#r"e:\font\SiYuanSongTiRegular\SourceHanSerifCN-Regular-1.otf"):
        self.text = text
        self.height = fontheight
        self.path = fontpath
        self.face = freetype.Face(fontpath)
        self.face.set_char_size(self.height * 64)
        if text:
            self.make(text)
    class CFontinfo:
        ch = ''
        width = 0
        height = 0
        left = 0
        top = 0
        advance = 0
        image = None
    def make(self,text):
        charr = []
        sumwidth = 0
        maxtop,maxbottom = 0,0
        if not self.face:
            return False
        for i,ch in enumerate(text):
            t = self.CFontinfo()
            self.face.load_char(ch)
            t.ch = ch
            t.width = self.face.glyph.bitmap.width
            t.height = self.face.glyph.bitmap.rows
            t.left = self.face.glyph.bitmap_left
            t.top = self.face.glyph.bitmap_top
            t.advance = self.face.glyph.advance.x // 64

            #选出最大的baseline线上部分
            maxtop = max(maxtop,t.top)
            #选出最大的baseline线下部分
            maxbottom = max(maxbottom,t.height-t.top)
            #生成并缓存图片
            tbm = numpy.array(self.face.glyph.bitmap.buffer) #临时数组
            tbm = tbm.reshape((self.face.glyph.bitmap.rows,self.face.glyph.bitmap.width))   #将数组从1维调整成X行X列

            if len(tbm) == 0:
                t.image = Image.new('L',(self.face.glyph.advance.x// 64,self.face.glyph.advance.x// 64))
            else:
                t.image = Image.fromarray(tbm)
            charr.append(t)            #连字的信息和图片存入临时数组中
            sumwidth += t.advance         #累加当前字宽

        sumheight = maxtop+maxbottom
        #根据得到的数据生成正好能装下字符串的图片
        self.image = Image.new('L',(sumwidth,sumheight))
        baseline = maxtop
        left = 0
        for t in charr:
            self.image.paste(t.image,(left+t.left,
                                        baseline - t.top,
                                        left+t.left+t.image.width,
                                        baseline - t.top+t.image.height))
            left += t.advance                      #累加宽度 
        freetype.FT_Done_Face()
        return True


#用固定宽度的size显示，汉字还好，英语惨不忍睹，间隙过大。
# 而且像“g”这种靠下的字母，非常别扭。
#使用for循环显示字，看完从网上下的例子后，看来要写2个循环，
#第一个，确定目标框的大小
#第二个，把图画上去
#现在还没有实现字符串出现空格会引起错误
if __name__ == '__main__':
    srcstr1 = "盼望着，盼望着，东风来了，春天的脚步近了。一切都像刚睡醒的样子，欣欣然张开了眼。"
    srcstr2 = "hello world.let's go!测试英汉混排，并测试空格的表现。所谓伊人，在水一方。"

    fi1 = CText(srcstr1,17,r'c:\Windows\Fonts\simsun.ttc')
    fi2 = CText(srcstr2)

    width = max(fi1.image.width , fi2.image.width)
    height = fi1.image.height + fi2.image.height
    img = Image.new('L',(width,height))

    left  = 0
    top   =0
    img.paste(fi1.image,(left,top,left+fi1.image.width,fi1.image.height))

    img.paste(fi2.image,(left,fi1.image.height,left+fi2.image.width,fi1.image.height+fi2.image.height))

    if img:
        img.show()


#img = target_img.crop((0,0,lw,pich))
#img.show()
#target_img.show()
