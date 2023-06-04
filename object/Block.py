from ursina import *
from script import Objects

class Voxel(Objects.ObjectButton):
    MyPhysical=False
    block=0
    image_scale=(1,1,1)
    image_rotation = (0,0,0)
    def __init__(self,position=(0,0,0)):
        super().__init__(
            parent=scene,
            position=position,
            model='cube',
            collider='box',
            texture='white_cube',
            color=self.c_color,
            scale_x=self.image_scale[0],
            scale_y=self.image_scale[1],
            scale_z=self.image_scale[2],
        )

class Triangle(Objects.ObjectButton):
    MyPhysical=False
    block=0 
    image_scale=(.005,1.41,1) 
    image_rotation = (0,80,0)
    def __init__(self,position=(0,0,0),rotation=45):
        super().__init__(
            parent=scene,
            model='cube',
            collider='box',
            texture='white_cube',
            color=color.color(0,0,random.uniform(0.9,1)),
            world_scale_z=self.image_scale[0],
            world_scale_x=self.image_scale[1],
            world_scale_y=self.image_scale[2],
            world_rotation=(0,rotation,0),
            position=position
        )

class BrokenVoxel(Objects.ObjectButton):
    block=0
    on=False
    c_color=color.rgb(255,106,0) 
    scale=(1,1,1)
    rotation = (0,0,0)
    def __init__(self,player,position=(0,0,0)):
        super().__init__(
            parent=scene,
            position=position,
            model='cube',
            collider='box',
            texture='white_cube',
            color=self.c_color,
            highlight_color=self.c_color,
            scale_x=self.scale[0],
            scale_y=self.scale[1],
            scale_z=self.scale[2],
            rotation=self.rotation
        ),
        self.player=player
    
    def Activate(self):
        destroy(self)  

    def input(self,key):
        if self.hovered:
            if distance_2d(self,self.player.playerCamera)<3 and key=='e' and not self.on:#see if the player the hit
                self.on=True 
                self.Activate() 

class Switches(BrokenVoxel):
    c_color=color.color(0,140,255)
    c_colorOn=color.color(95,239,95)

    def Activate(self):
        self.color=self.c_colorOn
        self.highlight_color=self.color

    def input(self,key):
        if distance_2d(self,self.player.playerCamera)<4 and key=='e' and not self.on:#see if the player the hit
            self.on=True 
            self.Activate()

class SwitchWithTime(Switches):
    time=30*20
    alarm=[time]

    def deactivate(self):
        self.color=self.c_color
        self.highlight_color=self.color
        self.on=False
        self.alarm[0]=self.time 
        
    def Activate(self):
        self.color=self.c_colorOn
        self.highlight_color=self.color

    def update(self):
        if self.on:
            if self.alarm[0]>0:
                self.alarm[0]-=1
            else:
                self.deactivate()

class Conduits(Objects.Object3D):
    MyPhysical=False
    block=0
    image_scale=(1,1,1)
    image_rotation = (0,0,0)
    #c_color=color.rgba(0,148,255,174)
    c_color=color.rgb(0,0,0)
    def __init__(self,position=(0,0,0)):
        super().__init__(
            parent=scene,
            position=position,
            model='cube',
            collider='box',
            texture='white_cube',
            color=self.c_color,
            scale_x=self.image_scale[0],
            scale_y=self.image_scale[1],
            scale_z=self.image_scale[2],
        )

class Water(Objects.Object3D):
    density=.1 

    MyPhysical=False
    block=0
    image_scale=(1,1,1)
    image_rotation = (0,0,0)
    c_color=color.rgba(0,148,255,100)  #alcantarilla (0,163,33,255) #acido (0,255,33,255) #lava (255,0,0,255) #agua contaminada (0,127,14,100)  # whater (0,148,255,100) 
    sprite_index='sprite/block/water.png'
    def __init__(self,position=(0,0,0)):
        super().__init__(
            parent=scene,
            position=position,
            model='cube',
            collider='box',
            texture=self.sprite_index,
            color=self.c_color,
            scale_x=self.image_scale[0],
            scale_y=self.image_scale[1],
            scale_z=self.image_scale[2],
        ) 

#----------block game
class Chair(Objects.Object2D3D):
    scale=(1,1,1)
    sprite_rigth='sprite/object/chair/chair_rigth.png'
    sprite_left='sprite/object/chair/chair_left.png'
    sprite_up='sprite/object/chair/chair_up.png'
    sprite_down='sprite/object/chair/chair_down.png'
    def __init__(self,player,position=(0,0,0)):
        super().__init__(
            parent=scene,
            position=position,
            model='cube',
            collider='box',
            texture='white_cube',
            color=self.c_color,
            highlight_color=self.c_color,
            scale_x=self.scale[0],
            scale_y=self.scale[1],
            scale_z=self.scale[2],
        ),
        self.player=player 

    def step(self):
        Objects.Physical.push(self,self.player.playerCamera,2)
        self.rotation=self.player.playerCamera.rotation

class Elevator(Switches):
    yStar=0
    xStar=0
    pass

class Barrel(Objects.ObjectButton):
    sprite_index='sprite/object/barrel/barrel.png'
    scale=(1,1.5,1)
    life=1
    '''
    scale_x=self.scale[0],
    scale_y=self.scale[1],
    scale_z=self.scale[2],'''
    def __init__(self,player,position=(0,0,0)):
        super().__init__(
            parent=scene,
            texture=self.sprite_index,
            position=position,
            model='cube',
            collider='box',
            color=self.c_color,
            highlight_color=self.c_color,
            world_scale_z=self.scale[2],
            world_scale_x=self.scale[0],
            world_scale_y=self.scale[1],
            origin_y=-.2
        ),
        self.player=player 

    def input(self,key):
        if self.hovered: #see if the player is targeting it
            if key=='left mouse down':#see if the player Shooting 
                if self.thePlayerCanShoot():# know if the player can shooting
                    self.life-=self.player.weapon.weaponDamage
                    #self.audio_play_sound_with_distance_player(self.audioWound)
    
    def thePlayerCanShoot(self):
        return distance_2d(self,self.player.playerCamera)<self.player.weapon.gunSight and self.player.weapon.ammunition>0 and self.player.weapon.recharge

    def step(self):
        Objects.Physical.push(self,self.player.playerCamera,2)
        self.rotation=self.player.playerCamera.rotation


