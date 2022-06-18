from OpenGL.GL import *
import pyrr

from CNode import CNode
#保存屏幕投影类型
class CScene:
    def __init__(self,window) -> None:
        self.window = window
        #self._proj = proj
    def update(self,window,width,height):
        glViewport(0,0,width,height)
        ASPECT = width / height
        hfw = width / 2
        hfh = height /2 
        self._proj = pyrr.matrix44.create_orthogonal_projection(0,width,height,0.0,0.0,10.0)
        uloc_ortho = glGetUniformLocation(self.shade,'ortho')
        glUniformMatrix4fv(uloc_ortho,1,GL_FALSE,self._proj)
    
    def renderlist(self,obj:list):
        self.listobj = obj
        self.shade = self.listobj[0].shade

    def draw(self):
        for i,c in enumerate(self.listobj):
            self.shade = c.shade
            c.draw()