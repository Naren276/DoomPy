#from resources import *
from levels import *
from walls import *


def init_world_controller():
    global world
    world = None


def load_level( level):
    
   

    level_as_list = level.splitlines()
    level_height = len(level_as_list)
    level_width = len(level_as_list[0])

    
    new_world = np.full([level_width, level_height], None)


    for c, row, in enumerate(level_as_list):
        for r, i, in enumerate(row):
            if i == '#': new_world[r, c] = wall(np.array([r * grid_size, c * grid_size]), color = WHITE)
            elif i == 'B': new_world[r, c] = textured_wall(np.array([r * grid_size, c * grid_size]), color = WHITE, texture = brick_texture)
            elif i =='M': new_world[r, c] = textured_wall(np.array([r * grid_size, c * grid_size]), color = WHITE, texture = metal_texture)
            elif i == 'S': new_world[r, c] = textured_wall(np.array([r * grid_size, c * grid_size]), color = WHITE, texture = stone_wall)
            elif i == 'Q': new_world[r, c] = textured_wall(np.array([r * grid_size, c * grid_size]), color = WHITE, texture = cobble_texture)
            elif i == 'W': new_world[r, c] = textured_wall(np.array([r * grid_size, c * grid_size]), color = WHITE, texture = wood_natural)
            elif i == 'G': new_world[r, c] = textured_wall(np.array([r * grid_size, c * grid_size]), color = WHITE, texture = gold_wall)
            elif i == 'N': new_world[r, c] = textured_wall(np.array([r * grid_size, c * grid_size]), color = WHITE, texture = smooth_bricks)
            elif i == 'J': new_world[r, c] = textured_wall(np.array([r * grid_size, c * grid_size]), color = WHITE, texture = weatherd_brick)
            elif i.isdigit(): new_world[r,c ] = wall(np.array([r * grid_size, c * grid_size]), color = wallcolors[int(i)])

    
    global world
    world= new_world
    


    




    






