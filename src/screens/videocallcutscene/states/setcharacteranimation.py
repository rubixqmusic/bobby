import pygame
import logging

from src.state import State
from src.screens.videocallcutscene.resources import *
from src.animatedsprite import AnimatedSprite

class SetCharacterAnimation(State):
    def __init__(self, states: dict, *args) -> None:
        super().__init__(states, *args)
        self.args = args[0]

        self.character_animation_number = self.args[0]
        self.spritesheet_path = self.args[1]
        self.animation_path = self.args[2]
        self.starting_animation = self.args[3]

    def on_state_enter(self, video_call_cutscene):
        spritesheet_path = f"{GRAPHICS_PATH}/{self.spritesheet_path}"
        animation_path = f"{ANIMATIONS_PATH}/{self.animation_path}"

        # print(f"\n {os.path.exists(animation_path)} \n")

        if video_call_cutscene.game.resource_exists(spritesheet_path) and video_call_cutscene.game.resource_exists(animation_path) and self.character_animation_number in video_call_cutscene.character_animations:
            video_call_cutscene.character_animations[self.character_animation_number]["spritesheet_path"] = self.spritesheet_path
            # video_call_cutscene.character_animations[self.character_animation_number]["animatied_sprite"] = AnimatedSprite(video_call_cutscene.game, video_call_cutscene.backgrounds[self.character_animation_number])

            # animated_sprite = video_call_cutscene.character_animations[self.character_animation_number]["animatied_sprite"]

            # animated_sprite = AnimatedSprite(video_call_cutscene.game, video_call_cutscene.game.get_screen())
            animated_sprite = AnimatedSprite(video_call_cutscene.game, video_call_cutscene.backgrounds[self.character_animation_number]["image"])

            animated_sprite.load_spritesheet(spritesheet_path)
            animated_sprite.load_sprite_data(animation_path)
            animated_sprite.set_animation(self.starting_animation)
            animated_sprite.play()

            video_call_cutscene.character_animations[self.character_animation_number]["animation_path"] = self.animation_path
            video_call_cutscene.character_animations[self.character_animation_number]["starting_animation"] = self.starting_animation
            video_call_cutscene.character_animations[self.character_animation_number]["animated_sprite"] = animated_sprite
                 
        else:
            logging.debug(f"image path is fucked up, homie, this is what you passed in: {animation_path} {spritesheet_path}. The fuck am I supposed to do with this??")
        video_call_cutscene.get_next_event()