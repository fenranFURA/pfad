# import pygame, to get all the pygame functionalities, rendering, starting game, exit .. etc
import pygame
# We now import all modules built by us in the project.
from Game import *
from Game.Scenes import *
from Game.Shared import *


class Breakout:

    def __init__(self):
        # We start with 5 lives and 0 score
        self.__lives = 1
        self.__score = 0

        # Create a level handler object
        self.__level = Level(self)
        # Load level 1
        self.__level.load(0)

        # create a new pad
        self.__pad = Pad((GameConstants.SCREEN_SIZE[0] / 2,
                          GameConstants.SCREEN_SIZE[1] - GameConstants.PAD_SIZE[1]),
                         pygame.image.load(GameConstants.SPRITE_PAD)
                         )

        self.__balls = [
            Ball((400, 400), pygame.image.load(GameConstants.SPRITE_BALL), self)
        ]


        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption("Game Programming with Python & PyGame")

        self.__clock = pygame.time.Clock()

        self.screen = pygame.display.set_mode(GameConstants.SCREEN_SIZE,
                                              pygame.DOUBLEBUF, 32)

        # set mouse to invisible, make game more awesome
        pygame.mouse.set_visible(0)

        # Create multiple scenes for this game and store them in a tuple
        self.__scenes = (
            PlayingGameScene(self),
            GameOverScene(self),
            HighscoreScene(self),
            MenuScene(self)
        )

        # Stores the current scene game is in
        self.__currentScene = 3

        self.__sounds = (
            pygame.mixer.Sound(GameConstants.SOUND_FILE_GAMEOVER),
            pygame.mixer.Sound(GameConstants.SOUND_FILE_HIT_BRICK),
            pygame.mixer.Sound(GameConstants.SOUND_FILE_HIT_BRICK_LIFE),
            pygame.mixer.Sound(GameConstants.SOUND_FILE_HIT_BRICK_SPEED),
            pygame.mixer.Sound(GameConstants.SOUND_FILE_HIT_WALL),
            pygame.mixer.Sound(GameConstants.SOUND_FILE_HIT_PAD) )


    def start(self):
        # Game loop, it has to keep running to run the game
        while 1:
            # set fps for the game, now the following code
            # will be only executed 100 times per second and not
            # every cpu tick
            self.__clock.tick(100)

            # fill the screen with black color. gets the screen
            # ready for the next screen render.
            self.screen.fill((0, 0, 0))

            # get a copy of reference object from scene list of
            # all scenes
            currentScene = self.__scenes[self.__currentScene]
            # Send events buffer to current scene every tick
            currentScene.handleEvents(pygame.event.get())
            # Render the current scene
            currentScene.render()

            # Update the display with the new data
            pygame.display.update()

            # loop continues . . .


    def changeScene(self, scene):
        self.__currentScene = scene

    def getLevel(self):
        return self.__level

    def getScore(self):
        return  self.__score

    def increaseScore(self, score):
        self.__score += score

    def getLives(self):
        return self.__lives

    def getBalls(self):
        return self.__balls

    def getPad(self):
        return self.__pad

    def playSound(self, soundClip):
        sound = self.__sounds[soundClip]

        sound.stop()
        sound.play()

    def reduceLives(self):
        self.__lives -= 1

    def increaseLives(self):
        self.__lives += 1

    def reset(self):
        self.__lives = 5
        self.__score = 0
        self.__level.load(0)

    def getName(self):
        print("Name: Breakout object")


Breakout().start()