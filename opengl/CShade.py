from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram,compileShader

class CShade:
    def __init__(self,vt_path:str,fg_path:str):
        f1 = open(vt_path,'r')
        vt_src = f1.read()
        f1.close()

        f2 = open(fg_path,'r')
        fg_src = f2.read()
        f2.close()

        # print(vt_src)
        # print(fg_src)

        self.shade = compileProgram(
            compileShader(vt_src,GL_VERTEX_SHADER),
            compileShader(fg_src,GL_FRAGMENT_SHADER))

if __name__ == '__main__':
    shade = CShade(r'./shade/grid_vt.vs',r'./shade/grid_fg.vs')