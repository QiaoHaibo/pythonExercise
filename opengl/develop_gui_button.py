from CWindow import *
from CScene import *
from CShade import *
from CNode import *

if __name__ == '__main__':
    

    win =CWindow(683,384,"QS OpenGL Window")

    node1 = CNode()
    node1.textTexture("文件(F)")

    scene =CScene(win)
    scene.renderlist([node1])
    win.attch(scene)
    win.resize(scene.update)

    win.main_loop()