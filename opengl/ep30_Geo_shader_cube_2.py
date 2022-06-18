import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram,compileShader
import numpy
import pyrr
from PIL import Image
from camera import Camera
# 错误： 死活不显示任何东东，clearcolor能正确显示清屏颜色
# 解决： 在几何着色器中 glposition的4维顶点，第4维设置为0了，改成1就显示了
# #
cam = Camera()
WIDTH,HEIGHT = 1024,576 #683,384
lastX, lastY = WIDTH/2,HEIGHT/2
first_mouse = True
left,right,forward,backward = False,False,False,False

def key_input_clb(window,key,scancode,action,mode):
    global left,right,forward,backward
    if key == glfw.KEY_ESCAPE and action ==glfw.PRESS:
        glfw.set_window_should_close(window,True)
    
    if action == glfw.PRESS:
        if key == glfw.KEY_W or key == glfw.KEY_UP:
            forward = True
        if key == glfw.KEY_S or key == glfw.KEY_DOWN:
            backward = True 
        if key == glfw.KEY_A or key == glfw.KEY_LEFT:
            left = True  
        if key == glfw.KEY_D or key == glfw.KEY_RIGHT:
            right = True
    if action == glfw.RELEASE:
       if key in [glfw.KEY_W,glfw.KEY_S,glfw.KEY_A,glfw.KEY_D,glfw.KEY_UP,glfw.KEY_DOWN,glfw.KEY_LEFT,glfw.KEY_RIGHT]:
           left,right,forward,backward = False,False,False,False 
            
        
def do_movement():
    if left:
        cam.process_keyboard("LEFT")
    if right:
        cam.process_keyboard("RIGHT")
    if forward:
        cam.process_keyboard("FORWARD")
    if backward:
        cam.process_keyboard("BACKWARD")
    

def mouse_look_clb(window,xpos,ypos):
    global lastX,lastY

    if first_mouse:
        lastX = xpos
        lastY = ypos

    xoffset =xpos - lastX
    yoffset =lastY -ypos

    lastX = xpos
    lastY = ypos

    cam.process_mouse_movement(xoffset,yoffset)


def mouse_enter_clb(window,entered):
    global first_mouse

    if entered:
        first_mouse = False
    else:
        first_mouse = True

#使用indices索引来渲染图形

vertex_src ='''
# version 330 core
layout(location = 0)in vec4 a_position;
layout(location = 1)in vec3 a_color;

out vec3 v_color;

void main()
{
    gl_Position = a_position;
    v_color = a_color;
}
'''
geometry_src = '''
#version 330 core
layout (points) in;
layout (triangle_strip, max_vertices = 14) out;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

out vec3 f_color;

void build_cube(mat4 mx,vec4 pt)
{
    float l = pt.w;
    vec4 position = vec4(pt.xyz,1.0);

    gl_Position = mx * (position + vec4(0.0, l ,0.0,0.0));
    f_color = vec3(0.0,0.0,1.0);
    EmitVertex();
    gl_Position = mx * (position + vec4( l , l ,0.0,0.0));
    f_color = vec3(0.0,0.0,1.0);
    EmitVertex();
    gl_Position = mx * (position + vec4(0.0,0.0,0.0,0.0));
    f_color = vec3(0.0,0.0,1.0);
    EmitVertex();
    gl_Position = mx * (position + vec4( l ,0.0,0.0,0.0));
    f_color = vec3(0.0,0.0,1.0);
    EmitVertex();
    gl_Position = mx * (position + vec4( l ,0.0, l ,0.0));
    f_color = vec3(0.0,0.0,1.0);
    EmitVertex();
    gl_Position = mx * (position + vec4( l , l ,0.0,0.0));
    f_color = vec3(0.0,1.0,1.0);
    EmitVertex();
    gl_Position = mx * (position + vec4( l , l , l ,0.0));
    f_color = vec3(0.0,1.0,1.0);
    EmitVertex();
    gl_Position = mx * (position + vec4(0.0, l ,0.0,0.0));
    f_color = vec3(0.0,0.0,1.0);
    EmitVertex();
    gl_Position = mx * (position + vec4(0.0, l , l ,0.0));
    f_color = vec3(1.0,0.0,1.0);
    EmitVertex();
    gl_Position = mx * (position + vec4(0.0,0.0,0.0,0.0));
    f_color = vec3(1.0,0.0,1.0);
    EmitVertex();
    gl_Position = mx * (position + vec4(0.0,0.0, l ,0.0));
    f_color = vec3(0.0,0.0,1.0);
    EmitVertex();
    gl_Position = mx * (position + vec4( l ,0.0, l ,0.0));
    f_color = vec3(0.0,0.0,1.0);
    EmitVertex();
    gl_Position = mx * (position + vec4(0.0, l , l ,0.0));
    f_color = vec3(0.0,1.0,0.0);
    EmitVertex();
    gl_Position = mx * (position + vec4( l , l , l ,0.0));
    f_color = vec3(0.0,1.0,0.0);
    EmitVertex();
    EndPrimitive();
}

void main() {
    mat4 mx = projection * view * model;

    build_cube(mx,gl_in[0].gl_Position);
}
'''



fragment_src ="""
# version 330 core

in vec3 f_color;

void main(){
    gl_FragColor = vec4(f_color, 1.0);
}

"""
def window_resize(window,width,height):
    glViewport(0,0,width,height)
    projection = pyrr.Matrix44.perspective_projection(45,width/height,0.1,100)
    glUniformMatrix4fv(proj_loc,1,GL_FALSE,projection)

if not glfw.init():
    raise Exception("glfw can not be initialized!")

#creating the window

window = glfw.create_window(WIDTH,HEIGHT,"QS OpenGL Window",None,None)

if not window:
    glfw.terminate()
    raise Exception("glfw window can not be created!")

glfw.set_window_pos(window,(1366-WIDTH)//2 ,(768-HEIGHT)//2)
glfw.set_window_size_callback(window,window_resize)
glfw.set_cursor_pos_callback(window,mouse_look_clb)
glfw.set_cursor_enter_callback(window,mouse_enter_clb)
#glfw.set_input_mode(window,glfw.CURSOR,glfw.CURSOR_DISABLED)
glfw.set_key_callback(window,key_input_clb)

#context
glfw.make_context_current(window)

vertices =[	0.0,	0.0,	0.0,	1.0,    1.0,	0.0,	0.0]

vertices =numpy.array(vertices,numpy.float32)

shade = compileProgram(compileShader(vertex_src,GL_VERTEX_SHADER),
                       compileShader(geometry_src,GL_GEOMETRY_SHADER),
                       compileShader(fragment_src,GL_FRAGMENT_SHADER))
VBO = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER,VBO)
glBufferData(GL_ARRAY_BUFFER,vertices.nbytes,vertices,GL_STATIC_DRAW)

glEnableVertexAttribArray(0)
glVertexAttribPointer(0,4,GL_FLOAT,GL_FALSE,28,ctypes.c_void_p(0))

glEnableVertexAttribArray(1)
glVertexAttribPointer(1,3,GL_FLOAT,GL_FALSE,28,ctypes.c_void_p(16))

glUseProgram(shade)
glClearColor(0,0.1,0.0,1)
glEnable(GL_DEPTH_TEST)
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA,GL_ONE_MINUS_SRC_ALPHA)

projection = pyrr.Matrix44.perspective_projection(45,WIDTH/HEIGHT,0.1,100.0)
proj_loc = glGetUniformLocation(shade,"projection")
view_loc = glGetUniformLocation(shade,"view")
model_loc = glGetUniformLocation(shade,"model")
#上传矩阵
glUniformMatrix4fv(proj_loc,1,GL_FALSE,projection)

#translate = pyrr.Matrix44.from_translation(pyrr.Vector3([0.0, 0.0,-3.0]))

#the main application loop
while not glfw.window_should_close(window):
    glfw.poll_events()
    do_movement()
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    #glPolygonMode(GL_FRONT_AND_BACK,GL_POINT)

    view = cam.get_view_matrix()
    glUniformMatrix4fv(view_loc,1,GL_FALSE,view)

    rot_y = pyrr.Matrix44.from_y_rotation(0.3 * glfw.get_time())
    #上传矩阵
    glUniformMatrix4fv(model_loc,1,GL_FALSE,rot_y)

    glDrawArrays(GL_POINTS,0,1)
    #使用索引列表的方式进行绘制
    #glDrawElements(GL_LINE,len(indices),GL_UNSIGNED_INT,None)#GL_TRIANGLES

    glfw.swap_buffers(window)

#shotdown the application
glfw.terminate()