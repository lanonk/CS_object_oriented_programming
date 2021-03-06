"""
File: skeet.py
Original Author: Br. Burton
Designed to be completed by others
This program implements an awesome version of skeet.
"""
import arcade
import math
import random
import abc
from abc import abstractmethod

# These are Global constants to use throughout the game
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

RIFLE_WIDTH = 100
RIFLE_HEIGHT = 20
RIFLE_COLOR = arcade.color.DARK_RED

BULLET_RADIUS = 3
BULLET_SPEED = 10

TARGET_RADIUS = 25
TARGET_SAFE_RADIUS = 15

class Point:
    def __init__(self):
        self.x = 0
        self.y = 0

class Velocity:
    def __init__(self):
        self.dx = 0
        self.dy = 0
        

class Flying_Object:
    def __init__(self):
       self.center = Point()
       self.velocity = Velocity()
       self.radius = 0.0
       self.alive = True
       
    def advance(self):
        self.center.x += self.velocity.dx
        self.center.y += self.velocity.dy

    def is_off_screen(self, SCREEN_WIDTH, SCREEN_HEIGHT):
        if(self.center.x >= SCREEN_WIDTH) \
            or (self.center.y < 0):
            return True
        else:
            return False

    @abstractmethod
    def draw(self):
        pass
    
class Bullet(Flying_Object):
    def __init__(self):
        super().__init__()
        self.angle =45
        self.radius = BULLET_RADIUS
        
    def fire(self, angle: float):
        self.velocity.dx = math.cos(math.radians(angle)) * BULLET_SPEED
        self.velocity.dy = math.sin(math.radians(angle)) * BULLET_SPEED
        
    def draw(self):
        bullet_texture = arcade.load_texture('bullet.png')
        arcade.draw_texture_rectangle(self.center.x, self.center.y, BULLET_RADIUS*2, BULLET_RADIUS*2 , bullet_texture)
    
    # def is_off_screen(self, SCREEN_WIDTH, SCREEN_HEIGHT):
    #     if (self.center.x >= SCREEN_WIDTH) and (self.center.y <=0):
    #         return True
    #     else:
    #         return False
        
        
        
class Target(Flying_Object):
    def __init__(self):
        super().__init__()
        self.lives = 0
     
    """
     hit is unique
    """
    @abstractmethod
    def hit(self):
        set.alive = False
        
    @abstractmethod
    def draw(self):
        pass    
    
    
class StandardTarget(Target):
    def __init__(self):
        super().__init__()
        # self.lives = 1
        self.radius = TARGET_RADIUS
        
    def hit(self):
        self.alive = False
        return 1

    def draw(self):
        if self.alive:
            arcade.draw_circle_filled(self.center.x, self.center.y, TARGET_RADIUS, arcade.color.BLUE)

    
class StrongTarget(Target):
    """
    StrongTarget is inheriting all the methods and attributes from the Flying Object
    """
    def __init__(self):
        super().__init__()
        self.lives = 3

        self.radius = TARGET_RADIUS
        
        
    def hit(self):
        self.lives -= 1
        if self.lives == 2:
            self.radius/=2       # reducing the size the size of the ball             
            return 1
        elif self.lives == 1:
            self.radius/=2       # reduces the size of the ball even further
            return 1
        elif self.lives == 0:
            self.alive = False
            return 5
        
        
    def draw(self):
        #arcade.draw_circle_filled(self.center.x, self.center.y, TARGET_RADIUS, arcade.color.RED)
        # if self.lives ==3:
            arcade.draw_circle_filled(self.center.x, self.center.y, self.radius, arcade.color.RED)
        # elif self.lives == 2:
        #     #return 10
        #     arcade.draw_circle_filled(self.center.x - 10, self.center.y, TARGET_RADIUS -10, arcade.color.RED)   
        # else:
        #     arcade.draw_circle_filled(self.center.x - 20, self.center.y, TARGET_RADIUS -20, arcade.color.RED)
        #     #return 15 
            
            

    
class SafeTarget(Target):
    def __init__(self):
        super().__init__()
        # self.lives = 1
        self.radius = TARGET_SAFE_RADIUS
        
    def hit(self):
        self.alive = False
        return -20       

        # def hit(self):
        #     self.alive = False
        #     return -10

    def draw(self):
        arcade.draw_circle_filled(self.center.x, self.center.y, self.radius, arcade.color.GREEN)


class Rifle:
    """
    The rifle is a rectangle that tracks the mouse.
    """
    def __init__(self):
        self.center = Point()
        self.center.x = 0
        self.center.y = 0

        self.angle = 45

    def draw(self):
        arcade.draw_rectangle_filled(self.center.x, self.center.y, RIFLE_WIDTH, RIFLE_HEIGHT, RIFLE_COLOR, self.angle)


class Game(arcade.Window):
    """
    This class handles all the game callbacks and interaction
    It assumes the following classes exist:
        Rifle
        Target (and it's sub-classes)
        Point
        Velocity
        Bullet
    This class will then call the appropriate functions of
    each of the above classes.
    You are welcome to modify anything in this class, but mostly
    you shouldn't have to. There are a few sections that you
    must add code to.
    """

    def __init__(self, width, height):
        """
        Sets up the initial conditions of the game
        :param width: Screen width
        :param height: Screen height
        """
        super().__init__(width, height)

        self.rifle = Rifle()
        self.score = 0

        self.bullets = [] 
        self.targets = [] 

        # TODO: Create a list for your targets (similar to the above bullets)


            
        
        
        arcade.set_background_color(arcade.color.AMAZON)

    def on_draw(self):
        """
        Called automatically by the arcade framework.
        Handles the responsibility of drawing all elements.
        """

        if self.score  < -10:
            arcade.start_render()
            arcade.draw_text("Game Over, YOU SUCK!!!", SCREEN_WIDTH/4, SCREEN_HEIGHT/2, arcade.color.PURPLE,30)
        # elif self.alive = False:
        #     arcade.start_render()
        #     arcade.draw_text("Oops!!!", SCREEN_WIDTH/4, SCREEN_HEIGHT/2, arcade.color.PURPLE,30)
            
        else:
        # clear the screen to begin drawing
            arcade.start_render()


            for bullet in self.bullets:
                bullet.draw()

        # draw each object
            self.rifle.draw()
            
        # TODO: iterate through your targets and draw them...
            for target in self.targets:
                target.draw()
            
            
            self.draw_score()

    def draw_score(self):
        """
        Puts the current score on the screen
        """
        score_text = "Score: {}".format(self.score)
        start_x = 10
        start_y = SCREEN_HEIGHT - 20
        arcade.draw_text(score_text, start_x=start_x, start_y=start_y, font_size=12, color=arcade.color.NAVY_BLUE)

    def update(self, delta_time):
        """
        Update each object in the game.
        :param delta_time: tells us how much time has actually elapsed
        """
        self.check_collisions()
        self.check_off_screen()

        # decide if we should start a target
    
        if random.randint(1, 50) == 1:
            self.create_target()

        for bullet in self.bullets:
            bullet.advance()
            
        for target in self.targets:
            target.advance()
            
            
        # TODO: Iterate through your targets and tell them to advance

    def create_target(self):
        """
        Creates a new target of a random type and adds it to the list.
        :return:
        """
        rand_target = random.randint(1,3)
        
        
        if rand_target == 1:
            target =StandardTarget()
            target.velocity.dx = random.uniform(1,5)
            target.velocity.dy = random.uniform(1,-4)
            target.center.y = random.uniform(300, SCREEN_HEIGHT)
            
            
        if rand_target == 2:
            target = StrongTarget()
            target.velocity.dx = random.uniform(1,5)
            target.velocity.dy = random.uniform(-4,1)
            target.center.y = random.uniform(300, SCREEN_HEIGHT)
            
        if rand_target == 3:
            target =SafeTarget()
            target.velocity.dx = random.uniform(1,6)
            target.velocity.dy = random.uniform(-9,1)
            target.center.y = random.uniform(300, SCREEN_HEIGHT)
            
        self.targets.append(target)
            
        # TODO: Decide what type of target to create and append it to the list

    def check_collisions(self):
        """
        Checks to see if bullets have hit targets.
        Updates scores and removes dead items.
        :return:
        """

        # NOTE: This assumes you named your targets list "targets"

        for bullet in self.bullets:
            for target in self.targets:

                # Make sure they are both alive before checking for a collision
                if bullet.alive and target.alive:
                    too_close = bullet.radius + target.radius

                    if (abs(bullet.center.x - target.center.x) < too_close and
                                abs(bullet.center.y - target.center.y) < too_close):
                        # its a hit!
                        bullet.alive = False
                        self.score += target.hit()

                        # We will wait to remove the dead objects until after we
                        # finish going through the list

        # Now, check for anything that is dead, and remove it
        self.cleanup_zombies()

    def cleanup_zombies(self):
        """
        Removes any dead bullets or targets from the list.
        :return:
        """
        for bullet in self.bullets:
            if not bullet.alive:
                self.bullets.remove(bullet)

        for target in self.targets:
            if not target.alive:
                self.targets.remove(target)

    def check_off_screen(self):
        """
        Checks to see if bullets or targets have left the screen
        and if so, removes them from their lists.
        :return:
        """
        for bullet in self.bullets:
            if bullet.is_off_screen(SCREEN_WIDTH, SCREEN_HEIGHT):
                self.bullets.remove(bullet)

        for target in self.targets:
            if target.is_off_screen(SCREEN_WIDTH, SCREEN_HEIGHT):
                self.targets.remove(target)

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        # set the rifle angle in degrees
        self.rifle.angle = self._get_angle_degrees(x, y)

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        # Fire!
        angle = self._get_angle_degrees(x, y)

        bullet = Bullet()
        bullet.fire(angle)

        self.bullets.append(bullet)

    def _get_angle_degrees(self, x, y):
        """
        Gets the value of an angle (in degrees) defined
        by the provided x and y.
        Note: This could be a static method, but we haven't
        discussed them yet...
        """
        # get the angle in radians
        angle_radians = math.atan2(y, x)

        # convert to degrees
        angle_degrees = math.degrees(angle_radians)

        return angle_degrees

# Creates the game and starts it going
window = Game(SCREEN_WIDTH, SCREEN_HEIGHT)
arcade.run()