from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from engine.script import Draw
from object import Weapon 
from engine.script import Objects

class Player(Objects.Object3D):
    sprite_interface='interface/interface'

    #hability
    life=10
    pause=False
    openInventory=False
    godPunch=False
    climb=False
    climbYStar=0
    fatality=False
    timeFatality=90


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
    pushForce=4008

    alarm=[timeDodge,timeFatality] 

    #player weapon 
    def __init__(self,playerCamera,room):
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
        self.room=room
        #self.hand=Weapon.StartingHands(self)
        self.weapon=Weapon.StartingHands(self) #Weapon.Gun(self) #Weapon.Weapon(self)
        self.inventary=Inventary()
        self.drawDash=Draw.Draw_animation_camera(0,0,'sprite/lifeBar/dash/dash',32,scale=(1.8,1,1))
        self.blood_on_screen=[]

        #Draw.Draw_sprite(0,0,'sprite/lifeBar/dash/dash-255.0003.png',scale=(1.8,1,1))

    #---------------interface--------------------------------
    def drawInterface(self):
        self.drawDash.alpha=1 if self.playerCamera.dash else 0
        self.drawDash.animation.alpha=1 if self.playerCamera.dash else 0

        self.draw_blood_on_screen()
    
    def openMenu(self):
        self.openInventory=True if held_keys['q'] else False
        if self.openInventory:
            self.inventary.setVisible(True)
            self.speed=4
        else:
            self.inventary.setVisible(False)
            self.speed=self.speedNorm          

    def draw_blood_on_screen(self):
        for array_blood in self.blood_on_screen:
            blood=array_blood[0]
            alarm_blood=array_blood[1]
            if alarm_blood>0:
                self.alarm[0]-=time.dt
                blood.alpha-=.005
            else:
                blood.visible=False
                self.blood_on_screen.remove(array_blood) 
                destroy(blood) 
                
    def set_life(self,add):
        self.life+=add
        self.life= self.life if self.life<10 else 10
        self.life= self.life if self.life>1 else 0

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

        if key=='e':
            self.search_for_the_nearest_enemy()

    def search_for_the_nearest_enemy(self):
        if len(self.room.roomEnemy)>0 and not self.fatality:
            nearestEnemyDistance=-1
            nearestEnemy=self.room.roomEnemy[0]
            limitDistance=4

            for enemy in  self.room.roomEnemy:
                distance_enemy=enemy.distPlayer
                if self.check_what_the_player_can_do_a_fatality(distance_enemy,limitDistance,enemy):
                    if nearestEnemyDistance==-1:
                        nearestEnemy=enemy
                        nearestEnemyDistance=distance_enemy
                    elif distance_enemy<nearestEnemyDistance:
                        nearestEnemy=enemy
                        nearestEnemyDistance=distance_enemy
                else:
                    pass 

            if self.check_what_the_player_can_do_a_fatality(nearestEnemy.distPlayer,limitDistance,nearestEnemy):
                nearestEnemy.make_a_fatality() 
                self.room.roomEnemy.remove(nearestEnemy)

    def check_what_the_player_can_do_a_fatality(self,nearestEnemyDistance,limitDistance,enemy):
        return nearestEnemyDistance<=limitDistance and enemy.fatality and enemy.stunned

    def chooseWeapon(self):
        self.changeWeapon(self.inventary.index)
        self.weapon.recharge=False
        self.weapon.pickUpTheWeapon()

    def playingRun(self):
        return self.drawDash.animation.alpha #held_keys['shift'] and (held_keys['a'] or held_keys['d'] or held_keys['w'] or held_keys['s'])

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

    def create_a_fatality(self):
        if self.fatality:
            if self.alarm[1]>0:
                self.alarm[1]-=1
                self.playerCamera.fatality=self.fatality
            else:
                self.alarm[1]=self.timeFatality
                self.fatality=False

                self.playerCamera.fatality=self.fatality
                self.changeWeapon(0)
            
    def changeWeapon(self,weapon):
        destroy(self.weapon.animation)
        destroy(self.weapon) 
        
        if weapon==0:
            self.weapon=Weapon.Gun(self)
        elif weapon==1:
            self.weapon=Weapon.Shongunt(self)
        elif weapon==2:
            self.weapon=Weapon.Shongunt(self)
        elif weapon==3:
            self.weapon=Weapon.Gun(self)
        else:
            pass 

    #---------------physical--------------------------------
    def Physical(self):
        pass#self.Dash() 
    
    #--------------------------------------------------------
    
    def update(self):
        self.Physical()
        self.openMenu()
        self.SeeIfThePlayerIsClimb()
        self.drawInterface()
        self.create_a_fatality()


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
