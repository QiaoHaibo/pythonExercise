from turtle import position
import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram,compileShader
import numpy
import pyrr
from PIL import Image


#使用indices索引来渲染图形

vertex_src ='''
# version 330 core
layout(location = 0)in vec3 a_position;
layout(location = 1)in vec3 a_color;
layout(location = 2)in vec2 a_texture;
out vec3 v_color;
out vec2 v_texture;

uniform mat4 rotation;

void main()
{
    gl_Position = rotation * vec4(a_position,1.0);
    v_color = a_color;
    v_texture = a_texture;
}
'''
fragment_src ="""
# version 330 core

in vec3 v_color;
out vec4 out_color;
in vec2 v_texture;
uniform sampler2D s_texture; 

void main(){
    //out_color = vec4(v_color, 1.0);
    out_color = texture(s_texture,v_texture) * vec4(v_color, 0.5);
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

vertices =[	-0.5,	-0.5,	0.5,	1.0,	0.0,	0.0,	0.0,	0.0,
            0.5,	-0.5,	0.5,	0.0,	1.0,	0.0,	1.0,	0.0,
            0.5,	0.5,	0.5,	0.0,	0.0,	1.0,	1.0,	1.0,
            -0.5,	0.5,	0.5,	1.0,	1.0,	1.0,	0.0,	1.0,
            
            -0.5,	-0.5,	-0.5,	1.0,	0.0,	0.0,	0.0,	0.0,
            0.5,	-0.5,	-0.5,	0.0,	1.0,	0.0,	1.0,	0.0,
            0.5,	0.5,	-0.5,	0.0,	0.0,	1.0,	1.0,	1.0,
            -0.5,	0.5,	-0.5,	1.0,	1.0,	1.0,	0.0,	1.0,
            
            0.5,	-0.5,	-0.5,	1.0,	0.0,	0.0,	0.0,	0.0,
            0.5,	0.5,	-0.5,	0.0,	1.0,	0.0,	1.0,	0.0,
            0.5,	0.5,	0.5,	0.0,	0.0,	1.0,	1.0,	1.0,
            0.5,	-0.5,	0.5,	1.0,	1.0,	1.0,	0.0,	1.0,
            
            -0.5,	0.5,	-0.5,	1.0,	0.0,	0.0,	0.0,	0.0,
            -0.5,	-0.5,	-0.5,	0.0,	1.0,	0.0,	1.0,	0.0,
            -0.5,	-0.5,	0.5,	0.0,	0.0,	1.0,	1.0,	1.0,
            -0.5,	0.5,	0.5,	1.0,	1.0,	1.0,	0.0,	1.0,
            
            -0.5,	-0.5,	-0.5,	1.0,	0.0,	0.0,	0.0,	0.0,
            0.5,	-0.5,	-0.5,	0.0,	1.0,	0.0,	1.0,	0.0,
            0.5,	-0.5,	0.5,	0.0,	0.0,	1.0,	1.0,	1.0,
            -0.5,	-0.5,	0.5,	1.0,	1.0,	1.0,	0.0,	1.0,
            
            0.5,	0.5,	-0.5,	1.0,	0.0,	0.0,	0.0,	0.0,
            -0.5,	0.5,	-0.5,	0.0,	1.0,	0.0,	1.0,	0.0,
            -0.5,	0.5,	0.5,	0.0,	0.0,	1.0,	1.0,	1.0,
            0.5,	0.5,	0.5,	1.0,	1.0,	1.0,	0.0,	1.0]

indices =[  0,	1,	2,	2,	3,	0,
            4,	5,	6,	6,	7,	4,
            8,	9,	10,	10,	11,	8,
            12,	13,	14,	14,	15,	12,
            16,	17,	18,	18,	19,	16,
            20,	21,	22,	22,	23,	20]

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
glVertexAttribPointer(0,3,GL_FLOAT,GL_FALSE,32,ctypes.c_void_p(0))

glEnableVertexAttribArray(1)
glVertexAttribPointer(1,3,GL_FLOAT,GL_FALSE,32,ctypes.c_void_p(12))

glEnableVertexAttribArray(2)
glVertexAttribPointer(2,2,GL_FLOAT,GL_FALSE,32,ctypes.c_void_p(24))

texture = glGenTextures(1)
glBindTexture(GL_TEXTURE_2D,texture)

glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_WRAP_S,GL_REPEAT)
glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_WRAP_T,GL_REPEAT)

glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_NEAREST)
glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_LINEAR)

#加载IMAGE
image = Image.open("textures/anime_girl_PNG45.png")
image = image.transpose(Image.FLIP_TOP_BOTTOM)
img_data = image.convert("RGBA").tobytes()

glTexImage2D(GL_TEXTURE_2D,0,GL_RGBA,image.width,image.height,0,GL_RGBA,GL_UNSIGNED_BYTE,img_data)

glUseProgram(shade)
glClearColor(0,0.1,0.1,1)
glEnable(GL_DEPTH_TEST)
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA,GL_ONE_MINUS_SRC_ALPHA)

rotation_loc = glGetUniformLocation(shade,"rotation")
#the main application loop
while not glfw.window_should_close(window):
    glfw.poll_events()

    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

    rot_x = pyrr.Matrix44.from_x_rotation(0.8 * glfw.get_time())
    rot_y = pyrr.Matrix44.from_y_rotation(0.3 * glfw.get_time())
    #上传矩阵
    glUniformMatrix4fv(rotation_loc,1,GL_FALSE,rot_x* rot_y)

    #glDrawArrays(GL_TRIANGLE_STRIP,0,4)
    #使用索引列表的方式进行绘制
    glDrawElements(GL_TRIANGLES,len(indices),GL_UNSIGNED_INT,None)

    glfw.swap_buffers(window)

#shotdown the application
glfw.terminate()


