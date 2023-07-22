from ursina import * 
from engine.script import PhysicalWater as pw

import math

def gravity2(self):
    height=self.scale[1]/2
    ray = raycast(self.world_position, self.down, ignore=(self,self.animation),distance=height+self.gravity,debug=False)
    if not ray.hit:
        self.vspeed+=self.gravity

        velocityX=Vec3(0)
        velocityX+=Vec3(0,-1,0) * time.dt * self.gravity
        self.position += (velocityX + Vec3(0,-self.vspeed,0)) * time.dt
    else:
        self.velocity = Vec3(0,0,0)

def gravity(self):
    height=self.scale[1]/2 #get the height of the object
    aceleration=self.gravity*self.timeAccelerationY
    # we will see if down of the object exits a wall
    ray = raycast(self.world_position, self.down, ignore=(self,self.animation),distance=height+self.gravity,debug=False)
    if not ray.hit:
        self.y-=aceleration
        self.timeAccelerationY+= .11 if self.timeAccelerationY<6 else 0
    else:  
        if ray.entities[0].name=='water':
            self.gravity=self.gravityOnWater
            self.animation.y-=aceleration
        if self.vspeed>0:
            self.vspeed-=self.friction

def gravityAnimation(self):
    height=self.animation.scale[1]/4 #get the height of the object
    aceleration=self.gravity*self.timeAccelerationY
    # we will see if down of the object exits a wall
    ray = raycast(self.animation.world_position, self.animation.down, ignore=(self,self.animation,),distance=height+aceleration,debug=False)
    if not ray.hit:
        self.animation.y-=aceleration
        self.timeAccelerationY+= .11 if self.timeAccelerationY<6 else 0
    else:  
        if ray.entities[0].name=='water':
            #self.timeAccelerationY-=.11 if self.timeAccelerationY>=6 else 0
            self.gravity=self.gravityOnWater
            self.animation.y-=aceleration
        else:
            self.timeAccelerationY=1
            self.gravity=self.gravityOnEarth
         
        if self.vspeed>0:
            self.vspeed-=self.friction

def freefall(self):
    pass

def push(self,objeto,range_collision):
    distance_object=distance(self,objeto)
    if distance_object<range_collision:
        self.pushForce=objeto.acceleration*objeto.weight #7

    if self.pushForce>0:
        #we will watche the direction of the camera
        self.direction=Vec3(
            self.forward
        ).normalized()

        #origin of the lightning
        origin=self.world_position #-self.up #(self.up*.5)

        #we will create the lightning
        hit_info=raycast(origin,self.direction,ignore=(self,),distance=1)

        #if the lightning not collision well we wwill move the object 
        if not hit_info.hit:
            self.position+=self.direction*time.dt*self.pushForce
            self.pushForce-=self.friction 
        else:
            self.position-=self.direction*time.dt*self.pushForce*2
            self.pushForce=0

#---parabolic movement
def accommodateForce(self):
    space=10
    if self.angle<=-90+space and self.angle>=-90-space:
        self.MHvi=2.25

def parabolicMovement(self):
    accommodateForce(self)
    getMaximumWidth(self)
    getMaximumHeight(self)

def getMaximumWidth(self):
    #xMax={ [vo^2][sen(2*angle)] }/g
    angle=math.radians(self.angle)
    self.vspeed=-((self.MHvi**2)*(math.sin(2*angle)))/self.gravity

def getMaximumHeight(self):
    #hMax={ [vo^2][sen^2(angle)] }/2g
    angle=math.radians(self.angle)
    self.hspeed=((self.MHvi**2)*(math.sin(angle)**2))/(2*self.gravity)
    self.hspeed=(self.y+self.hspeed)

def maximumHeight(self):
    #move the object 
    ray=raycast(self.world_position,self.forwardData,distance=.5,ignore=(self,self.player,))
    if not ray.hit:
        self.world_position+=(0,self.forwardData[1],0)
        self.hspeed-=1
    else:
        self.hspeed=0

def maximumWidth(self):
    #move the object 
    ray=raycast(self.world_position,self.forwardData,distance=.5,ignore=(self,self.player,))
    if not ray.hit:
        self.world_position+=(self.forwardData[0],0,self.forwardData[2])
        self.vspeed-=1
    else:
        self.vspeed=0

#-----------new
def get_acceleration(f,m):
    return f/m 

def get_final_height(vi,g,angle):
    return ((vi**2)*sin(angle**2))/(2*g)

def get_final_x(vi,angle):
    angle= 360-angle if angle>0 else angle*-1
    angle=math.radians(angle)
    return abs(vi*cos(angle))*2
    #return abs(vi*cos(angle))*1.75

def get_maximum_width(vo,angle,g):
    ov=37.5
    if abs(angle)<ov:
        #angle=90-angle if angle>0 else 90+angle 
        return 1
    else:
        angle=90-angle if angle>0 else angle*-1#90+angle 

    angle=math.radians(angle)
    return ((vo**2)*(sin(2*angle)))/g

def parabolic_mov(self):
    #we will watch if the object is collision with other object
    hit_info=self.intersects()
    if hit_info:
        self.velocity = Vec3(0,0,0)
        return
    
    #if the object not is collision so we will create a parabolic mov
    self.velocity_parabolic_mov = lerp(self.velocity_parabolic_mov, Vec3(0), time.dt)
    self.velocity_parabolic_mov -= lerp(self.velocity_parabolic_mov, Vec3(0), time.dt)*self.hspeed
    self.position += (self.velocity_parabolic_mov) * time.dt

    



#----water
def gravityWater(self):
  #intersect with Conduits
        hit_info=self.intersects()
        if not hit_info.entity==None:
            if hit_info.entities[0].name=='water':
                self.gravity=self.gravityOnWater
        else:
            self.gravity=self.gravityOnEarth

def buoyancyEffect(self):
    #pF=
    #vS submerged volume 
    # g=gravity
    pass