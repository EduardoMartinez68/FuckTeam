from ursina import *
from script import Objects, Draw
import random 
class Weapon(Objects.Object2DCam):
    #character for weapon
    star=False
    weapon=0
    gunSight=10 #mira del arma 
    ammunition=10 #municion 
    weaponDamage=1
    weight=1 #1, 1.5, 2
    height=.4
    zoom=80

    #
    recharge=True
    alarm=[30]

    #texture and design
    position=Vec2(0,0)
    sprite_index='sprite/Weapon/Shotgun/shotgun'
    image_index=0
    image_speed=15
    image_scale=(1,1,1)
    sprite_index_zoom='sprite/Weapon/Shotgun/shotgun'
    audio='audio/weapon/shotgun.wav'
    
    #animation 
    heigthMov=.3
    heigthStop=.12 #.15
    animationSpeed=.5/weight
    animationSpeedStop=.5/weight
    frameAnimation=0

    #--------------------create animation of strop 
    frameAnimationStop=0
    stepAnimationStopY=[]
    n=8
    for i in range(n):
        num=i/100
        stepAnimationStopY.append(num-heigthStop)
        stepAnimationStopY.append(num+.005-heigthStop)
    for i in range(n):
        num=(n-i)/100
        stepAnimationStopY.append(num+.005-heigthStop)
        stepAnimationStopY.append(num-heigthStop)

    #create animation of mov 
    numFrame=4
    stepAnimationMovX=[]
    for i in range(numFrame): 
        num=i/10
        stepAnimationMovX.append(num)
        stepAnimationMovX.append(num+.05)
    for i in range(numFrame): 
        num=(numFrame-i)/10
        stepAnimationMovX.append(num+.05)
        stepAnimationMovX.append(num)
    for i in range(numFrame): 
        num=-i/10
        stepAnimationMovX.append(num)
        stepAnimationMovX.append(num-.05)
    for i in range(numFrame): 
        num=(-numFrame+i)/10
        stepAnimationMovX.append(num-.05)
        stepAnimationMovX.append(num) 


    stepAnimationMovY=[]
    for i in stepAnimationMovX:
        stepAnimationMovY.append(i**2-heigthMov)

    def __init__(self,player,enemy=None,**kwargs):
        super().__init__(
            player=player,
            enemy=enemy,
            animation=Animation(
                            self.sprite_index,
                            parent=camera.ui,
                            position=self.position,
                            scale=self.image_scale,
                            fps=self.image_speed,
                            loop=False,
                            autoplay=True
                            )
        )

    #-------------------------------shooter---------------------------    
    def input(self,key):
        if key=='left mouse down' and self.recharge and not self.player.fatality: 
            self.animation.start() 
            self.recharge=False
            Audio(self.audio,loop=False,autoplay=True).volume=.5
            
            #create a bullet damage
            BulletDamage(self.player,position=self.player.playerCamera.camera_pivot.world_position,rotation=self.player.playerCamera.camera_pivot.world_rotation)

        if key=='e':
            self.pickUpTheWeapon()

    def rayCastingBullet(self):
        #get the coordinate of the player
        origin=self.player.playerCamera[0].camera_pivot.world_position
        positionBeam=origin
        direction=self.player.playerCamera[0].camera_pivot.world_rotation
        aux=.5
        beamDistance=aux
        #move the beam
        while beamDistance<self.gunSight:
            #use raycasting for see if the beam collision with the well
            hit_info=raycast(origin,direction,ignore=(self,),distance=beamDistance,debug=False)
            if not hit_info.hit:
                beamDistance+=aux
                positionBeam+=direction*beamDistance
            else:
                BulletDamage(self.player,position=positionBeam,rotation=self.player.playerCamera[0].camera_pivot.world_rotation)
                break

    def updateScaleForZoom(self):
        if not self.player.fatality:
            if held_keys['right mouse']: #know if the player have the zoom on
                self.animation.scale=(self.image_scale[0]*2,self.image_scale[1]*2,self.image_scale[2]*2)
                #self.animation.texture=self.sprite_index_zoom
            else:
                self.animation.scale=(self.image_scale[0],self.image_scale[1],self.image_scale[2])
                #self.animation.texture=self.sprite_index
    
    def pickUpTheWeapon(self):
        self.animation.visible=True
        self.star=False

    #------------gun animation---------------------------------------------------
    def thePlayerIsMoving(self):
        return held_keys['a'] or held_keys['d'] or held_keys['w'] or held_keys['s']

    def animationOfWeapon(self):
        #see if the player is moving or is shooting up
        if self.thePlayerIsMoving() and self.recharge and not self.player.fatality:
            self.animationInMov()
        else:
            self.animation.x=0
             #will see if the player is shooting for decide that will be doing
            if not self.recharge:
                self.animation.y=0
            else:
                self.animacionManoQuieta()
    
    def animationInMov(self):
        #we will if the user actived the inventary 
        if self.player.openInventory:
            animationSpeed=self.animationSpeed/3 #this is so that the weapon is at the same speed as the player
        else:
            animationSpeed=self.animationSpeed*2 if held_keys['shift'] else self.animationSpeed #this is so that the weapon is at the same speed as the player
        
        self.frameAnimation+=animationSpeed if len(self.stepAnimationMovX)-1>self.frameAnimation else -self.frameAnimation #so that the animation does not pace 
        #we place the weapon in the corresponding coordinates
        i=int(self.frameAnimation)
        self.animation.x=self.stepAnimationMovX[i]
        self.animation.y=self.stepAnimationMovY[i]

    def animacionManoQuieta(self):
        self.frameAnimationStop+=self.animationSpeedStop if len(self.stepAnimationStopY)-1>self.frameAnimationStop else -self.frameAnimationStop 
        i=int(self.frameAnimationStop)
        self.animation.y=self.stepAnimationStopY[i] 

    def animationPickUpTheWeapon(self):
        #we will see if the weapon is visible 
        if self.animation.visible:
            #we'll raise the gun
            if self.animation.y<self.stepAnimationStopY[0]:
                self.animation.y+=.05
            else:
                #activate the weapon 
                self.star=True 
                self.recharge=True
                self.animation.y=self.stepAnimationStopY[0]
        else:
            self.recharge=True
            self.animation.y=self.stepAnimationStopY[0]-self.height

    #-----------------------------------------------------------------------------
    def update(self):
        if self.star:
            self.animationOfWeapon()
            self.updateScaleForZoom()
            if self.recharge==False:
                if self.alarm[0]>0:
                    self.alarm[0]-=1
                else:
                    self.alarm[0]=30
                    self.recharge=True

            #camera rotation 
            self.animation.rotation_z=self.player.playerCamera.camera_pivot.rotation_z*2
        else:
            self.animationPickUpTheWeapon()

class StartingHands(Weapon):
    sprite_index='sprite/Weapon/starting_hands/manos'
    alarm=[30,40]

    def input(self,key):
        pass 

    def update(self):
        #---old character
        self.animationOfWeapon()
        self.updateScaleForZoom()
        if self.recharge==False:
            if self.alarm[0]>0:
                self.alarm[0]-=1
            else:
                self.alarm[0]=30
                self.recharge=True 

        #----new character
        if self.alarm[1]>0:
            self.alarm[1]-=1
        else:
            self.player.weapon=Gun(self.player)
            self.player.weapon.animation.visible=True
            destroy(self)
        
class Gun(Weapon):
    sprite_index='sprite/Weapon/gun/gun'
    sprite_index_zoom='sprite/Weapon/gun/gun'
    audio='audio/weapon/shotgun.wav'

    #character for weapon
    weapon=1
    gunSight=30 #mira del arma 
    ammunition=10 #municion 
    weaponDamage=.5
    weight=1 #1, 1.5, 2
    height=.4
    zoom=85 #francotirador

    #
    recharge=True
    alarm=[15]

    
    #animation 
    heigthMov=.3
    heigthStop=.09 #.15
    animationSpeed=.5/weight
    animationSpeedStop=.5/weight
    frameAnimation=0

    #--------------------create animation of strop 
    frameAnimationStop=0
    stepAnimationStopY=[]
    n=8
    for i in range(n):
        num=i/100
        stepAnimationStopY.append(num-heigthStop)
        stepAnimationStopY.append(num+.005-heigthStop)
    for i in range(n):
        num=(n-i)/100
        stepAnimationStopY.append(num+.005-heigthStop)
        stepAnimationStopY.append(num-heigthStop)

    #create animation of mov 
    numFrame=4
    stepAnimationMovX=[]
    stepAnimationMovY=[]
    for i in range(numFrame): 
        num=i/10
        stepAnimationMovX.append(num)
        stepAnimationMovX.append(num+.05)
    for i in range(numFrame): 
        num=(numFrame-i)/10
        stepAnimationMovX.append(num+.05)
        stepAnimationMovX.append(num)
    for i in range(numFrame): 
        num=-i/10
        stepAnimationMovX.append(num)
        stepAnimationMovX.append(num-.05)
    for i in range(numFrame): 
        num=(-numFrame+i)/10
        stepAnimationMovX.append(num-.05)
        stepAnimationMovX.append(num) 
    for i in stepAnimationMovX:
        stepAnimationMovY.append(i**2-heigthMov)

class Shongunt(Weapon):
    sprite_index='sprite/Weapon/Shotgun/shotgun'  

class Hostages(Weapon):
    sprite_index='sprite/Weapon/hostages/weapon/E'
    sprite_index_zoom='sprite/Weapon/hostages/weapon/E'
    sprite_hostages='sprite/Weapon/hostages/nurse/nurse.png'

    enemyLife=10

    def animationEnemy(self):
        enemyX,enemyY,enemyZ=self.animation.position[0],self.animation.position[1],self.animation.position[2]
        self.enemy.position=(enemyX-.4,enemyY-.5,enemyZ)

        #know if the player threw the enemy
        if held_keys['right mouse']:
            self.launchObject()
            self.enemyLife=0
            destroy(self.enemy)

    def launchObject(self):
        obj=ThrownEnemy(self.player,position=self.player.playerCamera.camera_pivot.world_position,rotation=self.player.playerCamera.camera_pivot.world_rotation)
        obj.visible=True
        obj.angle=self.player.playerCamera.camera_pivot.world_rotation[0]
        obj.MHvi=5 #5 #launch force (1=90)
        Objects.Physical.parabolicMovement(obj)

    def update(self):
        #----------------old event
        self.animationOfWeapon()
        self.updateScaleForZoom()
        if self.recharge==False:
            if self.alarm[0]>0:
                self.alarm[0]-=1
            else:
                self.alarm[0]=30
                self.recharge=True 

        #-----------------new event
        if self.enemyLife>0:
            self.animationEnemy()

class FatalityEnemy(Weapon):
    sprite_index='sprite/Weapon/patadas/patada' 

class FatalityEnemy1(Weapon):
    sprite_index='sprite/Weapon/Shotgun/shotgun'  

#--------
class BulletDamage(Objects.Object2D):
    MyPhysical=False
    run=True
    sprite_blood=['sprite/Weapon/damage/damage1.png',
                'sprite/Weapon/damage/damage2.png',
                'sprite/Weapon/damage/damage3.png',
                'sprite/Weapon/damage/damage1.png',
                'sprite/Weapon/damage/damage2.png']

    sprite_wall=['sprite/Weapon/damage/damage6.png',
                'sprite/Weapon/damage/damage7.png',
                'sprite/Weapon/damage/damage8.png',
                'sprite/Weapon/damage/damage9.png',
                'sprite/Weapon/damage/damage10.png']
    
    image_scale=(.3,.3,.3) #.3
    speed=60
    timeAlarm=1
    alarm=[1]

    particles=True 
    numParticle=0
    colorParticle=(0,0,0)

    def __init__(self,player,position=(0,0),rotation=(0,0,0),**kwargs):
        super().__init__(
            parent=scene,
            texture=self.sprite_wall[0],
            position=position,
            model='quad',
            Collider='box',
            scale=self.image_scale,
            world_scale_z=self.image_scale[0],
            world_scale_x=self.image_scale[1],
            world_scale_y=self.image_scale[2],
            rotation=rotation,
            visible=False
        ),
        self.forwardData=self.forward
        self.player=player

    def chooseSkin(self,type):

        #choose the sprite 
        if type==0: #wall
            self.texture=self.sprite_wall[random.randint(0,4)]
            self.timeAlarm=16
            self.alarm=[self.timeAlarm]
            self.colorParticle=color.color(255,0,0) 
            self.numParticle=random.randint(4,10)
        else: #blood
            self.texture=self.sprite_blood[random.randint(0,4)]
            self.timeAlarm=.5
            self.alarm=[self.timeAlarm]    
            self.colorParticle=color.color(0,140,255)
            self.numParticle=random.randint(10,15)

        #set the direction 
        self.rotation=(0,self.player.playerCamera.rotation[1],0)
              
    def createParticle(self):
        for i in range(self.numParticle):
            MoveX=random.randint(-2,2)/50
            MoveZ=random.randint(-2,2)/50
            MoveY=random.randint(-2,0)/100
            Particles(self.position,MoveX,MoveZ,MoveY,self.colorParticle)

    def moveBullet(self,world_position,forward):
        #move the bullet
        ray=raycast(world_position,forward,distance=.35,ignore=(self,self.player,))
        if not ray.hit:
            world_position+=forward*self.speed*time.dt
        else:
            self.chooseSkin(ray.entity.block)
            self.visible=True 
            self.run=False #exit loop

    def seeTheDistance(self,world_position):
        #if the bullet did not collide the object will be destroing  
        dist=self.player.gunSight
        x,y,z=abs(world_position[0]),abs(world_position[1]),abs(world_position[2])
        x2,y2,z2=abs(self.player.playerCamera.position[0])+dist,abs(self.player.playerCamera.position[1])+dist,abs(self.player.playerCamera.position[2])+dist
        
        #we will see if the bullet if about of the limit 
        if x>x2 or y>y2 or z>z2:
            self.run=False
    
    def destruction(self):
        if self.alarm[0]>0:
            self.alarm[0]-=time.dt
            self.alpha-=.005
        else:
            self.visible=False
            self.alarm[0]=self.timeAlarm
            destroy(self)

    def step(self):
        #get the data
        world_position=self.world_position
        forward=self.forward

        #move the bullet with a loop until it crash
        while self.run:
            self.world_position=world_position
            self.moveBullet(world_position,forward)
            self.seeTheDistance(world_position) #for that the bullet self destruction and get out of the loop
        
        #create particles if the bullet collision 
        if self.particles and self.visible:
            self.particles=False
            self.createParticle()

        #if the bullet collision star the self destruction
        self.destruction()

class ThrownEnemy(BulletDamage):
    MyPhysical=True
    colorParticle=color.rgb(0,0,255)
    vspeed=10
    image_scale=(1,2,2)
    sprite_wall=[
        'sprite/enemy/thrown/nurse.png',
    ]
    rep=2

    def createParticle(self):
        for i in range(40):
            MoveX=random.randint(-6,6)/50
            MoveZ=random.randint(-6,6)/50
            MoveY=random.randint(-4,0)/100
            Particles(self.position,MoveX,MoveZ,MoveY,self.colorParticle)
        
    def step(self):
        self.visible=True
        self.rotation=(0,self.player.playerCamera.rotation[1],0)

        hit_info=self.intersects()
        if hit_info.hit:
            self.vspeed=0
            self.hspeed=0
            self.createParticle()
            destroy(self)
        
class Particles(Objects.Object3D):
    MyPhysical=False
    def __init__(self,position=(0,0,0),moveX=0,moveY=0,moveZ=0,c_color=(0,0,0),**kwargs):
        super().__init__(
            parent=scene,
            texture='white_cube',
            position=position,
            model='cube',
            Collider='box',
            scale=.05,
            color=c_color
        ),
        self.moveX=moveX,
        self.moveY=moveY,
        self.moveZ=moveZ,


    def update(self):
        self.x+=self.moveX[0]
        self.z+=self.moveZ[0]
        self.y+=self.moveY[0]
        self.scale-=.0015
        self.alpha-=.005
        if self.scale<=.005:
            destroy(self)
