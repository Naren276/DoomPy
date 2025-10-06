from resources import *
from settings import *
import Sprite_Controller
import world_controller


def DDA(pos, dir):

    hit_sprites = []

    rayPositionX, rayPositionY  = pos

    mapX, mapY = int(rayPositionX), int(rayPositionY)

    rayDirectionX, rayDirectionY = dir
    rayDirectionY += 0.000000001

    deltaDistanceX = math.sqrt(1.0 + (rayDirectionY * rayDirectionY) / (rayDirectionX * rayDirectionX))
    deltaDistanceY = math.sqrt(1.0 + (rayDirectionX * rayDirectionX) / (rayDirectionY * rayDirectionY))

    # We need sideDistanceX and Y for distance calculation. Checks quadrant
    if (rayDirectionX < 0):
        stepX = -1
        sideDistanceX = (rayPositionX - mapX) * deltaDistanceX

    else:
        stepX = 1
        sideDistanceX = (mapX + 1.0 - rayPositionX) * deltaDistanceX

    if (rayDirectionY < 0):
        stepY = -1
        sideDistanceY = (rayPositionY - mapY) * deltaDistanceY

    else:
        stepY = 1
        sideDistanceY = (mapY + 1.0 - rayPositionY) * deltaDistanceY

    # Finding distance to a wall
    hit = 0
    if (mapX, mapY) in Sprite_Controller.Sprite.sprites_world:
        hit_sprites.extend(Sprite_Controller.Sprite.sprites_world[(mapX, mapY)])
    while  (hit == 0):
        if (sideDistanceX < sideDistanceY):
            sideDistanceX += deltaDistanceX
            mapX += stepX
            side = 0
            
        else:
            sideDistanceY += deltaDistanceY
            mapY += stepY
            side = 1


    

        hit_square = world_controller.world[mapX, mapY]
    
        if (mapX, mapY) in Sprite_Controller.Sprite.sprites_world:
            hit_sprites.extend(Sprite_Controller.Sprite.sprites_world[(mapX, mapY)])
            continue

        if hit_square != None: 
            if (side == 0):
                perpWallDistance = abs((mapX - rayPositionX + ( 1.0 - stepX ) / 2.0) / rayDirectionX)
            else:
                perpWallDistance = abs((mapY - rayPositionY + ( 1.0 - stepY ) / 2.0) / rayDirectionY)

            return perpWallDistance, hit_square, side, hit_sprites

class ray():
    def __init__(self, parent, dir) -> None:
        self.parent = parent
        self.pos = parent.pos
        self.direction = dir

    def march_ray(self):
        return DDA(self.pos/grid_size, self.direction)
    
    def update(self):
        self.pos = self.parent.pos
        
    def at(self, t):
        return self.pos + self.direction * t