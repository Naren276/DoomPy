import pygame

pygame.init()

info = pygame.display.Info()


screen_width, screen_height = 960, 540

#screen_width, screen_height = info.current_w, info.current_h

screen = pygame.display.set_mode((screen_width, screen_height))

grid_size = 32

ROTATIONSPEED = 0.025# 0.015
PLAYERSPEED = 2
PLAYER_RADIUS = 3
RANGED_UNIT_DIST = 200
res = 3 #Resolution scale = screen_width/RES
fps = 120

TICK_SPEED = int(fps/2)
MAX_DRAW_HEIGHT = 1000

ENEMY_HEALTH = 100

ENEMY_SPEED = 0.5

BULLET_SPEED = 1
BULLET_LIFETIME = 2