from ursina import *
from engine.script import Draw
from engine.script import Physical
class ObjectCharacteristic(Entity):
    #------------------------------image characteristic 
    sprite_index=''
    image_index=0
    image_speed=0
    image_scale=(1,1,1)
    image_alpha=1
    image_rotation=(0,0,0)
    c_color=color.color(0,0,random.uniform(0.9,1))
    #-----------------------------programming characteristic
    block=0
    life=0
    player=None 
    weight=0
    acceleration=0
    animation=None
    
    #-----------------------------physical
    MyPhysical=True
    gravityOnEarth=.125 #/2
    gravityOnWater=gravityOnEarth/6 #6
    gravity=gravityOnEarth 

    pushForce=0
    friction=.125
    frictionX=.25 
    frictionY=.25 
    mass=0 #kg
    velocity_parabolic_mov=Vec3(0)
    myFriction=0

    timeAccelerationY=0
    vspeed=0
    hspeed=0 
    speed=0
    direction=0
    angle=0

    #maximum height
    MHvi=0
    MHvf=0

    #maximum width
    MWvi=0
    MWvf=0
    
    #water
    density=0

    #resource
    resource=False
    '''
    def __init__(self, **kwargs):
        super().__init__()
        #------------------------------image characteristic 
        self.sprite_index=''
        self.image_index=0
        self.image_speed=0
        self.image_scale=(1,1,1)
        self.image_alpha=1
        self.image_rotation=(0,0,0)
        self.c_color=color.color(0,0,random.uniform(0.9,1))
        #-----------------------------programming characteristic
        self.block=0
        self.life=0
        self.player=None 
        self.weight=0
        self.acceleration=0
        self.animation=None
        
        #-----------------------------physical
        self.MyPhysical=True
        self.gravityOnEarth=.125 #/2
        self.gravityOnWater=self.gravityOnEarth/6 #6
        self.gravity=self.gravityOnEarth 

        self.pushForce=0
        self.friction=.125

        self.timeAccelerationY=0
        self.vspeed=0
        self.hspeed=0 
        self.speed=0
        self.direction=0
        self.angle=0

        #maximum height
        self.MHvi=0
        self.MHvf=0

        #maximum width
        self.MWvi=0
        self.MWvf=0
        
        #water
        self.density=0

        #resource
        self.resource=False'''

    #---function audio 
    def audio_play_sound(self,audio,loop=False,volume=1):
        Audio(audio,loop=loop,autoplay=True).volume=volume 

    def audio_play_sound_with_distance_player(self,audio,loop=False):
        soundDistance=(  self.player.weapon.gunSight-distance(self,self.player.playerCamera)*4  ) if self.player!=None else 1
        self.audio_play_sound(audio,loop,soundDistance)

    def audio_play_sound_with_distance(self,obj1,obj2,noiseDistance,audio,loop=False):
        soundDistance=abs((noiseDistance-distance(obj1,obj2))*4)
        self.audio_play_sound(audio,loop,soundDistance)

    def physical(self):
        if self.hspeed<=0:
            if self.animation!=None:
                Physical.gravityAnimation(self)
            else:
                Physical.gravity(self)

        #parabolic movement
        
        if self.hspeed>0:
            Physical.maximumHeight(self)
        if self.vspeed>0:
            Physical.maximumWidth(self)
        
        Physical.parabolic_mov(self)



    def step(self):
        pass 

    def update(self):
        if self.MyPhysical:
            self.physical()
        self.step()



















class Object3D(ObjectCharacteristic):
    pass

class ObjectButton(ObjectCharacteristic):
    pass 

class Object2D(ObjectCharacteristic):
    pass

class Object2D3D(ObjectCharacteristic):
    sprite_rigth=''
    sprite_left=''
    sprite_up=''
    sprite_down=''

    def accomodateAngle(self,angle):
        if angle>360 or angle<-360:
            angle=angle-360*int(angle/360) if angle>360 else angle+360*int(-angle/360)
        
        angle=angle+360 if angle<0 else angle
        return angle 

    def accommodateImage(self):
        if not self.player==None:
            #acommodate angle vision and object 
            angleVision=self.accomodateAngle(self.player.playerCamera.rotation[1])
            angleObj=self.accomodateAngle(self.angle)
            angle=angleObj+angleVision

            #choose image 
            if angle>=0 and angle<=45:
                self.texture=self.sprite_rigth
            elif angle>45 and angle<=135:
                self.texture=self.sprite_up
            elif angle>135 and angle<=225:
                self.texture=self.sprite_left
            elif angle>255 and angle<=315:
                self.texture=self.sprite_down
            elif angle>315 and angle<=360:
                self.texture=self.sprite_rigth

    def update(self):
        if self.MyPhysical:
            self.physical()
        self.accommodateImage()
        self.step()

class Object2DCam(ObjectCharacteristic):
    pass 