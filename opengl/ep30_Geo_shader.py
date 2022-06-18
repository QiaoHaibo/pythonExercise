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
uniform mat4 projection;

out VS_OUT {
    vec3 color;
} vs_out;

void main()
{
    gl_Position = projection * vec4(a_position,1.0);
    vs_out.color = a_color;
}
'''

geometry_src = '''
#version 330 core
layout (points) in;
layout (line_strip, max_vertices = 2) out;

in VS_OUT {
    vec3 color;
} gs_in[];

out vec3 fColor;

void main() {    
    fColor = gs_in[0].color;

    gl_Position = gl_in[0].gl_Position + vec4(-0.1, 0.0, 0.0, 0.0); 
    EmitVertex();

    gl_Position = gl_in[0].gl_Position + vec4( 0.1, 0.0, 0.0, 0.0);
    EmitVertex();

    EndPrimitive();
}
'''

fragment_src ="""
# version 330 core

in vec3 fColor;
out vec4 out_color;

void main(){
    out_color = vec4(fColor, 1.0);
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

vertices =[-0.5, -0.5,  0,  1.0,  0.0, 0,
            0.5, -0.5,  0,  0,  1.0,   0,
           -0.5,  0.5,  0,  0,  0,   1.0,
            0.5,  0.5,  0,  1,  1,   1.0]

vertices =numpy.array(vertices,numpy.float32)

shade = compileProgram(compileShader(vertex_src,GL_VERTEX_SHADER),
        compileShader(geometry_src,GL_GEOMETRY_SHADER),
        compileShader(fragment_src,GL_FRAGMENT_SHADER))

VBO = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER,VBO)
glBufferData(GL_ARRAY_BUFFER,vertices.nbytes,vertices,GL_STATIC_DRAW)

glEnableVertexAttribArray(0)
glVertexAttribPointer(0,3,GL_FLOAT,GL_FALSE,24,ctypes.c_void_p(0))

glEnableVertexAttribArray(1)
glVertexAttribPointer(1,3,GL_FLOAT,GL_FALSE,24,ctypes.c_void_p(12))


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
    #glUniformMatrix4fv(model_loc,1,GL_FALSE,translate*rot_x* rot_y)

    #glDrawArrays(GL_TRIANGLE_STRIP,0,4)
    glDrawArrays(GL_POINTS,0,4)

    glfw.swap_buffers(window)

#shotdown the application
glfw.terminate()


