import pygame
from pygame.locals import *

from Control.pauser import Pause
from Model.constants import *
from Model.nodes import NodeGroup
from Model.pacman import Pacman
from Model.pacman2 import Pacman2
from Model.pellets import PelletGroup
from Model.ghosts import GhostGroup
from Model.fruit import Fruit
from Model.text import TextGroup
from View.sprites import LifeSprites, MazeSprites

class GameController(object):
    def __init__(self, STATE):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREENSIZE, 0, 32)
        self.background = None
        self.clock = pygame.time.Clock()
        self.fruit = None
        self.pause = Pause(True)
        self.level = 0
        self.lives = 5
        self.score = 0
        self.score2 = 0
        self.STATE = STATE
        self.textgroup = TextGroup(self.STATE)
        self.lifesprites = LifeSprites(self.lives)

    def restartGame(self):
        self.lives = 5
        self.level = 0
        self.pause.paused = True
        self.fruit = None
        self.startGame()
        self.textgroup.showText(READYTXT)
        self.score = 0
        self.textgroup.updateScore(self.score)
        self.textgroup.updateLevel(self.level)
        self.lifesprites = LifeSprites(self.lives)

    def resetLevel(self):
        self.pause.paused = True
        self.pacman.reset()
        self.ghosts.reset()
        self.fruit = None
        self.textgroup.showText(READYTXT)
        self.lifesprites.resetLives(self.lives)

    def nextLevel(self):
        self.showEntities()
        self.level += 1
        self.pause.paused = True
        self.startGame()
        self.textgroup.updateLevel(self.level)
        self.textgroup.showText(READYTXT)

    def setBackground(self):
        self.background = pygame.surface.Surface(SCREENSIZE).convert()
        self.background.fill(BLACK)

    def startGame(self):
        # self.mazedata.loadMaze(self.level)
        self.setBackground()
        self.mazesprites = MazeSprites("map/maze1.txt", "map/maze1_rotation.txt")
        self.background = self.mazesprites.constructBackground(self.background, self.level % 5)
        self.nodes = NodeGroup("map/maze1.txt")
        self.nodes.setPortalPair((0, 17), (27, 17))
        homekey = self.nodes.createHomeNodes(11.5, 14)
        self.nodes.connectHomeNodes(homekey, (12, 14), LEFT)
        self.nodes.connectHomeNodes(homekey, (15, 14), RIGHT)
        self.pacman = Pacman(self.nodes.getNodeFromTiles(15, 26))  #(1, 4)
        self.nodes.denyHomeAccess(self.pacman)
        if self.STATE == STATE2:
            self.pacman2 = Pacman2(self.nodes.getNodeFromTiles(12, 8)) # Trường hợp chơi 2 nguời
            self.nodes.denyHomeAccess(self.pacman2)
        else:
            self.ghosts = GhostGroup(self.nodes.getStartTempNode(), self.pacman)
            self.ghosts.blinky.setStartNode(self.nodes.getNodeFromTiles(2 + 11.5, 0 + 14))
            self.ghosts.pinky.setStartNode(self.nodes.getNodeFromTiles(2 + 11.5, 3 + 14))
            self.ghosts.inky.setStartNode(self.nodes.getNodeFromTiles(0 + 11.5, 3 + 14))
            self.ghosts.clyde.setStartNode(self.nodes.getNodeFromTiles(4 + 11.5, 3 + 14))
            self.ghosts.setSpawnNode(self.nodes.getNodeFromTiles(2+11.5, 3+14))
            # khi bắt đầu phải từ nhà đi ra
            self.nodes.denyHomeAccessList(self.ghosts)
            self.nodes.denyAccessList(2 + 11.5, 3 + 14, LEFT, self.ghosts)
            self.nodes.denyAccessList(2 + 11.5, 3 + 14, RIGHT, self.ghosts)
            self.ghosts.inky.startNode.denyAccess(RIGHT, self.ghosts.inky)
            self.ghosts.clyde.startNode.denyAccess(LEFT, self.ghosts.clyde)
            self.nodes.denyAccessList(12, 14, UP, self.ghosts)
            self.nodes.denyAccessList(15, 14, UP, self.ghosts)
            self.nodes.denyAccessList(12, 26, UP, self.ghosts)
            self.nodes.denyAccessList(15, 26, UP, self.ghosts)
        self.pellets = PelletGroup("map/maze1.txt")

    def update(self):
        dt = self.clock.tick(30) / 1000.0 # delta time = tg hiện tại - tg trước
        self.textgroup.update(dt)
        self.pellets.update(dt)
        if not self.pause.paused:
            self.pacman.update(dt)
            if self.STATE == STATE2:
                self.pacman2.update(dt)
            else:
                self.ghosts.update(dt)
                self.checkGhostEvents()

            if self.fruit is not None:
                self.fruit.update(dt)
            self.checkPelletEvents()
            self.checkFruitEvents()

        afterPauseMethod = self.pause.update(dt)
        if afterPauseMethod is not None:
            afterPauseMethod()
        self.checkEvents()
        self.render()

    def updateScore(self, points):
        self.score += points
        self.textgroup.updateScore(self.score)

    def updateScore2(self, points):
        self.score2 += points
        self.textgroup.updateScore2(self.score2)

    def checkFruitEvents(self):
        if self.pellets.numEaten == 50 or self.pellets.numEaten == 140:
            if self.fruit is None:
                self.fruit = Fruit(self.nodes.getNodeFromTiles(9, 20))
        if self.fruit is not None:
            if self.pacman.collideCheck(self.fruit):
                self.updateScore(self.fruit.points)
                self.textgroup.addText(str(self.fruit.points), WHITE, self.fruit.position.x,
                                       self.fruit.position.y, 8, time=1)
                self.fruit = None
            elif STATE == STATE2 and self.pacman2.collideCheck(self.fruit):
                self.updateScore2(self.fruit.points)
                self.textgroup.addText(str(self.fruit.points), WHITE, self.fruit.position.x,
                                       self.fruit.position.y, 8, time=1)
                self.fruit = None
            elif self.fruit.destroy:
                self.fruit = None

    def checkGhostEvents(self):
        for ghost in self.ghosts:
            if self.pacman.collideGhost(ghost):
                if ghost.mode.current is FREIGHT:
                    self.pacman.visible = False
                    ghost.visible = False
                    self.updateScore(ghost.points)
                    ## khi ăn ghost
                    self.textgroup.addText(str(ghost.points), WHITE, ghost.position.x, ghost.position.y, 8, time=1)
                    self.ghosts.updatePoints()
                    self.pause.setPause(pauseTime=0, func=self.showEntities())
                    ghost.startSpawn()
                    self.nodes.allowHomeAccess(ghost)
                elif ghost.mode.current is not SPAWN:
                    if self.pacman.alive:
                        self.lives -= 1
                        self.lifesprites.removeImage()
                        self.pacman.die()
                        self.ghosts.hide()
                        if self.lives <= 0:
                            self.textgroup.showText(GAMEOVERTXT)
                            ## khi gameover
                            self.pause.setPause(pauseTime=3, func=self.restartGame)
                        else:
                            self.pause.setPause(pauseTime=3, func=self.resetLevel)

    def showEntities(self):
        self.pacman.visible = True
        if self.STATE == STATE1:
            self.ghosts.show()
        else:
            self.pacman2.visible = True

    def hideEntities(self):
        self.pacman.visible = False
        if self.STATE == STATE1:
            self.ghosts.hide()
        else:
            self.pacman2.visible = False

    def checkEvents(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    if self.pacman.alive:
                        self.pause.setPause(playerPaused=True)
                        if not self.pause.paused:
                            self.textgroup.hideText()
                            self.showEntities()
                        else:
                            self.textgroup.showText(PAUSETXT)
                            self.hideEntities()

    def render(self):
        self.screen.blit(self.background, (0, 0))
        self.pellets.render(self.screen)
        if self.fruit is not None:
            self.fruit.render(self.screen)
        self.pacman.render(self.screen)
        if self.STATE == STATE1:
            self.ghosts.render(self.screen)
        else:
            self.pacman2.render(self.screen)
        self.textgroup.render(self.screen)

        for i in range(len(self.lifesprites.images)):
            x = self.lifesprites.images[i].get_width() * i
            y = SCREENHEIGHT - self.lifesprites.images[i].get_height()
            self.screen.blit(self.lifesprites.images[i], (x, y))

        pygame.display.update()

    def checkPelletEvents(self):
        if self.STATE == STATE1:
            pellet = self.pacman.eatPellets(self.pellets.pelletList)
            if pellet:
                self.pellets.numEaten += 1
                self.updateScore(pellet.points)
                ## sound khi ăn
                if self.pellets.numEaten == 30:
                    self.ghosts.inky.startNode.allowAccess(RIGHT, self.ghosts.inky)
                if self.pellets.numEaten == 70:
                    self.ghosts.clyde.startNode.allowAccess(LEFT, self.ghosts.clyde)
                self.pellets.pelletList.remove(pellet)
                if pellet.name == POWERPELLET:
                    self.ghosts.startFreight()
                if self.pellets.isEmpty():
                    self.showEntities()
                    print(self.level)
                    if self.level == 0:
                        self.textgroup.showText(WINTXT)
                        saveScore(self.score)
                        self.pause.setPause(pauseTime=3, func=self.restartGame)
                        print(self.score)
                    else:
                        self.pause.setPause(pauseTime=3, func=self.nextLevel)

        elif STATE == STATE2:
            pellet = self.pacman.eatPellets(self.pellets.pelletList)
            pellet2 = self.pacman2.eatPellets(self.pellets.pelletList)
            if pellet:
                self.pellets.numEaten += 1
                self.updateScore(pellet.points)
                self.pellets.pelletList.remove(pellet)

            if pellet2:
                self.pellets.numEaten += 1
                self.updateScore2(pellet2.points)
                self.pellets.pelletList.remove(pellet2)

            if self.pellets.isEmpty():
                # self.hideEntities(STATE)
                self.textgroup.showText(WINPLAYER1 if self.score > self.score2 else WINPLAYER2)
                self.pause.setPause(pauseTime=3, func=self.nextLevel)


def saveScore(score):
    try:
        try:
            with open("asset/SaveScore.txt", "r") as file:
                hightScore = file.read().strip()
                if hightScore:
                    high_score = int(hightScore)
                else:
                    high_score = 0
        except FileNotFoundError:
            high_score = 0

        if score > high_score:
            with open("asset/SaveScore.txt", "w") as file:
                file.write(str(score))
    except IOError:
        print("Error: Unable to save high score.")

if __name__ == "__main__":
    STATE = STATE1
    game = GameController(STATE)
    game.startGame()
    while True:
        game.update()