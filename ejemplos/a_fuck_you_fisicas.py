from ursina import *
import math

app = Ursina(size=(1280,720))

physics_entities = []

def get_flight_time(vi,g):
    return (2*vi)/g

def get_acceleration(f,m):
    return f/m 

def get_final_height(vi,g,angle):
    return ((vi**2)*sin(angle**2))/(2*g)

def get_final_x(vi,angle):
    angle= 360-angle if angle>0 else angle*-1
    angle=math.radians(angle)
    return abs(vi*cos(angle))*2
    #return abs(vi*cos(angle))*1.75

def get_dh(vo,angle,g):
    ov=37.5
    if abs(angle)<ov:
        #angle=90-angle if angle>0 else 90+angle 
        return 1
    else:
        angle=90-angle if angle>0 else angle*-1#90+angle 

    angle=math.radians(angle)
    return ((vo**2)*(sin(2*angle)))/g

class PhysicsEntity(Entity):
    vspeed=0
    hspeed=1.4
    gravity=.098
    friction=.25 #.25
    mass=10

    vi=2#get_acceleration(20,mass)
    def __init__(self, model='cube', collider='box', **kwargs):
        super().__init__(model=model, collider=collider, **kwargs)
        physics_entities.append(self)
        

    def update(self):
        if self.intersects():
            self.stop()
            return
        self.velocity = lerp(self.velocity, Vec3(0), time.dt) #*self.hspeed
        self.velocity += Vec3(0,-1,0) * time.dt * self.gravity
        self.position += (self.velocity + Vec3(0,-self.vspeed,0)) * time.dt #-4

        #we will aument the vspeed
        self.vspeed+=self.gravity

        if self.hspeed>1:
            self.hspeed-=self.friction
        else:
            self.hspeed=1

    def calculate_acceleration(self,force):
        self.hspeed=force/self.mass 

    def stop(self):
        self.velocity = Vec3(0,0,0)
        if self in physics_entities:
            physics_entities.remove(self)

    def on_destroy(self):
        self.stop()


    def throw(self, direction, force):
        pass

from ursina.shaders import lit_with_shadows_shader
Entity.default_shader = lit_with_shadows_shader
DirectionalLight().look_at(Vec3(1,-1,-1))

ground = Entity(model='plane', scale=32, texture='white_cube', texture_scale=Vec2(32), collider='box')

from ursina.prefabs.first_person_controller import FirstPersonController
player = FirstPersonController()

def input(key):
    if key == 'left mouse down':
        #e = PhysicsEntity(model='cube', color=color.azure, velocity=Vec3(0), position=player.position+Vec3(0,1.5,0)+player.forward, collider='sphere')
        e = PhysicsEntity(model='cube', color=color.azure, velocity=Vec3(0), position=player.position+Vec3(0,1.5,0)+player.forward, collider='sphere')
        #e.hspeed=get_dh(1,camera.world_rotation_x,0.98)
        e.velocity = (camera.forward + Vec3(0,0,0)) * get_acceleration(4008,34)

    if key=='escape':
        exit()

def update():
    #camera.world_rotation_x+=1
    #camera.world_rotation_y+=1
    #print(camera.world_rotation_x)
    pass 
Sky()
app.run()
