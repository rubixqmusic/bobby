import pygame

from res.settings import *
from res.framework.animatedsprite import AnimatedSprite
from res.framework.state import State
from res.framework.signal import Signal

LAND_ON_LEVEL_SOUND = f"{SOUNDS_PATH}/land_on_level.wav"

class Player:
    def __init__(self,game, world_map, x, y, width, height, spritesheet, animation, draw_target, camera) -> None:
        self.game = game
        self.world_map = world_map
        self.x = x
        self.y = y
        self.offset_y = -8
        self.direction = "down"
        self.walking_speed = 1
        self.walking_speed_step = 0
        self.camera = camera
        self.width = width
        self.height = height
        self.rect = pygame.rect.Rect(x, y, width, height)
        self.current_level = None
        self.level = None

        self.animated_sprite = AnimatedSprite(game,draw_target)
        self.animated_sprite.load_spritesheet(game.load_resource(spritesheet))
        self.animated_sprite.load_sprite_data(game.load_resource(animation))
        self.animated_sprite.set_position(self.x, self.y)

        self.state = State(player_states)
        self.state.set_state(self, "init")

        self.animated_sprite.set_animation("down")
        self.animated_sprite.play()

    def update(self):
        self.walking_speed_step += 1 
        self.walking_speed_step = self.walking_speed_step % self.walking_speed
        
        self.animated_sprite.update()
        self.state.update(self)

        self.rect[0] = self.x
        self.rect[1] = self.y
    
    def draw(self):
        self.animated_sprite.set_position(self.x - self.camera.x, self.y - self.camera.y +self.offset_y)
        self.animated_sprite.draw()
        self.state.draw(self)

    def set_player_idle(self):
        self.state.set_state(self, "idle")
    
    def set_player_idle_on_landing(self,no_sound=False):
        if no_sound == False:
            self.game.play_sound(self.game.load_resource(LAND_ON_LEVEL_SOUND))
        self.current_level = "landing"
        self.world_map.set_current_level("landing")
        self.state.set_state(self, "idle_on_landing")

    def set_player_idle_on_level(self, level_name, entrance_direction):
        self.game.play_sound(self.game.load_resource(LAND_ON_LEVEL_SOUND))
        self.world_map.set_current_level(level_name)
        self.state.set_state(self, "idle_on_level", level_name, entrance_direction)
    
    def set_player_walking(self):
        self.state.set_state(self, "walking")


class IdleOnLevel(State):
    def __init__(self, states: dict, *args) -> None:
        super().__init__(states, *args)
        self.level_name = args[0]
        self.entrance_direction = args[1]


    def on_state_enter(self, player: Player):
        self.level_data = player.game.get_level_data(self.level_name)
        if self.level_data:
            self.level_data["map_entrance_direction"] = self.entrance_direction
            player.game.set_level_data(self.level_name, "map_entrance_direction", self.entrance_direction)
        player.animated_sprite.set_animation("down")
        self.started_walking = False
    
    def update(self, player: Player):
        x_previous = player.x
        y_previous = player.y
        # started_walking = False
        if self.level_data:
            if self.level_data["money"] < self.level_data["quota"]:
                if player.game.is_button_released(DOWN_BUTTON) and self.entrance_direction == "s":
                    
                    player.y += 1
                    player.rect[1] = player.y

                    for map_path in player.world_map.map_path:
                        if player.rect.colliderect(map_path.rect):
                            self.started_walking = True
                            player.direction = "down"
                            player.set_player_walking()
                            break
                    if self.started_walking == False:
                        player.x = x_previous
                        player.y = y_previous
                        player.rect[0] = player.x
                        player.rect[1] = player.y

                elif player.game.is_button_released(UP_BUTTON) and self.entrance_direction == "n":
                    player.y -= 1
                    player.rect[1] = player.y

                    for map_path in player.world_map.map_path:
                        if player.rect.colliderect(map_path.rect):
                            self.started_walking = True
                            player.direction = "up"
                            player.set_player_walking()
                            break
                    if self.started_walking == False:
                        player.x = x_previous
                        player.y = y_previous
                        player.rect[0] = player.x
                        player.rect[1] = player.y
                
                elif player.game.is_button_released(LEFT_BUTTON) and self.entrance_direction == "w":
                    player.x -= 1
                    player.rect[0] = player.x

                    for map_path in player.world_map.map_path:
                        if player.rect.colliderect(map_path.rect):
                            self.started_walking = True
                            player.direction = "left"
                            player.set_player_walking()
                            break

                    if self.started_walking == False:
                        player.x = x_previous
                        player.y = y_previous
                        player.rect[0] = player.x
                        player.rect[1] = player.y

                elif player.game.is_button_released(RIGHT_BUTTON) and self.entrance_direction == "e":
                    player.x += 1
                    player.rect[0] = player.x

                    for map_path in player.world_map.map_path:
                        if player.rect.colliderect(map_path.rect):
                            self.started_walking = True
                            player.direction = "right"
                            player.set_player_walking()
                            
                            break
                    if self.started_walking == False:
                        player.x = x_previous
                        player.y = y_previous
                        player.rect[0] = player.x
                        player.rect[1] = player.y

            else:
                if player.game.is_button_released(DOWN_BUTTON):
                    
                    player.y += 1
                    player.rect[1] = player.y

                    for map_path in player.world_map.map_path:
                        if player.rect.colliderect(map_path.rect):
                            self.started_walking = True
                            player.direction = "down"
                            player.set_player_walking()
                            break
                    if self.started_walking == False:
                        player.x = x_previous
                        player.y = y_previous
                        player.rect[0] = player.x
                        player.rect[1] = player.y

                elif player.game.is_button_released(UP_BUTTON):
                    player.y -= 1
                    player.rect[1] = player.y

                    for map_path in player.world_map.map_path:
                        if player.rect.colliderect(map_path.rect):
                            self.started_walking = True
                            player.direction = "up"
                            player.set_player_walking()
                            break
                    if self.started_walking == False:
                        player.x = x_previous
                        player.y = y_previous
                        player.rect[0] = player.x
                        player.rect[1] = player.y
                
                elif player.game.is_button_released(LEFT_BUTTON):
                    player.x -= 1
                    player.rect[0] = player.x

                    for map_path in player.world_map.map_path:
                        if player.rect.colliderect(map_path.rect):
                            self.started_walking = True
                            player.direction = "left"
                            player.set_player_walking()
                            break

                    if self.started_walking == False:
                        player.x = x_previous
                        player.y = y_previous
                        player.rect[0] = player.x
                        player.rect[1] = player.y

                elif player.game.is_button_released(RIGHT_BUTTON):
                    player.x += 1
                    player.rect[0] = player.x

                    for map_path in player.world_map.map_path:
                        if player.rect.colliderect(map_path.rect):
                            self.started_walking = True
                            player.direction = "right"
                            player.set_player_walking()
                            
                            break
                    if self.started_walking == False:
                        player.x = x_previous
                        player.y = y_previous
                        player.rect[0] = player.x
                        player.rect[1] = player.y
        
        else:
            if player.game.is_button_released(DOWN_BUTTON):
                        
                player.y += 1
                player.rect[1] = player.y

                for map_path in player.world_map.map_path:
                    if player.rect.colliderect(map_path.rect):
                        self.started_walking = True
                        player.direction = "down"
                        player.set_player_walking()
                        break

                if self.started_walking == False:
                    player.x = x_previous
                    player.y = y_previous
                    player.rect[0] = player.x
                    player.rect[1] = player.y

            elif player.game.is_button_released(UP_BUTTON):
                player.y -= 1
                player.rect[1] = player.y

                for map_path in player.world_map.map_path:
                    if player.rect.colliderect(map_path.rect):
                        self.started_walking = True
                        player.direction = "up"
                        player.set_player_walking()
                        break
                if self.started_walking == False:
                    player.x = x_previous
                    player.y = y_previous
                    player.rect[0] = player.x
                    player.rect[1] = player.y
            
            elif player.game.is_button_released(LEFT_BUTTON):
                player.x -= 1
                player.rect[0] = player.x

                for map_path in player.world_map.map_path:
                    if player.rect.colliderect(map_path.rect):
                        self.started_walking = True
                        player.direction = "left"
                        player.set_player_walking()
                        break

                if self.started_walking == False:
                    player.x = x_previous
                    player.y = y_previous
                    player.rect[0] = player.x
                    player.rect[1] = player.y

            elif player.game.is_button_released(RIGHT_BUTTON):
                player.x += 1
                player.rect[0] = player.x

                for map_path in player.world_map.map_path:
                    if player.rect.colliderect(map_path.rect):
                        self.started_walking = True
                        player.direction = "right"
                        player.set_player_walking()
                        
                        break
                if self.started_walking == False:
                    player.x = x_previous
                    player.y = y_previous
                    player.rect[0] = player.x
                    player.rect[1] = player.y

class IdleOnLanding(State):

    def on_state_enter(self, player: Player):
        player.animated_sprite.set_animation("down")
        self.started_walking = False

    def update(self, player: Player):
        x_previous = player.x
        y_previous = player.y
        # started_walking = False

        if player.game.is_button_released(DOWN_BUTTON):
            
            player.y += 1
            player.rect[1] = player.y

            for map_path in player.world_map.map_path:
                if player.rect.colliderect(map_path.rect):
                    self.started_walking = True
                    player.direction = "down"
                    player.set_player_walking()
                    break
            if self.started_walking == False:
                player.x = x_previous
                player.y = y_previous
                player.rect[0] = player.x
                player.rect[1] = player.y
        
        elif player.game.is_button_released(UP_BUTTON):
            player.y -= 1
            player.rect[1] = player.y

            for map_path in player.world_map.map_path:
                if player.rect.colliderect(map_path.rect):
                    self.started_walking = True
                    player.direction = "up"
                    player.set_player_walking()
                    break
            if self.started_walking == False:
                player.x = x_previous
                player.y = y_previous
                player.rect[0] = player.x
                player.rect[1] = player.y
            
        elif player.game.is_button_released(LEFT_BUTTON):
            player.x -= 1
            player.rect[0] = player.x

            for map_path in player.world_map.map_path:
                if player.rect.colliderect(map_path.rect):
                    self.started_walking = True
                    player.direction = "left"
                    player.set_player_walking()
                    break

            if self.started_walking == False:
                player.x = x_previous
                player.y = y_previous
                player.rect[0] = player.x
                player.rect[1] = player.y

        elif player.game.is_button_released(RIGHT_BUTTON):
            player.x += 1
            player.rect[0] = player.x

            for map_path in player.world_map.map_path:
                if player.rect.colliderect(map_path.rect):
                    self.started_walking = True
                    player.direction = "right"
                    player.set_player_walking()
                    
                    break
            if self.started_walking == False:
                player.x = x_previous
                player.y = y_previous
                player.rect[0] = player.x
                player.rect[1] = player.y

        # if started_walking == False:
        #     player.x = x_previous
        #     player.y = y_previous
        #     player.rect[0] = player.x
        #     player.rect[1] = player.y
        
        
                    

class Walking(State):
    def on_state_enter(self, player: Player):
        self.x = 0
        self.y = 0
        if player.direction == "down":
            player.animated_sprite.set_animation("down")
            self.y = 1
        if player.direction == "up":
            player.animated_sprite.set_animation("up")
            self.y = -1
        if player.direction == "left":
            player.animated_sprite.set_animation("left")
            self.x = -1
        if player.direction == "right":
            player.animated_sprite.set_animation("right")
            self.x = 1
    
    def update(self, player: Player):

        if player.walking_speed_step == 0:
            player.x += self.x
            player.y += self.y
            player.camera.move(self.x, self.y)

            entrance_direction = 0

            if self.x == 1 and self.y == 0:
                entrance_direction = "w"
            if self.x == -1 and self.y == 0:
                entrance_direction = "e"
            if self.x == 0 and self.y == 1:
                entrance_direction = "n"
            if self.x == 0 and self.y == -1:
                entrance_direction = "s"

            for landing in player.world_map.landings:
                if player.rect.colliderect(landing.rect):
                    if player.x == landing.x and player.y == landing.y:
                        player.set_player_idle_on_landing()

            for level in player.world_map.level_tiles:
                if player.rect.colliderect(level.rect):
                    if player.x == level.x and player.y == level.y:
                        player.set_player_idle_on_level(level.level_name, entrance_direction)

class Init(State):
    def on_state_enter(self, player: Player):
        player.set_player_idle()


class Idle(State):

    def update(self, player: Player):
        for level_tile in player.world_map.level_tiles:
            if player.rect.colliderect(level_tile.rect):
                player.current_level = level_tile.level_name
                player.set_player_idle()

        for landing in player.world_map.landings:          
            if player.rect.colliderect(landing.rect):
                player.set_player_idle_on_landing(no_sound=True)

player_states = {
                    "init" : Init,
                    "idle" : Idle,
                    "idle_on_landing" : IdleOnLanding,
                    "idle_on_level" : IdleOnLevel,
                    "walking" : Walking

                }