import pygame
import logging

from res.settings import *

class Camera:
    def __init__(self, x, y, width, height) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.rect.Rect(x, y, width, height)

        self.surface = pygame.surface.Surface((width, height))

        self.limit_left = 0
        self.limit_right = SCREEN_WIDTH
        self.limit_top = 0
        self.limit_bottom = SCREEN_HEIGHT
    
    def set_bounds(self, left, right, top, bottom):
        self.limit_left = left
        self.limit_right = right
        self.limit_top = top
        self.limit_bottom = bottom
    
    def center(self, center_x, center_y):
        self.rect.centerx = center_x
        self.rect.centery = center_y
        self.x = self.rect[0]
        self.y = self.rect[1]
    
    def move(self, x, y):
        self.x += x
        self.y += y
        if self.x < self.limit_left or self.x > self.limit_right:
            self.x -= x
        if self.y < self.limit_top or self.y > self.limit_bottom:
            self.y -= y
        self.rect[0] = self.x
        self.rect[1] = self.y