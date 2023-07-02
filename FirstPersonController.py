from ursina import *

class FirstPersonController(Entity):
    def __init__(self, **kwargs):
        self.cursor = Entity(parent=camera.ui, model='quad', color=color.pink, scale=.008, rotation_z=45)
        super().__init__()
        self.direction=Vec3(0,0,0).normalized()
        self.speed = 10
        self.vspeed=0
        self.hspeed=0
        self.friction=.2
        self.acceleration=0
        self.timeAcceleration=5
        self.dash=False
        self.timeDash=30
        self.timeLoadDash=0
        self.boostDash=self.speed*2 #3/4
        self.directionOldDash=Vec3(0,0,0)
        self.weight=2
        self.height = 2
        self.camera_pivot = Entity(parent=self, y=self.height)

        camera.parent = self.camera_pivot
        camera.position = (0,0,0)
        camera.rotation = (0,0,0)
        camera.fov = 90
        mouse.locked = True
        self.mouse_sensitivity = Vec2(40, 40)

        self.gravity = 1
        self.grounded = False
        self.jump_height = 2
        self.jump_up_duration = .5
        self.fall_after = .35 # will interrupt jump up
        self.jumping = False
        self.air_time = 0

        self.climb=True
        self.alarm=[30]

        self.fatality=False
        


        for key, value in kwargs.items():
            setattr(self, key ,value)

        # make sure we don't fall through the ground if we start inside it
        if self.gravity:
            ray = raycast(self.world_position+(0,self.height,0), self.down, ignore=(self,))
            if ray.hit:
                self.y = ray.world_point.y

    def getAceleration(self):
        if held_keys['w'] or held_keys['s'] or held_keys['d'] or held_keys['a']:
            self.timeAcceleration-=.125 if self.timeAcceleration>1.25 else 0
            self.acceleration=self.speed/self.timeAcceleration
        else:
            self.timeAcceleration=6

        #camera shake effect
        movCam=0
        if  held_keys['d']:
            movCam=1
        elif held_keys['a']:
            movCam=-1

        #limit 
        if movCam is not 0:
            limitCam=4
            self.camera_pivot.rotation_z+=.125*movCam*self.acceleration

            if self.camera_pivot.rotation_z>=limitCam:
                self.camera_pivot.rotation_z=limitCam
            elif self.camera_pivot.rotation_z<=-limitCam:
                self.camera_pivot.rotation_z=-limitCam 
        else:
            movCamStart=.125
            if self.camera_pivot.rotation_z>0:
                self.camera_pivot.rotation_z-=movCamStart
            elif self.camera_pivot.rotation_z<0:
                self.camera_pivot.rotation_z+=movCamStart
            

    def seeIfCanClimb(self):
        wallBody=raycast(self.position+Vec3(0,0.5,0), self.direction, ignore=(self,), distance=.5, debug=False) 
        wallHead=raycast(self.position+Vec3(0,1,0), self.direction, ignore=(self,), distance=.5, debug=False)

        if wallBody.hit and not wallHead.hit:
            if wallBody.entities[0].name!='water':
                self.position=wallBody.entities[0].position+Vec3(0,1,0)
                self.climb=False 

    def seeIfThePlayerIsClimbing(self):
        #we will see if the player is climbing or if already did
        if self.climb:
            self.seeIfCanClimb()
        else: #already did
            if self.alarm[0]>0:
                self.alarm[0]-=1
            else:
                self.climb=True
                self.alarm[0]=30   

    def Dash(self):
        if not self.dash and held_keys['shift']:
            self.dash=True
            self.hspeed=self.boostDash

        if self.dash:
            if self.timeDash>0:
                self.timeDash-=1
            else: 
                self.hspeed=self.speed
                self.dash=False
                self.timeDash=30
                self.timeLoadDash=30

    def directionDash(self):
            advanceX=1
            advanceY=0
            if held_keys['w'] or held_keys['s'] or held_keys['d'] or held_keys['a']:
                advanceX= (held_keys['w'] - held_keys['s']) if held_keys['w'] or held_keys['s'] else 0
                advanceY= (held_keys['d'] - held_keys['a']) if held_keys['d'] or held_keys['a'] else 0

            self.direction = Vec3(
                self.forward * advanceX
                + self.right * advanceY
                ).normalized()

    def moveThePlayer(self):
        #we see if the player be move
        if held_keys['w'] or held_keys['s'] or held_keys['d'] or held_keys['a']:
            self.direction = Vec3(
                self.forward * (held_keys['w'] - held_keys['s'])
                + self.right * (held_keys['d'] - held_keys['a'])
                ).normalized()
            
            self.directionOldDash=self.direction 
            self.hspeed+=.35 if self.hspeed<self.speed else 0
        else:
            self.hspeed-=self.friction if self.hspeed>0 else 0
        
        self.getAceleration()
        self.seeIfThePlayerIsClimbing()

    def update(self):
        if not self.fatality:
            #the time that the player should wait for do other dash
            if self.timeLoadDash<=0:
                self.timeLoadDash=0
                self.Dash()
            else:
                self.timeLoadDash-=.25
            
            if not self.dash:
                self.moveThePlayer()
            else:
                self.directionDash()


            #------------------------------------------old code-----------------------------------------
            self.rotation_y += mouse.velocity[0] * self.mouse_sensitivity[1]

            self.camera_pivot.rotation_x -= mouse.velocity[1] * self.mouse_sensitivity[0]
            self.camera_pivot.rotation_x= clamp(self.camera_pivot.rotation_x, -90, 90)

            feet_ray = raycast(self.position+Vec3(0,0.5,0), self.direction, ignore=(self,), distance=.5, debug=False)
            head_ray = raycast(self.position+Vec3(0,self.height-.1,0), self.direction, ignore=(self,), distance=.5, debug=False)
            if (not feet_ray.hit and not head_ray.hit):
                self.move()
            elif (feet_ray.hit and head_ray.hit): #we will see if the player collision with the water
                self.moveWater() 

            if self.gravity:
                # gravity
                ray = raycast(self.world_position+(0,self.height,0), self.down, ignore=(self,))

                if ray.distance <= self.height+.1:
                    if not self.grounded:
                        self.land()
                    self.grounded = True
                    # make sure it's not a wall and that the point is not too far up
                    if ray.world_normal.y > .7 and ray.world_point.y - self.world_y < .5: # walk up slope
                        self.y = ray.world_point[1]
                    return
                else:
                    self.grounded = False

                # if not on ground and not on way up in jump, fall
                self.y -= min(self.air_time, ray.distance-.05) * time.dt * 100
                self.air_time += time.dt * .25 * self.gravity
            #------------------------------------------old code-----------------------------------------

     #------------------------------------------old code-----------------------------------------
    
    def move(self):
        move_amount = self.direction * time.dt * self.hspeed #self.speed

        if raycast(self.position+Vec3(-.0,1,0), Vec3(1,0,0), distance=.5, ignore=(self,)).hit:
            move_amount[0] = min(move_amount[0], 0)
        if raycast(self.position+Vec3(-.0,1,0), Vec3(-1,0,0), distance=.5, ignore=(self,)).hit:
            move_amount[0] = max(move_amount[0], 0)
        if raycast(self.position+Vec3(-.0,1,0), Vec3(0,0,1), distance=.5, ignore=(self,)).hit:
            move_amount[2] = min(move_amount[2], 0)
        if raycast(self.position+Vec3(-.0,1,0), Vec3(0,0,-1), distance=.5, ignore=(self,)).hit:
            move_amount[2] = max(move_amount[2], 0)
        self.position += move_amount 

    def moveWater(self):
        move_amount = self.direction * time.dt * self.speed
        mov=0
        collision1=raycast(self.position+Vec3(-.0,1,0), Vec3(1,0,0), distance=.5, ignore=(self,))
        collision2=raycast(self.position+Vec3(-.0,1,0), Vec3(-1,0,0), distance=.5, ignore=(self,))
        collision3=raycast(self.position+Vec3(-.0,1,0), Vec3(0,0,1), distance=.5, ignore=(self,))
        collision4=raycast(self.position+Vec3(-.0,1,0), Vec3(0,0,-1), distance=.5, ignore=(self,))

        if collision1.hit:
            if collision1.entities[0].name=='water':
                move_amount[0] = min(move_amount[0], 0)
                mov=1
        if collision2.hit:
            if collision2.entities[0].name=='water':
                move_amount[0] = max(move_amount[0], 0)
                mov=1
        if collision3.hit:
            if collision3.entities[0].name=='water':
                move_amount[2] = min(move_amount[2], 0)
                mov=1
        if collision4.hit:
            if collision4.entities[0].name=='water':
                move_amount[2] = max(move_amount[2], 0)
                mov=1
        
        if mov==1:
            self.position += move_amount 

    def input(self, key):
        if key == 'space' or (key=='space hold' or key=='space up'):
            aux=1.5 if key =='space up' else 0
            self.jump(aux)

    def jump(self,aux):
        if not self.grounded:
            return
        self.grounded = False
        self.animate_y(self.y+self.jump_height+aux, self.jump_up_duration, resolution=int(1//time.dt), curve=curve.out_expo)
        invoke(self.start_fall, delay=self.fall_after)

    def start_fall(self):
        self.y_animator.pause()
        self.jumping = False

    def land(self):
        # print('land')
        self.air_time = 0
        self.grounded = True

    def on_enable(self):
        mouse.locked = True
        self.cursor.enabled = True

    def on_disable(self):
        mouse.locked = False
        self.cursor.enabled = False

    #------------------------------------------old code-----------------------------------------


if __name__ == '__main__':
    from ursina.prefabs.first_person_controller import FirstPersonController
    window.vsync = False
    app = Ursina()
    # Sky(color=color.gray)
    ground = Entity(model='plane', scale=(100,1,100), color=color.yellow.tint(-.2), texture='white_cube', texture_scale=(100,100), collider='box')
    e = Entity(model='cube', scale=(1,5,10), x=2, y=.01, rotation_y=45, collider='box', texture='white_cube')
    e.texture_scale = (e.scale_z, e.scale_y)
    e = Entity(model='cube', scale=(1,5,10), x=-2, y=.01, collider='box', texture='white_cube')
    e.texture_scale = (e.scale_z, e.scale_y)

    player = FirstPersonController(y=2, origin_y=-.5)
    player.gun = None


    gun = Button(parent=scene, model='cube', color=color.blue, origin_y=-.5, position=(3,0,3), collider='box')
    gun.on_click = Sequence(Func(setattr, gun, 'parent', camera), Func(setattr, player, 'gun', gun))

    gun_2 = duplicate(gun, z=7, x=8)
    slope = Entity(model='cube', collider='box', position=(0,0,8), scale=6, rotation=(45,0,0), texture='brick', texture_scale=(8,8))
    slope = Entity(model='cube', collider='box', position=(5,0,10), scale=6, rotation=(80,0,0), texture='brick', texture_scale=(8,8))
    # hill = Entity(model='sphere', position=(20,-10,10), scale=(25,25,25), collider='sphere', color=color.green)
    # hill = Entity(model='sphere', position=(20,-0,10), scale=(25,25,25), collider='mesh', color=color.green)
    # from ursina.shaders import basic_lighting_shader
    # for e in scene.entities:
    #     e.shader = basic_lighting_shader

    hookshot_target = Button(parent=scene, model='cube', color=color.brown, position=(4,5,5))
    hookshot_target.on_click = Func(player.animate_position, hookshot_target.position, duration=.5, curve=curve.linear)

    def input(key):
        if key == 'left mouse down' and player.gun:
            gun.blink(color.orange)
            bullet = Entity(parent=gun, model='cube', scale=.1, color=color.black)
            bullet.world_parent = scene
            bullet.animate_position(bullet.position+(bullet.forward*50), curve=curve.linear, duration=1)
            destroy(bullet, delay=1)

    # player.add_script(NoclipMode())
    app.run()
