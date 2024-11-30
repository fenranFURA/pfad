import pygame
from Game.Shared import *


class Ball(GameObject):

    def __init__(self, position, sprite, game):
        self.__game = game
        self.__speed = 3
        self.__increment = [2, 2]
        self.__direction = [1, 1]
        self.__inMotion = 0

        super(Ball, self).__init__(position, GameConstants.BALL_SIZE, sprite)

    def setSpeed(self, newSpeed):
        self.__speed = newSpeed

    def resetSpeed(self):
        self.setSpeed(3)

    def getSpeed(self):
        return self.__speed

    def isInMotion(self):
        return self.__inMotion

    def setMotion(self, isMoving):
        self.__inMotion = isMoving
        self.resetSpeed()

    def changeDirection(self, gameObject):
        ball = self.getPosition()
        ballSize = self.getSize()
        brick = gameObject.getPosition()
        brickSize = gameObject.getSize()

        X = 0
        Y = 1

        if ball[Y] > brick[Y] and \
                ball[Y] < brick[Y] + brickSize[Y] and \
                ball[X] > brick[X] and \
                ball[X] < brick[X] + brickSize[X]:
            self.setPosition((ball[X], brick[Y] + brickSize[Y]))
            self.__direction[Y] *= -1

        elif ball[Y] + ballSize[Y] > brick[Y] and \
                ball[Y] + ballSize[Y] < brick[Y] + brickSize[Y] and \
                ball[X] > brick[X] and \
                ball[X] < brick[X] + brickSize[X]:
            self.setPosition((ball[X], brick[Y] - brickSize[Y]))
            self.__direction[Y] *= -1

        elif ball[X] + ballSize[X] > brick[X] and \
                ball[X] + ballSize[X] < brick[X] + brickSize[X]:
            self.setPosition((brick[X] - ballSize[X], ball[Y]))
            self.__direction[X] *= -1

        else:
            self.setPosition((brick[X] + brickSize[X], ball[Y]))
            self.__direction[X] *= -1
            self.__direction[Y] *= -1
        

    def updatePosition(self):

        if not self.isInMotion():
            padPosition = self.__game.getPad().getPosition()
            self.setPosition((
                padPosition[0] + GameConstants.PAD_SIZE[0] / 2,
                GameConstants.SCREEN_SIZE[1] - GameConstants.PAD_SIZE[1] - GameConstants.BALL_SIZE[1]
            ))
            return

        position = self.getPosition()
        size = self.getSize()

        newPosition = [position[0] + (self.__increment[0] * self.__speed) * self.__direction[0],
                       position[1] + (self.__increment[1] * self.__speed) * self.__direction[1]]

        if newPosition[0] + size[0] >= GameConstants.SCREEN_SIZE[0]:
            self.__direction[0] *= -1
            newPosition = [GameConstants.SCREEN_SIZE[0] - size[0], newPosition[1]]
            self.__game.playSound(GameConstants.SOUND_HIT_WALL)

        if newPosition[0] <= 0:
            self.__direction[0] *= -1
            newPosition = [0, newPosition[1]]
            self.__game.playSound(GameConstants.SOUND_HIT_WALL)

        if newPosition[1] + size[1] >= GameConstants.SCREEN_SIZE[1]:
            self.__direction[1] *= -1
            newPosition = [newPosition[0], GameConstants.SCREEN_SIZE[1] - size[1]]

        if newPosition[1] <= 0:
            self.__direction[1] *= -1
            newPosition = [newPosition[0], 0]
            self.__game.playSound(GameConstants.SOUND_HIT_WALL)

        self.setPosition(newPosition)

    def isBallDead(self):
        position = self.getPosition()
        size = self.getSize()

        if position[1] + size[1] >= GameConstants.SCREEN_SIZE[1]:
            return 1

        return 0
