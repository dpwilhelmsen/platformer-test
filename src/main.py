import random, pygame, sys
from pygame.locals import *

FPS = 30
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
BGCOLOR = (60,60,100)


def main():
    global FPSCLOCK, DISPLAYSURF
    pygame.init()

    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Platformer Test')

    while True:

        DISPLAYSURF.fill(BGCOLOR) #Drawing the window

        for event in pygame.event.get(): #event handling loop
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

        pygame.display.update()
        FPSCLOCK.tick(FPS)


if __name__ == '__main__':
    main()