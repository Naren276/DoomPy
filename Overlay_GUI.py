from resources import *
from settings import *
import Player_Controller


hp_bar = load_image_with('images/hp_outline.png', (HP_BAR_SIZE, HP_BAR_SIZE/4))
def draw_overlays():
    pygame.draw.rect(screen, (238,38,38), [20 + HP_BAR_SIZE/5.5, screen_height - HP_BAR_SIZE/6 - 20, HP_BAR_SIZE * Player_Controller.p1.health/100 - HP_BAR_SIZE/4.7, HP_BAR_SIZE/8])
    screen.blit(hp_bar, (20, screen_height - HP_BAR_SIZE/4 - 20))


class Overlay_Text():
    text_overlays = []
    def __init__(self, text, pos, font, time = 120) -> None:
        self.text = text
        self.ticks_left = time
        self.pos = pos
        self.font = font
        self.t_surf = pixel_font_super.render(self.text, 1, (255,255, 255))

        Overlay_Text.text_overlays.append(self)
    
    def on_tick(self):

        if self.ticks_left == 0: 
            Overlay_Text.text_overlays.remove(self)
            return



        w, h = self.t_surf.get_size()

        screen.blit(self.t_surf, (self.pos[0] - w/2,self.pos[1] - h/2 ))
        

        self.ticks_left -= 1

    
        
    

class Animation_Handeler():
    active_animations = set()
    def __init__(self, animation, pos, time_per_frame) -> None:
        self.animation = animation 
        self.frame_time = time_per_frame
        self.pos = pos
        self.curr_frame = 0
        self.frame_count = len(self.animation)
        self.life_time = 0
        Animation_Handeler.active_animations.add(self)
    
    @staticmethod
    def draw_animations():
        for a in Animation_Handeler.active_animations:
            if a.life_time != 0: 

                a.life_time -= 1
                a.curr_frame = a.frame_count - 1 - a.life_time//a.frame_time
            
            else: a.curr_frame = 0
                
            screen.blit(a.animation[a.curr_frame], (a.pos))
            

#Doom animation from https://www.spriters-resource.com/pc_computer/doomdoomii/
Doom_Gun_Animation = [load_image_with('images/DOOM_shotgun_idle.png', (DOOM_GUN_SIZE, DOOM_GUN_SIZE))]
Doom_Gun_Animation.extend([load_image_with(f'images/DOOM_shotgun_{i + 1}.png', (DOOM_GUN_SIZE, DOOM_GUN_SIZE)) for i in range(5)])
