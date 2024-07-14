import pygame

from src.signal import Signal
from src.state import State
from settings import *

class Hitbox:
    def __init__(self) -> None:
        self._enabled = True
        self._hitbox = pygame.rect.Rect(0,0,0,0)
        self._position = pygame.Vector2((0,0))
        self._offset = pygame.Vector2((0,0))
        self._type = None
        self._collision_types = []
        self._colliders = None
        self._groups = []
        self.properties = {}
        self.on_collision = Signal()

    def set_groups(self, groups: list):
        self._groups = groups

    def get_groups(self):
        return self._groups
    
    def add_to_group(self, group: str):
        self._groups.append(group)
    
    def is_in_group(self, group):
        return True if group in self._groups else False

    def set_hitbox(self, x, y, w, h):
        self._hitbox = pygame.rect.Rect(x, y, w, h)

    def get_hitbox(self):
        return self._hitbox
    
    def set_position(self, x, y):
        self._position.x = x + self._offset.x
        self._position.y = y + self._offset.y
        self._hitbox[0] = self._position.x
        self._hitbox[1] = self._position.y
    
    def set_offset(self, x_offset, y_offset):
        self._offset.x = x_offset
        self._offset.y = y_offset
    
    def set_collision_types(self, collision_types: list):
        self._collision_types = collision_types
    
    def get_collision_types(self):
        return self._collision_types
    
    def add_collision_type(self, collision_type: str):
        self._collision_types.append(collision_type)
    
    def set_colliders(self, colliders: dict):
        self._colliders = colliders
    
    def get_collisions(self):
        if not self._colliders:
            return []
        collisions = []
        for collision_type in self._collision_types:
            if collision_type in self._colliders:
                for hitbox in self._colliders[collision_type]:
                    if hitbox is not None:
                        if self._hitbox.colliderect(hitbox.get_hitbox()):
                            collisions.append(hitbox)
        return collisions

    def set_type(self, type):
        self._type = type

    def get_type(self):
        return self._type
    
    def set_property(self, key, value):
        self.properties[key] = value

    def get_property(self, key):
        if key in self.properties:
            return self.properties[key]
        return None
    
    def enable(self):
        self._enabled = True

    def disable(self):
        self._enabled = False

    def is_enabled(self) -> bool:
        return True if self._enabled else False
    
