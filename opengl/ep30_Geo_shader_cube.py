import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram,compileShader
import numpy
import pyrr
from PIL import Image

#开始时报valid faltrue，原是color没有传递
#输出线段的数量不对，应该输出4条线段，实际输出了三条。
#是设置属性时，一行的跨度不对，原来是‘24’，改成‘12’就好了。
#第一面 zyx
#010    011
#000    001
#第二面 
#011    111
#001    101
vertex_src ='''
# version 330 core
layout(location = 0)in vec3 a_position;

void main()
{
    gl_Position = vec4(a_position,1.0);
}
'''

geometry_src = '''
#version 330 core
layout (points) in;
layout (triangle_strip, max_vertices = 10) out;

uniform mat4 projection;
out vec3 fcolor;
void build_cube(mat4 mx,vec4 position,float l)
{
    gl_Position = mx * position;    // 1:原点(左下角)
    fcolor = vec3(1.0,0.0,0.0);
    EmitVertex();   
    gl_Position = mx * (position + vec4(0.0, l, 0.0, 0.0));    // 2:左上
    EmitVertex();   
    gl_Position = mx * (position + vec4( l, 0.0, 0.0, 0.0)) ;    // 3:右下
    EmitVertex();
    gl_Position = mx * (position + vec4( l,  l, 0.0, 0.0));    // 4:右上
    fcolor = vec3(1.0,1.0,0.0);
    EmitVertex();
    gl_Position = mx * (position + vec4( l,  0.0, l, 0.0));    // 5:右后下
    EmitVertex();
    gl_Position = mx * (position + vec4( l,  l, l, 0.0));    // 6:右后上
    EmitVertex();
    gl_Position = mx * (position + vec4( 0,  0, l, 0.0));    // 7:左后下
    fcolor = vec3(0.0,1.0,0.0);
    EmitVertex();
    gl_Position = mx * (position + vec4( 0,  l, l, 0.0));    // 8:左后上
    EmitVertex();
    gl_Position = mx * position;                            // 9:原点(左下角)
    fcolor = vec3(1.0,0.0,1.0);
    EmitVertex();   
    gl_Position = mx * (position + vec4(0.0, l, 0.0, 0.0));    // 10:左上
    fcolor = vec3(1.0,0.0,1.0);
    EmitVertex();
    EndPrimitive();
}

void main() {    
    build_cube(projection,gl_in[0].gl_Position,0.2);
}
'''

fragment_src ="""
# version 330 core
in vec3 fcolor;

void main(){
    gl_FragColor = vec4(fcolor.rgb, 1.0);
}

"""

def window_resize(window,width,height):
    glViewport(0,0,width,height)
    r = width/height
    projection = pyrr.Matrix44.orthogonal_projection(-r,r,1,-1,-1,100)
    glUniformMatrix4fv(proj_loc,1,GL_FALSE,projection)

if not glfw.init():
    raise Exception("glfw can not be initialized!")

#creating the window
width = 683
height = 384
window = glfw.create_window(683,384,"QS OpenGL Window",None,None)

if not window:
    glfw.terminate()
    raise Exception("glfw window can not be created!")

glfw.set_window_pos(window,341,25)
glfw.set_window_size_callback(window,window_resize)
#context
glfw.make_context_current(window)

vertices =[0.0, 0.0,  0, 
            0.5, -0.5,  0 ]

vertices =numpy.array(vertices,numpy.float32)

shade = compileProgram(compileShader(vertex_src,GL_VERTEX_SHADER),
        compileShader(geometry_src,GL_GEOMETRY_SHADER),
        compileShader(fragment_src,GL_FRAGMENT_SHADER))

VBO = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER,VBO)
glBufferData(GL_ARRAY_BUFFER,vertices.nbytes,vertices,GL_STATIC_DRAW)

glEnableVertexAttribArray(0)
glVertexAttribPointer(0,3,GL_FLOAT,GL_FALSE,12,ctypes.c_void_p(0))

glUseProgram(shade)
glClearColor(0,0.1,0.1,1)
r = width/height
projection = pyrr.Matrix44.orthogonal_projection(-r,r,1,-1,-1,100)
proj_loc = glGetUniformLocation(shade,"projection")
#上传矩阵
glUniformMatrix4fv(proj_loc,1,GL_FALSE,projection)

#the main application loop
while not glfw.window_should_close(window):
    glfw.poll_events()

    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    #上传矩阵
    rot_y = pyrr.Matrix44.from_y_rotation(0.3 * glfw.get_time())
    rot_x = pyrr.Matrix44.from_x_rotation(0.1 * glfw.get_time())
    #上传矩阵
    glUniformMatrix4fv(proj_loc,1,GL_FALSE,rot_x* rot_y)

    #glDrawArrays(GL_TRIANGLE_STRIP,0,4)
    glDrawArrays(GL_POINTS,0,2)

    glfw.swap_buffers(window)

#shotdown the application
glfw.terminate()


