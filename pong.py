# -*- coding: utf-8 -*-
"""
Created on Fri Feb  7 12:41:39 2020

@author: nolanchiggs 
"""

import arcade
import random

# These are Global constants to use throughout the game
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500
BALL_RADIUS = 10

PADDLE_WIDTH = 10
PADDLE_HEIGHT = 50
MOVE_AMOUNT = 5

SCORE_HIT = 1
SCORE_MISS = 5




class Point:
    def __init__(self):
        self.x = 0
        self.y = 0


class Velocity:
    def __init__(self):
        self.dx = 0
        self.dy = 0
    


class Ball:
    def __init__(self):
        self.center = Point()
        self.velocity = Velocity()        
        self.restart()                             #restart is defined as method, makes it easier to recall than duplicate
        
        
    def bounce_horizontal(self):
        self.velocity.dx *= -1                # CHANGES THE DIRECTIONS OF THE BALL IN THE X DIRECTION
      #  self.center.x = 385 
    
    def bounce_vertical(self):
         self.velocity.dy *= -1               #CHANGES THE DIRECTIONS OF THE BALL IN THE Y DIRECTION
            
         
         
    
    def draw(self):
        arcade.draw_circle_filled(self.center.x, self.center.y, BALL_RADIUS, arcade.color.RED)
        
        arcade.draw_text("TODAY IS MY BIRTHDAY!!!!.",
                         SCREEN_WIDTH //4, SCREEN_HEIGHT // 2, arcade.color.GREEN, 20)        
    def advance(self):
        self.center.x += self.velocity.dx
        self.center.y += self.velocity.dy


    def restart(self):
       # __init__(self)
        self.center.x = 0
        self.center.y = random.uniform(0,SCREEN_HEIGHT)
        self.velocity.dx = random.uniform(1,5)                              #Speed of the ball
        self.velocity.dy = random.uniform(1,5) 
        
class Paddle:
    def __init__(self):
        self.center = Point()
        self.center.x = SCREEN_WIDTH - 5              #SCREEN WIDTH -(PADDLE_HEIGHT/2)
        self.center.y= SCREEN_HEIGHT/2
    
    def move_up(self):
        if self.center.y <= SCREEN_HEIGHT-PADDLE_HEIGHT//2:
            self.center.y +=5
            
        
    
    def move_down(self):
        if self.center.y >= PADDLE_HEIGHT//2:
            self.center.y -=5
        
    def draw(self):
        arcade.draw_rectangle_filled(self.center.x, self.center.y,PADDLE_WIDTH, PADDLE_HEIGHT,arcade.color.PURPLE)
    

        
    
class Pong(arcade.Window):

    """
    
    This class handles all the game callbacks and interaction
    It assumes the following classes exist:
        Point
        Velocity
        Ball
        Paddle
    This class will then call the appropriate functions of
    each of the above classes.
    You are welcome to modify anything in this class,
    but should not have to if you don't want to.
    """
    
    def __init__(self, width, height):
    
        """
        Sets up the initial conditions of the game
        :param width: Screen width
        :param height: Screen height
        """
        super().__init__(width, height)

        self.ball = Ball()
        self.paddle = Paddle()
        self.score = 0

        # These are used to see if the user is
        # holding down the arrow keys
        self.holding_left = False
        self.holding_right = False

        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        """
        Called automatically by the arcade framework.
        Handles the responsiblity of drawing all elements.
        """

        # clear the screen to begin drawing
        arcade.start_render()

        # draw each object
        self.ball.draw()
        self.paddle.draw()

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

        # Move the ball forward one element in time
        self.ball.advance()

        # Check to see if keys are being held, and then
        # take appropriate action
        self.check_keys()

        # check for ball at important places
        self.check_miss()
        self.check_hit()
        self.check_bounce()

    def check_hit(self):
        """
        Checks to see if the ball has hit the paddle
        and if so, calls its bounce method.
        :return:
        """
        too_close_x = (PADDLE_WIDTH / 2) + BALL_RADIUS
        too_close_y = (PADDLE_HEIGHT / 2) + BALL_RADIUS

        if (abs(self.ball.center.x - self.paddle.center.x) < too_close_x and
                    abs(self.ball.center.y - self.paddle.center.y) < too_close_y and
                    self.ball.velocity.dx > 0):
            # we are too close and moving right, this is a hit!
            self.ball.bounce_horizontal()
            self.score += SCORE_HIT

    def check_miss(self):
        """
        Checks to see if the ball went past the paddle
        and if so, restarts it.
        """
        if self.ball.center.x > SCREEN_WIDTH:
            # We missed!
            self.score -= SCORE_MISS  
            self.ball.restart()

    def check_bounce(self):
        """
        Checks to see if the ball has hit the borders
        of the screen and if so, calls its bounce methods.
        """
        if self.ball.center.x < 0 and self.ball.velocity.dx < 0:
            self.ball.bounce_horizontal()

        if self.ball.center.y < 0 and self.ball.velocity.dy < 0:
            self.ball.bounce_vertical()

        if self.ball.center.y > SCREEN_HEIGHT and self.ball.velocity.dy > 0:
            self.ball.bounce_vertical()

    def check_keys(self):
        """
        Checks to see if the user is holding down an
        arrow key, and if so, takes appropriate action.
        """
        if self.holding_left:
            self.paddle.move_down()

        if self.holding_right:
            self.paddle.move_up()

    def on_key_press(self, key, key_modifiers):
        """
        Called when a key is pressed. Sets the state of
        holding an arrow key.
        :param key: The key that was pressed
        :param key_modifiers: Things like shift, ctrl, etc
        """
        if key == arcade.key.LEFT or key == arcade.key.DOWN:
            self.holding_left = True

        if key == arcade.key.RIGHT or key == arcade.key.UP:
            self.holding_right = True

    def on_key_release(self, key, key_modifiers):
        """
        Called when a key is released. Sets the state of
        the arrow key as being not held anymore.
        :param key: The key that was pressed
        :param key_modifiers: Things like shift, ctrl, etc
        """
        if key == arcade.key.LEFT or key == arcade.key.DOWN:
            self.holding_left = False

        if key == arcade.key.RIGHT or key == arcade.key.UP:
            self.holding_right = False

# Creates the game and starts it going
window = Pong(SCREEN_WIDTH, SCREEN_HEIGHT)
arcade.run()