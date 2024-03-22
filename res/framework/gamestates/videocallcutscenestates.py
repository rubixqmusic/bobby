import pygame
import logging
import os
import textwrap
import math

from res.settings import *
from res.framework.state import State
from res.framework.animatedsprite import AnimatedSprite

VIDEO_CALL_RINGING_IMAGE_PATH = f"{GRAPHICS_PATH}/video_call_cutscenes/video_call_ringing.png"
VIDEO_CALL_RINGING_MUSIC_PATH = f"{MUSIC_PATH}/video_call_ringing.mp3"

VIDEO_CALL_SELECT_SOUND_PATH = f"{SOUNDS_PATH}/video_call_select.wav"
VIDEO_CALL_DECLINE_SOUND_PATH = f"{SOUNDS_PATH}/video_call_decline.wav"
VIDEO_CALL_ACCEPT_SOUND_PATH = f"{SOUNDS_PATH}/video_call_accept.wav"

VIDEO_CALL_BLANK_BACKGROUND_PATH = f"{GRAPHICS_PATH}/backgrounds/video_call_blank_background.png"
VIDEO_CALL_TEXT_BOX_PATH = f"{GRAPHICS_PATH}/backgrounds/video_call_text_box.png"
TEXT_BOX_ADVANCE_ICON = f"{GRAPHICS_PATH}/icons/text_box_advance_icon.png"

DIALOG_ADVANCE_SOUND = f"{SOUNDS_PATH}/dialog_advance.wav"
DIALOG_SOUND_PATH = f"{SOUNDS_PATH}/dialog.wav"
DIALOG_FONT_PATH = f"{FONTS_PATH}/{DEFAULT_FONT}"
DIALOG_SIZE = 12
DIALOG_COLOR = f"#ffffff"

CURRENT_SPEAKER_COLOR = f"#e3eaee"

class VideoCallRinging(State):
    def on_state_enter(self, video_call_cutscene):
        self.selection = "accept"
        self.status = "decline"
        self.WAIT_TIMER = 120
        
        self.video_call_ringing_image = pygame.image.load(video_call_cutscene.game.load_resource(VIDEO_CALL_RINGING_IMAGE_PATH))
        self.video_call_ringing_rect = self.video_call_ringing_image.get_rect(center=(SCREEN_WIDTH/2,SCREEN_HEIGHT/2))

        self.video_call_blank_background = pygame.image.load(video_call_cutscene.game.load_resource(VIDEO_CALL_BLANK_BACKGROUND_PATH))
        self.video_call_blank_background_rect = self.video_call_blank_background.get_rect(center=(SCREEN_WIDTH/2,SCREEN_HEIGHT/2))
        self._wait_timer = self.WAIT_TIMER

        self.SELECTION_X = self.video_call_ringing_rect.x
        self.SELECTION_y = self.video_call_ringing_rect.y + 32
        self.SELECTION_RECT_WIDTH = 64
        self.SELECTION_RECT_HEIGHT = 32
        self.SELECTION_RECT_COLOR = "#ffffff"
        self.ACCEPT_X = self.video_call_ringing_rect.x
        self.DECLINE_X = self.video_call_ringing_rect.x + 64

        video_call_cutscene.game.stop_music()
    
    def update(self, video_call_cutscene):
        if self.status == "ringing":
            if video_call_cutscene.game.is_button_released(LEFT_BUTTON):
                video_call_cutscene.game.play_sound(video_call_cutscene.game.load_resource(VIDEO_CALL_SELECT_SOUND_PATH))
                if self.selection == "accept":
                    self.selection = "decline"
                elif self.selection == "decline":
                    self.selection = "accept"
            if video_call_cutscene.game.is_button_released(RIGHT_BUTTON):
                video_call_cutscene.game.play_sound(video_call_cutscene.game.load_resource(VIDEO_CALL_SELECT_SOUND_PATH))
                if self.selection == "accept":
                    self.selection = "decline"
                elif self.selection == "decline":
                    self.selection = "accept"
            
            if video_call_cutscene.game.is_button_released(START_BUTTON):
                if self.selection == "decline":
                    self.status = "decline"
                    video_call_cutscene.game.stop_music()
                    video_call_cutscene.game.play_sound(video_call_cutscene.game.load_resource(VIDEO_CALL_DECLINE_SOUND_PATH))

                if self.selection == "accept":
                    self.status = "accept"
                    video_call_cutscene.game.stop_music()
                    video_call_cutscene.game.play_sound(video_call_cutscene.game.load_resource(VIDEO_CALL_ACCEPT_SOUND_PATH))

        elif self.status == "decline":
            self._wait_timer -= 1
            if self._wait_timer < 0:
                self._wait_timer = self.WAIT_TIMER
                self.status = "ringing"
                self.selection = "accept"
                video_call_cutscene.game.play_music(video_call_cutscene.game.load_resource(VIDEO_CALL_RINGING_MUSIC_PATH))
        
        elif self.status == "accept":
            self._wait_timer -= 1
            if self._wait_timer < 0:
                self._wait_timer = self.WAIT_TIMER
                self.accept_call_and_get_next_event(video_call_cutscene)
                self.status = "end"
                # self.selection = "accept"
                # video_call_cutscene.game.play_music(video_call_cutscene.game.load_resource(VIDEO_CALL_RINGING_MUSIC_PATH))
            ...
    def accept_call_and_get_next_event(self, video_call_cutscene):
        image_path = video_call_cutscene.game.load_resource(VIDEO_CALL_TEXT_BOX_PATH)
        if os.path.exists(image_path):

            # set the cutscene text box image to something other than None so that it is present for each new event in the cutscene
            # until explicitly set to none again
            video_call_cutscene.text_box["path"] = image_path
            video_call_cutscene.text_box["image"] = pygame.image.load(image_path)
        video_call_cutscene.get_next_event()
        
    def draw(self, video_call_cutscene):
        if self.status == "ringing":
            ringing_image = self.video_call_ringing_image
            
            if self.selection == "accept":
                selection_rect = pygame.rect.Rect(self.ACCEPT_X, self.SELECTION_y, self.SELECTION_RECT_WIDTH, self.SELECTION_RECT_HEIGHT)
            elif self.selection == "decline":
                selection_rect = pygame.rect.Rect(self.DECLINE_X, self.SELECTION_y, self.SELECTION_RECT_WIDTH, self.SELECTION_RECT_HEIGHT)

            video_call_cutscene.game.get_screen().fill("#000000")
            video_call_cutscene.game.get_screen().blit(ringing_image,self.video_call_ringing_rect)
            pygame.draw.rect(video_call_cutscene.game.get_screen(),self.SELECTION_RECT_COLOR,selection_rect,width=2)
            # print(selection_rect)
            # print(self.selection)

        if self.status == "decline":
            video_call_cutscene.game.get_screen().fill("#000000")

        if self.status == "accept":

            video_call_cutscene.game.get_screen().fill("#000000")
            video_call_cutscene.game.get_screen().blit(self.video_call_blank_background,self.video_call_blank_background_rect)

class EndCall(State):
    def __init__(self, states: dict, *args) -> None:
        super().__init__(states, *args)
        self.args = args[0]
        self.next_game_state = self.args[0]
        self._wait_timer = 120
        self.status = "end_call"
    
    # def load_next_game_state(self, video_call_cutscene):
    #     if self.next_game_state == "world_map":
    #         video_call_cutscene.game.load_world_map()
        ...

    def on_state_enter(self, video_call_cutscene):
        self.video_call_blank_background = pygame.image.load(video_call_cutscene.game.load_resource(VIDEO_CALL_BLANK_BACKGROUND_PATH))
        self.video_call_blank_background_rect = self.video_call_blank_background.get_rect(center=(SCREEN_WIDTH/2,SCREEN_HEIGHT/2))
        video_call_cutscene.game.play_sound(video_call_cutscene.game.load_resource(VIDEO_CALL_DECLINE_SOUND_PATH))

    def update(self, video_call_cutscene):
        if self.status == "end_call":
            self._wait_timer -= 1
            if self._wait_timer < 0:
                self._wait_timer = 120
                self.status = "load_next_game_state"
        
        elif self.status == "load_next_game_state":
            self._wait_timer -= 1
            if self._wait_timer < 0:
                self._wait_timer = 120
                self.status = "end"
                video_call_cutscene.load_next_game_state(self.next_game_state)
    
    def draw(self, video_call_cutscene):
        if self.status == "end_call":
            video_call_cutscene.game.get_screen().fill("#000000")
            video_call_cutscene.game.get_screen().blit(self.video_call_blank_background,self.video_call_blank_background_rect)

        elif self.status == "load_next_game_state" or "end":
            video_call_cutscene.game.get_screen().fill("#000000")

    ...


class SetBackgroundImage(State):
    def __init__(self, states: dict, *args) -> None:
        super().__init__(states, *args)
        self.args = args[0]

        self.background_number = self.args[0]
        self.image_path = self.args[1]


    def on_state_enter(self, video_call_cutscene):
        image_path = video_call_cutscene.game.load_resource(f"{GRAPHICS_PATH}/{self.image_path}")
        if os.path.exists(image_path) and self.background_number in video_call_cutscene.backgrounds:
            video_call_cutscene.backgrounds[self.background_number]["path"] = self.image_path
            video_call_cutscene.backgrounds[self.background_number]["image"] = pygame.image.load(image_path)
        else:
            logging.debug(f"image path is fucked up, homie, this is what you passed in: {image_path}. The fuck am I supposed to do with this??")
        video_call_cutscene.get_next_event()

    ...

class SetCharacterAnimation(State):
    def __init__(self, states: dict, *args) -> None:
        super().__init__(states, *args)
        self.args = args[0]

        self.character_animation_number = self.args[0]
        self.spritesheet_path = self.args[1]
        self.animation_path = self.args[2]
        self.starting_animation = self.args[3]

    def on_state_enter(self, video_call_cutscene):
        spritesheet_path = video_call_cutscene.game.load_resource(f"{GRAPHICS_PATH}/{self.spritesheet_path}")
        animation_path = video_call_cutscene.game.load_resource(f"{ANIMATIONS_PATH}/{self.animation_path}")

        # print(f"\n {os.path.exists(animation_path)} \n")

        if os.path.exists(spritesheet_path) and os.path.exists(animation_path) and self.character_animation_number in video_call_cutscene.character_animations:
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

class ShowDialog(State):
    def __init__(self, states: dict, *args) -> None:
        super().__init__(states, *args)

        MAX_LINES = 2
        TEXT_SIZE = 16
        MAX_LINE_WIDTH = 32
        # print(self)
        self.args = args[0]
        self.dialog = self.args[0]

        self.sound_speed = 5
        self.sound_speed_step = 0

        self.text_advance_icon_blink_speed = 10
        self.text_advance_icon_step = 0
        self.text_advance_icon_position = [370, 195]
        self.toggle_text_advance_icon = True
        
        
        
        
        self.text_surfaces = {}
        self.text_lines = textwrap.wrap(self.dialog, MAX_LINE_WIDTH)
        self.number_of_lines = len(self.text_lines)
        

        self.text_positions = [
                                [124, 178],
                                [124, 196]
        ]

        
        self.current_character = 0
        self.current_line = 0

        self.status = "get_next_character"
    
    def on_state_enter(self, video_call_cutscene):
        self.current_speaker_font = pygame.font.Font(video_call_cutscene.game.load_resource(DIALOG_FONT_PATH), 10)
        self.text_advance_icon_surface = pygame.image.load(video_call_cutscene.game.load_resource(TEXT_BOX_ADVANCE_ICON))
        self.font = pygame.font.Font(video_call_cutscene.game.load_resource(DIALOG_FONT_PATH), DIALOG_SIZE)
    
    def update(self, video_call_cutscene):

        if self.status == "get_next_character":
            self.sound_speed_step += 1
            self.sound_speed_step = self.sound_speed_step%self.sound_speed
            
    
            if self.current_line > len(self.text_lines) -1:
                self.current_line = 0
                self.status = "wait_for_button"
            elif self.current_character > len(self.text_lines[self.current_line]):
                self.current_character = 0
                self.current_line += 1   
            else:
                new_text = self.text_lines[self.current_line][0:self.current_character]
                new_text_surface = self.font.render(new_text,True,DIALOG_COLOR)
                self.text_surfaces[self.current_line] = new_text_surface
                self.current_character += 1
                if self.sound_speed_step == 0:
                    video_call_cutscene.game.play_sound(video_call_cutscene.game.load_resource(DIALOG_SOUND_PATH))
        
        elif self.status == "wait_for_button":
            self.text_advance_icon_step += 1
            self.text_advance_icon_step = self.text_advance_icon_step%self.text_advance_icon_blink_speed
            if self.text_advance_icon_step == 0:
                self.toggle_text_advance_icon = not self.toggle_text_advance_icon

            if video_call_cutscene.game.is_button_released(START_BUTTON):
                video_call_cutscene.game.play_sound(video_call_cutscene.game.load_resource(DIALOG_ADVANCE_SOUND))
                self.status = "get_next_event"
                video_call_cutscene.get_next_event()
    
    def draw(self, video_call_cutscene):
        if self.text_surfaces != {}:
            for text_surface in self.text_surfaces:
                video_call_cutscene.game.get_screen().blit(self.text_surfaces[text_surface], self.text_positions[text_surface])

        if self.status == "get_next_character":
            if video_call_cutscene.backgrounds[1]["image"] is not None:
                current_speaker_rect = video_call_cutscene.backgrounds[1]["image"].get_rect(topleft=video_call_cutscene.backgrounds[1]["position"])
                pygame.draw.rect(video_call_cutscene.game.get_screen(), CURRENT_SPEAKER_COLOR, current_speaker_rect, 5)
                current_speaker_text_surface = self.current_speaker_font.render(f"Cody Feiko", True, "#ffffff", "#000055")
                video_call_cutscene.game.get_screen().blit(current_speaker_text_surface, (video_call_cutscene.backgrounds[1]["position"][0] + 10, video_call_cutscene.backgrounds[1]["position"][1] + 76))
        elif self.status == "wait_for_button":
            if self.toggle_text_advance_icon:
                video_call_cutscene.game.get_screen().blit(self.text_advance_icon_surface, self.text_advance_icon_position)


class Wait(State):
    def __init__(self, states: dict, *args) -> None:
        super().__init__(states, *args)
        self.args = args[0]
        self.wait_time = self.args[0]
        self.status = "waiting"
    
    def update(self, video_call_cutscene):
        if self.status == "waiting":
            if video_call_cutscene.game.is_button_released(START_BUTTON):
                self.wait_time = 0
            self.wait_time -= 1

            if self.wait_time < 0:
                self.status = "get_next_event"
                video_call_cutscene.get_next_event()


class Choice(State):
    def __init__(self, states: dict, *args) -> None:
        super().__init__(states, *args)

        MAX_LINES = 2
        TEXT_SIZE = 16
        MAX_LINE_WIDTH = 32
        self.args = args[0]
        self.dialog = self.args[0]
        self.choices_args = self.args[1]
        self.choices = []
        self.choice = ""
        self.x_start = 124
        self.x_spacing = 40
        self.y_start = 196

        self.max_text_grow = 5.0
        self.text_grow_step_size = 0.1
        self.sine_degrees = 0
        self.grow_factor = 0

        
        self.text_surfaces = {}
        self.text_lines = textwrap.wrap(self.dialog, MAX_LINE_WIDTH)
        self.number_of_lines = len(self.text_lines)

        self.text_positions = [
                                [124, 178],
                                [124, 196]
        ]

        self.current_character = 0
        self.current_line = 0

        self.status = "get_next_character"


        for choice in self.choices_args:
            new_choice = {}
            new_choice[choice[0]] = choice[1]
            new_choice["name"] = choice[0]
            new_choice["text"] = choice[0]
            self.choices.append(new_choice)

            # self.choices[]
    
    def on_state_enter(self, video_call_cutscene):
        self.font = pygame.font.Font(video_call_cutscene.game.load_resource(DIALOG_FONT_PATH), DIALOG_SIZE)
    
    def update(self, video_call_cutscene):
        self.grow_factor = int(math.sin(self.sine_degrees) * self.max_text_grow)
        self.sine_degrees += self.text_grow_step_size%self.max_text_grow

        if self.status == "get_next_character":
            if self.current_line > len(self.text_lines) -1:
                self.current_line = 0
                self.choice = self.choices[0]["name"]
                self.status = "make_choice"
            elif self.current_character > len(self.text_lines[self.current_line]):
                self.current_character = 0
                self.current_line += 1   
            else:
                new_text = self.text_lines[self.current_line][0:self.current_character]
                new_text_surface = self.font.render(new_text,True,DIALOG_COLOR)
                self.text_surfaces[self.current_line] = new_text_surface
                self.current_character += 1
                video_call_cutscene.game.play_sound(video_call_cutscene.game.load_resource(DIALOG_SOUND_PATH))
        
        elif self.status == "make_choice":
            if video_call_cutscene.game.is_button_released(START_BUTTON):
                for choice in self.choices:
                    if choice["name"] == self.choice:
                        # video_call_cutscene.game.play_sound(video_call_cutscene.game.load_resource(VIDEO_CALL_ACCEPT_SOUND_PATH))
                        next_event = choice[self.choice]
                        states = video_call_cutscene.get_states_from_cutscene(next_event)
                        video_call_cutscene.state = State(states)
                        video_call_cutscene.event_index = -1
                        video_call_cutscene.get_next_event()
            elif video_call_cutscene.game.is_button_released(RIGHT_BUTTON):
                video_call_cutscene.game.play_sound(video_call_cutscene.game.load_resource(VIDEO_CALL_SELECT_SOUND_PATH))
                self.choice = self.get_next_menu_item(self.choices, self.choice)
            elif video_call_cutscene.game.is_button_released(LEFT_BUTTON):
                video_call_cutscene.game.play_sound(video_call_cutscene.game.load_resource(VIDEO_CALL_SELECT_SOUND_PATH))
                self.choice = self.get_previous_menu_item(self.choices, self.choice)

    
    def draw(self, video_call_cutscene):
        if self.text_surfaces != {}:
            for text_surface in self.text_surfaces:
                video_call_cutscene.game.get_screen().blit(self.text_surfaces[text_surface], self.text_positions[text_surface])

        if self.status == "get_next_character":
            if video_call_cutscene.backgrounds[1]["image"] is not None:
                    current_speaker_rect = video_call_cutscene.backgrounds[1]["image"].get_rect(topleft=video_call_cutscene.backgrounds[1]["position"])
                    pygame.draw.rect(video_call_cutscene.game.get_screen(), CURRENT_SPEAKER_COLOR, current_speaker_rect, 5)
        elif self.status == "make_choice":
            self.draw_menu(self.choices,self.choice, self.x_start, self.x_spacing, self.font, DIALOG_COLOR, video_call_cutscene.game.get_screen(), self.grow_factor)
    
    def draw_menu(self,
              menu: list, 
              current_selection: str, 
              x_start: int, 
              x_spacing: int, 
              font: pygame.font.Font, 
              font_color: str, 
              destination_surface: pygame.surface.Surface, 
              grow_factor: int,
              drop_shadow=False,
              drop_shadow_color=f"#000000",
              drop_shadow_x=1,
              drop_shadow_y=1):
    
        menu_item_index = 0
        for menu_item in menu:
            text_surface = font.render(menu_item['text'],True,font_color)
            text_surface_base_size = text_surface.get_width(), text_surface.get_height()
            drop_shadow_surface = None
            if drop_shadow:
                drop_shadow_surface = font.render(menu_item['text'],False,drop_shadow_color)
            
            if menu_item["name"] == current_selection:
                if drop_shadow_surface is not None:
                    drop_shadow_surface_new = pygame.transform.scale(drop_shadow_surface, 
                                        (text_surface_base_size[0] + grow_factor, 
                                        text_surface_base_size[1] + grow_factor))
                    drop_shadow_rect = drop_shadow_surface_new.get_rect(topleft=(drop_shadow_x, x_start + (menu_item_index*x_spacing)+drop_shadow_y, self.y_start))
                    destination_surface.blit(drop_shadow_surface, drop_shadow_rect)
                
                new_surface = pygame.transform.scale(text_surface, 
                                        (text_surface_base_size[0] + grow_factor, 
                                        text_surface_base_size[1] + grow_factor))
                text_rect = new_surface.get_rect(topleft=(x_start + (menu_item_index*x_spacing), self.y_start))
                destination_surface.blit(new_surface, text_rect)
            else:
                if drop_shadow_surface is not None:
                    drop_shadow_rect = drop_shadow_surface.get_rect(center=( x_start + (menu_item_index*x_spacing)+drop_shadow_y,self.y_start+drop_shadow_y))
                    destination_surface.blit(drop_shadow_surface, drop_shadow_rect)
                text_rect = text_surface.get_rect(topleft=(x_start + (menu_item_index*x_spacing), self.y_start))
                destination_surface.blit(text_surface, text_rect)
        
            menu_item_index += 1
    ...

    def get_next_menu_item(self, menu: list, current_selection: str):
        index = 0
        for menu_item in menu:
            if menu_item["name"] == current_selection:
                index += 1
                if index > len(menu) - 1:
                    index = 0
                return menu[index]["name"]
            index += 1

    def get_previous_menu_item(self, menu: list, current_selection: str):
        index = 0
        for menu_item in menu:
            if menu_item["name"] == current_selection:
                index -= 1
                if index < 0:
                    index = len(menu) - 1
                return menu[index]["name"]
            index += 1
        # return current_selection

class PlaySound(State):
    def __init__(self, states: dict, *args) -> None:
        super().__init__(states, *args)
        self.args = args[0]
        self.sound_name = self.args[0]

    def on_state_enter(self, video_call_cutscene):
        video_call_cutscene.game.play_sound(video_call_cutscene.game.load_resource(f"{SOUNDS_PATH}/{self.sound_name}"))
        video_call_cutscene.get_next_event()


class GoTo(State):
    def __init__(self, states: dict, *args) -> None:
        super().__init__(states, *args)
        self.args = args[0]
        self.next_cutscene = self.args[0]

    def on_state_enter(self, video_call_cutscene):
        states = video_call_cutscene.get_states_from_cutscene(self.next_cutscene)
        video_call_cutscene.state = State(states)
        video_call_cutscene.event_index = -1
        video_call_cutscene.get_next_event()

class PlayMusic(State):
    def __init__(self, states: dict, *args) -> None:
        super().__init__(states, *args)
        self.args = args[0]
        self.song_name = self.args[0]
        self.volume = self.args[1]

    def on_state_enter(self, video_call_cutscene):
        video_call_cutscene.game.play_music(video_call_cutscene.game.load_resource(f"{MUSIC_PATH}/{self.song_name}"), self.volume)
        video_call_cutscene.get_next_event()
       

            