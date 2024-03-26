import pygame

class MapPath:
    def __init__(self, x, y, width, height, image) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = image
        self.rect = pygame.rect.Rect(x, y, width, height)
        pass