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
        self.appearance = PhotoImage(file=str(random.randint(0, 2)) + ".gif")
        self.healthColor="Green"

    def __repr__(self):
        return "%s, level %d, health %d, attack %d" % (self.name, self.level, self.health, self.attack)
    def getHashables(self):
        return (self.name, self.gender, self.level, self.health, self.attack)
    def __hash__(self):
        hash(self.getHashables())
    def __eq__(self, other):
        return isinstance(other, self.__class__.__name__) and self.getHashables() == other.getHashables()
    def draw(self, canvas):
        canvas.create_image(self.cx, self.cy, image=self.appearance)
        canvas.create_text(self.cx, self.cy + 5, text=self.health, fill=self.healthColor)
    def isCollision(self, other):
        if ((other.cx - other.r <= self.cx <= other.cx + other.r) and
            (other.cy - other.r <= self.cy <= other.cy + other.r)):
            return True

class NPC(object):
    def __init__(self, name, gender, level, health, attack, cx, cy, r, color = "Red"):
        self.name = name
        self.gender = gender
        self.level = level
        self.health = health
        self.maxHealth = health
        self.attack = attack
        self.cx = cx
        self.cy = cy
        self.r = r
        self.originalR = r
        self.dead = False
        self.color = color
        self.appearance = PhotoImage(file="wiseau.gif")

    def __repr__(self):
        return "%s, level %d, health %d, attack %d" % (self.name, self.level, self.health, self.attack)
    def getHashables(self):
        return (self.name, self.gender, self.level, self.health, self.attack)
    def __hash__(self):
        hash(self.getHashables())
    def __eq__(self, other):
        return isinstance(other, self.__class__.__name__) and self.getHashables() == other.getHashables()
    def draw(self, canvas):
        canvas.create_image(self.cx, self.cy, image=self.appearance)
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
    def isCollision(self, other):
        if ((other.cx - other.r <= self.cx <= other.cx + other.r) and
            (other.cy - other.r <= self.cy <= other.cy + other.r)):
            return True

class EnemyAttackOrb(object):
    def __init__(self, cx, cy, r):
        self.cx = cx
        self.cy = cy
        self.r = r
        self.usedUp = False
        # West, East, South, North, Northwest, Northeast, Southwest, Southeast
        self.direction = ([(1, 0), (-1, 0), (0, 1), (0, -1),
        (-1, -1), (1, -1), (-1, 1), (1, 1)][random.randint(0, 7)])

    def __repr__(self):
        return "an attack orb from the enemy"
    def getHashables(self):
        return (self.cx, self.cy, self.r)
    def __hash__(self):
        hash(self.getHashables())
    def __eq__(self, other):
        return isinstance(other, self.__class__.__name__) and self.getHashables() == other.getHashables()
    def draw(self, canvas):
        canvas.create_oval(self.cx - self.r, self.cy - self.r, self.cx + self.r, self.cy + self.r, fill = "Red")
    def isCollision(self, other):
        if ((other.cx - other.r <= self.cx <= other.cx + other.r) and
            (other.cy - other.r <= self.cy <= other.cy + other.r)):
            return True
        

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
        self.appearance = PhotoImage(file="spinach" + ".gif")

    def __repr__(self):
        return "%s, level %d, health %d, healing %d" % (self.name, self.level, self.health, self.healing)
    def getHashables(self):
        return (self.name, self.gender, self.level, self.health, self.healing)
    def __hash__(self):
        hash(self.getHashables())
    def __eq__(self, other):
        return isinstance(other, self.__class__.__name__) and self.getHashables() == other.getHashables()
    def draw(self, canvas):
        canvas.create_image(self.cx, self.cy, image=self.appearance)
        canvas.create_text(self.cx, self.cy + 5, text=self.health)

def init(data):
    data.Emilia = Player("Emilia", "Female", 1, 50, 2, data.width // 2, data.height // 2, 50)
    data.enemyList = []
    data.enemyAttackOrbList = []
    data.healingOrbList = []
    data.attackOrbList = []
    data.timerCall = 0
    data.gameOver = False
    data.score = 0

def mousePressedAction(event, data):
    # use event.x and event.y
    for enemy in data.enemyList:
        enemy.health -= data.Emilia.attack

def mousePressed(event, data):
    if data.gameOver == False:
        mousePressedAction(event, data)

def keyPressedAction(event, data):
    # Move, wrap around when out of bounds
    if event.keysym == "Left":
        data.Emilia.cx -= 5
        if data.Emilia.cx < 0:
            data.Emilia.cx = data.width - data.Emilia.r * 2
    elif event.keysym == "Right":
        data.Emilia.cx += 5
        if data.Emilia.cx > data.width:
            data.Emilia.cx = data.Emilia.r * 2
    elif event.keysym == "Down":
        data.Emilia.cy += 5
        if data.Emilia.cy > data.height:
            data.Emilia.cy = data.Emilia.r * 2
    elif event.keysym == "Up":
        data.Emilia.cy -= 5
        if data.Emilia.cy < 0:
            data.Emilia.cy = data.height - data.Emilia.r * 2
    # fire only when there are enemies.
    elif event.keysym == "space" and data.enemyList != list():
        data.attackOrbList.append(AttackOrb(data.Emilia.cx, data.Emilia.cy, 5))
        

def keyPressed(event, data):
    if data.gameOver == False:
        keyPressedAction(event, data)

def ShooterEnemies(data):
    for enemy in data.enemyList:
        x = random.randint(0, 100)
        if x % 20 == 0:
            data.enemyAttackOrbList.append(EnemyAttackOrb(enemy.cx, enemy.cy, 5))

def moveEnemyAttackOrbs(enemyAttackOrb):
    # move enemyAttackOrbs based on random direction
    enemyAttackOrb.cx += enemyAttackOrb.direction[0] * 5
    enemyAttackOrb.cy += enemyAttackOrb.direction[1] * 5

def outOfBoundsEnemyAttackOrb(data, enemyAttackOrb):
    if enemyAttackOrb.cx < 0 or enemyAttackOrb.cx > data.width:
        enemyAttackOrb.usedUp = True
    if enemyAttackOrb.cy < 0 or enemyAttackOrb.cy > data.height:
        enemyAttackOrb.usedUp = True

def timerFiredAction(data):
    data.timerCall += 1
    if data.timerCall % 500 == 0:
        if data.score >= 1500:
            data.enemyList.append(NPC("Chris-R", "Male", 5, random.randint(200, 1000), 10, random.randint(0, data.width), random.randint(0, data.height), 50))
            data.score += 250
        else:
            data.enemyList.append(NPC("Wiseau", "Male", 5, random.randint(20, 500), 10, random.randint(0, data.width), random.randint(0, data.height), 50))
            data.score += 50
    # only one healing orb at any time
    if data.timerCall % 5000 == 0 and data.healingOrbList == list():
        data.healingOrbList.append(HealingOrb("Danielle", "Female", 50, 100, 10, random.randint(0, data.width), random.randint(0, data.height), 50))
    # any enemy should chase the player if she is close to it.
    for enemy in data.enemyList:
        enemy.chasePlayer(data.Emilia)
        # if enemy runs out of health,
        # it dies and is removed from the list.
        if enemy.health <= 0:
            enemy.dead = True
            data.score += enemy.maxHealth
        # the player will be damaged if she is too close to an enemy.
        if data.Emilia.isCollision(enemy):
            if data.timerCall % 5 == 0: data.Emilia.health -= 1
            # the player dies if she runs out of health,
            # resulting in a game over.
            if data.Emilia.health <= 0:
                data.gameOver = True
    # list comprehension for removing dead enemies
    data.enemyList = [enemy for enemy in data.enemyList if enemy.dead == False]
    # Healing orbs appear half as frequently as enemies.
    # They can heal the player but also run out of
    # fuel if used too long, and disappear.
    for orb in data.healingOrbList:
        if orb.health <= 0:
            orb.usedUp = True
        if data.Emilia.isCollision(orb):
            if data.Emilia.health < data.Emilia.maxHealth:
                if data.timerCall % 5 == 0:
                    data.Emilia.health += 1
                    orb.health -= 1
    # remove used-up orbs
    data.healingOrbList = [orb for orb in data.healingOrbList if orb.usedUp == False]
    # attack orbs, generated by the player, home in on nearest enemy
    for attackOrb in data.attackOrbList:
        for enemy in data.enemyList:
            if attackOrb.isCollision(enemy):
                enemy.health -= data.Emilia.attack
                attackOrb.usedUp = True
    # list comprehension for removing used-up attack orbs
    data.attackOrbList = [attackOrb for attackOrb in data.attackOrbList if attackOrb.usedUp == False]
    # remove attack orbs if nothing to attack
    if data.enemyList == list():
        data.attackOrbList = list()
    
    # list comprehension for removing used-up enemy attack orbs
    data.enemyAttackOrbList = [enemyAttackOrb for enemyAttackOrb in data.enemyAttackOrbList if enemyAttackOrb.usedUp == False]
    
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
    
    ### More difficulty: Enemies shoot projectiles in four cardinal directions!
    if data.score >= 1500:
        ShooterEnemies(data)
    for enemyAttackOrb in data.enemyAttackOrbList:
        # move orbs
        moveEnemyAttackOrbs(enemyAttackOrb)
        if enemyAttackOrb.isCollision(data.Emilia):
            # damage the player
            data.Emilia.health -= 1
            # orb is now used up
            enemyAttackOrb.usedUp = True
    
    # health text is different color depending on health percentage
    if data.Emilia.maxHealth // 4 < data.Emilia.health <= data.Emilia.maxHealth // 2:
        data.Emilia.healthColor = "Yellow"
    elif data.Emilia.health <= data.Emilia.maxHealth // 4:
        data.Emilia.healthColor = "Red"
    else:
        data.Emilia.healthColor = "Green"

def timerFired(data):
    # keep going until player dies
    if data.gameOver == False:
        timerFiredAction(data)
        
def gameOverScreen(canvas, data):
    canvas.create_text(data.width // 2, data.height // 2, anchor="s", text="You died. Final Score: %d" % (data.score), fill="Red", font="Helvetica 56 bold")

def redrawAll(canvas, data):
    # draw in canvas
    canvas.create_rectangle(0, 0, data.width, data.height, fill = "black", width=0)
    # if game is not over
    if data.gameOver == False:
        data.Emilia.draw(canvas)
    else:
        # game is over
        gameOverScreen(canvas, data)
    for enemy in data.enemyList:
        enemy.draw(canvas)
    for orb in data.healingOrbList:
        orb.draw(canvas)
    for attackOrb in data.attackOrbList:
        attackOrb.draw(canvas)
    for enemyOrb in data.enemyAttackOrbList:
        enemyOrb.draw(canvas)
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
