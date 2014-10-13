import random, pygame, sys, math
from pygame.locals import *

FPS = 30
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
BGCOLOR = (60,60,100)

#Key Constants
UP = 'up'
DOWN = 'down'
RIGHT = 'right'
LEFT = 'left'

class Player:
    FRICTION = 0.6
    SPEED_LIMIT = 5
    GRAVITY = 0.8
    ACCELERATION = 1.5
    BOUNCE = -0.3
    JUMP_FORCE = -10
    BOTTOM_OFFSET = 0 #Pixels from the bottom of the window to the top of the ground

    def __init__(self, x, y):

        # Set image for player
        self.image = pygame.image.load('spellun-sprite.png')
        self.rect = self.image.get_rect()
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.x = x
        self.y = y
        self._accelerationX = 0
        self._accelerationY = 0
        self._vx = 0
        self._vy = 0
        self._isOnGround = True
        self._friction = self.FRICTION
        self._bounceX = 0
        self._bounceY = 0
        self._spriteFacing = 'right'

    def onKeyDown(self, event):
        if event.key == K_LEFT or event.key == K_RIGHT:
            #Player is moving so disable friction
            self._friction = 1

        if event.key == K_LEFT:
            self._accelerationX = -self.ACCELERATION
            if self._spriteFacing == 'right':
                self.image = pygame.transform.flip(self.image,True,False)
                self._spriteFacing = 'left'
        if event.key == K_RIGHT:
            self._accelerationX = self.ACCELERATION
            if self._spriteFacing == 'left':
                self.image = pygame.transform.flip(self.image,True,False)
                self._spriteFacing = 'right'
        if event.key == K_UP or event.key == K_SPACE:
            if self._isOnGround:
                self._accelerationY = self.JUMP_FORCE
                self._isOnGround = False


    def onKeyUp(self, event):
        if event.key == K_LEFT or event.key == K_RIGHT:
            self._accelerationX = 0
            self._friction = self.FRICTION
        if event.key == K_UP or event.key == K_SPACE:
            self._accelerationY = 0

    def update(self):
        #Apply Acceleration
        self._vx += self._accelerationX
        if self._vx > self.SPEED_LIMIT:
            self._vx = self.SPEED_LIMIT
        if self._vx < -self.SPEED_LIMIT:
            self._vx = -self.SPEED_LIMIT

        self._vy += self._accelerationY
        if self._vy > self.SPEED_LIMIT * 3:
            self._vy = self.SPEED_LIMIT * 3

        #Apply Friction
        if self._isOnGround:
            self._vx *= self._friction
        #Make sure velocity eventually reaches zero
        if math.fabs(self._vx) < 0.1:
            self._vx = 0
        if math.fabs(self._vy) < 0.1:
            self._vy = 0

        self._vy += self.GRAVITY

        #Apply bounce from collisions
        self.x += self._bounceX
        self.y += self._bounceY

        #Move Player
        self.x += self._vx
        self.y += self._vy

        #Reset platform bounce values
        self._bounceX = 0
        self._bounceY = 0

        #Prevent player from moving up if it's not on the ground
        if not self._isOnGround:
            self._accelerationY = 0

        if self._vy >= 0:
            self._isOnGround = False

        #Set window boundries
        if self.x + self.width > WINDOWWIDTH:
            self._vx = 0
            self.x = WINDOWWIDTH - self.width
        elif self.x < 0:
            self._vx = 0
            self.x = 0
        if self.y - self.height < 0:
            self._vy = 0
            self.y = 0 + self.height
        elif self.y + self.height > WINDOWHEIGHT - self.BOTTOM_OFFSET:
            self._vy *= self.BOUNCE
            self.y = WINDOWHEIGHT - self.height - self.BOTTOM_OFFSET
            self._isOnGround = True

def main():
    global FPSCLOCK, DISPLAYSURF
    pygame.init()

    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Platformer Test')
    player = Player(15, WINDOWHEIGHT - 32)

    while True:

        DISPLAYSURF.fill(BGCOLOR) #Drawing the window

        for event in pygame.event.get(): #event handling loop
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN :
                player.onKeyDown(event)
            if event.type == KEYUP :
                player.onKeyUp(event)

        player.update()
        DISPLAYSURF.blit(player.image, (player.x, player.y))

        pygame.display.update()
        FPSCLOCK.tick(FPS)


if __name__ == '__main__':
    main()