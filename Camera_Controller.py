from resources import *
from settings import *
from walls import *
from ray_2d import *
import Player_Controller
import Sprite_Controller




class cam():
    def __init__(self, parent) -> None:
        self.parent = parent
        self.pos = parent.pos
        self.plane = np.array([0.0, 0.5])
        self.direction = parent.direction
        self.angular_movement = 0
        self.fov = 60

        self.projection_plane_width = screen_width
        self.dist_to_projection_plane = int((self.projection_plane_width/2) / math.tan(math.radians(self.fov/2)))

    def update(self):

        self.angular_movement = self.parent.angular_movement

        if self.angular_movement == 1:
            self.plane[0], self.plane[1] = self.plane[0] * LEFT_RV[COS] - self.plane[1] * LEFT_RV[SIN], self.plane[0] * LEFT_RV[SIN] + self.plane[1] * LEFT_RV[COS]
        elif self.angular_movement == -1:
            self.plane[0], self.plane[1] = self.plane[0] * RIGHT_RV[COS] - self.plane[1] * RIGHT_RV[SIN], self.plane[0] * RIGHT_RV[SIN] + self.plane[1] * RIGHT_RV[COS]

        self.pos = self.parent.pos
        self.direction = self.parent.direction



    #Loosly based off this sprite casting guide for C++ https://lodev.org/cgtutor/raycasting3.html
    def render_enviroment(self):
        hit_sprites = []
        col_buffer = []
        for u in range(0, self.projection_plane_width, res):
            col = u
            u = 2 * u/self.projection_plane_width - 1
            r = ray(self, self.direction + self.plane * u)
            dist, hitobj, side, sprites_hit = r.march_ray()
            col_buffer.append(dist)
            for i in sprites_hit:
                if i not in hit_sprites:
                    hit_sprites.append(i)
            lineHEIGHT = abs(int(screen_height / (dist+.0000001)))
            drawStart = -lineHEIGHT / 2.0 + screen_height / 2.0

            #if (drawStart < 0):
                #drawStart = 0

            drawEnd = lineHEIGHT / 2.0 + screen_height / 2.0

            if (drawEnd >= screen_height):
                drawEnd = screen_height - 1

            color = np.copy(hitobj.color)
            
            if side == 1: color/=2
            
            if type(hitobj) == wall:
                pygame.draw.line(screen, color, (col,drawStart), (col, drawEnd), res)
            elif type(hitobj) == textured_wall:
            
                hit_point = r.at(dist * grid_size)
                if side: ns = 0
                else: ns = 1
                
                img = hitobj.texture
                if side == 1: img = hitobj.shaded_texture
                clipped = pygame.Surface((1, grid_size))
                clipped.blit(img, (0,0), (hit_point[ns] % (grid_size), 0, 1, grid_size))
                clipped = pygame.transform.scale(clipped, (res, lineHEIGHT))
                screen.blit(clipped, (col, drawStart))
        
        hit_sprites.sort(key = Player_Controller.sprite_dist_squared, reverse= True)
        for sprite in hit_sprites:
            
            if sprite in Sprite_Controller.Sprite.hittable_sprites and not sprite.active: sprite.active = True
            sx, sy = sprite.pos
            px, py = Player_Controller.p1.pos
            dx, dy = sx - px, sy - py
            dirX, dirY = self.direction

            invDet = 1.0/ (self.plane[0] * dirY - self.plane[1] * dirX)

            transformX = invDet * (dirY * dx - dirX * dy)
            transformY = (invDet * (- self.plane[1] * dx + self.plane[0] * dy)) + 0.0000001

            
            startX = (screen_width/2) * (1 + transformX/transformY)

            lineHEIGHT = int(abs(screen_height / (transformY+.0000001)) * grid_size * sprite.size) 
            drawStart = -lineHEIGHT / 2.0 + screen_height / 2.0 + sprite.height

            startX = int(- lineHEIGHT/2 + startX)
            img = sprite.img

            lineHEIGHT = min(lineHEIGHT, MAX_DRAW_HEIGHT)
            if lineHEIGHT == MAX_DRAW_HEIGHT:
                break
            img = pygame.transform.scale(img, (lineHEIGHT, lineHEIGHT))
            
            strip = 0
            
            for col in range(startX, startX + lineHEIGHT, res):
                
                if col >= 0 and col < screen_width and col_buffer[int(col / res)] * grid_size > transformY:
                    col_buffer[int(col / res)] = transformY
                    
                    clipped = pygame.Surface((res, lineHEIGHT))
                    clipped.blit(img, (0,0), (strip, 0, res, lineHEIGHT))
                    clipped.set_colorkey((0,0,0))
                    screen.blit(clipped, (col, drawStart))
                
                
                strip += res