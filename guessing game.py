# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import random
from random import randint
print("Lets get guessy!")
my_seed = input("Enter random seed: ")
random.seed(my_seed)
number = random.randint(1,100)
attempted = 0


play_again = "yes"
while play_again == "yes":
    guess = 101
    number = random.randint(1,100)
    attempted = 0
    while guess != number:
        guess = int(input("Enter a guess: "))
        if guess < number:
            attempted = attempted + 1
            print("Guess higher", attempted, "attempt")
        elif guess > number:
            attempted= attempted + 1
            print("Guess lower", attempted, "attempt")
        else:
           attempted = attempted + 1 
           print("Congrats")
           print("It took you", attempted, "attempts")
    play_again = input("Would you like to play again(yes/no)?")

print("Thank you. Goodbye!!!")