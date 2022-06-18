import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram,compileShader
import numpy
import pyrr
from PIL import Image
from camera import Camera
# 目标:
#  （2022年06月11日）
# 1 使用 Geometry Shade 画出一个立方体 ✅
#    问题：
#       1.1 昨天尝试直接把几何着色器copy进来，造成混乱，如绘制网络的program根本没必要有几何着色器
#    解决：
#       1.2 使用了2个不同的program分开，顺利完成目标
# 2 实现用鼠标对体素进行选择、细分、删除、增加的功能
#       2.1 点选
#           鼠标在屏幕上点击发射出一条光线，光线的的起点是cmaera的position，方向是起点与屏幕鼠标位置的连线
#           ⑴ 坐标转换
#                 ① 将鼠标的屏幕坐标转换为世界坐标
#                 ② 需要用到：camera.pos camera.dir
# 
# 3 增加界面UI控制按钮
#       3.1 显示中文
#           ⑴ 网上参照大量资料（大部分是C++），都说只要设置“io.fonts.add_font_from_file_ttf”就可以。
#               实际上没有任何反应。解决：在pyimgui文档上的“extra”部分找到了实例：再用text方法之前，
#               refrash
#               imgui.font()
#       3.2 添加按钮，选择当前鼠标点击操作是“铅笔”？“橡皮”？“细分”？“合并”？
#       3.3 当鼠标指针“hover”在体素上时，显示黄色或桔红色的边框
# 4 实现体素光照
#       问题：
#           如果使用“triangle strip”来绘制带光影的立方体就会遇到法线重叠问题
#       解决：
#           恐怕需要使用24个顶点版本的“triangles”版本
#       4.1 “triangle strip”使用从网上抄来的“平均法向量”产生的效果是错的
#       4.2 使用“triangles”重写几何着色器版本的cube显示
#
# 错误： 按“最大化”按钮，程序崩溃 报：“cannot unpack non-iterable int object”
# 解决： 原来 写作“WIDTH = width,HEIGHT = height” 改“WIDTH,HEIGHT = width,height”
# 错误： 按“w”“s”“a”“d”走动后显示图形的位置移动了
# 解决： 错觉，原因是grid的Y轴设置成了“-1”,绘图对象“漂浮”在网络之上
# 尝试：    去掉了片段着色器里的switcher问题仍然存在
# 尝试：    检查同样使用Camera类的“ep16_glfw_FPS_2.py”也有问题
# 尝试：    会不会是错觉?绘图对象“漂浮”在网络之上


# 错误： 期待显示一四边形，只显示一半（三角形）
# 解决： 调用绘制函数 glDrawArrays时，第1个参数，传入了“GL_TRIANGLE”,应该传入“GL_TRIANGLE_STRIP”

# 错误： 期待显示一四边形，其中一半（三角形）不停闪烁
# 解决： 调用绘制函数 glDrawArrays时，第3个参数（最后一个），传入的数量比实际数量多
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

Grid_vt_src ='''
# version 330 core
layout(location = 0)in vec3 a_position;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

void main()
{
    mat4 mx = projection * view * model;
    gl_Position = mx * vec4(a_position,1.0);
}
'''
Grid_ft_src ="""
# version 330 core

void main(){
    gl_FragColor = vec4(0.5, 1.0, 1.0, 0.5);
}

"""

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
in vec3 v_color[];

out vec3 f_color;
out vec3 aNormal;

void build_cube(mat4 mx,vec4 pt)
{
    float l = pt.w;
    vec4 position = vec4(pt.xyz,1.0);
    f_color = v_color[0];

    gl_Position = mx * (position + vec4(0.0, l ,0.0,0.0));
    aNormal = vec3(0.0,0.0,-1.0);
    EmitVertex();
    gl_Position = mx * (position + vec4( l , l ,0.0,0.0));
    aNormal = vec3(0.0,0.0,-1.0);
    EmitVertex();
    gl_Position = mx * (position + vec4(0.0,0.0,0.0,0.0));
    aNormal = vec3(0.0,0.0,-1.0);
    EmitVertex();
    gl_Position = mx * (position + vec4( l ,0.0,0.0,0.0));
    aNormal = vec3(0.0,0.0,-1.0);
    EmitVertex();
    gl_Position = mx * (position + vec4( l ,0.0, l ,0.0));
    aNormal = vec3(1.0,0.0,0.0);
    EmitVertex();
    gl_Position = mx * (position + vec4( l , l ,0.0,0.0));
    aNormal = vec3(1.0,0.0,0.0);
    EmitVertex();
    gl_Position = mx * (position + vec4( l , l , l ,0.0));
    aNormal = vec3(1.0,0.0,0.0);
    EmitVertex();
    gl_Position = mx * (position + vec4(0.0, l ,0.0,0.0));
    aNormal = vec3(0.0,1.0,0.0);
    EmitVertex();
    gl_Position = mx * (position + vec4(0.0, l , l ,0.0));
    aNormal = vec3(0.0,1.0,0.0);
    EmitVertex();
    gl_Position = mx * (position + vec4(0.0,0.0,0.0,0.0));
    aNormal = vec3(-1.0,0.0,0.0);
    EmitVertex();
    gl_Position = mx * (position + vec4(0.0,0.0, l ,0.0));
    aNormal = vec3(-1.0,0.0,0.0);
    EmitVertex();
    gl_Position = mx * (position + vec4( l ,0.0, l ,0.0));
    aNormal = vec3(0.0,-1.0,0.0);
    EmitVertex();
    gl_Position = mx * (position + vec4(0.0, l , l ,0.0));
    aNormal = vec3(0.0,-1.0,0.0);
    EmitVertex();
    gl_Position = mx * (position + vec4( l , l , l ,0.0));
    aNormal = vec3(0.0,-1.0,0.0);
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
in vec3 aNormal;
in vec3 f_color;

void main(){
    vec3 lightDir = vec3(0.27,0.8,0.5);
    vec3 lightColor = vec3(1.0,1.0,1.0);

    float ambientStrength = 0.5;
    vec3 ambient = ambientStrength * lightColor;

    float diff = max(dot(aNormal, lightDir), 0.0);
    vec3 diffuse = diff * lightColor;
    vec3 result = (ambient + diffuse) * f_color;
    gl_FragColor = vec4(result, 1.0);
    //gl_FragColor = vec4(f_color, 1.0);
}
"""
def window_resize(window,width,height):
    global WIDTH,HEIGHT
    WIDTH,HEIGHT = width,height
    glViewport(0,0,width,height)

if not glfw.init():
    raise Exception("glfw can not be initialized!")

#4级抗锯齿 glfwWindowHint(GLFW_SAMPLES, 4)
glfw.window_hint(glfw.SAMPLES, 4)
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

vertices =[	0.0,	0.0,	0.0,	0.5,    1.0,	0.0,	0.0,
            0.5,	0.0,	0.0,	0.5,    1.0,	1.0,	0.0,
            0.0,	0.0,	0.5,	0.5,    0.0,	0.0,	1.0,
            0.5,	0.5,	0.5,	0.5,    0.0,	1.0,	0.0,
            0.5,	0.0,	0.5,	0.25,    0.0,	1.0,	1.0
            ]


vertices =numpy.array(vertices,numpy.float32)
#编译着色器程序
gird_shade = compileProgram(
                    compileShader(Grid_vt_src,GL_VERTEX_SHADER),
                    compileShader(Grid_ft_src,GL_FRAGMENT_SHADER))
oct_shade = compileProgram(
                    compileShader(vertex_src,GL_VERTEX_SHADER),
                    compileShader(geometry_src,GL_GEOMETRY_SHADER),
                    compileShader(fragment_src,GL_FRAGMENT_SHADER))


# Cube VAO
cube_VAO = glGenVertexArrays(1)
glBindVertexArray(cube_VAO)

VBO = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER,VBO)
glBufferData(GL_ARRAY_BUFFER,vertices.nbytes,vertices,GL_STATIC_DRAW)

glEnableVertexAttribArray(0)
glVertexAttribPointer(0,4,GL_FLOAT,GL_FALSE,28,ctypes.c_void_p(0))

glEnableVertexAttribArray(1)
glVertexAttribPointer(1,3,GL_FLOAT,GL_FALSE,28,ctypes.c_void_p(16))

# Cube VAO
grid_VAO = glGenVertexArrays(1)
glBindVertexArray(grid_VAO)

VBO = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER,VBO)
glBufferData(GL_ARRAY_BUFFER,vertices_grid.nbytes,vertices_grid,GL_STATIC_DRAW)

glEnableVertexAttribArray(0)
glVertexAttribPointer(0,3,GL_FLOAT,GL_FALSE,12,ctypes.c_void_p(0))


glClearColor(0,0.1,0.1,1)
glEnable(GL_DEPTH_TEST)
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA,GL_ONE_MINUS_SRC_ALPHA)

#the main application loop
while not glfw.window_should_close(window):
    glfw.poll_events()
    do_movement()
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

    projection = pyrr.Matrix44.perspective_projection(45,WIDTH/HEIGHT,0.5,100.0)
    view = cam.get_view_matrix()
    model = pyrr.Matrix44.identity()

    #画 网格
    glUseProgram(gird_shade)
    proj_loc = glGetUniformLocation(gird_shade,"projection")
    view_loc = glGetUniformLocation(gird_shade,"view")
    model_loc = glGetUniformLocation(gird_shade,"model")

    glUniformMatrix4fv(proj_loc,1,GL_FALSE,projection)
    glUniformMatrix4fv(view_loc,1,GL_FALSE,view)
    glUniformMatrix4fv(model_loc,1,GL_FALSE,model)
  
    glBindVertexArray(grid_VAO)
    glDrawArrays(GL_LINES,0,vertices_grid.nbytes//12)

    #画 立方体
    glUseProgram(oct_shade)
    proj_loc = glGetUniformLocation(oct_shade,"projection")
    view_loc = glGetUniformLocation(oct_shade,"view")
    model_loc = glGetUniformLocation(oct_shade,"model")

    glUniformMatrix4fv(proj_loc,1,GL_FALSE,projection)
    glUniformMatrix4fv(view_loc,1,GL_FALSE,view)
    glUniformMatrix4fv(model_loc,1,GL_FALSE,model)
    
    glBindVertexArray(cube_VAO)
    glDrawArrays(GL_POINTS,0,vertices.nbytes//28)


    glfw.swap_buffers(window)

#shotdown the application
glfw.terminate()