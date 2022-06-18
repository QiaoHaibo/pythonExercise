import glfw

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

#the main application loop
while not glfw.window_should_close(window):
    glfw.poll_events()
    glfw.swap_buffers(window)

#shotdown the application
glfw.terminate()


