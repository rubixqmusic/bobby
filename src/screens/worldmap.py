import logging
import pygame
import math

from settings import *
from src.state import State
from src.camera import Camera
from src.worldmap.mappath import MapPath
from src.worldmap.landing import Landing
from src.worldmap.leveltile import LevelTile
from src.worldmap.player import Player
from src.animatedsprite import AnimatedSprite

WORLD_MAP_MUSIC = f"{MUSIC_PATH}/world_map.mp3"
BACKGROUND_IMAGE = f"{GRAPHICS_PATH}/backgrounds/world_map_background.png"

MAP_ANIMATED_TILESET = f"{GRAPHICS_PATH}/animated_tilesets/world_map_tileset.png"
MAP_ANIMATION = f"{TILESET_ANIMATIONS_PATH}/world_map_tileset.json"
MAP_BOX = f"{GRAPHICS_PATH}/backgrounds/world_map_box.png"
MAP_POSITION = 91, 66

MAP_PATH_IMAGE = f"{GRAPHICS_PATH}/world_map/map_path.png"
MAP_LANDING_IMAGE = f"{GRAPHICS_PATH}/world_map/landing.png"

LEVEL_TILE_SPRITESHEET = f"{GRAPHICS_PATH}/world_map/level_tile.png"
LEVEL_TILE_ANIMATION = f"{ANIMATIONS_PATH}/level_tile.json"

PLAYER_SPRITESHEET = f"{GRAPHICS_PATH}/world_map/world_map_player.png"
PLAYER_ANIMATION = f"{ANIMATIONS_PATH}/world_map_player.json"

QUIT_MENU_IMAGE = f"{GRAPHICS_PATH}/text_box/text_box.png"
QUIT_MENU_SELECT_SOUND = f"{SOUNDS_PATH}/menu_select.wav"
RETURN_TO_MAIN_MENU_SOUND = f"{SOUNDS_PATH}/return_to_main_menu.wav"
LEVEL_START_SOUND = f"{SOUNDS_PATH}/level_start.wav"
MENU_OPEN_SOUND = f"{SOUNDS_PATH}/menu_open.wav"
MENU_CLOSE_SOUND = f"{SOUNDS_PATH}/menu_close.wav"


PERCENT_TO_PLAN_CENTER = [132,38]
LEVEL_NAME_CENTER = [304,38]

MAX_TEXT_GROW = 5.0
TEXT_GROW_STEP_SIZE = 0.1

GO_BOBBY_TEXT = f"It's Bobby Time!"



class WorldMap(State):
    def on_state_enter(self, game):
        
        self.game = game
        self.paused = False

        self.sine_degrees = 0
        self.grow_factor = 0

        self.animated_tileset = None

        self.camera = Camera(0, 0, WORLD_MAP_WIDTH, WORLD_MAP_HEIGHT)
        
        self.background_image = pygame.image.load(game.load_resource(BACKGROUND_IMAGE)).convert_alpha()
        self.background_image.set_alpha(200)
        self.map_box = pygame.image.load(game.load_resource(MAP_BOX)).convert_alpha()

        self.tilesets = {}
        self.tile_size = 16

        self.font_size = 12
        self.font_color = GOLD_COLOR
        self.font = pygame.font.Font(game.load_resource(f"{FONTS_PATH}/{DEFAULT_FONT}"), self.font_size)

        self.tile_layer_1 = {}
        self.tile_layer_2 = {}
        self.level_tiles = []
        self.map_path = []
        self.landings = []
        self.player = None
        self.overlay_layer_1 = {}

        self.scene_x = 0
        self.scene_y = 0
        self.scene_width = 0
        self.scene_height = 0

        self.scene_name = None
        self.level_name = None
        self.level_name_surface = None
        self.percent_to_plan_surface = None

        game.play_music(WORLD_MAP_MUSIC)

        current_level = self.game.get_save_data('current_level')
        scene_name = None
        player_start_position = None

        if current_level == None:
            scene_name = WORLD_MAP_DEFAULT_SCENE
            for level in self.game.get_levels_from_world():
                if scene_name == level["identifier"]:
                    level_layers = level["layerInstances"]

                    for layer in level_layers:
                        if layer["__identifier"] == ENTITIES_LAYER_NAME:
                            entity_instances = layer["entityInstances"]
                            for entity in entity_instances:
                                if entity["__identifier"] == "world_map_object":
                                    entity_properties = entity["fieldInstances"]
                                    for property in entity_properties:
                                        if property["__value"] == "default_start":
                                            x = entity["__worldX"]
                                            y = entity["__worldY"]
                                            player_start_position = [x,y]

        else:
            for level in self.game.get_levels_from_world():
                level_name = level["identifier"]
                level_layers = level["layerInstances"]

                for layer in level_layers:
                    if layer["__identifier"] == ENTITIES_LAYER_NAME:
                        entity_instances = layer["entityInstances"]
                        for entity in entity_instances:
                            if entity["__identifier"] == "world_map_object":
                                entity_properties = entity["fieldInstances"]
                                for property in entity_properties:
                                    if property["__identifier"] == "level_name":
                                        if property["__value"] == current_level:
                                            scene_name = level_name
                                            x = entity["__worldX"]
                                            y = entity["__worldY"]
                                            player_start_position = [x,y]

        self.state = State(world_map_states)

        self.load_map(scene_name, player_start_position)
    
    def process_events(self, game):
        if game.game_should_quit():
            game.quit_game()
        self.state.process_events(self)

    def update(self, game):

        self.grow_factor = int(math.sin(self.sine_degrees) * MAX_TEXT_GROW)
        self.sine_degrees += TEXT_GROW_STEP_SIZE%MAX_TEXT_GROW

    
        if not self.paused:
            if self.animated_tileset:
                self.animated_tileset.update()

            if self.level_tiles:
                for level_tile in self.level_tiles:
                    level_tile.update()
            
            if self.player:
                self.player.update()

        self.state.update(self)
    
    def draw(self, game):

        if self.animated_tileset:
            self.animated_tileset.draw()

        game.get_screen().fill("#000000")
        game.get_screen().blit(self.background_image, (0,0))
        game.get_screen().blit(self.map_box, (0,0))
        self.camera.surface.fill("#000000")


        # future you: to solve the animated tile problem, just set an animated sprites draw target to the tileset's image
        # in the 'tilesets' dictionary. then call update, and draw, and then blit from the tileset image

        if self.tile_layer_1:
            
            tileset_path = f"{BASE_PATH}{self.tile_layer_1['tileset']}"

            if tileset_path in self.tilesets:
                tileset_image = self.tilesets[tileset_path]
                for tile in self.tile_layer_1["tiles"]:
                    dest = tile["px"]
                    source = tile["src"]
                    grid_size = self.tile_layer_1["grid_size"]
                    camera_pos = self.camera.get_position()
                    draw_x = dest[0] - camera_pos[0]
                    draw_y = dest[1] - camera_pos[1]
                    self.camera.surface.blit(tileset_image,[draw_x,draw_y],[source[0], source[1], grid_size, grid_size])

    
            
        if self.tile_layer_2:
            tileset_path = f"{BASE_PATH}{self.tile_layer_2['tileset']}"

            if tileset_path in self.tilesets:
                tileset_image = self.tilesets[tileset_path]
                for tile in self.tile_layer_2["tiles"]:
                    dest = tile["px"]
                    source = tile["src"]
                    grid_size = self.tile_layer_2["grid_size"]
                    camera_pos = self.camera.get_position()
                    draw_x = dest[0] - camera_pos[0]
                    draw_y = dest[1] - camera_pos[1]
                    self.camera.surface.blit(tileset_image,[draw_x,draw_y],[source[0], source[1], grid_size, grid_size])
        
        if self.map_path:
            for map_path in self.map_path:
                dest = [map_path.x, map_path.y]
                camera_pos = self.camera.get_position()
                dest[0] -= camera_pos[0]
                dest[1] -= camera_pos[1]
                self.camera.surface.blit(map_path.image, dest)

        if self.landings:
            for landing in self.landings:
                dest = [landing.x, landing.y]
                camera_pos = self.camera.get_position()
                dest[0] -= camera_pos[0]
                dest[1] -= camera_pos[1]
                self.camera.surface.blit(landing.image, dest)
        
        if self.level_tiles:
            for level_tile in self.level_tiles:
                level_tile.draw()
        
        if self.player:
            self.player.draw()
        
        if self.overlay_layer_1:
            tileset_path = f"{BASE_PATH}{self.overlay_layer_1['tileset']}"

            if tileset_path in self.tilesets:  
                tileset_image = self.tilesets[tileset_path]
                for tile in self.overlay_layer_1["tiles"]:
                    dest = tile["px"]
                    source = tile["src"]
                    grid_size = self.overlay_layer_1["grid_size"]
                    camera_pos = self.camera.get_position()
                    draw_x = dest[0] - camera_pos[0]
                    draw_y = dest[1] - camera_pos[1]
                    self.camera.surface.blit(tileset_image,[draw_x,draw_y],[source[0], source[1], grid_size, grid_size])

        self.game.get_screen().blit(self.camera.surface, MAP_POSITION)

        if self.level_name_surface:
            level_name_rect = self.level_name_surface.get_rect(center=LEVEL_NAME_CENTER)
            self.game.get_screen().blit(self.level_name_surface, level_name_rect)
        if self.percent_to_plan_surface:
            percent_rect = self.percent_to_plan_surface.get_rect(center=PERCENT_TO_PLAN_CENTER)
            self.game.get_screen().blit(self.percent_to_plan_surface, percent_rect)
        
        self.state.draw(self)


    def load_tileset(self, image_path):
        if image_path not in self.tilesets:
            if self.game.resource_exists(image_path):
                new_tileset_surface = pygame.image.load(self.game.load_resource(image_path)).convert_alpha()
                self.tilesets[image_path] = new_tileset_surface
            else:
                logging.debug(f"could not load tileset! image path {image_path} does not exist!")
        else:
            if self.game.resource_exists(image_path):
                new_tileset_surface = pygame.image.load(self.game.load_resource(image_path)).convert_alpha()
                self.tilesets[image_path] = new_tileset_surface
            else:
                logging.debug(f"could not load tileset! image path {image_path} does not exist!")
    

    def set_current_level(self, level_name):
        if level_name == None:
            return
        if level_name == "landing":
            self.level_name = "landing"
            self.level_name_surface = None
            self.percent_to_plan_surface = None
            return
        level_data = self.game.get_level_data(level_name)
        if level_data:
            self.level_name = level_name
            self.level_name_surface = self.font.render(f"{level_data['name']}",True,self.font_color)
            self.percent_to_plan_surface = self.font.render(f"{level_data['percent_to_plan']}/100 %",True,self.font_color)

    def pause(self):
        self.paused = True
    
    def unpause(self):
        self.paused = False

    def load_map(self, scene_name, player_start_position):
        self.pause() 
        self.state.set_state(self, "load_map", scene_name, player_start_position)   
    
    def fade_in(self):
        self.pause()
        self.state.set_state(self, "fade_in")

    def map_active(self):
        self.unpause()
        self.state.set_state(self, "map_active")
    
    def start_level(self):
        self.game.play_sound(LEVEL_START_SOUND)
        self.game.stop_music()
        self.state.set_state(self, "start_level")

    def quit_menu(self):
        self.pause()
        self.state.set_state(self, "quit_menu")
    
    def quit_to_main_menu(self):
        self.state.set_state(self, "quit_to_main_menu")

    def load_scene(self):
        for level in self.level_tiles:
            if level.level_name == self.level_name:
                if level.leads_to_scene == None:
                    return
                else:
                    leads_to_scene_data = level.leads_to_scene
                    scene_and_starting_position = self.game.get_scene_and_starting_position_from_iid(leads_to_scene_data["levelIid"], leads_to_scene_data["entityIid"])
                    if scene_and_starting_position == None:
                        return
                    else:
                        self.game.load_level(scene_and_starting_position[0], scene_and_starting_position[1], DEFAULT_TRANSITION)

class QuitToMainMenu(State):
    def on_state_enter(self, world_map: WorldMap):
        self.min_fade = 0
        self.max_fade = 255
        self.fade = self.max_fade
        self.fade_step = 5
    
    def draw(self, world_map: WorldMap):
        if self.fade > self.min_fade:
            world_map.game.get_screen().fill((self.fade,self.fade,self.fade), special_flags=pygame.BLEND_MULT)
            self.fade -= self.fade_step
        else:
            self.fade = 0
            world_map.game.get_screen().fill((self.fade,self.fade,self.fade), special_flags=pygame.BLEND_MULT)
            world_map.game.load_title_screen()


class StartLevel(State):
    def on_state_enter(self, world_map: WorldMap):
        self.rectangle_height = 16
        self.rectangle_width = SCREEN_WIDTH + 128
        self.x_step_size = 10
        self.x_step = 0
        self.max_x = SCREEN_WIDTH 
        self.num_rectangles = int(SCREEN_HEIGHT/self.rectangle_height)
        
        self.go_bobby_text_surface = world_map.font.render(GO_BOBBY_TEXT, True, GOLD_COLOR)

        self.timer = 20

        self.status = "wait"
    
    def update(self, world_map: WorldMap):
        if self.status == "wait":
            self.timer -= 1
            if self.timer < 0:
                self.timer = 20
                self.status = "rectangles"

        elif self.status == "rectangles":
            self.x_step += self.x_step_size
            if self.x_step > self.max_x:
                self.status = "hold_1"

        elif self.status == "hold_1":
            self.timer -= 1
            if self.timer < 0:
                self.timer = 120
                self.status = "go_bobby"
        
        elif self.status == "go_bobby":
            self.timer -= 1
            if self.timer < 0:
                self.timer = 60
                self.status = "hold_2"
        
        elif self.status == "hold_2":
            self.timer -= 1
            if self.timer < 0:
                self.timer = 120
                world_map.load_scene()
            
    
    def draw(self, world_map: WorldMap):
        if self.status == "rectangles":
            for rectangle in range(self.num_rectangles):
                if rectangle%2 == 1:
                    x = SCREEN_WIDTH - self.x_step
                elif rectangle%2 == 0:
                    x = -SCREEN_WIDTH + self.x_step
                rect = pygame.rect.Rect(x,rectangle*self.rectangle_height,self.rectangle_width, self.rectangle_height)
                pygame.draw.rect(world_map.game.get_screen(),f"#000000", rect, border_radius=20)

        elif self.status == "hold_1":
            world_map.game.get_screen().fill(f"#000000")

        elif self.status == "go_bobby":
            rect = self.go_bobby_text_surface.get_rect(center=(SCREEN_WIDTH/2,SCREEN_HEIGHT/2))
            world_map.game.get_screen().fill(f"#000000")
            world_map.game.get_screen().blit(self.go_bobby_text_surface, rect)
        
        elif self.status == "hold_2":
            world_map.game.get_screen().fill(f"#000000")
        


class LoadMap(State):
    def __init__(self, states: dict, *args) -> None:
        super().__init__(states, *args)
        self.scene_name = args[0]
        self.player_start_position = args[1]

    def on_state_enter(self, world_map: WorldMap):
        # world_map.pause()
        self.game = world_map.game
        world_map.tile_layer_1 = {}
        world_map.tile_layer_2 = {}
        world_map.level_tiles = []
        world_map.map_path = []
        world_map.player = None
        world_map.overlay_layer_1 = {}
        world_map.scene_x = 0
        world_map.scene_y = 0
        world_map.scene_width = 0
        world_map.scene_height = 0

        for level in self.game.get_levels_from_world():
            if level["identifier"] == self.scene_name:
                '''this is where all of the code goes that you want to run when the world map scene loads. 
                this is where the loading starts '''
                world_map.scene_name = level["identifier"]
                world_map.scene_x = level["worldX"]
                world_map.scene_y = level["worldY"]
                world_map.scene_width = level["pxWid"]
                world_map.scene_height = level["pxHei"]
                level_layers = level["layerInstances"]

                for layer in level_layers:
                    if layer["__identifier"] == GROUND_1_LAYER_NAME:
                        world_map.tile_layer_1["tileset"] = layer["__tilesetRelPath"]
                        world_map.tile_layer_1["grid_size"] = layer["__gridSize"]
                        world_map.tile_layer_1["tiles"] = layer["gridTiles"]
                        world_map.load_tileset(f"{BASE_PATH}{world_map.tile_layer_1['tileset']}")
                    if layer["__identifier"] == GROUND_2_LAYER_NAME:
                        world_map.tile_layer_2["tileset"] = layer["__tilesetRelPath"]
                        world_map.tile_layer_2["grid_size"] = layer["__gridSize"]
                        world_map.tile_layer_2["tiles"] = layer["gridTiles"]
                        world_map.load_tileset(f"{BASE_PATH}{world_map.tile_layer_2['tileset']}")

                    if layer["__identifier"] == ENTITIES_LAYER_NAME:
                        entity_instances = layer["entityInstances"]
                        for entity in entity_instances:
                            if entity["__identifier"] == "world_map_object":
                                entity_properties = entity["fieldInstances"]
                                for property in entity_properties:
                                    if property["__value"] == "path":
                                        try:
                                            image = pygame.image.load(self.game.load_resource(MAP_PATH_IMAGE))
                                        except:
                                            logging.debug(f"could not load map path image!!!")
                                            image = pygame.surface.Surface([entity["width"], entity["height"]])
                                        new_map_path = MapPath(entity["__worldX"], entity["__worldY"],entity["width"], entity["height"], image)
                                        world_map.map_path.append(new_map_path)
                                    if property["__value"] == "landing":
                                        try:
                                            image = pygame.image.load(self.game.load_resource(MAP_LANDING_IMAGE))
                                        except:
                                            logging.debug(f"could not load map path image!!!")
                                            image = pygame.surface.Surface([entity["width"], entity["height"]])
                                        new_map_landing = Landing(entity["__worldX"], entity["__worldY"],entity["width"], entity["height"], image)
                                        world_map.landings.append(new_map_landing)
                                    if property["__value"] == "level_tile":
                                        level_name = None
                                        leads_to_scene = None
                                        for property in entity_properties:
                                            if property["__identifier"] == "level_name":
                                                level_name = property["__value"]
                                            if property["__identifier"] == "leads_to_scene":
                                                leads_to_scene = property["__value"]
                                        try:
                                            spritesheet = LEVEL_TILE_SPRITESHEET
                                        except:
                                            logging.debug(f"could not load map path image!!!")
                                            # spritesheet = pygame.surface.Surface([entity["width"], entity["height"]])
                                        
                                        animation = LEVEL_TILE_ANIMATION

                                        new_level_tile = LevelTile(self.game, level_name, entity["__worldX"], entity["__worldY"], entity["width"],spritesheet, animation, world_map.camera.surface, world_map.camera, leads_to_scene)
                                        # entity["__worldX"], entity["__worldY"],entity["width"], entity["height"], image
                                        world_map.level_tiles.append(new_level_tile)

                    if layer["__identifier"] == OVERLAY_1_LAYER_NAME:
                        world_map.overlay_layer_1["tileset"] = layer["__tilesetRelPath"]
                        world_map.overlay_layer_1["grid_size"] = layer["__gridSize"]
                        world_map.overlay_layer_1["tiles"] = layer["gridTiles"]
                        world_map.load_tileset(f"{BASE_PATH}{world_map.overlay_layer_1['tileset']}")
                break
        
        world_map.animated_tileset = AnimatedSprite(world_map.game, world_map.tilesets[f"{BASE_PATH}{world_map.tile_layer_1['tileset']}"])
        world_map.animated_tileset.load_spritesheet(MAP_ANIMATED_TILESET)
        world_map.animated_tileset.load_sprite_data(MAP_ANIMATION)
        world_map.animated_tileset.set_animation("idle")
        world_map.animated_tileset.play()

        # print(world_map.animated_tileset.spritesheet, world_map.animated_tileset.animations)
        
        world_map.player = Player(self.game, world_map, self.player_start_position[0], self.player_start_position[1],world_map.tile_size, world_map.tile_size, PLAYER_SPRITESHEET, PLAYER_ANIMATION,world_map.camera.surface,world_map.camera)
        
        world_map.camera.set_bounds(world_map.scene_x, world_map.scene_x + world_map.scene_width, world_map.scene_y, world_map.scene_y + world_map.scene_height)
        # world_map.camera.set_position(467,300)
        world_map.camera.center(self.player_start_position[0], self.player_start_position[1])
        world_map.fade_in()
    
    def draw(self, world_map):
        world_map.game.get_screen().fill("#000000")
        

class FadeIn(State):
    def on_state_enter(self, world_map: WorldMap):
        self.min_fade = 0
        self.max_fade = 255
        self.fade = self.min_fade
        self.fade_step = 5
    
    def draw(self, world_map: WorldMap):
        if self.fade < self.max_fade:
            world_map.game.get_screen().fill((self.fade,self.fade,self.fade), special_flags=pygame.BLEND_MULT)
            self.fade += self.fade_step
        else:
            world_map.map_active()
    
    # def on_state_exit(self, world_map: WorldMap):
    #     world_map.unpause()


class MapActive(State):
    def update(self, world_map: WorldMap):
        if world_map.game.is_button_released(SELECT_BUTTON):
            world_map.quit_menu()


class QuitMenu(State):
    def on_state_enter(self, world_map: WorldMap):
        self.menu_box_surface = pygame.image.load(world_map.game.load_resource(QUIT_MENU_IMAGE))
        self.menu_box_rect = self.menu_box_surface.get_rect()
        self.menu_box_width = self.menu_box_surface.get_width()
        self.max_menu_box_y = self.menu_box_surface.get_height()
        self.min_menu_box_size = 1
        self.menu_box_step_size = 10
        self.menu_box_step = 0

        self.current_menu_selection = "continue"

        self.menu = [
                        {"name" : "continue", "text": "Continue", "position" : [SCREEN_WIDTH/2, 128]},
                        {"name" : "return_to_main_menu", "text": "Return To Main Menu", "position" : [SCREEN_WIDTH/2, 160]}
                    ]
        
        self.set_status("open_menu")
        world_map.game.play_sound(MENU_OPEN_SOUND)

    def update(self, world_map: WorldMap):
        if self.status == "open_menu":
            self.open_menu()

        elif self.status == "menu_active":
            if world_map.game.is_button_released(SELECT_BUTTON):
                self.set_status("close_menu")
                world_map.game.play_sound(MENU_CLOSE_SOUND)
            
            if world_map.game.is_button_released(DOWN_BUTTON):
                self.current_menu_selection = get_next_menu_item(self.menu, self.current_menu_selection)
                world_map.game.play_sound(QUIT_MENU_SELECT_SOUND)
            if world_map.game.is_button_released(UP_BUTTON):
                self.current_menu_selection = get_previous_menu_item(self.menu, self.current_menu_selection)
                world_map.game.play_sound(QUIT_MENU_SELECT_SOUND)

            if world_map.game.is_button_released(START_BUTTON) or world_map.game.is_button_released(ACTION_BUTTON_1):
                if self.current_menu_selection == "continue":
                    self.set_status("close_menu")
                    world_map.game.play_sound(MENU_CLOSE_SOUND)
                elif self.current_menu_selection == "return_to_main_menu":
                    world_map.quit_to_main_menu()
                    world_map.game.play_sound(RETURN_TO_MAIN_MENU_SOUND)
                    world_map.game.stop_music()
            

        elif self.status == "close_menu":
            self.close_menu()
                # world_map.map_active()
        elif self.status == "return_to_map":
            world_map.map_active()
    

    def draw(self, world_map: WorldMap):
        if self.status == "open_menu":
            scaled_menu_image = pygame.transform.scale(self.menu_box_surface, [self.menu_box_width, self.menu_box_step])
            menu_rect = scaled_menu_image.get_rect(center=(SCREEN_WIDTH/2,SCREEN_HEIGHT/2))
            world_map.game.get_screen().blit(scaled_menu_image, menu_rect)
        
        if self.status == "menu_active":
            # scaled_menu_image = pygame.transform.scale(self.menu_box_surface, [self.menu_box_width, self.menu_box_step])
            menu_rect = self.menu_box_surface.get_rect(center=(SCREEN_WIDTH/2,SCREEN_HEIGHT/2))
            world_map.game.get_screen().blit(self.menu_box_surface, menu_rect)
            draw_menu(self.menu, self.current_menu_selection, world_map.font, world_map.font_color, world_map.game.get_screen(),world_map.grow_factor)

        if self.status == "close_menu":
            scaled_menu_image = pygame.transform.scale(self.menu_box_surface, [self.menu_box_width, self.menu_box_step])
            menu_rect = scaled_menu_image.get_rect(center=(SCREEN_WIDTH/2,SCREEN_HEIGHT/2))
            world_map.game.get_screen().blit(scaled_menu_image, menu_rect)

    def set_status(self, status):
        self.status = status

    def open_menu(self):
        self.menu_box_step += self.menu_box_step_size
        if self.menu_box_step > self.max_menu_box_y:
            self.menu_box_step = self.max_menu_box_y
            self.set_status("menu_active")
    
    def close_menu(self):
        self.menu_box_step -= self.menu_box_step_size
        if self.menu_box_step < 1:
            self.menu_box_step = 1
            self.set_status("return_to_map")


def draw_menu(menu: list, 
              current_selection: str, 
            #   y_start: int, 
            #   y_spacing: int, 
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
            drop_shadow_surface = font.render(menu_item['text'],True,drop_shadow_color)
        
        if menu_item["name"] == current_selection:
            if drop_shadow_surface is not None:
                drop_shadow_surface_new = pygame.transform.scale(drop_shadow_surface, 
                                    (text_surface_base_size[0] + grow_factor, 
                                    text_surface_base_size[1] + grow_factor))
                drop_shadow_rect = drop_shadow_surface_new.get_rect(center=(menu_item["position"][0] + drop_shadow_x, menu_item["position"][1]+drop_shadow_y))
                destination_surface.blit(drop_shadow_surface, drop_shadow_rect)
            
            new_surface = pygame.transform.scale(text_surface, 
                                    (text_surface_base_size[0] + grow_factor, 
                                    text_surface_base_size[1] + grow_factor))
            text_rect = new_surface.get_rect(center=(menu_item["position"][0], menu_item["position"][1]))
            destination_surface.blit(new_surface, text_rect)
        else:
            if drop_shadow_surface is not None:
                drop_shadow_rect = drop_shadow_surface.get_rect(center=(menu_item["position"][0] + drop_shadow_x, menu_item["position"][1]+drop_shadow_y))
                destination_surface.blit(drop_shadow_surface, drop_shadow_rect)
            text_rect = text_surface.get_rect(center=(menu_item["position"][0], menu_item["position"][1]))
            destination_surface.blit(text_surface, text_rect)
    
        menu_item_index += 1
    ...

def get_next_menu_item(menu: list, current_selection: str):
    index = 0
    for menu_item in menu:
        if menu_item["name"] == current_selection:
            index += 1
            if index > len(menu) - 1:
                index = 0
            return menu[index]["name"]
        index += 1

def get_previous_menu_item(menu: list, current_selection: str):
    index = 0
    for menu_item in menu:
        if menu_item["name"] == current_selection:
            index -= 1
            if index < 0:
                index = len(menu) - 1
            return menu[index]["name"]
        index += 1
    # return current_selection


world_map_states = {
                    "fade_in" : FadeIn,
                    "load_map" : LoadMap,
                    "map_active" : MapActive,
                    "quit_menu" : QuitMenu,
                    "start_level" : StartLevel,
                    "quit_to_main_menu" : QuitToMainMenu
                    }