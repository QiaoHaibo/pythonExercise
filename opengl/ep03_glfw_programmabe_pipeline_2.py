from turtle import position
import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram,compileShader
import numpy
from math import sin,cos

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
    out_color = vec4(v_color, 1.0);
}

"""

if not glfw.init():
    raise Exception("glfw can not be initialized!")

#creating the window
window = glfw.create_window(650,650,"QS OpenGL Window",None,None)

if not window:
    glfw.terminate()
    raise Exception("glfw window can not be created!")

glfw.set_window_pos(window,341,25)

#context
glfw.make_context_current(window)

try:
    n = glGetIntegerv(GL_MAX_VERTEX_ATTRIBS)
    print(n)
except error as e:
    print("出现错误",e)


vertices =[-0.433, -0.249, 0,  1.0,  0.0,   0,
            0.433, -0.249, 0,  0,  1.0,   0,
            0,      0.5,   0,  0,  0,   1.0]

vertices =numpy.array(vertices,numpy.float32)

shade = compileProgram(compileShader(vertex_src,GL_VERTEX_SHADER),compileShader(fragment_src,GL_FRAGMENT_SHADER))
VBO = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER,VBO)
glBufferData(GL_ARRAY_BUFFER,vertices.nbytes,vertices,GL_STATIC_DRAW)

position = glGetAttribLocation(shade,'a_position')
glEnableVertexAttribArray(position)
glVertexAttribPointer(position,3,GL_FLOAT,GL_FALSE,24,ctypes.c_void_p(0))

color = glGetAttribLocation(shade,'a_color')
glEnableVertexAttribArray(color)
glVertexAttribPointer(color,3,GL_FLOAT,GL_FALSE,24,ctypes.c_void_p(12))

glUseProgram(shade)
glClearColor(0,0.1,0.1,1)

#the main application loop
while not glfw.window_should_close(window):
    glfw.poll_events()

    glClear(GL_COLOR_BUFFER_BIT)

    glDrawArrays(GL_TRIANGLES,0,3)

    glfw.swap_buffers(window)

#shotdown the application
glfw.terminate()


