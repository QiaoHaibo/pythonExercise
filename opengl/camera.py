from pyrr import vector,vector3,Vector3,matrix44
from math import sin,cos,radians

class Camera:
    def __init__(self,pos = [0.0,1.0,3.0],front = [0.0,0.0,0.0],up =[0.0,1.0,0.0],right =[1.0,0.0,0.0] ):
        self.camera_pos = Vector3(pos)
        self.camera_front = Vector3(front)
        self.camera_up = Vector3(up)
        self.camera_right = Vector3(right)

        self.mouse_sensitivity = 0.25
        self.yaw = -90
        self.pitch = 0

        self.velocity = 0.02

    def get_view_matrix(self):
        return matrix44.create_look_at(self.camera_pos,self.camera_pos + self.camera_front,self.camera_up)
    def process_mouse_movement(self,xoffset,yoffset,constrain_pitch=True):
        xoffset *=self.mouse_sensitivity
        yoffset *=self.mouse_sensitivity

        self.yaw += xoffset
        self.pitch += yoffset

        if constrain_pitch:
            if self.pitch > 45:
                self.pitch = 45
            if self.pitch < -45:
                self.pitch = -45
        
        self.update_mouse_vectors()

    def update_mouse_vectors(self):
        front = Vector3([0.0,0.0,0.0])
        front.x = cos(radians(self.yaw))* cos(radians(self.pitch))
        front.y = sin(radians(self.pitch))
        front.z = sin(radians(self.yaw))*cos(radians(self.pitch))
        if not vector.squared_length(front) > 0:
            return

        self.camera_front = vector.normalise(front)
        self.camera_right = vector.normalise(vector3.cross(self.camera_front,Vector3([0,1,0])))
        self.camera_up    = vector.normalise(vector3.cross(self.camera_right,self.camera_front))

    def process_keyboard(self,direction):

        if direction =="FORWARD":
            self.camera_pos += self.camera_front * self.velocity
        if direction == "BACKWARD":
            self.camera_pos -= self.camera_front * self.velocity
        if direction == "LEFT":
            self.camera_pos -= self.camera_right * self.velocity
        if direction == "RIGHT":
            self.camera_pos += self.camera_right * self.velocity