from ursina import *
from script import Objects, Draw
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

    #fatalitys
    fatality=True
    sprs_fatalitys=[]

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
                            model='quad',
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
        if self.animation.hovered and not self.player.fatality: #see if the player is targeting it animation
            if key=='left mouse down':#see if the player Shooting 
                if self.thePlayerCanShoot():# know if the player can shooting
                    self.life-=self.player.weapon.weaponDamage
                    self.audio_play_sound_with_distance_player(self.audioWound)
                    self.checkTheStun()
                    self.blood_on_screen()

            #we will watch if the player be to a radius of distance permitted for use the especial attacks
            if self.distPlayer<=6:
                #if the player pick up to the enemy like hostage
                if self.stunned and key=='f':
                    #delete the weapon of the player
                    destroy(self.player.weapon.animation)
                    destroy(self.player.weapon)
                    enemy=Objects.Draw.Draw_sprite(-.4,-.6,'sprite/Weapon/hostages/nurse/nurse.png',scale=(1.8,1.8,1.8))
                    self.player.weapon=Weapon.Hostages(self.player,enemy)
                    Objects.Draw.Transition()
                    
                    #delete to the enemy
                    destroy(self.animation)
                    destroy(self)

                #if the player would like be a fatality
                '''
                if self.stunned and key=='e' and self.fatality:
                    destroy(self.player.weapon.animation)
                    destroy(self.player.weapon)
                    self.player.weapon=Weapon.FatalityEnemy(self.player)
                    self.player.fatality=True

                    #delete to the enemy
                    destroy(self.animation)
                    destroy(self)'''

    def make_a_fatality(self):
        #raise the life of the player
        self.player.set_life(20)

        #destroy the weapon of the player
        destroy(self.player.weapon.animation)
        destroy(self.player.weapon)

        #add a fatality animation
        self.player.weapon=Weapon.FatalityEnemy(self.player)
        self.player.fatality=True

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
                            model='quad',
                            Collider='box',
                            position=oldPosition,
                            origin_y=-.25,
                            scale=self.scale,
                            collider='box',
                            block=self.block
                )

    def blood_on_screen(self):
        #we will watch where is the player
        blood_distance_max=50
        distance_player=distance(self.player.playerCamera,self)
        if distance_player<blood_distance_max: #we watch if the player can be staining of blood
            
            #calculate the blood alpha depending of his distance with the player
            alpha=1-(distance_player/blood_distance_max)
            sprite=f'sprite\\lifeBar\\blood\\blood_00{random.randint(0, 4)}' #get a sprite aleatory
            spr_x,spr_y=random.uniform(0, 1),random.uniform(0, 1)#random.randint(0, 1920), random.randint(0, 1080) #place it at random coordinates on the screen
            spr_scale=[random.uniform(.5, 1.8),random.uniform(.5, 1),random.uniform(.5, 1)]
            blood_object=Draw.Draw_sprite(spr_x,spr_y,sprite,scale=(spr_scale)) #create the blood 
            blood_object.alpha=alpha 
            self.player.blood_on_screen.append([blood_object,30]) #add the stain to the list of the player

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
