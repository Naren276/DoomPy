from resources import *
from settings import *
import world_controller
from Sprite_Controller import *
from ray_2d import *


class Player():
    def __init__(self) -> None:

        self.pos = np.array([50.0, 50.0])
        self.velocity = 0
        self.velocity_perp = 0
        self.direction = np.array([1.0, 0.0])
        self.angular_movement = 0
        self.angle = 0
        self.health = 100

    def update(self):
        
            

        if self.angular_movement == 1:
            self.direction[0], self.direction[1] = self.direction[0] * LEFT_RV[COS] - self.direction[1] * LEFT_RV[SIN], self.direction[0] * LEFT_RV[SIN] + self.direction[1] * LEFT_RV[COS]
        elif self.angular_movement == -1:
            self.direction[0], self.direction[1] = self.direction[0] * RIGHT_RV[COS] - self.direction[1] * RIGHT_RV[SIN], self.direction[0] * RIGHT_RV[SIN] + self.direction[1] * RIGHT_RV[COS]
        
        newPos = self.pos + self.direction * self.velocity * 7 
        newPos += np.array([ - self.direction[1], self.direction[0]]) * self.velocity_perp * 7
        
        self.angle = math.atan2(self.direction[1],self.direction[0])
        
        new_world_pos = world_controller.world[int(newPos[0]/grid_size), int(newPos[1]/grid_size)]
        if new_world_pos == None:
            self.pos += self.direction * self.velocity 
            self.pos += np.array([ - self.direction[1], self.direction[0]]) * self.velocity_perp * 0.5
    

    
    def shoot(self):
        
        r = ray(self, self.direction)
        dist, _, _, hit_sprites = r.march_ray()
        hit_sprites = [s for s in hit_sprites if s in Sprite.hittable_sprites]
        if hit_sprites == []: 
            return False
        
        for sprite in hit_sprites:
            if intersection_sphere_line((sprite.pos, sprite.radius), (self.pos, r.at(dist))):
                sprite.subtract_health(35)

p1 = Player()

def sprite_dist_squared(s):
    return dist_sqaured(p1.pos[0], p1.pos[1], s.pos[0], s.pos[1])