# import libraries

# importing everything from Ursina, including basic models,textures,etc., does not include prefabs
from ursina import *

# importing the first person controller prefab from Ursina
from ursina.prefabs.first_person_controller import FirstPersonController

# import libraries done

# creating an application variable which will run at the end of the code
app = Ursina()

# texture loader

# texture used for the skybox, original asset
Skybox_Texture = load_texture("assets/skybox")


# texture loader done

# classes

# detailed explanation for most of the characteristics will be done in the following class only and additional
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
            scale=Vec3(50, 1, 50),

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
            model='cube',
            position=position,
            scale=scale,

            # rotation is the angles of which the object is rotated at, uses vector 3 and follows the XYZ coordinates
            # system
            rotation=Vec3(90, 0, 0),
            texture='white_cube',
            color=color.red,
            origin_y=0
        )


# Target class creates the gun model as well as provide the origin point of bullets
class Gun(Entity):
    def __init__(self):
        super().__init__(
            collision=False,
            collider=None,
            parent=camera,
            position=Vec3(0, -1, 2),
            model='sphere',
            scale=Vec3(0.5, 1, 1.5),
            color=color.black
        )

    # shot and idle functions are both for cosmetic purposes representing recoil
    def shot(self):
        self.position = Vec3(0, -1, 1.5)

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

    # pressing the left mouse button calls the shot function
    if held_keys['left mouse']:
        Gun.shot()
    else:
        Gun.idle()

    # input handler for update function done

    # teleport the player if the player falls off the map
    if Player.position.y < -5:
        Player.position = Vec3(0, 2, 0)

# input handler

# this function is used mostly for creating and shooting bullets, though can be used for other functions
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
                position=Vec3(0, 0.5, 0)
            )

    # an individual update function so that the bullet update function would not interfere the global update function
        def update(self):

            # stating global variables
            global Points
            global Points_Count

            # stating global variables done

            # collision check every tick
            hit_info = self.intersects()
            if hit_info.hit:

                # checks if the collision target is the entity Target, if so adds the point and updates the GUI
                if hit_info.entity == Target:
                    Points_Count += 10
                    Points.text = "Points:" + str(Points_Count)
                destroy(self)

    # input handling for left click specifically
    if key == 'left mouse down' and Ammo_Count > 0:
        Bullet = Bullet()

        #code from Ursina manual

        # this piece of code was taken directly from the Ursina manual, with few minor adjustments. The code worked
        # better than the ones created by the developer. The adjustments made are changing the speed to a multiple of
        # 25000, multiplying the speed with time.dt so speed are consistent no matter the frame rate,
        # and the delay/animate time to 3 seconds (code origin: Ursina engine API manual,
        # https://www.ursinaengine.org/cheat_sheet.html#FirstPersonController)
        Bullet.world_parent = scene
        Bullet.animate_position(Bullet.position + (Bullet.forward * 25000) * time.dt, curve=curve.linear, duration=3)
        destroy(Bullet, delay=3)

        # code from Ursina manual done

        # decrease ammo in clip and updates the GUI
        Ammo_Count -= 1
        Ammo.text = "Ammo:" + str(Ammo_Count)

# input handler done

# functions done

# main body

# basic variables
Ammo_Count = 9
Points_Count = 0

# basic variables done

# declaring object instances
Level = Level()
Player = FirstPersonController()
Player.cursor.color = color.white
Target = Target(position=Vec3(5, 2, 10))
Gun = Gun()

# font is the font that the text uses
Ammo = Text(text='Ammo:9', position=Vec2(-0.5, -0.4), color=color.white, font=Text.default_font)
Ammo.create_background()
Points = Text(text='Points:0000', position=Vec2(-0.7, -0.4), color=color.white, font=Text.default_font)
Points.create_background()

# double sided is assigning the texture on both sides of the model (inside and outside)
Skybox = Entity(model='sphere', parent=scene, texture=Skybox_Texture, scale=200, double_sided=True)

# declaring object instances done

# main body done

# run app
app.run()
