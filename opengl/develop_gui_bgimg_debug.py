from PIL import Image
import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram,compileShader
import numpy
import pyrr         #矩阵等数学库

#使用 ortho 投影，如果不使用的话长宽比例不对

vertex_src ='''
# version 330 core
layout(location = 0)in vec2 a_position;
uniform mat4 ortho;

void main()
{
    gl_Position = ortho * vec4(a_position,1.0,1.0);
}
'''
fragment_src ="""
# version 330 core

out vec4 out_color;
void main(){
    out_color = vec4(1.0,0.0,0.0,1.0);
}

"""
WIDTH,HEIGHT= 683,384
ASPECT = WIDTH/HEIGHT
def window_resize(window,width,height):
    glViewport(0,0,width,height)
    ASPECT = width / height
    hfw = width / 2
    hfh = height /2 
    mt_ortho = pyrr.matrix44.create_orthogonal_projection(-hfw,hfw,-hfh,hfh,0.0,10.0)#构造正交投影矩阵 ortho
    uloc_ortho = glGetUniformLocation(shade,'ortho')
    glUniformMatrix4fv(uloc_ortho,1,GL_FALSE,mt_ortho)
if not glfw.init():
    raise Exception("glfw can not be initialized!")

#creating the window
window = glfw.create_window(WIDTH,HEIGHT,"QS OpenGL Window",None,None)

if not window:
    glfw.terminate()
    raise Exception("glfw window can not be created!")

m1 = glfw.get_primary_monitor()     #得到第一个显示器、宽、高、位深、刷新率等属性
vmode = glfw.get_video_mode(m1)

glfw.set_window_pos(window,(vmode.size.width -WIDTH)//2,(vmode.size.height -HEIGHT)//2)
glfw.set_window_size_callback(window,window_resize)
#context
glfw.make_context_current(window)

vertices =[-50.0, -50.0,  0.0,  0.0,
            50.0, -50.0,  1.0,  0.0,
           -50.0,  50.0,  1.0,  1.0,
            50.0,  50.0,  0.0,  1.0]
indices =[0,1,2,
          1,2,3]
vertices =numpy.array(vertices,numpy.float32)
indices =numpy.array(indices,numpy.uint)

shade = compileProgram(compileShader(vertex_src,GL_VERTEX_SHADER),compileShader(fragment_src,GL_FRAGMENT_SHADER))
VBO = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER,VBO)
glBufferData(GL_ARRAY_BUFFER,vertices.nbytes,vertices,GL_STATIC_DRAW)

#索引缓存注册
EBO = glGenBuffers(1)
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER,EBO)
glBufferData(GL_ELEMENT_ARRAY_BUFFER,indices.nbytes,indices,GL_STATIC_DRAW)

glEnableVertexAttribArray(0)
glVertexAttribPointer(0,2,GL_FLOAT,GL_FALSE,16,ctypes.c_void_p(0))

glUseProgram(shade)
glClearColor(0.0,0.32,0.22,1)

hfw = WIDTH / 2
hfh = HEIGHT / 2
mt_ortho = pyrr.matrix44.create_orthogonal_projection(-hfw,hfw,-hfh,hfh,0.0,10.0)#构造正交投影矩阵 ortho
uloc_ortho = glGetUniformLocation(shade,'ortho')
glUniformMatrix4fv(uloc_ortho,1,GL_FALSE,mt_ortho)

#the main application loop
while not glfw.window_should_close(window):
    glClear(GL_COLOR_BUFFER_BIT)

    glDrawElements(GL_TRIANGLES,len(indices),GL_UNSIGNED_INT,None)
    
    glfw.poll_events()
    glfw.swap_buffers(window)
 
#shotdown the application
glfw.terminate()


