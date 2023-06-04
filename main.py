from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
#--my libreary
from object import Player, Block, Enemies
from levels import readLevel as rl
from script import Draw


app=Ursina()
#we will create a player
playerCamera=FirstPersonController(model='sphere',collider='box',origin=(5,0,5),position=(0,3,0)) #sphere
p=Player.Player(playerCamera)
camera.z=-5
class Level():
    def __init__(self):
        pass 

    #read the map
    def createMap(self,level):
        #read the map
        pathLevel='levels/'+level
        floor=rl.scanMap(pathLevel+'/floor.txt')

        z=len(floor)
        x=len(floor[0])
        f=Block.Voxel(position=(int(x/2),.5,int(z/2)))
        f.world_scale_z=z
        f.world_scale_x=x
        f.world_scale_y=.05
        f.model='plane'
        f.texture_scale=(x,z)
        #techo=rl.scanMap(pathLevel+'/techo.txt')
        #textura_nivel=rl.scanMap(pathLevel+'/textura.txt')
        objects=rl.scanMap(pathLevel+'/objects.txt')
        #self.readArrayMap(floor,0)
        self.readArrayMap(objects,1)

    def readArrayMap(self,array,type):
        for z in range(len(array)):
            for x in range(len(array[z])):
                num=array[z][x]
                if type==0:
                    self.createFloor(num,x,z)
                elif type==1:
                    self.createObjects(num,x,z)

    def createFloor(self,num,x,z): 
        if num==0:
            Block.Voxel(position=(x,0,z)) 

    def createObjects(self,num,x,z):
        if num==1: #wall
            Block.Voxel(position=(x,1,z))  
            for i in range(3): Block.Voxel(position=(x,i+1,z))  
        elif num==2:
            Block.Triangle(position=(x+0.0026,1,z),rotation=135) 
            for i in range(3): Block.Triangle(position=(x+0.0026,i+1,z),rotation=135) 
        elif num==3:
            Block.Triangle(position=(x+0.0026,1,z)) 
            for i in range(3): Block.Triangle(position=(x+0.0026,i+1,z)) 
        elif num==4:
            Enemies.Enemy(p,position=(x,1,z))

nv=Level()
nv.createMap('demo')
Block.BrokenVoxel(p,position=(4,1,8))
Block.Switches(p,position=(5,1,8))
Block.SwitchWithTime(p,position=(7,1,8))
e=Enemies.Nurse(p,position=(4,1,5))
Block.Barrel(p,position=(4,3,5))

#Enemies.Nurse(p,position=(5,50,7))

'''
for i in range(3):
    Block.Water(position=(4,i+1,6))
    Block.Water(position=(5,i+1,6))
    Block.Water(position=(6,i+1,6))
    Block.Water(position=(4,i+1,7))
    Block.Water(position=(5,i+1,7))
    Block.Water(position=(6,i+1,7))
'''

def input(key):
    if key=='escape':
        exit()

def updateCamera():
    camera.y=p.weapon.animation.y if p.weapon.star else camera.y
    if held_keys['right mouse']: #know if the player have the zoom on
       if not p.weapon.name=='hostages': #if the player not have a hostage
            camera.fov=p.weapon.zoom
    else: 
        camera.fov=105 if p.playingRun() else 90

def update():
    updateCamera()

app.run()
