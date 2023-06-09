from ursina import *
class Draw_sprite(Entity):
    def __init__(self,x,y,sprite,scale=(1,1,1)):
        super().__init__(
            parent=camera.ui,
            position=Vec2(x,y),
            model='cube',
            rotation=Vec3(0,0,0),
            texture=sprite,
            scale=scale,  
            scaleStar=scale
        )

class Draw_animation_camera(Entity):
    def __init__(self,x,y,sprite,image_speed,scale=(1,1,1)):
        super().__init__(

        )
        self.animation=Animation(
                            sprite,
                            parent=camera.ui,
                            fps=image_speed,
                            loop=True,
                            autoplay=True,
                            model='quad',
                            #Collider='box',
                            #color=self.c_color,
                            position=Vec2(x,y),
                            rotation=Vec3(0,0,0),
                            scale=scale,
        )

class Transition(Entity):
    def __init__(self):
        super().__init__(
            parent=camera.ui,
            position=Vec2(0,0),
            model='cube',
            rotation=Vec3(0,0,0),
            texture='white_cube',
            color=color.rgb(255, 255, 0),
            scale=4,
            alpha=0.3
        )

    def update(self):
        #time to disappear
        if self.alpha>0:
            self.alpha-=.05
        else:
            destroy(self)
