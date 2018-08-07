# Basic Animation Framework

from tkinter import *
import random, copy, math, sys

####################################
# customize these functions
####################################

class Player(object):
    def __init__(self, name, gender, level, health, attack, cx, cy, r):
        self.name = name
        self.gender = gender
        self.level = level
        self.health = health
        self.attack = attack
        self.cx = cx
        self.cy = cy
        self.r = r

    def __repr__(self):
        return "%s, level %d, health %d, attack %d" % (self.name, self.level, self.health, self.attack)
    def getHashables(self):
        return (self.name, self.gender, self.level, self.health, self.attack)
    def __hash__(self):
        hash(self.getHashables())
    def __eq__(self, other):
        return isinstance(other, self.__class__.__name__) and self.getHashables() == other.getHashables()
    def draw(self, canvas):
        canvas.create_oval(self.cx - self.r, self.cy - self.r, self.cx + self.r, self.cy + self.r, fill = "yellow")
        canvas.create_text(self.cx, self.cy + 5, text=self.health)
    def isCollision(self, other):
        if ((other.cx - other.r <= self.cx <= other.cx + other.r) and
            (other.cy - other.r <= self.cy <= other.cy + other.r)):
            return True

class NPC(object):
    def __init__(self, name, gender, level, health, attack, cx, cy, r):
        self.name = name
        self.gender = gender
        self.level = level
        self.health = health
        self.attack = attack
        self.cx = cx
        self.cy = cy
        self.r = r
        self.dead = False

    def __repr__(self):
        return "%s, level %d, health %d, attack %d" % (self.name, self.level, self.health, self.attack)
    def getHashables(self):
        return (self.name, self.gender, self.level, self.health, self.attack)
    def __hash__(self):
        hash(self.getHashables())
    def __eq__(self, other):
        return isinstance(other, self.__class__.__name__) and self.getHashables() == other.getHashables()
    def draw(self, canvas):
        canvas.create_oval(self.cx - self.r, self.cy - self.r, self.cx + self.r, self.cy + self.r, fill = "Red")
        canvas.create_text(self.cx, self.cy + 5, text=self.health)
    def chasePlayer(self, other):
        if ((other.__class__.__name__ == "Player" and other.health > 0) and
        (((other.cx - self.cx) ** 2 + (other.cy - self.cy) ** 2) ** 0.5) < 500):
            if other.cx + other.r < self.cx:
                self.cx -= 10
            elif other.cx - other.r > self.cx:
                self.cx += 10
            if other.cy + other.r < self.cy:
                self.cy -= 10
            elif other.cy - other.r > self.cy:
                self.cy += 10

class HealingOrb(object):
    def __init__(self, name, gender, level, health, healing, cx, cy, r):
        self.name = name
        self.gender = gender
        self.level = level
        self.health = health
        self.healing = healing
        self.cx = cx
        self.cy = cy
        self.r = r
        self.usedUp = False

    def __repr__(self):
        return "%s, level %d, health %d, healing %d" % (self.name, self.level, self.health, self.healing)
    def getHashables(self):
        return (self.name, self.gender, self.level, self.health, self.healing)
    def __hash__(self):
        hash(self.getHashables())
    def __eq__(self, other):
        return isinstance(other, self.__class__.__name__) and self.getHashables() == other.getHashables()
    def draw(self, canvas):
        canvas.create_oval(self.cx - self.r, self.cy - self.r, self.cx + self.r, self.cy + self.r, fill = "Cyan")
        canvas.create_text(self.cx, self.cy + 5, text=self.health)

def init(data):
    data.Emma = Player("Emma", "Female", 1, 50, 10, data.width // 2, data.height // 2, 50)
    data.enemyList = []
    data.healingOrbList = []
    data.timerCall = 0
    data.gameOver = False

def mousePressedAction(event, data):
    # use event.x and event.y
    for enemy in data.enemyList:
        enemy.health -= data.Emma.attack

def mousePressed(event, data):
    if data.gameOver == False:
        mousePressedAction(event, data)

def keyPressedAction(event, data):
    # use event.char and event.keysym
    if event.keysym == "Left":
        data.Emma.cx -= 10
    elif event.keysym == "Right":
        data.Emma.cx += 10
    elif event.keysym == "Up":
        data.Emma.cy -= 10
    elif event.keysym == "Down":
        data.Emma.cy += 10

def keyPressed(event, data):
    if data.gameOver == False:
        keyPressedAction(event, data)

def timerFiredAction(data):
    data.timerCall += 1
    if data.timerCall % 50 == 0:
        data.enemyList.append(NPC("Wiseau", "Male", 50, 100, 10, random.randint(0, data.width), random.randint(0, data.height), 50))
    if data.timerCall % 100 == 0:
        data.healingOrbList.append(HealingOrb("Danielle", "Female", 50, 100, 10, random.randint(0, data.width), random.randint(0, data.height), 50))
    # any enemy should chase the player if she is close to it.
    for enemy in data.enemyList:
        enemy.chasePlayer(data.Emma)
        # if enemy runs out of health,
        # it dies and is removed from the list.
        if enemy.health <= 0:
            enemy.dead = True
        # the player will be damaged if she is too close to an enemy.
        if data.Emma.isCollision(enemy):
            data.Emma.health -= 1
            # the player dies if she runs out of health,
            # resulting in a game over.
            if data.Emma.health <= 0:
                data.gameOver = True
    # list comprehension for removing dead enemies
    data.enemyList = [enemy for enemy in data.enemyList if enemy.dead == False]
    # Healing orbs appear half as frequently as enemies.
    # They can heal the player but also run out of
    # fuel if used too long, and disappear.
    for orb in data.healingOrbList:
        if orb.health <= 0:
            orb.usedUp = True
        if data.Emma.isCollision(orb):
            data.Emma.health += 1
            orb.health -= 1
    # remove used-up orbs
    data.healingOrbList = [orb for orb in data.healingOrbList if orb.usedUp == False]

def timerFired(data):
    if data.gameOver == False:
        timerFiredAction(data)
        

def gameOverScreen(canvas, data):
    canvas.create_text(data.width // 2, data.height // 2, anchor="s", text="You died.", fill="Red")

def redrawAll(canvas, data):
    # draw in canvas
    canvas.create_rectangle(0, 0, data.width, data.height, fill = "green", width=0)
    # if game is not over
    if data.gameOver == False:
        data.Emma.draw(canvas)
    else:
        # game is over
        gameOverScreen(canvas, data)
    for enemy in data.enemyList:
        enemy.draw(canvas)
    for orb in data.healingOrbList:
        orb.draw(canvas)

####################################
# use the run function as-is
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    root = Tk()
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(1920, 1080)
