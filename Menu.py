import pygame, sys
from resources import *
from settings import *
import world_controller
import Sprite_Controller
import Player_Controller
import Camera_Controller
from levels import *
import Overlay_GUI

paused = False

def resume(from_scene = None):
    global paused
    paused = False


def load_sprites(level):
    level_as_list = level.splitlines()

    for c, row, in enumerate(level_as_list):
        for r, i, in enumerate(row):
            locX, locY = r * grid_size + grid_size/2, c * grid_size + grid_size/2
            if i == 'C': Sprite_Controller.basic_enemy(crab_img, np.array([locX, locY]))
            elif i == 'R': Sprite_Controller.ranged_enemy(ranged_unit_img,  np.array([locX, locY]))
            elif i == 'H': Sprite_Controller.health_pickup(health_pick_up_img,  np.array([locX, locY]))
            elif i == 'P': Sprite_Controller.win_portal(portal_texture, np.array([locX, locY]))

def load_world(l):
    Player_Controller.p1.pos = np.array([50.0, 50.0])
    Player_Controller.p1.health = 100
    while len(Sprite_Controller.Sprite.sprites) > 0:
        Sprite_Controller.Sprite.sprites[0].delete()
    Sprite_Controller.Sprite.sprites_world = {}
    world_controller.load_level(l)
    load_sprites(l)
    Overlay_GUI.Overlay_Text(f"LEVEL: {LEVELS.index(l)}", (screen_width/2, screen_height/2), pixel_font_super, 180)
    

def start_new_game(from_scene = None):
    global paused
    paused = False
    load_world(LEVELS[0])




def update_res(n):
    global res
    res = n

def update_sensitivity(n):
    global ROTATIONSPEED
    ROTATIONSPEED = n

def update_fps(n):
    global fps
    fps = n



class button():
    buttons = []
    def __init__(self, img, rect, func, last_scene) -> None:
        x, y, w, h = rect
        self.rect = rect
        self.img = pygame.transform.scale(img, (w, h))
        self.cords = (x, y)
        self.func = func
        self.last_scene = last_scene

        button.buttons.append(self)
        

    def in_cords(self, cords):
        mx, my = cords
        x, y, w, h = self.rect

        if mx >= x and mx <= x + w:
            if my >= y and my <= y + h:
                button.buttons = []
                self.func(self.last_scene)

    def draw(self, surf):
        surf.blit(self.img, self.cords)

class textBox():
    textBoxes = []
    def __init__(self, name, rect, func) -> None:
        self.name = name
        x, y, w, h = rect
        self.rect = rect
        self.text = ''
        self.x, self.y = x, y
        self.w, self.h = w, h
        self.func = func

        textBox.textBoxes.append(self)

    def in_cords(self, cords):
        mx, my = cords
        x, y, w, h = self.rect

        if mx >= x and mx <= x + w:
            if my >= y and my <= y + h:
                inText = True
                while inText:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            sys.exit()
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_RETURN:
                                textBox.textBoxes = []
                                if self.text.isdigit():
                                    self.func(float(self.text))
                            elif event.key == pygame.K_BACKSPACE:
                                self.text = self.text[:-1]

                            else: 
                                self.text += event.unicode

                        elif event.type == pygame.MOUSEBUTTONUP: 
                            self.text = ''
                            inText = False


                    self.draw(screen)

                    clock.tick(fps)

                    pygame.display.update()

                        
    
    def draw(self, surf):
        
        
        label = base_font.render(self.name, 1, (255,255,255))
        surf.blit(label, (self.x, self.y - 30))
        pygame.draw.rect(surf, (0,0,0), self.rect)
        pygame.draw.rect(surf, (255, 255,255), self.rect, width= 2)

        render_pixel_text(surf, self.text, (self.x + self.w/2, self.y + self.h/2))
    
    

        
def show_death_screen(from_screen = None):
    global paused
    button(menu_img, [screen_width/2 - (screen_width/15 * 3.04)/2, 300, screen_width/15 * 3.04, b_height], show_menu_screen, show_death_screen)
    paused = True
    
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                for b in button.buttons:
                    b.in_cords(pos)

        render_pixel_text(screen, 'OH NO YOU DIED!', (screen_width/2, 200), font_to_use= pixel_font_super)

        for b in button.buttons:
            b.draw(screen)

        
        clock.tick(fps)

        pygame.display.update()


        


def show_settings_screen(from_screen):
    settings_screen = screen
    in_settings = True
    textBox('', [screen_width/2 + 200 , 186, 70, 30], update_res)
    textBox('', [screen_width/2 + 200 , 236, 70, 30], update_sensitivity)
    textBox('', [screen_width/2 + 200 , 286, 70, 30], update_fps)
    while in_settings:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: 
                    in_settings = False
                    screen.fill((0,0,0))
                    from_screen()
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                for box in textBox.textBoxes:
                    box.in_cords(pos)

        settings_screen.fill((0,0,0))

        label = base_font.render('Press a box to enter a value: ', 1, (255,255,255))
        settings_screen.blit(label, (screen_width/2 - 150, 70))

        render_pixel_text(settings_screen, 'Settings:', np.array([screen_width/2, 50]))
        render_pixel_text(settings_screen, f'Resoluton Scale: {res}', np.array([screen_width/2, 200]))
        render_pixel_text(settings_screen, f'Turning Sensitivity: {ROTATIONSPEED}', np.array([screen_width/2, 250]))
        render_pixel_text(settings_screen, f'fps cap: {fps}', np.array([screen_width/2, 300]))

        for box in textBox.textBoxes:
            box.draw(settings_screen)


        
        clock.tick(fps)

        pygame.display.update()

def show_levels_screen(from_screen = None):
    pass


def show_menu_screen(from_screen =None):
    global paused
    paused = True
    menu_screen = screen

    #button(settings_img, [screen_width/2 - b_width/2, 100, b_width, b_height], show_settings_screen, show_menu_screen)
    button(play_img, (screen_width/2 - (screen_width/15 * 3.04)/2, 200, screen_width/15 * 3.04, b_height), start_new_game, show_menu_screen)
    #button(levels_img, [screen_width/2 - b_width/2, 300, b_width, b_height], show_levels_screen, show_menu_screen)

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                pass

            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                for b in button.buttons:
                    b.in_cords(pos)

        
        menu_screen.blit(menu_background, (0,0))


        for b in button.buttons:
            b.draw(menu_screen)


        clock.tick(fps)
        pygame.display.update()



def show_pause_screen(from_screen = None):
    global paused
    paused = True
    
    
    paused_screen = screen
    #button(settings_img, [screen_width/2 - b_width/2, 100, b_width, b_height], show_settings_screen, show_pause_screen)
    button(play_img, (screen_width/2 - (screen_width/15 * 3.04)/2, 200, screen_width/15 * 3.04, b_height), resume, show_pause_screen)
    button(menu_img, [screen_width/2 - (screen_width/15 * 3.04)/2, 300, screen_width/15 * 3.04, b_height], show_menu_screen, show_pause_screen)

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: 
                    button.buttons = []
                    paused = False
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                for b in button.buttons:
                    b.in_cords(pos)
                        

                                 
        paused_screen.blit(screen, (0,0))

        for b in button.buttons:
            b.draw(paused_screen)

        
        clock.tick(fps)

        pygame.display.update()

