from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram,compileShader
from PIL import Image
from CText import CText
import numpy
import pyrr

class CNode:
    vertex_src ='''
    # version 330 core
    layout(location = 0)in vec2 a_position;
    layout(location = 1)in vec2 a_texture;
    out vec2 v_texture; 
    uniform mat4 ortho;
    uniform mat4 model;

    void main()
    {
        gl_Position = ortho*model*vec4(a_position,0.0,1.0);
        v_texture = a_texture;
    }
    '''
    fragment_src ="""
    # version 330 core

    out vec4 out_color;
    in vec2 v_texture;
    uniform sampler2D s_texture; 
    uniform vec4 text_color;
    void main(){
        out_color = texture(s_texture,v_texture)*text_color;
    }

    """
    def __init__(self):
        offsetX = -0.5
        offsetY = -0.5
        width = 1
        height = 1

        self.vertices =[
            offsetX,            offsetY+height, 0.0,    1.0,
            offsetX+width,      offsetY+height, 1.0,    1.0,
            offsetX,            offsetY,        0.0,    0.0,
            offsetX+width,      offsetY,        1.0,    0.0  ]
        self.vertices =numpy.array(self.vertices,numpy.float32)

        self.shade = compileProgram(compileShader(self.vertex_src,GL_VERTEX_SHADER),
        compileShader(self.fragment_src,GL_FRAGMENT_SHADER))
        self.VBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER,self.VBO)
        glBufferData(GL_ARRAY_BUFFER,self.vertices.nbytes,self.vertices,GL_STATIC_DRAW)

        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0,2,GL_FLOAT,GL_FALSE,16,ctypes.c_void_p(0))

        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1,2,GL_FLOAT,GL_FALSE,16,ctypes.c_void_p(8))

        self.model_loc = glGetUniformLocation(self.shade, "model")
        self.textcolor = glGetUniformLocation(self.shade, "text_color")

        self.texture('./textures/buttons_PNG60.png')

    def texture(self,imagepath:str):
        #加载贴图
        self.bg_texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D,self.bg_texture)
        glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_WRAP_S,GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_WRAP_T,GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_LINEAR)
        #加载IMAGE
        image = Image.open(imagepath)
        #image = image.transpose(Image.FLIP_TOP_BOTTOM)
        img_data = image.convert("RGBA").tobytes()
        glTexImage2D(GL_TEXTURE_2D,0,GL_RGBA,image.width,image.height,0,GL_RGBA,GL_UNSIGNED_BYTE,img_data)

        glUseProgram(self.shade)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA,GL_ONE_MINUS_SRC_ALPHA)

    def textTexture(self,text:str):
        #加载贴图
        self.text_texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D,self.text_texture)
        glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_WRAP_S,GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_WRAP_T,GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_LINEAR)
        #加载IMAGE
        image = CText(text,12).image
        self.image_width = image.width
        self.image_height = image.height
        #image = image.transpose(Image.FLIP_TOP_BOTTOM)
        img_data = numpy.array(image)
        img_data =  img_data.repeat(4)

        glTexImage2D(GL_TEXTURE_2D,0,GL_RGBA,image.width,image.height,0,GL_RGBA,GL_UNSIGNED_BYTE,img_data)

        glUseProgram(self.shade)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA,GL_ONE_MINUS_SRC_ALPHA)
    def draw(self):

        mt_model = pyrr.matrix44.create_from_scale(pyrr.Vector3([self.image_width*2,self.image_height*2,1.0]))
        mt_model = mt_model @ pyrr.matrix44.create_from_translation(pyrr.Vector3([50.0,50.0,0.0]))
        glUniformMatrix4fv(self.model_loc, 1, GL_FALSE, mt_model)
        glUniform4f(self.textcolor, 1.0,1.0,1.0,1.0)
        glBindTexture(GL_TEXTURE_2D,self.bg_texture)
        glDrawArrays(GL_TRIANGLE_STRIP,0,4)

        mt_model = pyrr.matrix44.create_from_scale(pyrr.Vector3([self.image_width,self.image_height,1.0]))
        mt_model = mt_model @ pyrr.matrix44.create_from_translation(pyrr.Vector3([50.0,50.0,0.0]))
        glUniformMatrix4fv(self.model_loc, 1, GL_FALSE, mt_model)
        glUniform4f(self.textcolor, 1.0,1.0,1.0,1.0)
        glBindTexture(GL_TEXTURE_2D,self.text_texture)
        glDrawArrays(GL_TRIANGLE_STRIP,0,4)