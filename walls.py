from resources import *
from settings import *


class wall():
    walls = set()
    def __init__(self, pos, color) -> None:
        self.pos = pos
        self.rect_value = [self.pos[0], self.pos[1], grid_size, grid_size]
        self.color = color

        wall.walls.add(self)

class textured_wall(wall):
    def __init__(self, pos, color, texture) -> None:
        super().__init__(pos, color)
        self.texture = texture
        self.shaded_texture = pygame.surfarray.array3d(texture) * 0.65
        self.shaded_texture = pygame.surfarray.make_surface(self.shaded_texture)