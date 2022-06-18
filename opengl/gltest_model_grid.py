from turtle import position
import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram,compileShader
import numpy

vertex_src ='''
# version 330 core
layout(location = 0)in vec3 a_position;
layout(location = 1)in vec3 a_color;
out vec3 v_color;

void main()
{
    gl_Position = vec4(a_position,1.0);
    v_color = a_color;
}
'''
fragment_src ="""
# version 330 core

in vec3 v_color;
out vec4 out_color;

void main(){
    out_color = vec4(1.0,1.0,1.0,1.0);
}

"""
def window_resize(window,width,height):
    glViewport(0,0,width,height)

if not glfw.init():
    raise Exception("glfw can not be initialized!")

#creating the window
window = glfw.create_window(683,384,"QS OpenGL Window",None,None)

if not window:
    glfw.terminate()
    raise Exception("glfw window can not be created!")

glfw.set_window_pos(window,341,25)
glfw.set_window_size_callback(window,window_resize)
#context
glfw.make_context_current(window)

#grid 的 size n;是哪个平面上的 1. xy平面 2.xz平面 3.yz平面
vertices_grid = []
n = 1
count = 10
step = 2*n /count
for x in range(0,count,1):     #纵向
    vertices_grid.append(-n+step*x)
    vertices_grid.append(0)
    vertices_grid.append(-n)
    vertices_grid.append(-n+step*x)
    vertices_grid.append(0)
    vertices_grid.append(n)
for y in range(0,count,1):     #横向
    vertices_grid.append(-n)
    vertices_grid.append(0)
    vertices_grid.append(n-step*y)
    vertices_grid.append(n)
    vertices_grid.append(0)
    vertices_grid.append(n-step*y)
vertices_grid =numpy.array(vertices_grid,numpy.float32)
print(vertices_grid)

shade = compileProgram(compileShader(vertex_src,GL_VERTEX_SHADER),compileShader(fragment_src,GL_FRAGMENT_SHADER))
VBO = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER,VBO)
glBufferData(GL_ARRAY_BUFFER,vertices_grid.nbytes,vertices_grid,GL_STATIC_DRAW)

glEnableVertexAttribArray(0)
glVertexAttribPointer(0,3,GL_FLOAT,GL_FALSE,12,ctypes.c_void_p(0))

glUseProgram(shade)
glClearColor(0,0.1,0.1,1)

#the main application loop
while not glfw.window_should_close(window):
    glfw.poll_events()

    glClear(GL_COLOR_BUFFER_BIT)

    glDrawArrays(GL_LINES,0,vertices_grid.nbytes//12)

    glfw.swap_buffers(window)

#shotdown the application
glfw.terminate()


