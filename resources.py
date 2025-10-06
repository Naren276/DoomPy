import pygame, numpy as np, math, sys
from settings import *

pygame.init()


world = None


BLACK = np.array([0.0, 0.0, 0.0])
WHITE = np.array([255.0, 255.0, 255.0])

b_width, b_height = screen_width/15 * 4.64, screen_width/15

level = 0

dist_sqaured = lambda x1, y1, x2, y2: (x2 -x1) * (x2 -x1) + (y2 - y1) * (y2 -y1)

clock = pygame.time.Clock()

basic_font = pygame.font.SysFont("Arial" , 18 , bold = True)

base_font = pygame.font.Font('Grand9k Pixel.ttf', 18)

pixel_font_large = pygame.font.Font('Grand9k Pixel.ttf', 24)

pixel_font_super = pygame.font.Font('Grand9k Pixel.ttf', 70)

DOOM_GUN_SIZE = screen_width/3

HP_BAR_SIZE = screen_width/4



#These two functions are taken from https://stackoverflow.com/questions/67946230/show-fps-in-pygame
def fps_counter():
    fps = str(int(clock.get_fps()))
    fps_t = base_font.render(fps , 1, pygame.Color("RED"))
    screen.blit(fps_t,(0,0))

def render_pixel_text(surf, text, pos, color = (255, 255,255), align = 'center', font_to_use = pixel_font_large ):
        
        t_surf = font_to_use.render(text, 1, color)
        if align == 'center': 
            w, h = t_surf.get_size()
            pos -= np.array([w/2, h/2])

        surf.blit(t_surf, pos)


def intersection_sphere_line(sphere, line):
    l1, l2 = line
    sp, radius = sphere
    x, y = sp
    slope = (l2[1] - l1[1])/(l2[0] - l1[0])
    c = l1[1] - (l1[0] * slope)
    a = slope
    b = -1
    dist = ((abs(a * x + b * y + c)) /
            math.sqrt(a * a + b * b))
    
    if dist< radius/4:
        return True
    return False

def load_image(source):
    return pygame.transform.scale(pygame.image.load(source), (grid_size, grid_size))

def load_image_with(path, size, colorkey = None):
    img = pygame.image.load(path)
    img = pygame.transform.scale(img, size)
    if colorkey != None:
        img.set_colorkey(colorkey)
    return img

def load_image_from_sheet(sheet, pos, size = 16):
     
     x, y = pos 
     clipped = pygame.surface.Surface((size, size))
     clipped.blit(sheet, (0,0), [x * size, y * size, size, size])

     return pygame.transform.scale(clipped, (grid_size, grid_size))

     


wallcolors = [np.array([232.0, 9.0, 24.0]), np.array([6.0, 191.0, 80.0]), np.array([4.0, 62.0, 209.0]), np.array([240.0, 236.0, 7.0]), np.array([112.0, 6.0, 189.0])]


LEFT_RV = (math.cos(ROTATIONSPEED), math.sin(ROTATIONSPEED))
RIGHT_RV = (math.cos(-ROTATIONSPEED), math.sin(-ROTATIONSPEED))
COS, SIN = 0, 1
TO_DEGREES = 180/math.pi







#Enemy Sprites and animations: https://www.spriters-resource.com/game_boy_advance/cima/
orb_img = load_image('images/orb.png')

explosion_img = load_image('images/explosion_1.png')

ranged_unit_img = load_image('images/r_unit_1.png')

static_enemy_img = load_image('images/floating_Col.png')

crab_img = load_image('images/Crab_1.png')

orb_img.set_colorkey((0,0,0))

hurt_crab = load_image('images/Crab_hurt.png')

hurt_r_unit = load_image('images/r_unit_hurt.png')

health_pick_up_img = load_image('images/health_pickup.png')




#Button Images: https://stock.adobe.com/images/interface-menu-buttons-pixel-art-set-menu-panel-collection-play-pause-store-settings-options-quit-8-bit-sprite-game-development-mobile-app-isolated-vector-illustration/539993440
settings_img = load_image_with('images/options_img.png', (b_width, b_height))

menu_img = load_image_with('images/Menu_img.png', (b_width, b_height))

levels_img = load_image_with('images/levels_img.png', (b_width, b_height))

quit_img = load_image_with('images/quit_img.png', (b_width, b_height))

play_img = load_image_with('images/play_img.png', (b_width, b_height))

sky_box = pygame.image.load('images/night_sky.png')



#https://wallpaperaccess.com/pixel-art-hd
menu_background = load_image_with('images/menu_background.png', (screen_width, screen_height))

render_pixel_text(menu_background, 'DoomPY - CS 112', (screen_width/2, 60), font_to_use= pixel_font_super)

menu_background.blit(base_font.render('Use arrow keys to rotate, WASD to move, and SPACE to shoot! Reach the portal to progress', 1, (255,255,255)), (0, screen_height - 40))

sky_box = pygame.transform.scale(sky_box, (screen_width, screen_height))

#Textures: https://piiixl.itch.io/textures
texture_sheet = pygame.image.load('images/Texture_sheet.png')

stone_wall = load_image_from_sheet(texture_sheet, (7, 1))

wood_natural = load_image_from_sheet(texture_sheet, (1, 10))

smooth_bricks = load_image_from_sheet(texture_sheet, (1, 4))

brick_texture = load_image_from_sheet(texture_sheet, (2, 4))

metal_texture = load_image_from_sheet(texture_sheet, (7, 4))

weatherd_brick = load_image_from_sheet(texture_sheet, (8, 4))

cobble_texture = load_image('images/Brick_Image.png')

gold_wall = load_image_from_sheet(texture_sheet, (5, 24))

portal_texture = load_image('images/portal_1.png')
