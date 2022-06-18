import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram,compileShader
import numpy
import pyrr
from PIL import Image
from camera import Camera

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
layout(location = 0)in vec3 a_position;
layout(location = 1)in vec3 a_color;
layout(location = 2)in vec2 a_texture;
out vec3 v_color;
out vec2 v_texture;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

mat4 mx = projection * view * model;

void main()
{
    gl_Position = mx * vec4(a_position,1.0);
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
uniform int switcher;

void main(){
    if (switcher==0)
    {
        out_color = texture(s_texture,v_texture);// * vec4(1.0,1.0,1.0,0.5); //* vec4(v_color, 0.8);
    }
    else if(switcher==1)
    {
        out_color = vec4(1.0, 0.0, 1.0, 1.0);
    }
    //gl_FragColor = vec4(1.0, 0.0, 0.0, 1.0);
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
s = glGetString(GL_VERSION)
print('opengl_version:',s)

#grid 的 size n;是哪个平面上的 1. xy平面 2.xz平面 3.yz平面
vertices_grid = []
n = 10
count = 20
step = 2*n /count
z = -0.5
for x in range(0,count+1):     #纵向
    vertices_grid.append(-n+step*x)
    vertices_grid.append(z)
    vertices_grid.append(-n)
    vertices_grid.append(-n+step*x)
    vertices_grid.append(z)
    vertices_grid.append(n)
for y in range(0,count+1):     #横向
    vertices_grid.append(-n)
    vertices_grid.append(z)
    vertices_grid.append(n-step*y)
    vertices_grid.append(n)
    vertices_grid.append(z)
    vertices_grid.append(n-step*y)
vertices_grid =numpy.array(vertices_grid,numpy.float32)

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

# Cube VAO
cube_VAO = glGenVertexArrays(1)
glBindVertexArray(cube_VAO)

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
glVertexAttribPointer(2,3,GL_FLOAT,GL_FALSE,32,ctypes.c_void_p(24))

texture = glGenTextures(1)
glBindTexture(GL_TEXTURE_2D,texture)

glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_WRAP_S,GL_REPEAT)
glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_WRAP_T,GL_REPEAT)

glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_LINEAR)
glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_LINEAR)

#加载IMAGE
image = Image.open("textures/crate1.jpg")
image = image.transpose(Image.FLIP_TOP_BOTTOM)
img_data = image.convert("RGBA").tobytes()

glTexImage2D(GL_TEXTURE_2D,0,GL_RGBA,image.width,image.height,0,GL_RGBA,GL_UNSIGNED_BYTE,img_data)

# Cube VAO
grid_VAO = glGenVertexArrays(1)
glBindVertexArray(grid_VAO)

VBO = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER,VBO)
glBufferData(GL_ARRAY_BUFFER,vertices_grid.nbytes,vertices_grid,GL_STATIC_DRAW)

glEnableVertexAttribArray(0)
glVertexAttribPointer(0,3,GL_FLOAT,GL_FALSE,12,ctypes.c_void_p(0))

glUseProgram(shade)
glClearColor(0,0.1,0.1,1)
glEnable(GL_DEPTH_TEST)
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA,GL_ONE_MINUS_SRC_ALPHA)

projection = pyrr.Matrix44.perspective_projection(45,WIDTH/HEIGHT,0.1,100.0)
proj_loc = glGetUniformLocation(shade,"projection")
view_loc = glGetUniformLocation(shade,"view")
model_loc = glGetUniformLocation(shade,"model")
switcher_loc = glGetUniformLocation(shade, "switcher")
#上传矩阵
glUniformMatrix4fv(proj_loc,1,GL_FALSE,projection)

#translate = pyrr.Matrix44.from_translation(pyrr.Vector3([0.0, 0.0,-3.0]))

#the main application loop
while not glfw.window_should_close(window):
    glfw.poll_events()
    do_movement()
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

    view = cam.get_view_matrix()
    glUniformMatrix4fv(view_loc,1,GL_FALSE,view)

    #rot_x = pyrr.Matrix44.from_x_rotation(0.8 * glfw.get_time())
    rot_y = pyrr.Matrix44.from_y_rotation(0.3 * glfw.get_time())
    
    #上传矩阵
    glUniformMatrix4fv(model_loc,1,GL_FALSE,rot_y)#rot_y
    glUniform1i(switcher_loc, 0)
    glBindVertexArray(cube_VAO)
    glBindTexture(GL_TEXTURE_2D,texture)
    glDrawElements(GL_TRIANGLES,len(indices),GL_UNSIGNED_INT,None)

    glUniformMatrix4fv(model_loc,1,GL_FALSE,pyrr.matrix44.create_identity())
    glUniform1i(switcher_loc, 1)
    glBindVertexArray(grid_VAO)
    glDrawArrays(GL_LINES,0,vertices_grid.nbytes//12)

    glfw.swap_buffers(window)

#shotdown the application
glfw.terminate()