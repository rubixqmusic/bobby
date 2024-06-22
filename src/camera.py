import pygame
import logging

from settings import *

class Camera:
    def __init__(self, x, y, width, height) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.rect.Rect(x, y, width, height)

        self.surface = pygame.surface.Surface((width, height))

        self._bounds_enabled = True

        self.limit_left = 0
        self.limit_right = SCREEN_WIDTH
        self.limit_top = 0
        self.limit_bottom = SCREEN_HEIGHT
    
    def set_bounds(self, left, right, top, bottom):
        self.limit_left = left
        self.limit_right = right
        self.limit_top = top
        self.limit_bottom = bottom
    
    def get_position(self):
        return self.x, self.y

    def bounds_enabled(self):
        return self._bounds_enabled
    
    def enable_bounds(self):
        self._bounds_enabled = True

    def disable_bounds(self):
        self._bounds_enabled = False
    
    def set_position(self, x, y):
        self.x = x
        self.y = y
        self.rect[0] = self.x
        self.rect[1] = self.y
    
    def center(self, center_x, center_y):
        
        self.rect.centerx = center_x
        self.rect.centery = center_y
        self.x = self.rect[0]
        self.y = self.rect[1]
        if self.bounds_enabled():
            if self.x + self.width > self.limit_right:
                self.x = self.limit_right - self.width          
            if self.x < self.limit_left:
                self.x = self.limit_left
            if self.y + self.height > self.limit_bottom:
                self.y = self.limit_bottom - self.height
            if self.y < self.limit_top:
                self.y = self.limit_top
            self.rect[0] = self.x
            self.rect[1] = self.y
            
            

        self.x = self.rect[0]
        self.y = self.rect[1]
    
    def move(self, x, y):
        self.x += x
        self.y += y
        if self.bounds_enabled():
            if self.x + self.width > self.limit_right:
                self.x = self.limit_right - self.width          
            if self.x < self.limit_left:
                self.x = self.limit_left
            if self.y + self.height > self.limit_bottom:
                self.y = self.limit_bottom - self.height
            if self.y < self.limit_top:
                self.y = self.limit_top
        self.rect[0] = self.x
        self.rect[1] = self.y