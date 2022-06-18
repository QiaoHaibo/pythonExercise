from turtle import position
from PIL import Image
import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram,compileShader
import pyrr
import numpy

vertex_src ='''
# version 330 core
layout(location = 0)in vec3 a_position;
layout(location = 1)in vec2 a_texture;
out vec2 v_texture; 
uniform mat4 ortho;

void main()
{
    gl_Position = ortho*vec4(a_position,1.0);
    v_texture = a_texture;
}
'''
fragment_src ="""
# version 330 core

out vec4 out_color;
in vec2 v_texture;
uniform sampler2D s_texture; 
void main(){
    out_color = texture(s_texture,v_texture) ;//* vec4(v_color, 0.8)
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
window = glfw.create_window(683,384,"QS OpenGL Window",None,None)

if not window:
    glfw.terminate()
    raise Exception("glfw window can not be created!")

m1 = glfw.get_primary_monitor()     #得到第一个显示器、宽、高、位深、刷新率等属性
vmode = glfw.get_video_mode(m1)
glfw.set_window_pos(window,(vmode.size.width -WIDTH)//2,(vmode.size.height -HEIGHT)//2)
glfw.set_window_size_callback(window,window_resize)
#context
glfw.make_context_current(window)

vertices =[-100.0, -100.0,  0,      0.0,0.0,
            100.0, -100.0,  0,      1.0,0.0,
           -100.0,  100.0,  0,      0.0,1.0,
            100.0,  100.0,  0,      1.0,1.0  ]

vertices =numpy.array(vertices,numpy.float32)

shade = compileProgram(compileShader(vertex_src,GL_VERTEX_SHADER),compileShader(fragment_src,GL_FRAGMENT_SHADER))
VBO = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER,VBO)
glBufferData(GL_ARRAY_BUFFER,vertices.nbytes,vertices,GL_STATIC_DRAW)

glEnableVertexAttribArray(0)
glVertexAttribPointer(0,3,GL_FLOAT,GL_FALSE,20,ctypes.c_void_p(0))

glEnableVertexAttribArray(1)
glVertexAttribPointer(1,2,GL_FLOAT,GL_FALSE,20,ctypes.c_void_p(12))

#加载贴图
texture = glGenTextures(1)
glBindTexture(GL_TEXTURE_2D,texture)
glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_WRAP_S,GL_REPEAT)
glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_WRAP_T,GL_REPEAT)
glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_LINEAR)
glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_LINEAR)
#加载IMAGE
image = Image.open("textures/wall.jpg")
image = image.transpose(Image.FLIP_TOP_BOTTOM)
img_data = image.convert("RGBA").tobytes()
glTexImage2D(GL_TEXTURE_2D,0,GL_RGBA,image.width,image.height,0,GL_RGBA,GL_UNSIGNED_BYTE,img_data)

glUseProgram(shade)
glClearColor(0,0.1,0.1,1)
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA,GL_ONE_MINUS_SRC_ALPHA)

hfw = WIDTH / 2
hfh = HEIGHT / 2
mt_ortho = pyrr.matrix44.create_orthogonal_projection(-hfw,hfw,-hfh,hfh,0.0,10.0)#构造正交投影矩阵 ortho
uloc_ortho = glGetUniformLocation(shade,'ortho')
glUniformMatrix4fv(uloc_ortho,1,GL_FALSE,mt_ortho)

#the main application loop
while not glfw.window_should_close(window):
    glfw.poll_events()

    glClear(GL_COLOR_BUFFER_BIT)

    glDrawArrays(GL_TRIANGLE_STRIP,0,4)

    glfw.swap_buffers(window)

#shotdown the application
glfw.terminate()


