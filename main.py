# Basic Animation Framework

from tkinter import *

import random, copy, math, sys

####################################
# customize these functions
####################################

class Player(object):
    def __init__(self, name, health, attack, cx, cy, r):
        # name
        self.name = name
        # health
        self.health = health
        # max health
        self.maxHealth = health
        # attack
        self.attack = attack
        # x-coordinate
        self.cx = cx
        # y-coordinate
        self.cy = cy
        # radius
        self.r = r
        # appearance (randomized)
        self.appearance = PhotoImage(file=str(random.randint(0, 3)) + ".gif")
        # health color
        self.healthColor="Green"

    def __repr__(self):
        return ("%s, health %d, attack %d" %
                (self.name, self.health, self.attack))
    def getHashables(self):
        return (self.name, self.health, self.attack)
    def __hash__(self):
        hash(self.getHashables())
    def __eq__(self, other):
        return (isinstance(other, self.__class__.__name__) and 
                self.getHashables() == other.getHashables())
    def draw(self, canvas):
        # create appearance
        canvas.create_image(self.cx, self.cy, image=self.appearance)
        canvas.create_text(self.cx, self.cy + 5,
                           text=self.health, fill=self.healthColor)
    def isCollision(self, other):
        # detect collision
        if ((other.cx - other.r <= self.cx <= other.cx + other.r) and
            (other.cy - other.r <= self.cy <= other.cy + other.r)):
            return True

class NPC(object):
    def __init__(self, health, attack, cx, cy, r, color):
        # health and max health
        self.health = health
        self.maxHealth = health
        # attack
        self.attack = attack
        # x and y coordinates
        self.cx = cx
        self.cy = cy
        # radius
        self.r = r
        # flag if dead
        self.dead = False
        # appearance
        self.appearance = PhotoImage(file="wiseau.gif")

    def __repr__(self):
        return "enemy, with health %d, attack %d" % (self.health, self.attack)
    def getHashables(self):
        return (self.health, self.attack)
    def __hash__(self):
        hash(self.getHashables())
    def __eq__(self, other):
        return (isinstance(other, self.__class__.__name__) and
                self.getHashables() == other.getHashables())
    def draw(self, canvas):
        # create appearance
        canvas.create_image(self.cx, self.cy, image=self.appearance)
        canvas.create_text(self.cx, self.cy + 5, text=self.health)
    def chasePlayer(self, other):
        # the enemy chases player
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
        # detect collision
        if ((other.cx - other.r <= self.cx <= other.cx + other.r) and
            (other.cy - other.r <= self.cy <= other.cy + other.r)):
            return True

class enemyOrb(object):
    # enemy's attack orbs (projectiles)
    def __init__(self, cx, cy, r):
        # x and y coordinates
        self.cx = cx
        self.cy = cy
        # radius
        self.r = r
        # usedUp flag
        self.usedUp = False
        # directions to move in
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
        return (isinstance(other, self.__class__.__name__) and
                self.getHashables() == other.getHashables())
    def draw(self, canvas):
        canvas.create_oval(self.cx - self.r, self.cy - self.r,
                           self.cx + self.r, self.cy + self.r, fill = "Red")
    def isCollision(self, other):
        if ((other.cx - other.r <= self.cx <= other.cx + other.r) and
            (other.cy - other.r <= self.cy <= other.cy + other.r)):
            return True

def randomColors():
    # returns a list of colors
    return (["Red", "Orange", "Yellow", "Green",
             "Cyan", "Blue", "Purple", "Indigo"])

class AttackOrb(object):
    # player's attack orbs
    def __init__(self, cx, cy, r):
        self.cx = cx
        self.cy = cy
        self.r = r
        self.usedUp = False
        self.color = randomColors()[random.randint(0, len(randomColors())-1)]

    def __repr__(self):
        return "an attack orb"
    def getHashables(self):
        return (self.cx, self.cy, self.r)
    def __hash__(self):
        hash(self.getHashables())
    def __eq__(self, other):
        return (isinstance(other, self.__class__.__name__) and
                self.getHashables() == other.getHashables())
    def draw(self, canvas):
        # draw the attack orb (projectile)
        canvas.create_oval(self.cx - self.r, self.cy - self.r,
                           self.cx + self.r, self.cy + self.r,
                           fill = self.color)
    def isCollision(self, other):
        # detect collision
        if ((other.cx - other.r <= self.cx <= other.cx + other.r) and
            (other.cy - other.r <= self.cy <= other.cy + other.r)):
            return True
    def homeIn(self, other):
        # home in toward enemies
        if other.cx + other.r < self.cx:
            self.cx -= 20
        elif other.cx - other.r > self.cx:
            self.cx += 20
        if other.cy + other.r < self.cy:
            self.cy -= 20
        elif other.cy - other.r > self.cy:
            self.cy += 20

class Spinach(object):
    # replenishes player's health
    def __init__(self, health, cx, cy, r):
        self.health = health
        self.cx = cx
        self.cy = cy
        self.r = r
        self.usedUp = False
        self.appearance = PhotoImage(file="spinach" + ".gif")

    def __repr__(self):
        return "spinach with health %d" % (self.health)
    def getHashables(self):
        return (self.health)
    def __hash__(self):
        hash(self.getHashables())
    def __eq__(self, other):
        return (isinstance(other, self.__class__.__name__) and
                self.getHashables() == other.getHashables())
    def draw(self, canvas):
        canvas.create_image(self.cx, self.cy, image=self.appearance)
        canvas.create_text(self.cx, self.cy + 5, text=self.health)

def init(data):
    # player
    data.Player = Player("Player", 50, 2, data.width // 2,
                         data.height // 2, 50)
    # lists of enemies and their projectiles
    data.enemyList = []
    data.enemyOrbList = []
    # spinach
    data.SpinachList = []
    # player's attack projectiles
    data.attackOrbList = []
    # timer call
    data.timerCall = 0
    # game over is initially set to false. set to true if health is 0.
    data.gameOver = False
    # score. increment it if enemy is defeated or another one spawns.
    data.score = 0

def mousePressedAction(event, data):
    pass

def mousePressed(event, data):
    if data.gameOver == False:
        mousePressedAction(event, data)

def keyPressedAction(event, data):
    # Move, wrap around when out of bounds
    if event.keysym == "Left":
        data.Player.cx -= 5
        if data.Player.cx < 0:
            data.Player.cx = data.width - data.Player.r * 2
    elif event.keysym == "Right":
        data.Player.cx += 5
        if data.Player.cx > data.width:
            data.Player.cx = data.Player.r * 2
    elif event.keysym == "Down":
        data.Player.cy += 5
        if data.Player.cy > data.height:
            data.Player.cy = data.Player.r * 2
    elif event.keysym == "Up":
        data.Player.cy -= 5
        if data.Player.cy < 0:
            data.Player.cy = data.height - data.Player.r * 2
    # fire only when there are enemies.
    elif event.keysym == "space" and data.enemyList != list():
        data.attackOrbList.append(AttackOrb(data.Player.cx, data.Player.cy,
                                            5))
        

def keyPressed(event, data):
    # wrapper for keyPressedAction, don't do anything if player dies
    if data.gameOver == False:
        keyPressedAction(event, data)

def ShooterEnemies(data):
    # enemies start firing their own projectiles
    for enemy in data.enemyList:
        x = random.randint(0, 100)
        if x % 20 == 0:
            data.enemyOrbList.append(enemyOrb(enemy.cx, enemy.cy, 5))

def upgradedShooterEnemies(data):
    # enemies fire more frequently
    for enemy in data.enemyList:
        x = random.randint(0, 100)
        if x % 7 == 0:
            data.enemyOrbList.append(enemyOrb(enemy.cx, enemy.cy, 5))

def moveEnemyOrbs(enemyOrb):
    # move enemyOrbs based on random direction
    enemyOrb.cx += enemyOrb.direction[0] * 5
    enemyOrb.cy += enemyOrb.direction[1] * 5

def outOfBoundsEnemyOrb(data, enemyOrb):
    # if enemy's attack projectile is out of bounds, use it up so it can
    # be removed.
    if enemyOrb.cx < 0 or enemyOrb.cx > data.width:
        enemyOrb.usedUp = True
    if enemyOrb.cy < 0 or enemyOrb.cy > data.height:
        enemyOrb.usedUp = True

def allEnemiesChaseYou(data):
    for enemy in data.enemyList:
        enemy.chasePlayer(data.Player)
        # if enemy runs out of health,
        # it dies and is removed from the list.
        if enemy.health <= 0:
            enemy.dead = True
            data.score += enemy.maxHealth
        # the player will be damaged if she is too close to an enemy.
        if data.Player.isCollision(enemy):
            if data.timerCall % 5 == 0: data.Player.health -= enemy.attack
            # the player dies if she runs out of health,
            # resulting in a game over.
            if data.Player.health <= 0:
                data.gameOver = True

def spawnEnemy(data):
    # spawn enemies with increasing difficulty after certain scores
    # have been reached.
    if 4000 > data.score >= 1500:
        data.enemyList.append(NPC(random.randint(200, 1000), 2,
        random.randint(0, data.width), random.randint(0, data.height), 50))
        data.score += 250
    elif data.score >= 4000:
        data.enemyList.append(NPC(random.randint(400, 2000), 5,
        random.randint(0, data.width), random.randint(0, data.height), 50))
        data.score += 500
    else:
        data.enemyList.append(NPC(random.randint(20, 500), 1,
        random.randint(0, data.width), random.randint(0, data.height), 50))
        data.score += 50

def spinachReplenishes(data):
    # use spinach for restoring health
    for spinach in data.SpinachList:
        if spinach.health <= 0:
            spinach.usedUp = True
        if data.Player.isCollision(spinach):
            if data.Player.health < data.Player.maxHealth:
                if data.timerCall % 5 == 0:
                    data.Player.health += 1
                    spinach.health -= 1

def attackOrbsCollide(data):
    # collide with enemies
    for attackOrb in data.attackOrbList:
        for enemy in data.enemyList:
            if attackOrb.isCollision(enemy):
                enemy.health -= data.Player.attack
                # use up orbs so that they are removed
                attackOrb.usedUp = True

def differentHealthColor(data):
    # health text is different color depending on health percentage
    if (data.Player.maxHealth // 4 < data.Player.health <=
        data.Player.maxHealth // 2):
        data.Player.healthColor = "Yellow"
    elif data.Player.health <= data.Player.maxHealth // 4:
        data.Player.healthColor = "Red"
    else:
        data.Player.healthColor = "Green"

def enemyPhases(data):
    # enemies will behave differently depending on score
    if 4000 > data.score >= 1500:
        # enemies shoot
        ShooterEnemies(data)
    elif data.score >= 4000:
        # enemies shoot more often
        upgradedShooterEnemies(data)
    for enemyOrb in data.enemyOrbList:
        # move orbs
        moveEnemyOrbs(enemyOrb)
        outOfBoundsEnemyOrb(data, enemyOrb)
        if enemyOrb.isCollision(data.Player):
            # damage the player
            data.Player.health -= 1
            # orb is now used up
            enemyOrb.usedUp = True

def attackOrbHomeIn(data):
    # get indices of enemy list. attack nearest enemy from indices.
    for attackOrb in data.attackOrbList:
        minEnemyDistance = None
        closestEnemyIndex = None
        for enemyIndex in range(len(data.enemyList)):
            enemyDistance = (
            int((((data.enemyList[enemyIndex].cx - attackOrb.cx) ** 2) +
            ((data.enemyList[enemyIndex].cy - attackOrb.cy) ** 2)) ** 0.5))
            if minEnemyDistance == None or enemyDistance < minEnemyDistance:
                minEnemyDistance = enemyDistance
                closestEnemyIndex = enemyIndex
        attackOrb.homeIn(data.enemyList[closestEnemyIndex])

def entityComprehensions(data):
    # comprehensions for entity lists
    # list comprehension for removing dead enemies
    data.enemyList = ([enemy for enemy in data.enemyList
                       if enemy.dead == False])
    # remove used-up spinach
    data.SpinachList = ([spinach for spinach in data.SpinachList
                         if spinach.usedUp == False])
    # list comprehension for removing used-up attack orbs
    data.attackOrbList = ([attackOrb for attackOrb in data.attackOrbList
                           if attackOrb.usedUp == False])
    # list comprehension for removing used-up enemy attack orbs
    data.enemyOrbList = ([enemyOrb for enemyOrb in data.enemyOrbList
                          if enemyOrb.usedUp == False])

def timerFiredAction(data):
    # spawn enemies once every 10 seconds
    if data.timerCall % 1000 == 0:
        spawnEnemy(data)
    # only one spinach at any time
    if (data.timerCall % 1500 == 0 and
    data.SpinachList == list() and data.timerCall != 0):
        data.SpinachList.append(Spinach(random.randint(20, 100),
        random.randint(0, data.width), random.randint(0, data.height), 50))
    # any enemy should chase the player if she is close to it.
    allEnemiesChaseYou(data)
    # spinach appears once in a while.
    # It can heal the player but also run out of
    # fuel if used too long, and disappear.
    spinachReplenishes(data)
    # attack orbs, generated by the player, home in on nearest enemy
    attackOrbsCollide(data)
    # remove attack orbs if nothing to attack
    if data.enemyList == list():
        data.attackOrbList = list()
    # home in on nearest enemy
    attackOrbHomeIn(data)
    ### More difficulty: Enemies shoot projectiles in random directions!
    enemyPhases(data)
    # health text is different color depending on health percentage
    differentHealthColor(data)
    # list comprehensions to remove usedUp entities
    entityComprehensions(data)
    # timer call
    data.timerCall += 1

def timerFired(data):
    # keep going until player dies
    if data.gameOver == False:
        timerFiredAction(data)
        
def gameOverScreen(canvas, data):
    # game over, when player dies
    canvas.create_text(data.width // 2, data.height // 2, anchor="s", text="You died. Final Score: %d" % (data.score), fill="Red", font="Helvetica 56 bold")

def redrawAll(canvas, data):
    # draw in canvas
    canvas.create_rectangle(0, 0, data.width, data.height, fill = "black", width=0)
    # if game is not over
    if data.gameOver == False:
        data.Player.draw(canvas)
    else:
        # game is over
        gameOverScreen(canvas, data)
    # draw all entities
    for enemy in data.enemyList:
        enemy.draw(canvas)
    for spinach in data.SpinachList:
        spinach.draw(canvas)
    for attackOrb in data.attackOrbList:
        attackOrb.draw(canvas)
    for enemyOrb in data.enemyOrbList:
        enemyOrb.draw(canvas)
    # score!
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
