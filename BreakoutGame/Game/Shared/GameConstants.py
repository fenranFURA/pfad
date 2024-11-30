import os


class GameConstants:
    BALL_SIZE = [16, 16]
    BRICK_SIZE = [100, 30]
    PAD_SIZE = [139, 13]
    SCREEN_SIZE = [800, 600]

    SPRITE_BALL = os.path.join("Assets", "ball.png")
    SPRITE_BRICK = os.path.join("Assets", "standard.png")
    SPRITE_SPEEDBRICK = os.path.join("Assets", "speed.png")
    SPRITE_LIFEBRICK = os.path.join("Assets", "life.png")
    SPRITE_PAD = os.path.join("Assets", "pad.png")
    SPRITE_HIGHSCORE = os.path.join("Assets", "highscore.png")
    SPRITE_MENU = os.path.join("Assets", "menu.png")

    SOUND_FILE_HIT_BRICK = os.path.join("Assets", "BrickHit.wav")
    SOUND_FILE_HIT_BRICK_LIFE = os.path.join("Assets", "ExtraLife.wav")
    SOUND_FILE_HIT_BRICK_SPEED = os.path.join("Assets", "SpeedUp.wav")
    SOUND_FILE_HIT_WALL = os.path.join("Assets", "WallBounce.wav")
    SOUND_FILE_HIT_PAD = os.path.join("Assets", "BrickHit.wav")
    SOUND_FILE_GAMEOVER = os.path.join("Assets", "GameOver.wav")

    SOUND_GAMEOVER = 0
    SOUND_HIT_BRICK = 1
    SOUND_HIT_BRICK_LIFE = 2
    SOUND_HIT_BRICK_SPEED = 3
    SOUND_HIT_WALL = 4
    SOUND_HTI_PAD = 5

    PLAYING_SCENE = 0
    GAMEOVER_SCENE = 1
    HIGHSCORE_SCENE = 2
    MENU_SCENE = 3