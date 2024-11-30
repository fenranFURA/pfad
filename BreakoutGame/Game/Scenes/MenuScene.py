from Game.Scenes.Scene import Scene
from Game.Shared.GameConstants import *

import pygame

class MenuScene(Scene):

    def __init__(self, game):
        super(MenuScene, self).__init__(game)

        self.__menuSprite = pygame.image.load(GameConstants.SPRITE_MENU).convert()

        self.addText("F1 - Start Game", x=300, y=200, size=30)
        self.addText("F2 - High Score", x=300, y=240, size=30)
        self.addText("F3 - Quit", x=300, y=280, size=30)


    def render(self):
        self.getGame().screen.blit(self.__menuSprite, (50, 50))

        super(MenuScene, self).render()

    def handleEvents(self, events):
        super(MenuScene, self).handleEvents(events)

        for event in events:
            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F1:
                    self.getGame().changeScene(GameConstants.PLAYING_SCENE)
                elif event.key == pygame.K_F2:
                    self.getGame().changeScene(GameConstants.HIGHSCORE_SCENE)
                elif event.key == pygame.K_ESCAPE or event.key == pygame.K_F3:
                    exit()
