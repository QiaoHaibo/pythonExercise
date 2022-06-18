from OpenGL.GL import *
import glfw
from numpy import double

class CWindow:
    
    def __init__(self,width:int,height:int,title:str):
        if not glfw.init():
            raise Exception('glfw can not be initilized!')
        #创建窗口
        self._w,self._h = width,height
        self.ASPECT = self._w/self._h
        self._win = glfw.create_window(width,height,title,None,None)
        
        if not self._win:
            glfw.terminate()
            raise Exception('glfw window can not be created!')
        #设置窗口位置 并 创建OpenGL上下文
        self.center()
        glfw.make_context_current(self._win)
        glfw.set_cursor_pos_callback(self._win,self.mouse_move)
    def mouse_move(self,window,x:double,y:double):
        #print('x:',x,' y:',y)
        pass
    def center(self):
        m1 = glfw.get_primary_monitor()     #得到第一个显示器、宽、高、位深、刷新率等属性
        vmode = glfw.get_video_mode(m1)
        glfw.set_window_pos(self._win,(vmode.size.width -self._w)//2,(vmode.size.height -self._h)//2)
    
    #当窗口改变大小时调用
    def resize(self,func):
        if func:
            glfw.set_window_size_callback(self._win,func)
    
    #附加上一个scene
    def attch(self,scene):
        self.scene = scene
        self.scene.update(self._win,self._w,self._h)

    def main_loop(self):
        glClearColor(0.0,0.32,0.22,1.0)
        while not glfw.window_should_close(self._win):
            glfw.poll_events()
            glClear(GL_COLOR_BUFFER_BIT)
            self.scene.draw()

            glfw.swap_buffers(self._win)
        
        glfw.terminate()

if __name__ == "__main__":
    win =CWindow(683,384,"QS OpenGL Window")
    win.main_loop()