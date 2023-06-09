from ursina import *
from FirstPersonController import FirstPersonController
#--my library
from object import Player, Block, Enemies
from levels import readLevel as rl
from script import Draw


app=Ursina()

class Level():
    def __init__(self):
        self.roomEnemy =[] 
        self.playerCamera=''
        self.p=''

    #read the map
    def createMap(self,level):
        #read the map
        pathLevel='levels/'+level
        floor=rl.scanMap(pathLevel+'/floor.txt')

        z=len(floor)
        x=len(floor[0])
        self.create_floor(x,z)

        #techo=rl.scanMap(pathLevel+'/techo.txt')
        #textura_nivel=rl.scanMap(pathLevel+'/textura.txt')
        objects=rl.scanMap(pathLevel+'/objects.txt')
        #self.readArrayMap(floor,0)
        self.readArrayMap(objects,1)

    def readArrayMap(self,array,type):
        self.create_player(0,3,0)
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
            self.roomEnemy.append(Enemies.Nurse(self.p,position=(x,1,z)))
    
    def create_floor(self,x,z):
        f=Block.Voxel(position=(int(x/2),.5,int(z/2)))
        f.world_scale_z=z
        f.world_scale_x=x
        f.world_scale_y=.05
        f.model='plane'
        f.texture_scale=(x,z) 

    def create_player(self,x,y,z):
        self.playerCamera=FirstPersonController(model='sphere',collider='box',origin=(5,0,5),position=(x,y,z)) #sphere
        self.p=Player.Player(self.playerCamera,self) 

nv=Level()
nv.createMap('demo')


def input(key):
    if key=='escape':
        exit()

def updateCamera():
    camera.y=nv.p.weapon.animation.y if nv.p.weapon.star else camera.y
    if held_keys['right mouse']: #know if the player have the zoom on
       if not p.weapon.name=='hostages' and not p.fatality: #if the player not have a hostage
            camera.fov=nv.p.weapon.zoom
    else: 
        camera.fov=105 if nv.p.playingRun() else 90

def update():
    updateCamera()

app.run()
