### Simple script to create the illusion of a moving wall
### Designed by Samantha Bookholder, 2019


import os
import keyboard
from time import sleep


def ask(text): # type each question out, like a typewriter
    for x in text:
        sleep(0.03)
        print(x, end="", flush=True)
    x = int(input("\n"))
    return x


cls = lambda: os.system('cls')
brick = "|___"
n = 587
wall_width = ask("How many bricks wide should your wall be?")
wall_height = ask("How many bricks tall should your wall be?")
cls()


#prints individual brick
# while n < 4, print the nth item (mod 4) in the string/list "brick", shifted by x
def printbrick(x):
    i = 0
    j = 0
    while i < 4:
        char = brick[(j + x) % 4]
        print(char, end="")
        j+=1
        i+=1

#prints row of bricks
def printrow(x):        
    i = 0
    while i <= wall_width - 1:
        printbrick(x)
        i += 1

def printcol(x):
    i = 0
    while i <= wall_height - 1:
        printrow(x)
        print("\n")
        i += 1

### Endlessly Moving Wall ###
def scroll(x):  
    while True:
        y = x % 4
        cls()
        printcol(y)
        x += 1
        sleep(1)
    
def keypress():
    n = 587
    while True:
        if keyboard.is_pressed("z"):
            cls()
            n = n - 1   # clear the screen, print a new wall shifted one to the left
            y = n % 4   # % operator means we're operating in mod-4 arithmetic
            printcol(y)
        if keyboard.is_pressed("/"):
            cls()
            n = n + 1
            y = n % 4
            printcol(y)
        if keyboard.is_pressed("q"):
            scroll(n)
            
            

printcol(3)
keypress()
