import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram,compileShader
from matplotlib.pyplot import title
import numpy
import pyrr
import imgui
from imgui.integrations.glfw import GlfwRenderer

from PIL import Image
from camera import Camera
# 目标:
#  （2022年06月11日）
# ⑴ 使用 Geometry Shade 画出一个立方体
# ⑵ 实现用鼠标对体素进行选择、细分、删除、增加的功能
# 

# 错误： 按“w”“s”“a”“d”走动后显示图形的位置移动了
# 解决： 错觉，原因是grid的Y轴设置成了“-1”,绘图对象“漂浮”在网络之上
# 尝试：    去掉了片段着色器里的switcher问题仍然存在
# 尝试：    检查同样使用Camera类的“ep16_glfw_FPS_2.py”也有问题
# 尝试：    会不会是错觉?绘图对象“漂浮”在网络之上


# 错误： 期待显示一四边形，只显示一半（三角形）
# 解决： 调用绘制函数 glDrawArrays时，第1个参数，传入了“GL_TRIANGLE”,应该传入“GL_TRIANGLE_STRIP”

# 错误： 期待显示一四边形，其中一半（三角形）不停闪烁
# 解决： 调用绘制函数 glDrawArrays时，第3个参数（最后一个），传入的数量比实际数量多

# 错误： pyrr 向量除法错误
# 解决： 在归一化中normalize添加了长度为0的判断
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
out vec3 v_color;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

void main()
{
    mat4 mx = projection * view * model;
    gl_Position = mx * vec4(a_position,1.0);
    v_color = a_color;
}
'''
fragment_src ="""
# version 330 core

in vec3 v_color;
out vec4 out_color;

uniform int switcher;

void main(){
    if (switcher==0)
    {
        out_color = vec4(v_color, 1.0);
    }
    else if(switcher==1)
    {
        out_color = vec4(1.0, 1.0, 1.0, 1.0);
    }
    //gl_FragColor = vec4(1.0, 0.0, 0.0, 1.0);
}

"""
def window_resize(window,width,height):
    WIDTH,HEIGHT = width,height
    glViewport(0,0,WIDTH,HEIGHT)

if not glfw.init():
    raise Exception("glfw can not be initialized!")

imgui.create_context()

    # OS X supports only forward-compatible core profiles from 3.2
glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)
glfw.window_hint(glfw.SAMPLES, 4)#glfwWindowHint(GLFW_SAMPLES, 4)
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
#print('opengl_version:',s)

impl = GlfwRenderer(window,False)
io = imgui.get_io()
io.display_size = 200, 200
new_font = io.fonts.add_font_from_file_ttf(r"C:\windows\fonts\simhei.ttf",13.0,io.fonts.get_glyph_ranges_chinese())
impl.refresh_font_texture()
# imgui.get_io().fonts.get_tex_data_as_rgba32()

#grid 的 size n;是哪个平面上的 1. xy平面 2.xz平面 3.yz平面
vertices_grid = []
n = 10
count = 20
step = 2*n /count
z = 0
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

vertices =[	0.0,	0.0,	0.0,	1.0,	0.0,	0.0,	0.0,	0.0,
            1.0,	0.0,	0.0,	0.0,	1.0,	0.0,	1.0,	0.0,
            0.0,	1.0,	0.0,	0.0,	0.0,	1.0,	1.0,	1.0,
            1.0,	1.0,	0.0,	1.0,	1.0,	1.0,	0.0,	1.0]


vertices =numpy.array(vertices,numpy.float32)

shade = compileProgram(compileShader(vertex_src,GL_VERTEX_SHADER),compileShader(fragment_src,GL_FRAGMENT_SHADER))

# Cube VAO
cube_VAO = glGenVertexArrays(1)
glBindVertexArray(cube_VAO)

VBO = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER,VBO)
glBufferData(GL_ARRAY_BUFFER,vertices.nbytes,vertices,GL_STATIC_DRAW)

glEnableVertexAttribArray(0)
glVertexAttribPointer(0,3,GL_FLOAT,GL_FALSE,32,ctypes.c_void_p(0))

glEnableVertexAttribArray(1)
glVertexAttribPointer(1,3,GL_FLOAT,GL_FALSE,32,ctypes.c_void_p(12))

glEnableVertexAttribArray(2)
glVertexAttribPointer(2,2,GL_FLOAT,GL_FALSE,32,ctypes.c_void_p(24))

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


proj_loc = glGetUniformLocation(shade,"projection")
view_loc = glGetUniformLocation(shade,"view")
model_loc = glGetUniformLocation(shade,"model")
switcher_loc = glGetUniformLocation(shade, "switcher")
#上传矩阵

radio_active = [True,False,False]
#translate = pyrr.Matrix44.from_translation(pyrr.Vector3([0.0, 0.0,-3.0]))

#the main application loop
while not glfw.window_should_close(window):
    glfw.poll_events()
    do_movement()

    impl.process_inputs()

    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

    #print("width:",WIDTH,HEIGHT)
    projection = pyrr.Matrix44.perspective_projection(45,WIDTH/HEIGHT,1.0,100.0)
    view = cam.get_view_matrix()
    glUniformMatrix4fv(proj_loc,1,GL_FALSE,projection)
    glUniformMatrix4fv(view_loc,1,GL_FALSE,view)
    glUniformMatrix4fv(model_loc,1,GL_FALSE,pyrr.Matrix44.identity())

    #画 网格
    glUniform1i(switcher_loc, 1)
    glBindVertexArray(grid_VAO)
    glDrawArrays(GL_LINES,0,vertices_grid.nbytes//12)

    #画 立方体
    glUniform1i(switcher_loc, 0)
    glBindVertexArray(cube_VAO)
    glDrawArrays(GL_TRIANGLE_STRIP,0,vertices.nbytes//32)

    #imgui start
    # start new frame context
    imgui.new_frame()

    # open new window context
    imgui.begin("camera state", True)
    with imgui.font(new_font):
    # draw text label inside of current window
        imgui.text("mouse pos : {},{}".format(lastX,lastY))
        imgui.text("位置 : {},{},{}".format(round(cam.camera_pos.x,2),round(cam.camera_pos.y,2),round(cam.camera_pos.z,2)))
        imgui.text("front : {},{},{}".format(round(cam.camera_front[0],2),round(cam.camera_front[1],2),round(cam.camera_front[2],2)))
        imgui.text("right : {},{},{}".format(round(cam.camera_right[0],2),round(cam.camera_right[1],2),round(cam.camera_right[2],2)))
        imgui.text("up : {},{},{}".format(round(cam.camera_up[0],2),round(cam.camera_up[1],2),round(cam.camera_up[2],2)))
        imgui.text_colored("yaw : {}".format(cam.yaw),1.0,1.0,0.0)
        imgui.text("pitch : {}".format(cam.pitch))
        
        if imgui.radio_button("铅笔",radio_active[0]):
            radio_active[0] = True
            radio_active[1] = False
            radio_active[2] = False
        imgui.same_line()
        if imgui.radio_button("橡皮",radio_active[1]):
            radio_active[0] = False
            radio_active[1] = True
            radio_active[2] = False
        imgui.same_line()
        if imgui.radio_button("小刀",radio_active[2]):
            radio_active[0] = False
            radio_active[1] = False
            radio_active[2] = True
    # close current window context
    imgui.end()

    # pass all drawing comands to the rendering pipeline
    # and close frame context
    imgui.render()
    impl.render(imgui.get_draw_data())
    imgui.end_frame()
    #imgui end

    glfw.swap_buffers(window)

#shotdown the application
glfw.terminate()