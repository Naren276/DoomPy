from resources import *
from Player_Controller import *
from Sprite_Controller import *
import world_controller
from walls import *
from ray_2d import *
from levels import *
from Camera_Controller import *
from settings import *
from Overlay_GUI import *
from Menu import * 
import time

pygame.init()

world_controller.init_world_controller()


camera = cam(p1)



show_menu_screen()

start_time = time.time()

Doom_Shotgun_Overlay = Animation_Handeler(Doom_Gun_Animation, (screen_width/2 - DOOM_GUN_SIZE/2 - 14, screen_height - DOOM_GUN_SIZE/1.24), 10)

FRAME_COUNT = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_RIGHT: 
                p1.angular_movement = 1

            elif event.key == pygame.K_LEFT: 
                p1.angular_movement = -1

            elif event.key == pygame.K_ESCAPE: show_pause_screen()

            elif event.key == pygame.K_w: p1.velocity = PLAYERSPEED
            elif event.key == pygame.K_s: p1.velocity = - PLAYERSPEED
            elif event.key == pygame.K_d: p1.velocity_perp = PLAYERSPEED
            elif event.key == pygame.K_a: p1.velocity_perp = - PLAYERSPEED
            elif event.key == pygame.K_SPACE: 
                if Doom_Shotgun_Overlay.life_time == 0:
                    p1.shoot()
                    Doom_Shotgun_Overlay.life_time = Doom_Shotgun_Overlay.frame_time * Doom_Shotgun_Overlay.frame_count

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT: p1.angular_movement = 0
            elif event.key == pygame.K_LEFT: p1.angular_movement = 0
            elif event.key == pygame.K_w: p1.velocity = 0
            elif event.key == pygame.K_s: p1.velocity = 0
            elif event.key == pygame.K_a: p1.velocity_perp = 0 
            elif event.key == pygame.K_d: p1.velocity_perp = 0

        

    p1.update()
    camera.update()

    for sprite in list(Sprite.hittable_sprites):
        sprite.update(p1)

    for b in bullet.bullets:
        if b.active == False:
            b.delete()

    if p1.health <= 0: show_death_screen()


    sky_offset = -5 * math.degrees(p1.angle) % screen_width
    screen.blit(sky_box, (sky_offset, 0))
    screen.blit(sky_box, (sky_offset - screen_width, 0))
    screen.blit(sky_box, (sky_offset + screen_width, 0))
    pygame.draw.rect(screen, (59, 62, 67), [0, screen_height/2, screen_width, screen_height] )
    

    camera.render_enviroment()
    
    Animation_Handeler.draw_animations()

    draw_overlays()
    
    for t_overlay in Overlay_Text.text_overlays:
        t_overlay.on_tick()

    pygame.draw.circle(screen, (255,255,255), (screen_width/2, screen_height/2), 3)

    clock.tick(fps)

    FRAME_COUNT += 1
    if FRAME_COUNT == fps: FRAME_COUNT = 0

    if FRAME_COUNT % (TICK_SPEED/4) == 0:
        
        for sprite in list(Sprite.hittable_sprites):
            sprite.update_animation()

        for pick_up in health_pickup.heal_pick_ups:
            pick_up.on_tick(p1)



    if FRAME_COUNT % TICK_SPEED == 0:

        

        for sprite in list(Sprite.hittable_sprites):

            sprite.on_tick(p1)
    
    fps_counter()

    render_pixel_text(screen, f'Time: {round((time.time() - start_time), 1)}s', (screen_width - 100, 14), font_to_use= base_font)

    pygame.display.update()
    