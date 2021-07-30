  #      -*- coding: utf-8 -*-
""" 
Created on Sat Feb 29 15:27:52 2020 

@author: nolanchiggs
"""

import arcade 
import math
import random as rdn
import abc
from abc import abstractmethod

# These are Global constants to use throughout the game
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

BULLET_RADIUS = 30
BULLET_SPEED = 10
BULLET_LIFE = 60

SHIP_TURN_AMOUNT = 3
SHIP_THRUST_AMOUNT = 0.25
SHIP_RADIUS = 70

INITIAL_ROCK_COUNT = 5

BIG_ROCK_SPIN = 1
BIG_ROCK_SPEED = 4.5
BIG_ROCK_RADIUS = 40

MEDIUM_ROCK_SPIN = -2
MEDIUM_ROCK_RADIUS = 25

SMALL_ROCK_SPIN = 5
SMALL_ROCK_RADIUS = 15     


class Point: 
    '''handles the center of all moving object'''
    def __init__(self):
        self.x = 0
        self.y = 0
        
    @property
    def x(self):
        return self._x
        
    @x.setter
    def x(self, new_x):
        self._x = new_x


    @property
    def y(self):
        return self._y
        
    @y.setter
    def y(self, new_y):
        self._y = new_y        

class Velocity:
    '''handles the speed of a moving object'''
    def __init__(self):
        self.dx = 0
        self.dy = 0
        

    # @property
    # def dx(self):
    #     return self._dx
        
    # @dx.setter
    # def dx(self, dx):
    #     if dx > 100:
    #         self._dx = 30
    #     elif dx > 100:
    #         self._dx = -30
    #     else:
    #         self._dx = dx


    # @property
    # def dy(self):
    #     return self._dy
        
    # @dx.setter
    # def dy(self, dy):
    #     if dy > 100:
    #         self._dy = 30
    #     elif dy > 100:
    #         self._dy = -30
    #     else:
    #         self._dy = dy


class Asteriod_FO:
    '''Parent Class or base class for all flying objects which will be inherited by child classes'''
    def __init__(self):
        self.center = Point()
        self.velocity = Velocity()
        self.radius = 5
        self.alive = True
        self.angle = 0
        # self.spin = 0
       
    def advance(self):
        self.center.x += self.velocity.dx
        self.center.y += self.velocity.dy
        
        
    
    def hit(self):
        self.alive = False
    
    def wrap(self):
        '''the object is able to exist from one end and appear on the other end'''
        if self.center.x > SCREEN_WIDTH:
            self.center.x = 0
 
        elif self.center.x < 0:
            self.center.x = SCREEN_WIDTH           

        elif self.center.y > SCREEN_HEIGHT:
            self.center.y = 0
 
        elif self.center.y < 0:
            self.center.y = SCREEN_HEIGHT           

    @abstractmethod
    def draw(self):
           pass
        
        
class Bullet(Asteriod_FO):
    '''child class,inherit from Asteriod_FO. Handles the bullets directions and causes it to appear'''
    def __init__(self):
        super().__init__()
        self.radius = BULLET_RADIUS
        self.lives = BULLET_LIFE

        
    def fire(self, angle: float, center):
        self.velocity.dx = math.cos(math.radians(angle)) * BULLET_SPEED
        self.velocity.dy = math.sin(math.radians(angle)) * BULLET_SPEED
        self.center.x = center.x
        self.center.y = center.y
        self.angle = angle
        
    def draw(self):
        bara = arcade.load_texture('laser.png')
        arcade.draw_texture_rectangle(self.center.x, self.center.y, bara.width, bara.height , bara, self.angle)


    def advance(self):
        '''bullet dies after every 60 frames'''                              # Overiding
        super().advance()                      #goes back to the parent class
        if self.lives == 0:
            self.alive = False
        self.lives -= 1            # 60 frames
  
class Shipp(Asteriod_FO):
    '''child class,inherit from Asteriod_FO'''
    def __init__(self):
        super().__init__() 
        self.center.x = SCREEN_WIDTH/2
        self.center.y =SCREEN_HEIGHT/2
        self.radius = SHIP_RADIUS
        self.angle = 90
        
    
    def draw(self): 
        if self.alive:
            shipp = arcade.load_texture('ship.png')
            arcade.draw_texture_rectangle(self.center.x, self.center.y, self.radius, self.radius,shipp, self.angle - 90)
         
    def rotate_clockwise(self):
        '''ships only circles around  clockwise'''
        self.angle += SHIP_TURN_AMOUNT
        
    def rotate_anticlockwise(self):
        '''ships only circles around  anticlockwise'''
        self.angle -= SHIP_TURN_AMOUNT  
        
        
    def ship_foward(self):
        ''''ship in the direction of where its nose is facing '''
        self.velocity.dx += math.cos(math.radians(self.angle)) * SHIP_THRUST_AMOUNT      #self. angle is referencing the angle of the ship
        self.velocity.dy += math.sin(math.radians(self.angle)) * SHIP_THRUST_AMOUNT
       
        
    def ship_backward(self):
        ''''ship in the opposite direction of where its nose is facing '''
        self.velocity.dx -= math.cos(math.radians(self.angle)) * SHIP_THRUST_AMOUNT
        self.velocity.dy -= math.sin(math.radians(self.angle)) * SHIP_THRUST_AMOUNT
    
            
    
class Large_asteriod(Asteriod_FO):
    '''The Largest Rock which contains mediums and small rocks'''
    def __init__(self):
        super().__init__()
        self.radius = BIG_ROCK_RADIUS
        self.center.x = rdn.randint(0,SCREEN_WIDTH)
        self.center.y =rdn.randint(0,SCREEN_HEIGHT)
        self.velocity.dx = rdn.uniform(-1 * BIG_ROCK_SPEED,BIG_ROCK_SPEED)
        self.velocity.dy = rdn.uniform(-1 * BIG_ROCK_SPEED,BIG_ROCK_SPEED)
        

        
    def draw(self):
        '''Causes Rocks to Appear'''
        if self.alive:
            Big = arcade.load_texture('big.png')
            arcade.draw_texture_rectangle(self.center.x, self.center.y, self.radius*2, self.radius*2 , Big,self.angle)
            self.angle += BIG_ROCK_SPIN



    def hit(self):
        '''Splits the rock into two_meidums rocks'''
        x = self.center.x
        y = self.center.y
        dy = self.velocity.dy
        dx = self.velocity.dx
        self.alive = False
        new = [Medium_asteriod(x,y,dx,dy,0,2),  Medium_asteriod(x,y,dx,dy, 0, -2), Small_asteriod(x,y,dx,dy, 0, 2)]
        return new


class Medium_asteriod(Asteriod_FO):
    ''' Causes the rocks to appears after the Large Asteriod is hit and conatins smaller roocks in it'''
    def __init__(self, x,y,dx,dy,a,b):
        super().__init__()
        self.radius = MEDIUM_ROCK_RADIUS
        self.center.x = x
        self.center.y =y
        self.velocity.dx = dx + a
        self.velocity.dy = dy + b
        
    
    def draw(self):
        '''Causes Medium_rocks to Appear'''
        if self.alive:
            mid = arcade.load_texture('medium.png')
            arcade.draw_texture_rectangle(self.center.x, self.center.y, self.radius*2, self.radius*2, mid, self.angle)
            self.angle += MEDIUM_ROCK_SPIN
            
            
    def hit(self):
        ''' splits the medium rocks into smaller ones'''
        x = self.center.x
        y = self.center.y
        dy = self.velocity.dy
        dx = self.velocity.dx
        self.alive = False
        new = [Small_asteriod(x,y,dx,dy, 0, 2), Small_asteriod(x,y,dx,dy, 0, 2)]
        return new
        
        
        

class Small_asteriod(Asteriod_FO):
    def __init__(self, x,y,dx,dy,a,b):
        super().__init__()
        self.radius = SMALL_ROCK_RADIUS
        self.center.x = x
        self.center.y = y
        self.velocity.dx = dx + a
        self.velocity.dy =  dy + b


    def hit(self):
        ''' since its polymorphism, it has to keep its property by returning a list,
        in this case an empty one. The rocks die or disappear'''
        x = self.center.x
        y = self.center.y
        dy = self.velocity.dy
        dx = self.velocity.dx
        self.alive = False
        new = []
        return new

        
      
    def draw(self):
        '''causes the small rocks to appear'''
        if self.alive:
            smally = arcade.load_texture('small.png')
            arcade.draw_texture_rectangle(self.center.x, self.center.y, self.radius*2, self.radius*2, smally, self.angle)
            self.angle += SMALL_ROCK_SPIN





class Game(arcade.Window):
    """
    This class handles all the game callbacks and interaction
    This class will then call the appropriate functions of
    each of the above classes.
    You are welcome to modify anything in this class.
    """

    def __init__(self, width, height):
        """
        Sets up the initial conditions of the game
        :param width: Screen width
        :param height: Screen height
        """
        super().__init__(width, height)
        # arcade.set_background_color(arcade.color.SMOKY_BLACK)
        
        self.held_keys = set()

        # TODO: declare anything here you need the game class to track
        self.bullets = []
        self.ship = Shipp()                                   # THESE ARE INSTANCES, THEY WILL HELP WHEN CALLING A FUNCTION
        self.rocks = [ ]
        for i in range(0,5):
            self.rocks.append(Large_asteriod())
        self.frame_count = 0
        
        # self.rockss = [ ]
        # for i in range(0,8):
        #     self.rockss.append(Medium_asteriod())
        # self.frame_count = 0
        
        
        # self.rocksss = [ ]
        # for i in range(0,8):
        #     self.rocksss.append(Small_asteriod())
        # self.frame_count = 0
        
    def on_draw(self): 
        """
        Called automatically by the arcade framework.
        Handles the responsibility of drawing all elements.
        """

       
        # clear the screen to begin drawing
        arcade.start_render()

        background = arcade.load_texture("gala.png")
        arcade.draw_texture_rectangle(SCREEN_WIDTH/2, SCREEN_HEIGHT/2,SCREEN_WIDTH , SCREEN_HEIGHT, background) 
        

        for asteriod in self.rocks:
            asteriod.draw()
            
        # for asteriod in self.rockss:
        #     asteriod.draw()

        # for asteriod in self.rocksss:
        #     asteriod.draw()            
            
        for bullet in self.bullets:
            bullet.draw()
        
        
        self.ship.draw()
        
        
        # TODO: draw each object

    def check_collisions(self):
        """
        Checks to see if bullets have hit targets.
        Updates scores and removes dead items.
        :return:
        """

        # NOTE: This assumes you named your targets list "targets"

        for big_rock in  self.rocks:
            for bullet in self.bullets:

                # Make sure they are both alive before checking for a collision
                if bullet.alive and big_rock.alive:
                    too_close = bullet.radius + big_rock.radius

                    if (abs(bullet.center.x - big_rock.center.x) < too_close and
                                abs(bullet.center.y - big_rock.center.y) < too_close):
                        # its a hit!
                        
                        # this is where the bullet hit comes in.
                        bullet.alive = False
                        self.rocks += big_rock.hit()
                        #  self.rocks.remove(big_rock)
                        
            """Avoids the user from  dying right after the game starts"""
            if self.frame_count > 200:
            
                if self.ship.alive and big_rock.alive:
                    too_close = self.ship.radius + big_rock.radius
                        
                    if (abs(self.ship.center.x - big_rock.center.x) < too_close and
                        abs(self.ship.center.y - big_rock.center.y) < too_close):
                            
                        # big_rock.split()
                        self.rocks += big_rock.hit()
                        # self.rocks.remove(big_rock)
                        self.ship.alive = False

    def cleanup_deadstuff(self):
        """
        Removes any dead bullets or targets from the list.
        :return:
        """
        for bullet in self.bullets:
            if not bullet.alive:
                self.bullets.remove(bullet)

        for big_rock in self.rocks:
            if not big_rock.alive:
                self.rocks.remove(big_rock)

    def update(self, delta_time):
        """
        Update each object in the game.
        :param delta_time: tells us how much time has actually elapsed
        """
        self.check_keys()

        
        # TODO: Tell everything to advance or move forward one step in time
        
        for Large_asteriod in self.rocks:
            Large_asteriod.advance()
            Large_asteriod.wrap()
                                                            #this is where I call my functions
        
        # TODO: Check for collisions
        for bullet in self.bullets:
            bullet.advance()
            bullet.wrap()
            
            
            
        self.check_collisions() 
        self.cleanup_deadstuff() 
        self.ship.advance()
        self.ship.wrap()
        self.frame_count += 1

    def check_keys(self):
        """
        This function checks for keys that are being held down.
        You will need to put your own method calls in here.
        """
        if arcade.key.LEFT in self.held_keys:
            self.ship.rotate_clockwise()                       #USE INSTANCES FOR CALLING FUNCTIONS

        if arcade.key.RIGHT in self.held_keys:
            self.ship.rotate_anticlockwise() 

        if arcade.key.UP in self.held_keys:
            self.ship.ship_foward()
            # self.ship.ship_upward()

        if arcade.key.DOWN in self.held_keys:
            self.ship.ship_backward()
            # self.ship.ship_downward()

        # Machine gun mode...
        if arcade.key.SPACE in self.held_keys:
            bullet = Bullet()
            bullet.fire(self.ship.angle, self.ship.center)

            self.bullets.append(bullet)


    def on_key_press(self, key: int, modifiers: int):
        """
        Puts the current key in the set of keys that are being held.
        You will need to add things here to handle firing the bullet.
        """
        if self.ship.alive:
            self.held_keys.add(key)

            if key == arcade.key.SPACE:
                # TODO: Fire the bullet here!
                bullet = Bullet()
                bullet.fire(self.ship.angle, self.ship.center)

                self.bullets.append(bullet)

    def on_key_release(self, key: int, modifiers: int):
        """
        Removes the current key from the set of held keys.
        """
        if key in self.held_keys:
            self.held_keys.remove(key)


# Creates the game and starts it going
window = Game(SCREEN_WIDTH, SCREEN_HEIGHT)
arcade.run()