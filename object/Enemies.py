from ursina import *
from script import Objects
from object import Weapon
class Enemy(Objects.ObjectButton):
    block=1
    sprite_index='white_cube'
    sprite_stunned=''
    image_speed=7
    scale=(1,1,1)
    c_color=color.color(0,1,random.uniform(0.9,1))
    life=4
    stunned=False
    speed=time.dt * 5

    distPlayer=0
    audioWound='audio/enemy/nurse/wound.wav'

    '''
        texture='white_cube',
        model='cube',
        color=self.c_color,
        position=position,
        collider='box',
        scale_x=self.scale[0],
        scale_y=self.scale[1],
        scale_z=self.scale[2],
        scale=self.scale,'''
    def __init__(self,player,position=(0,0,0),**kwargs):
        super().__init__(
            scale_x=self.scale[0],
            scale_y=self.scale[1],
            scale_z=self.scale[2],
            scale=self.scale,            
            animation=Animation(
                            self.sprite_index,
                            parent=scene,
                            fps=self.image_speed,
                            loop=True,
                            autoplay=True,
                            model='squad',
                            Collider='box',
                            #color=self.c_color,
                            position=position,
                            origin_y=-.25,
                            scale=self.scale,
                            collider='box',
                            block=self.block
            )
        ),
        self.player=player

    def collisionCoordinates(self):
        pass 

    def thePlayerCanShoot(self):
        #print(not self.player.weapon.recharge)
        return distance_2d(self,self.player.playerCamera)<self.player.weapon.gunSight and self.player.weapon.ammunition>0 and self.player.weapon.recharge

    def input(self,key):
        if self.animation.hovered: #see if the player is targeting it
            if key=='left mouse down':#see if the player Shooting 
                if self.thePlayerCanShoot():# know if the player can shooting
                    self.life-=self.player.weapon.weaponDamage
                    self.audio_play_sound_with_distance_player(self.audioWound)
                    self.checkTheStun()

            #if the player pick up to the enemy like hostage
            if self.stunned and key=='e':
                #delete the weapon of the player
                destroy(self.player.weapon.animation)
                destroy(self.player.weapon)
                enemy=Objects.Draw.Draw_sprite(-.4,-.6,'sprite/Weapon/hostages/nurse/nurse.png',scale=(1.8,1.8,1.8))
                self.player.weapon=Weapon.Hostages(self.player,enemy)
                Objects.Draw.Transition()
                
                #delete to the enemy
                destroy(self.animation)
                destroy(self)

    def checkTheStun(self):
        #if the enemy reached his limit we can see if they will is stunned
        if self.life==3:
            if True:#if random.randint(0, 1)==1:
                self.stunned=True
                oldPosition=self.animation.position
                destroy(self.animation)
                #create a new animation with the sprite of sprite_stunned
                self.animation=Animation(
                            self.sprite_stunned,
                            parent=scene,
                            fps=self.image_speed,
                            loop=True,
                            autoplay=True,
                            model='squad',
                            Collider='box',
                            position=oldPosition,
                            origin_y=-.25,
                            scale=self.scale,
                            collider='box',
                            block=self.block
                )

    def death(self):
        if self.life<=0:
            destroy(self.animation)
            destroy(self)

    def seeThePlayer(self):
        #self.animation.look_at_2d(self.player.playerCamera[0].position, 'y') 
        self.animation.rotation=self.player.playerCamera.rotation #[1]

    def characterOfTheEnemy(self):
        pass 
    
    def speedInventary(self):
        if self.player.openInventory:
            self.animation.fps=0
            self.speed=1
        else:
            self.animation.fps=self.image_speed

    def step(self):
        #we will see if the player be in the margin of atack
        self.distPlayer=distance(self.animation,self.player.playerCamera)
        if self.distPlayer>=40:
            return 

        #global classes
        self.speedInventary()
        self.seeThePlayer()

        #if the enemy is not stunned then they can follow with his program
        if not self.stunned:
            self.characterOfTheEnemy()
        self.death()

class Nurse(Enemy):
    scale=(2,4,1)
    c_color=color.color(255,255,255,.5)
    sprite_index='sprite/enemy/nurse/nurse'
    sprite_stunned='sprite/enemy/nurse/stunned/nursesTunned'

    def move(self):
        if self.distPlayer>5:
            hit_info = raycast(self.animation.world_position + Vec3(0,1,0), self.animation.forward, 30, ignore=(self.animation,self,),debug=True)
            if not hit_info.hit:
                self.animation.position += self.animation.forward * time.dt * 5

    def characterOfTheEnemy(self):
        pass 
        #self.move()
