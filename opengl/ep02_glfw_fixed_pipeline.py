import glfw
from OpenGL.GL import *
import numpy
from math import sin,cos

if not glfw.init():
    raise Exception("glfw can not be initialized!")

#creating the window
window = glfw.create_window(683,384,"QS OpenGL Window",None,None)

if not window:
    glfw.terminate()
    raise Exception("glfw window can not be created!")

glfw.set_window_pos(window,341,192)

#context
glfw.make_context_current(window)

vertices =[-0.5, -0.5, 0,
            0.5, -0.5, 0,
            0,    0.5, 0]

colors =[1.0, 0, 0,
         0,  1.0,0,
         0, 0, 1.0]

vertices =numpy.array(vertices,numpy.float32)
colors =numpy.array(colors,numpy.float32)

glEnableClientState(GL_VERTEX_ARRAY)
glVertexPointer(3,GL_FLOAT,0,vertices)

glEnableClientState(GL_COLOR_ARRAY)
glColorPointer(3,GL_FLOAT,0,colors)

glClearColor(0,0.1,0.1,1)

#the main application loop
while not glfw.window_should_close(window):
    glfw.poll_events()

    glClear(GL_COLOR_BUFFER_BIT)

    ct = glfw.get_time()

    glLoadIdentity()
    glScale(abs(sin(ct)),abs(sin(ct)),1)
    glRotatef(sin(ct)*45,0,0,1)
    glTranslate(sin(ct),cos(ct),0)

    glDrawArrays(GL_TRIANGLES,0,3)

    glfw.swap_buffers(window)

#shotdown the application
glfw.terminate()


