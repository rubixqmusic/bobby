import pygame
import logging
import os
import textwrap

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

DIALOG_FONT_PATH = f"{FONTS_PATH}/{DEFAULT_FONT}"
DIALOG_SIZE = 12
DIALOG_COLOR = f"#ffffff"

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
            if video_call_cutscene.game.is_button_released("left_button"):
                video_call_cutscene.game.play_sound(video_call_cutscene.game.load_resource(VIDEO_CALL_SELECT_SOUND_PATH))
                if self.selection == "accept":
                    self.selection = "decline"
                elif self.selection == "decline":
                    self.selection = "accept"
            if video_call_cutscene.game.is_button_released("right_button"):
                video_call_cutscene.game.play_sound(video_call_cutscene.game.load_resource(VIDEO_CALL_SELECT_SOUND_PATH))
                if self.selection == "accept":
                    self.selection = "decline"
                elif self.selection == "decline":
                    self.selection = "accept"
            
            if video_call_cutscene.game.is_button_released("start_button"):
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
        self.font = pygame.font.Font(video_call_cutscene.game.load_resource(DIALOG_FONT_PATH), DIALOG_SIZE)
    
    def update(self, video_call_cutscene):

        if self.status == "get_next_character":
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
        
        elif self.status == "wait_for_button":
            if video_call_cutscene.game.is_button_released("start_button"):
                self.status = "get_next_event"
                video_call_cutscene.get_next_event()
    
    def draw(self, video_call_cutscene):
        if self.text_surfaces != {}:
            for text_surface in self.text_surfaces:
                video_call_cutscene.game.get_screen().blit(self.text_surfaces[text_surface], self.text_positions[text_surface])

            ...
        

    

class EndCall(State):
    ...

class Choice(State):
    ...

class GoTo(State):
    def __init__(self, states: dict, *args) -> None:
        super().__init__(states, *args)
        self.args = args[0]
        self.next_cutscene = self.args[0]



    def on_state_enter(self, video_call_cutscene):
        # video_call_cutscene.go_to_next_event(self.next_cutscene)
        states = video_call_cutscene.get_states_from_cutscene(self.next_cutscene)
        # print(states)
        video_call_cutscene.state = State(states)
        video_call_cutscene.event_index = -1
        video_call_cutscene.get_next_event()
        # print(video_call_cutscene.state.states)
        # video_call_cutscene.state.start(video_call_cutscene,0)
    
    def on_state_exit(self, video_call_cutscene):
        print(video_call_cutscene.states[video_call_cutscene.event_index])        

        

        # video_call_cutscene.state.set_state(video_call_cutscene,video_call_cutscene.event_index)
        
    ...