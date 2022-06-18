from typing import Any
import numpy

#spares voxel octree
#  ▇     ▇     ▇     ▇
# bkid  child  vilder  leaf
# 16b    16b     8b     8b
# 新变化，原来的node数据结构设计适用于加载多边形模型变换成svo，所以一个block大概只有一个far pointer(远程指针)
#一旦生成模型之后，不会轻易发生变化，可以视作是静态的树结构。而我要在程序中使用的是一个建模程序。
# 已经固定的节点，后面也有可能进行修改。所以上面的结构就不能适应现在的用途了。必须创造一个新的数据结构。
# 不使用far标记，而使用1个或者2个字节容纳block index。
#8个子节点:    0       1       2       3       4       5       6       7 
#二进制  :    000     001     010     011     100     101     110     111
#用二进制的个位十位百位分别代表x轴y轴z轴
# x = value >> 0 & 1 
# y = value >> 1 & 1 
# z = value >> 2 & 1 
#  move :    (0,1) + -0.5 = (-0.5,0.5)
# scale :    (0,1) * 100  = (0   ,100)

class node:
    '''将表示节点的数字解压和压缩'''
    def __init__(self,val:numpy.uint64):
        self.val = val
    #设置vild 目标为'1'
    def setVild1(self,n):
        self.vild = n
    #设置vild目标为'0'
    def setVild0(self,n):
        dst = self.val >> 24 & 0xff
        src = 0xff ^ 1<< n
        self.__dict__['vild'] = dst & src
        self.__dict__['val'] = self.bkid << 48 | self.fchd << 32 | self.vild << 24 | self.leaf << 16
    #将第n个子节点的标志位置‘1’
    def setLeaf1(self,n):
        self.leaf = n
    #将第n个子节点的标志位置‘0’
    def setLeaf0(self,n):
        dst = self.val >> 16 & 0xff
        src = 0xff ^ 1 << n
        self.__dict__['leaf'] = dst & src
        self.__dict__['val'] = self.bkid << 48 | self.fchd << 32 | self.vild << 24 | self.leaf << 16

    def __setattr__(self, __name: str, __value: Any) -> None:
        
        if __name == 'val':
            self.__dict__['bkid'] = __value >> 48               #block index
            self.__dict__['fchd'] = __value >> 32 & 0xffff      #first child address  16bit+32bit 并去掉最高位
            self.__dict__['vild'] = __value >> 24 & 0xff        #子节点指示器 'valid mask' slot
            self.__dict__['leaf'] = __value >> 16 & 0xff        #叶节点指示器 'leaf mask' slot

            self.__dict__[__name] = __value
        elif __name == 'bkid':
            self.__dict__[__name] = __value
        elif __name == 'fchd':
            self.__dict__[__name] = __value
        elif __name == 'vild':
            #只能设置目标为'1'，从路径中得到的是第几个节点的序号，设置标志位，需要位移一下
            vid = self.val >> 24 & 0xff
            vid = vid | 1<< __value
            self.__dict__[__name] = vid
        elif __name == 'leaf':
            lef = self.val >> 16 & 0xff
            lef = lef | 1 << __value
            self.__dict__[__name] = lef
        
        self.__dict__['val'] = self.bkid << 48 | self.fchd << 32 | self.vild << 24 | self.leaf << 16

class space:
    index = 0       #当前block的索引
    length = 0      #闲置空间长度
    bid = 0         #block id
    def __init__(self,bid,index,length):
        self.index = index
        self.length = length
        self.bid = bid
#稀疏八叉树的类
class SVO:
    buffers = []    #用来存储大量block内存

    avaSpace = []   #Available space
    
    def __init__(self) -> None:
        pass

    def newBlock(self):
        '''生成一个新的空的块内存'''
        block = numpy.zeros(0x7fff,numpy.uint64)
        self.buffers.append(block)      #将新创建的node加入到的缓存列表中
        return 0x7fff
    def createRoot(self):
        #返回根节点的ID
        if len(self.buffers) >0:
            block = self.buffers[0]
            N = node(block[0])
        else:
            #第一次创建，更新空间管理
            idx,bid = self.allocate(1)
        


    def newNode(self,path:numpy.ndarray):
        '''增加一个新的节点，如果在一个闲置的位置更新点的位置，将必须有一种方法把这个位置描述出来。
        只需要3位就可以确定1级8个子节点的位置。一个4字节变量，可以描述10级的深度。
        path是uint32的数组
        得保存深度值，暂规定第1个值是深度值
        '''
        deep = path[0]              #得到数组装载的
        dep = 0                     #深度值从path的索引1开始存储
        ci = 0                      #current index
        cb = 0                      #当前块
        block = self.buffers[cb]     #得到root所在block

        while dep < deep-1:
            #每个uint32数，装了10级深度，怎么跳转到下一个uint32，用deep // 10 ?
            #如果deep不够10级，如何正确处理
            pci =(path[dep // 10 +1] >> 3*(dep % 10)) & 7     #子节点索引 child_idx 从树根开始索引 root
            #根据child index 查找子节点
            N = node(self.buffers[cb][ci])
            
            #等于0的情况是没有子节点（没有创建）
            if N.fchd == 0:
                #创建整整一级8个子节点:,创建时候需要检测一下空间够不够
                N.fchd,N.bkid = self.allocate(8)
                N.vild = pci
                self.buffers[cb][ci] = N.val

            ci = N.fchd + pci
            cb = N.bkid
            dep += 1 
        #当前点是叶节点，设置标志
        N = node(self.buffers[cb][ci])
        pci =(path[dep // 10 +1] >> 3*(dep % 10)) & 7     #子节点索引 child_idx 从树根开始索引 root
        N.leaf = pci
        N.vild = pci

        if N.fchd == 0:
            #创建整整一级8个子节点:,创建时候需要检测一下空间够不够
            N.fchd,N.bkid = self.allocate(8)
            self.buffers[cb][ci] = N.val



    def delNode(self,path):
        '''删除节点，将此节点置0，并且要将它的所有子节点释放。
        只需要3位就可以确定1级8个子节点的位置。一个4字节变量，可以描述10级的深度。
        path是uint32的数组
        得保存深度值，暂规定第1个值是深度值
        '''
        deep = path[0]              #得到数组装载的
        dep = 0                     #深度值从path的索引1开始存储
        block = self.buffers[0]     #得到root所在block
        ci = 0                      #current index
        cb = 0                      #当前块
        while dep < deep:
            #每个uint32数，装了10级深度，怎么跳转到下一个uint32，用deep // 10 ?
            #如果deep不够10级，如何正确处理
            pci =(path[dep // 10 +1] >> 3*(dep % 10)) & 7     #子节点索引 child_idx 从树根开始索引 root
            #根据child index 查找子节点
            N = node(self.buffers[cb][ci])
            ci = N.fchd + pci
            cb = N.bkid
        
        #这里已经找到目标节点，现在应该修改标志位信息并递归释放所有子节点。
        stack = [(cb,ci)]  #堆栈

        while len(stack) > 0:
            cb,ci = stack.pop()
            #检查子区标志
            N = node(self.buffers[cb][ci])
            if N.vild > 0:   #至少存在一个子节点
                
                for i in range(8):
                    #如果当前节点有1个子节点，并且自己不是叶节点
                    if N.vild & 1 << i and (N.leaf & 1<< i) == 0:
                        stack.append((N.bkid,N.fchd + i))
                self.recycle(N.bkid,N.fchd,8)
            #
            self.buffers[cb][ci] = 0



    #需要闲置空间管理，以下函数用于检测当前的block内存块中有没有足够的闲置空间，容纳操作
    #最小单元64bit的uint64，返回index索引，返回是否有申请到空间，返回的索引是否在当前block中
    #用list管理闲置空间 
    def allocate(self,length):
        for i,sp in enumerate(self.avaSpace):
            #如果请求的空间小于空闲的空间，就使用这个空间
            if sp.length >= length:
                index = sp.index                    #保存索引值
                sp.index = sp.index + length        #更新信息
                sp.length = sp.length - length
                return index,sp.bid
            else:
                continue
        #走到这里，应该是没有符合的空置空间
        l = self.newBlock()         #返回值是block的size
        bid = len(self.buffers)-1   #block在buffers里的索引
        #加入空间管理
        sp = space(bid,length,l - length)
        self.avaSpace.append(sp)
        return 0,bid

    #释放index表示的空间为闲置空间，使其可以再次利用
    #按bid大小排序
    #零散空间合并
    def recycle(self,bid,index,length):
        
        self.avaSpace.append(space(bid,index,length))

        # if len(self.avaSpace) > 0:
        #     for n in self.avaSpace:
        #         if n.bid == bid:
        #             pass
        #         elif n.bid > bid:
        #             pass

        # else:
        #     self.avaSpace.append(space(bid,index,length))
        # pass
    #节点显示列表
    def displayLists(self):
        pass    

if __name__ == '__main__':
    far = 1
    chi = 99
    vid = 3
    lef = 3

    a = far <<63 | chi << 48 | vid << 40 | lef << 32
    b = node(a)
    print('b far:',b.bkid)
    print('b chi:',b.fchd)
    print('b vid:',b.vild)
    print('b lef:',b.leaf)
    b.bkid = 0
    print('将far设置为0，b.bkid:',b.bkid)
    print('将far设置为，结果：',bin(b.val))