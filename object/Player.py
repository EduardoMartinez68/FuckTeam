from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from object import Weapon 
from script import Objects, Draw

class Player(Objects.Object3D):
    sprite_interface='interface/interface'

    #hability
    pause=False
    openInventory=False
    godPunch=False
    climb=False
    climbYStar=0

    #character for weapon
    weapon=0
    gunSight=10 #mira del arma 
    ammunition=10 #municion 
    weaponDamage=1
    recharge=True

    #physical
    speedNorm=8
    speed=speedNorm
    speedInventary=speed/2
    timeDodge=30
    dodge=False 
    dash=True
    timeDash=30
    boostDash=16


    alarm=[timeDodge] 

    #player weapon 
    def __init__(self,playerCamera):
        super().__init__(
            animation=Animation(
                            self.sprite_interface,
                            parent=camera.ui,
                            position=Vec2(0,-.425),
                            scale=(1.85,.1,1),
                            fps=1,
                            loop=True,
                            autoplay=True
                            )
        ),
        self.playerCamera=playerCamera
        #self.hand=Weapon.StartingHands(self)
        self.weapon=Weapon.StartingHands(self) #Weapon.Gun(self) #Weapon.Weapon(self)
        self.inventary=Inventary()
        self.drawDash=Draw.Draw_sprite(0,0,'sprite/lifeBar/dash/dash.png',scale=(1.8,1,1))

    #---------------interface--------------------------------
    def drawInterface(self):
        self.drawDash.alpha=1 if self.playerCamera.dash else 0
    
    def openMenu(self):
        self.openInventory=True if held_keys['q'] else False
        if self.openInventory:
            self.inventary.setVisible(True)
            self.speed=4
        else:
            self.inventary.setVisible(False)
            self.speed=self.speedNorm          

    #---------------hability--------------------------------
    def input(self,key):
        if self.openInventory:
            #move for the inventary
            if key=='scroll up':
                self.inventary.moveInventary(1)
                self.chooseWeapon()
            elif key=='scroll down':
                self.inventary.moveInventary(-1)
                self.chooseWeapon()

    def chooseWeapon(self):
        destroy(self.weapon.animation)
        destroy(self.weapon)
        if self.inventary.index==0:
            self.weapon=Weapon.Gun(self)
        elif self.inventary.index==1:
            self.weapon=Weapon.Shongunt(self)
        else:
            self.weapon=Weapon.Gun(self)
        self.weapon.recharge=False
        self.weapon.pickUpTheWeapon()

    def playingRun(self):
        return held_keys['shift'] and (held_keys['a'] or held_keys['d'] or held_keys['w'] or held_keys['s'])

    def weaponZoom(self):
        pass 
    
    def Dodge(self):
        if self.dodge==False:
            if self.alarm[0]>0:
                self.alarm[0]-=1
            else:
                self.dodge=True 
                self.alarm[0]=self.timeDodge
    
    def ActivateGodPunch(self):
        if held_keys['e'] and not self.climb:
            self.climb=True
            self.climbYStar=int(self.playerCamera[0].y+2)
            
        #move to the player 
        if self.climb:
            if self.climbYStar>self.playerCamera[0].y:
                self.playerCamera[0].y+=.4
            else:
                self.climb=False
    
    def SeeIfThePlayerIsClimb(self):
        if self.weapon.star:
            self.weapon.animation.visible=self.playerCamera.climb

    #---------------physical--------------------------------
    def Physical(self):
        pass#self.Dash() 
    
    #--------------------------------------------------------
    
    def update(self):
        self.Physical()
        self.openMenu()
        self.SeeIfThePlayerIsClimb()
        self.drawInterface()


class Inventary():
    index=0
    sc=.26
    scale=(sc,sc,sc)
    iX,iY=.75,-.250
    def __init__(self):
        super().__init__(
            
        )
        self.walppaper=Objects.Draw.Draw_sprite(self.iX,self.iY,'interface/inventary/inventary_000.png',self.scale)
        self.wapon=Objects.Draw.Draw_sprite(self.iX,self.iY,'interface/inventary/weapon.png',self.scale)
        self.inventary=Objects.Draw.Draw_sprite(self.iX,self.iY,'interface/inventary/inventary_001.png',self.scale)
        self.inventary.alpha=.7

    def setVisible(self,i):
        self.walppaper.visible=i
        self.inventary.visible=i
        self.wapon.visible=i

    def moveInventary(self,i):
        self.index=self.index+i if self.index<3 else 0
        self.inventary.rotation_z=self.index*90
 
class Health_bar(Entity):
    def __init__(self,x):
        super().__init__()
        self.mode='cube'
        self.color=color.white
        self.z=-.1
        self.origin=(-.5,-.5)
        #self.origin=(-.5,-.5)
        #self.position=(-x//2,0)
        self.position=(0,0)
        self.scale_max=x
        self.scale_x=x
        self.scale=(self.scale_x,10)

    def update(self):
        self.scale_x-=held_keys['e']*time.dt*5
        self.scale_x+=held_keys['r']*time.dt*5
        self.scale_x=clamp(self.scale_x,0,self.scale_max)
