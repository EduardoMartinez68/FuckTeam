from ursina import *
from script import Physical
class Npc(Entity):
    block=1
    scale=(1,1,1)
    rotation = (0,0,0)
    c_color=color.color(0,0,random.uniform(0.9,1))
    sprite_index=''
    image_speed=0

    audio=''
    
    def __init__(self,player):
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
        self.player=player,

    def speeking(self):
        Physical.AudioWithDistance(self,self.audio)