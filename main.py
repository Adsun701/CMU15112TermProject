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
        self.maxHealth = health
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
        self.maxHealth = health
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
        if (other.__class__.__name__ == "Player" and other.health > 0):
            if other.cx + other.r < self.cx:
                self.cx -= 1
            elif other.cx - other.r > self.cx:
                self.cx += 1
            if other.cy + other.r < self.cy:
                self.cy -= 1
            elif other.cy - other.r > self.cy:
                self.cy += 1

class AttackOrb(object):
    def __init__(self, cx, cy, r):
        self.cx = cx
        self.cy = cy
        self.r = r
        self.usedUp = False

    def __repr__(self):
        return "an attack orb"
    def getHashables(self):
        return (self.cx, self.cy, self.r)
    def __hash__(self):
        hash(self.getHashables())
    def __eq__(self, other):
        return isinstance(other, self.__class__.__name__) and self.getHashables() == other.getHashables()
    def draw(self, canvas):
        canvas.create_oval(self.cx - self.r, self.cy - self.r, self.cx + self.r, self.cy + self.r, fill = "White")
    def isCollision(self, other):
        if ((other.cx - other.r <= self.cx <= other.cx + other.r) and
            (other.cy - other.r <= self.cy <= other.cy + other.r)):
            return True
    def homeIn(self, other):
        if other.cx + other.r < self.cx:
            self.cx -= 20
        elif other.cx - other.r > self.cx:
            self.cx += 20
        if other.cy + other.r < self.cy:
            self.cy -= 20
        elif other.cy - other.r > self.cy:
            self.cy += 20

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
    data.Emma = Player("Emma", "Female", 1, 50, 2, data.width // 2, data.height // 2, 50)
    data.enemyList = []
    data.healingOrbList = []
    data.attackOrbList = []
    data.timerCall = 0
    data.gameOver = False
    data.score = 0

def mousePressedAction(event, data):
    # use event.x and event.y
    for enemy in data.enemyList:
        enemy.health -= data.Emma.attack

def mousePressed(event, data):
    if data.gameOver == False:
        mousePressedAction(event, data)

def keyPressedAction(event, data):
    # Move, wrap around when out of bounds
    if event.keysym == "Left":
        data.Emma.cx -= 5
        if data.Emma.cx < 0:
            data.Emma.cx = data.width - data.Emma.r * 2
    elif event.keysym == "Right":
        data.Emma.cx += 5
        if data.Emma.cx > data.width:
            data.Emma.cx = data.Emma.r * 2
    elif event.keysym == "Down":
        data.Emma.cy += 5
        if data.Emma.cy > data.height:
            data.Emma.cy = data.Emma.r * 2
    elif event.keysym == "Up":
        data.Emma.cy -= 5
        if data.Emma.cy < 0:
            data.Emma.cy = data.height - data.Emma.r * 2
    elif event.keysym == "space" and data.enemyList != list() and len(data.attackOrbList) < 5:
        data.attackOrbList.append(AttackOrb(data.Emma.cx, data.Emma.cy, 5))
        

def keyPressed(event, data):
    if data.gameOver == False:
        keyPressedAction(event, data)

def timerFiredAction(data):
    data.timerCall += 1
    if data.timerCall % 500 == 0:
        data.enemyList.append(NPC("Wiseau", "Male", 5, random.randint(20, 500), 10, random.randint(0, data.width), random.randint(0, data.height), 50))
        data.score += 50
    # only one healing orb at any time
    if data.timerCall % 5000 == 0 and data.healingOrbList == list():
        data.healingOrbList.append(HealingOrb("Danielle", "Female", 50, 100, 10, random.randint(0, data.width), random.randint(0, data.height), 50))
    # any enemy should chase the player if she is close to it.
    for enemy in data.enemyList:
        enemy.chasePlayer(data.Emma)
        # if enemy runs out of health,
        # it dies and is removed from the list.
        if enemy.health <= 0:
            enemy.dead = True
            data.score += enemy.maxHealth
        # the player will be damaged if she is too close to an enemy.
        if data.Emma.isCollision(enemy):
            if data.timerCall % 5 == 0: data.Emma.health -= 1
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
            if data.Emma.health < 50:
                if data.timerCall % 5 == 0:
                    data.Emma.health += 1
                    orb.health -= 1
    # remove used-up orbs
    data.healingOrbList = [orb for orb in data.healingOrbList if orb.usedUp == False]
    # attack orbs, generated by the player, home in on nearest enemy
    for attackOrb in data.attackOrbList:
        for enemy in data.enemyList:
            if attackOrb.isCollision(enemy):
                enemy.health -= data.Emma.attack
                attackOrb.usedUp = True
    # list comprehension for removing used-up attack orbs
    data.attackOrbList = [attackOrb for attackOrb in data.attackOrbList if attackOrb.usedUp == False]
    # remove attack orbs if nothing to attack
    if data.enemyList == list():
        data.attackOrbList = list()
    # get indices of enemy list. attack nearest enemy from indices.
    for attackOrb in data.attackOrbList:
        minEnemyDistance = None
        closestEnemyIndex = None
        for enemyIndex in range(len(data.enemyList)):
            enemyDistance = int((((data.enemyList[enemyIndex].cx - attackOrb.cx) ** 2) + ((data.enemyList[enemyIndex].cy - attackOrb.cy) ** 2)) ** 0.5)
            if minEnemyDistance == None or enemyDistance < minEnemyDistance:
                minEnemyDistance = enemyDistance
                closestEnemyIndex = enemyIndex
        attackOrb.homeIn(data.enemyList[closestEnemyIndex])
        

def timerFired(data):
    # keep going until player dies
    if data.gameOver == False:
        timerFiredAction(data)
        

def gameOverScreen(canvas, data):
    canvas.create_text(data.width // 2, data.height // 2, anchor="s", text="You died. Final Score: %d" % (data.score), fill="Red", font="Helvetica 56 bold")

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
    for attackOrb in data.attackOrbList:
        attackOrb.draw(canvas)
    canvas.create_text(300, 300, text=data.score, fill="Magenta", font="Helvetica 56 bold")

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
    data.timerDelay = 5 # milliseconds
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
