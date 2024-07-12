import pygame
import logging
import os
import json

from src.signal import Signal
from src.state import State
from settings import *


class AnimatedSprite():
    def __init__(self) -> None:
        self.position = pygame.Vector2(0,0)
        self.relative_position = pygame.Vector2(0,0)
        self.enabled = True
        self.blend_mode = pygame.BLEND_ALPHA_SDL2
        self.draw_target = None
        
        self.spritesheet = None
        self.animations = {}
        self.frames = []
        self.frame = 0
        self.frame_duration = 1.0
        self.time_elapsed = 0.0
        self.start_frame = 0
        self.stop_frame = 0
        self.loop = True
        self.animation = "default"
        self.playing = False
        self._animation_did_finish = False
        self.state = State(states)
        self.state.start(self, "stopped")

        self.image_changed = Signal()
        self.spritesheet_changed = Signal()
        self.animation_started = Signal()
        self.animation_stopped = Signal()
        self.animation_finished = Signal()

    def set_position(self, x, y):
        self.position.x = x
        self.position.y = y
    
    def enable(self):
        self.enabled = True
    
    def disable(self):
        self.enabled = False

    def is_enabled(self):
        return True if self.enabled else False
    
    def load_spritesheet(self, spritesheet_path):
        self.spritesheet = pygame.image.load(spritesheet_path).convert_alpha()
        self.spritesheet_changed.emit(self.spritesheet)
    
    def load_animation(self, data_path):
        sprite_data = {}
        sprite_data = json.load(data_path)


        if 'frames' in sprite_data:

            for frame in sprite_data['frames']:
                new_frame = {}
                new_frame['duration'] = frame['duration']/1000
                new_frame['frame'] = pygame.rect.Rect(frame['frame']['x'],
                                                        frame['frame']['y'],
                                                        frame['frame']['w'],
                                                        frame['frame']['h'])
                self.frames.append(new_frame)
        
        if 'meta' in sprite_data:
            for animation in sprite_data['meta']['frameTags']:
                new_animation_name = animation['name']
                new_animation_start_frame = animation['from']
                new_animation_stop_frame = animation['to']
                if 'repeat' in animation:
                    new_animation_loop = False
                else:
                    new_animation_loop = True
                
                self.animations[new_animation_name] = {'start frame': new_animation_start_frame, 'stop frame': new_animation_stop_frame, 'loop': new_animation_loop}

    def set_draw_target(self, draw_target):
        if not isinstance(draw_target, pygame.surface.Surface):
            return
        self.draw_target = draw_target
    
    def get_spritesheet(self) -> pygame.surface.Surface:
        return self.spritesheet

    def get_frame_image(self):
        frame_image = pygame.surface.Surface((self.frames[self.frame]['frame'][2], self.frames[self.frame]['frame'][3]))
        frame_image.blit(self.spritesheet, 
                        (0,0), 
                        self.frames[self.frame]['frame'], 
                            special_flags=self.blend_mode)
        frame_image.set_colorkey((0,0,0))
        return frame_image
    
    def get_frame(self) -> int:
        return self.frame
    
    def get_frame_duration(self) -> float:
        return self.frame_duration
    
    def get_animation(self) -> str:
        return self.animation
    
    def set_animation(self, animation) -> None:
        if animation == self.animation:
            return
        if animation not in self.animations:
            logging.debug(f"animation {animation} is not in this objects animations!")
            return
        self.animation = animation
        self.start_frame = self.animations[animation]['start frame']
        self.frame = self.start_frame
        self.stop_frame = self.animations[animation]['stop frame']
        self.loop = self.animations[animation]['loop']
        self.frame_duration = self.frames[self.start_frame]['duration']
        self.time_elapsed = 0.0
        self._animation_did_finish = False

    def is_playing(self) -> bool:
        return True if self.playing else False
    
    def toggle_playing(self) -> None:
        self.playing = not self.playing

    def play(self) -> None:
        self.playing = True
        self.animation_started.emit(self)
    
    def stop(self)->None:
        self.playing = False
        self.animation_stopped.emit(self)
    
    def update(self, delta):
        if not self.is_enabled():
            return
        if self.animations == {} or self.frames == []:
            return 
        if self.frame > len(self.frames):
            self.frame = len(self.frames)-1 
        self.state.update(self, delta)

    def draw(self):
        if not self.is_enabled():
            return
        if self.draw_target is None:
            return
        if self.animations == {} or self.frames == []:
            return

        self.draw_target.blit(self.spritesheet, 
                            (self.position.x, self.position.y), 
                            self.frames[self.frame]['frame'], 
                            special_flags=self.blend_mode)


class Stopped(State):
    def on_state_enter(self, sprite: AnimatedSprite):
        sprite.frame = sprite.start_frame
        if sprite.frames == []:
            return
        sprite.frame_duration = sprite.frames[sprite.start_frame]['duration']
        sprite.animation_finished = False

    def update(self, sprite: AnimatedSprite, delta):
        if sprite.playing:
            sprite.state.set_state(sprite, "playing")
            return


class Playing(State):
            
    def update(self, sprite: AnimatedSprite, delta):
        if not sprite.playing:
            sprite.state.set_state(sprite, "stopped")
            return
        sprite.time_elapsed += delta
        if sprite.time_elapsed >= sprite.frame_duration:
            sprite.time_elapsed = 0.0
            sprite.frame += 1
            if sprite.frame > sprite.stop_frame:
                if sprite.loop:
                    sprite.animation_finished.emit(sprite.animation)
                    sprite.frame = sprite.start_frame
                else:
                    sprite.frame = sprite.stop_frame
                    if not sprite._animation_did_finish:
                        sprite._animation_did_finish = True
                        sprite.animation_finished.emit(sprite.animation)
            sprite.frame_duration = sprite.frames[sprite.frame]['duration']
        

states = {
    "playing" : Playing,
    "stopped" : Stopped
}