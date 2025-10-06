from resources import *
from settings import *
from walls import * 
import world_controller
import Menu
from levels import *


class Sprite:
    sprites = []
    sprites_world = dict()
    hittable_sprites = set()
    def __init__(self, texture, pos) -> None:
        
        self.health = ENEMY_HEALTH
        
        self.pos = pos
        self.mapX, self.mapY = int(self.pos[0]/grid_size), int(self.pos[1]/grid_size)
        self.img = texture 
        self.idle_img = texture
        self.size = 1
        self.height = 0
        self.radius = self.size * grid_size
        
        self.animations = {}
        self.curr_animation = ''
        self.animation_frame = 0
        self.playing_animation = False

        Sprite.sprites.append(self)
        if (self.mapX, self.mapY) not in Sprite.sprites_world: Sprite.sprites_world[(self.mapX, self.mapY)] = [self]
        else: Sprite.sprites_world[(self.mapX, self.mapY)].append(self)
    
    
    def __hash__(self):
        return hash(str(self))
    
    def __eq__(self, other):
        if str(self) == str(other): return True

    def move(self, dir, magnitude = ENEMY_SPEED):
        
        new_pos = self.pos + dir * float(magnitude)
        new_pos += dir * 7
        
        if world_controller.world[int(new_pos[0]/grid_size), int(new_pos[1]/grid_size)] in wall.walls: return False
        
        self.pos = self.pos + dir * magnitude
        newR, newC = int(self.pos[0]/grid_size), int(self.pos[1]/grid_size)
        if self.mapX == newR and self.mapY == newC: return True
        

        Sprite.sprites_world[(self.mapX, self.mapY)].remove(self)
        if (newR, newC) not in Sprite.sprites_world: Sprite.sprites_world[(newR, newC)] = [self]
        else: Sprite.sprites_world[(newR, newC)].append(self)

        self.mapX, self.mapY = newR, newC 

        return True

    def subtract_health(self, amount):
        self.health -= amount
        if self.health <= 0:
            if 'death_animation' in self.animations:
                self.curr_animation = 'death_animation'
                self.active = False
                self.playing_animation = True
        elif  'hurt_animation' in self.animations:
            self.curr_animation = 'hurt_animation'
            self.playing_animation = True

    
    def move_to(self, target_pos, magnitude = ENEMY_SPEED):
        dx, dy = target_pos[0] - self.pos[0], target_pos[1] - self.pos[1] 
        target_dir = np.array([dx, dy])
        target_dir /= np.linalg.norm(target_dir)
        self.move(target_dir, magnitude)

    def collides(self, point, radius):
        if math.dist(self.pos, point) <= self.radius + radius:
            return True
        return False
    
    def delete(self):
        if self in Sprite.hittable_sprites: Sprite.hittable_sprites.remove(self)
        if self in Sprite.sprites: Sprite.sprites.remove(self)
        for key in Sprite.sprites_world:
            value = Sprite.sprites_world[key]
            if self in value:

                value.remove(self)

    def play_animation(self):
        animation = self.animations[self.curr_animation]
        self.animation_frame += 1

        if self.animation_frame >= len(animation):
            if self.health <= 0: self.delete()
            self.playing_animation = False
            self.animation_frame = 0
            self.img = self.idle_img

        

        elif self.animation_frame != len(animation):
            self.img = animation[self.animation_frame]



    def update_animation(self):
        if self.playing_animation: self.play_animation()


            

        


class orb_sprite(Sprite):
    def __init__(self, texture, pos) -> None:
        super().__init__(texture, pos)
        
        self.active = False

        Sprite.hittable_sprites.add(self)

class basic_enemy(Sprite):
    def __init__(self, texture, pos) -> None:
        super().__init__(texture, pos)

        self.active = False
        
        self.touching_player = False

    

        self.animations['hurt_animation'] = [hurt_crab, hurt_crab, hurt_crab]

        self.animations['death_animation'] = [load_image_with(f'images/explosion_{i + 1}.png', (self.size * grid_size, self.size * grid_size) ) for i in range(4)]

        self.animations['attack_animation'] = [load_image_with(f'images/Crab_{i + 1}.png', (self.size * grid_size, self.size * grid_size) ) for i in range(4)]

        Sprite.hittable_sprites.add(self)

    def update(self, player):
        if self.active:

            if not self.touching_player and self.playing_animation == False:
                self.move_to(player.pos, ENEMY_SPEED * 1.5)



    def on_tick(self, player):
        if self.active:
            if self.collides(player.pos, PLAYER_RADIUS):
                self.curr_animation = 'attack_animation'
                self.playing_animation = True

                player.health -= 20
            

                self.touching_player = True
            
            else: self.touching_player = False

class moving_obstacle(Sprite):
    def __init__(self, texture, pos, positions) -> None:
        super().__init__(texture, pos)

        self.active = False

        self.positions = [pos] + positions

        self.curr_goal_index = 1

        Sprite.hittable_sprites.add(self)

    def update(self, player):
        if self.active:

           target = self.positions[self.curr_goal_index]
           
           self.move_to(target)

           if int(self.pos[0]) == int(target[0]) and int(self.pos[1]) == int(target[1]): 
               
               
               self.curr_goal_index =  (self.curr_goal_index + 1) % len(self.positions)



    def on_tick(self, player):
        if self.active:
            if self.collides(player.pos, PLAYER_RADIUS):
                
                player.health -= 20
            
    
class bullet(Sprite):
    bullets = []
    def __init__(self, texture, pos, speed, dir) -> None:
        super().__init__(texture, pos)

        self.speed = speed

        self.size = 0.2

        self.lifeSpan = fps * BULLET_LIFETIME

        self.radius = self.size * grid_size

        self.direction = dir

        self.active = True

        Sprite.hittable_sprites.add(self)

        bullet.bullets.append(self)

    def update(self, player):

        
        self.lifeSpan -= 1

        if self.lifeSpan == 0:
            self.delete()

        elif not self.move(self.direction, self.speed): self.active = False
        

        elif self.collides(player.pos, PLAYER_RADIUS):


            player.health -= 20
            

            self.active = False

    def delete(self):
        bullet.bullets.remove(self)
        Sprite.hittable_sprites.remove(self)
        Sprite.sprites.remove(self)
        for key in Sprite.sprites_world:
            value = Sprite.sprites_world[key]
            if self in value:
                value.remove(self)

    def on_tick(self, player):
        pass


class ranged_enemy(Sprite):
    ranged_units = []
    def __init__(self, texture, pos) -> None:
        super().__init__(texture, pos)

        self.active = False

        self.in_range = True

        self.shot_last_iter = False

        self.animations['hurt_animation'] = [hurt_r_unit, hurt_r_unit, hurt_r_unit]

        self.animations['shooting_animation'] = [load_image_with(f'images/r_unit_{i + 1}.png', (self.size * grid_size, self.size * grid_size) ) for i in range(4)]
        
        self.animations['death_animation'] = [load_image_with(f'images/explosion_{i + 1}.png', (self.size * grid_size, self.size * grid_size) ) for i in range(4)]
    
        Sprite.hittable_sprites.add(self)

        ranged_enemy.ranged_units.append(self)

    def update(self, player):
        if self.active:
            
            if math.dist(self.pos, player.pos) >= RANGED_UNIT_DIST :
                self.move_to(player.pos)
                self.in_range = False

            else: self.in_range = True

  
    
    def shoot(self, target_pos):
        dx, dy = target_pos[0] - self.pos[0], target_pos[1] - self.pos[1] 
        target_dir = np.array([dx, dy])
        target_dir /= np.linalg.norm(target_dir)
    
        self.curr_animation = 'shooting_animation'
        self.playing_animation = True
        b = bullet(orb_img, self.pos, BULLET_SPEED, target_dir)
        b.height -= 15

    def delete(self):
        ranged_enemy.ranged_units.remove(self)
        Sprite.hittable_sprites.remove(self)
        Sprite.sprites.remove(self)
        for key in Sprite.sprites_world:
            value = Sprite.sprites_world[key]
            if self in value:
                value.remove(self)
        
    def on_tick(self, player):
        
        if self.active:

            
            if self.in_range:
                self.shot_last_iter = True

            if self.shot_last_iter and not self.playing_animation:

                self.shoot(player.pos)

                self.shot_last_iter = False

            if self.collides(player.pos, PLAYER_RADIUS):
                
                player.health -= 20
                


class health_pickup(Sprite):
    heal_pick_ups = []
    def __init__(self, texture, pos) -> None:
        super().__init__(texture, pos)

        self.size = 0.4

        self.radius = self.size * grid_size

        health_pickup.heal_pick_ups.append(self)

    def on_tick(self, player):

        if self.collides(player.pos, PLAYER_RADIUS):

            player.health = min(100, player.health + 50)



            if self in Sprite.sprites: Sprite.sprites.remove(self)

            health_pickup.heal_pick_ups.remove(self)

            for key in Sprite.sprites_world:
                value = Sprite.sprites_world[key]
                if self in value:
                    value.remove(self)

        

class win_portal(Sprite):
    def __init__(self, texture, pos) -> None:
        super().__init__(texture, pos)

        self.active = False

        self.size = 1.4

        self.animations['idle_animation'] = [load_image_with(f'images/portal_{i + 1}.png', (self.size * grid_size, self.size * grid_size)) for i in range(8)]

        self.curr_animation = 'idle_animation'

        self.playing_animation = True

        Sprite.hittable_sprites.add(self)

    def subtract_health(self, amount):
        pass

    def update(self, player):
        pass

    def on_tick(self, player):

        if self.active:
            
            if not self.playing_animation:
                self.curr_animation = 'idle_animation'

                self.playing_animation = True


            if self.collides(player.pos, PLAYER_RADIUS):
                global level
                level += 1
                Menu.load_world(LEVELS[level])
            
        
                


