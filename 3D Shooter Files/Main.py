# Disclaimer: Some aspects of code are taken from the Ursina Manual and inspired by tutorials from youtube. Ursina
# Engine has an MIT license, and the other code inspired by the tutorials are provided credit at specific points
# where said code is used, and given proper credit in the documentation of this project. All Assets not included in
# the Ursina Engine are original and created by me

# Manual(controls): WASD to move, left mouse button to shoot, r to reload, p to quit

# import libraries

# importing everything from Ursina, including basic models,textures,etc., does not include prefabs
from ursina import *

# importing the first person controller prefab from Ursina
from ursina.prefabs.first_person_controller import FirstPersonController
import random as r

# import libraries done

# creating an application variable which will run at the end of the code
app = Ursina()

# texture loader
Skybox_Texture = load_texture("assets/skybox.png")
Target_Texture = load_texture("assets/target.png")
Gun_Texture = load_texture("assets/gun.png")


# texture loader done

# classes

# detailed explanation for most of the characteristics will be done in the following class only. Additional
# characteristics will be explained in other classes. In Ursina, classes need to be assigned as either Entity, Text,
# Button, mouse, and raycaster for them to be recognized in the program and have the correct properties

# Level class creates a floor for the player character to stand on
class Level(Entity):
    def __init__(self):
        super().__init__(

            # collision determines if the object can detect collision with other objects, entity collision by default
            # is false
            collision=True,

            # collider chooses the collision mesh that the object uses, there are 3 basic meshes, 'box', 'sphere',
            # and 'mesh'
            collider='box',

            # parent places this object as a child of said parent, which means the child's properties will be based
            # around the parent first, used mostly for positioning
            parent=scene,

            # model is what the object would be shaped like, the collision mesh does not have to be exactly the same
            # as the model, there are some basic models such as 'cube', 'quad', 'sphere', etc.
            model='cube',

            # position is the position of the object relative to the parent's position and origin point, uses vector
            # 3 and follows the XYZ coordinates system
            position=Vec3(0, -0.5, 0),

            # scale is the size of the object, uses vector 3 and follows the XYZ coordinates system
            scale=Vec3(25, 1, 25),

            # texture is the outer layer of the model, and it determines what the model would look like, attaches to
            # the model through UV map
            texture='white_cube',

            # color is the color the object takes on, can use RGBA and HSV schemes
            color=color.white,

            # origin point is the center point of the object
            origin_y=0.5
        )


# Target class creates the main goal of what the player should shoot at
class Target(Entity):
    def __init__(self, position=Vec3(0, 0, 0), scale=Vec3(2, 1, 2)):
        super().__init__(
            collision=True,
            collider='box',
            parent=scene,
            model='assets/Box',
            position=position,
            scale=scale,

            # rotation is the angles of which the object is rotated at, uses vector 3 and follows the XYZ coordinates
            # system
            rotation=Vec3(90, 0, 0),
            texture=Target_Texture,
        )

    # simple teleporting function when shot, the target moves away
    def teleport(self):
        self.position = Vec3(r.uniform(-50, 50), r.uniform(0, 5), r.uniform(25, 100))


# gun class creates the gun model as well as provide the origin point of bullets
class Gun(Entity):
    def __init__(self):
        super().__init__(
            collision=False,
            collider=None,
            parent=camera,
            position=Vec3(0, -1, 2),
            model='assets/Gun',
            texture=Gun_Texture,
            scale=Vec3(1, 1, 1),
            rotation=Vec3(0, 90, 0),
        )

    # shot and idle functions are both for cosmetic purposes representing recoil, inspired by the code in the
    # tutorial: Creating Minecraft in Python [with the Ursina Engine] (Link:
    # https://www.youtube.com/watch?v=DHSRaVeQxIk&t=1779s&ab_channel=ClearCode)
    def shot(self):
        self.position = Vec3(0, -1, 1.8)

    def idle(self):
        self.position = Vec3(0, -1, 2)


# classes done

# functions

# update functions run in a loop every tick/frame
def update():
    # stating global variables
    global Bullet
    global Ammo_Count

    # stating global variables done

    # input handler for update function

    # pressing p quits the application
    if held_keys['p']: quit()

    # pressing r reloads the gun and updates the GUI
    if held_keys['r']:
        Ammo_Count = 9
        Ammo.text = "Ammo:" + str(Ammo_Count)

    # pressing the left mouse button calls the shot function, have to be separated from the input function as it wont
    # work well otherwise
    if held_keys['left mouse']:
        Gun.shot()
    else:
        Gun.idle()

    # input handler for update function done

    # teleport the player if the player falls off the map
    if Player.position.y < -5:
        Player.position = Vec3(0, 2, 0)


# input handler

# this function is used mostly for creating and shooting bullets, though can be used for other functions separating
# this from the update function gives it a semi-automatic shooting effect, which means 1 bullet per mouse click
# instead of 1 bullet per tick
def input(key):
    # stating global variables
    global Ammo_Count

    # stating global variables done

    # creating bullet class in the function so it can be used in the function
    class Bullet(Entity):
        def __init__(self):
            super().__init__(
                parent=Gun,
                model='cube',
                collision=True,
                collider='box',
                scale=Vec3(0.1, 0.1, 0.2),
                color=color.gray,
                position=Vec3(0, 0.5, 0),
                rotation=Vec3(0, -90, 0)
            )

        # an individual update function so that the bullet update function would not interfere the global update
        # function
        def update(self):

            # stating global variables
            global Points
            global Points_Count

            # stating global variables done

            # collision check every tick
            hit_info = self.intersects()
            if hit_info.hit:
                # checks if the collision target is the entity Target, if so adds the point and updates the GUI
                if hit_info.entity in Target_List.values():
                    Points_Count += int(distance(Player, hit_info.entity))
                    Points.text = "Points:" + str(Points_Count)
                    hit_info.entity.teleport()
                destroy(self)

    # input handling for left click specifically
    if key == 'left mouse down' and Ammo_Count > 0:
        Bullet = Bullet()

        # code from Ursina manual

        # this piece of code was taken directly from the Ursina manual, with few minor adjustments. The code worked
        # better than the ones created by the developer. The adjustments made are changing the speed to a multiple of
        # 100000, multiplying the speed with time.dt so speed are consistent no matter the frame rate,
        # and the delay/animate time to 3 seconds (code origin: Ursina engine API manual,
        # https://www.ursinaengine.org/cheat_sheet.html#FirstPersonController)
        Bullet.world_parent = scene
        Bullet.animate_position(Bullet.position + (Bullet.forward * 100000) * time.dt, curve=curve.linear, duration=5)
        destroy(Bullet, delay=5)

        # code from Ursina manual done

        # decrease ammo in clip and updates the GUI
        Ammo_Count -= 1
        Ammo.text = "Ammo:" + str(Ammo_Count)


# input handler done

# functions done

# main body

# basic variables
# based on a stereotypical pistol with a clip of 9
Ammo_Count = 9

# points start at 0
Points_Count = 0

Target_List = {}
# basic variables done

# declaring object instances
Level = Level()
Player = FirstPersonController()
Player.cursor.color = color.white
Gun = Gun()

for x in range(5):
    Target_List["target"+str(x)] = Target(position=Vec3(r.uniform(-50, 50), r.uniform(0, 5), r.uniform(25, 100)), scale=(Vec3(2, 1, 2)))
# font is the font that the text uses
Ammo = Text(text='Ammo:9', position=Vec2(-0.5, -0.4), color=color.white, font=Text.default_font)
Ammo.create_background()
Points = Text(text='Points:0000', position=Vec2(-0.7, -0.4), color=color.white, font=Text.default_font)
Points.create_background()

# double sided is assigning the texture on both sides of the model (inside and outside), inspired by the code in the
# tutorial: Creating Minecraft in Python [with the Ursina Engine] (Link:
# https://www.youtube.com/watch?v=DHSRaVeQxIk&t=1779s&ab_channel=ClearCode)
Skybox = Entity(model='sphere', parent=scene, texture=Skybox_Texture, scale=500, double_sided=True)

# declaring object instances done

# main body done

# run app
app.run()
