import logging
import pygame
import math

from src.screens.gameplay.resources import *
from src.screens.gameplay.screenstates import level_states
from src.state import State
from src.camera import Camera
from src.hud import Hud
from src.animatedsprite import AnimatedSprite
from src.particleengine import ParticleEngine

from src.components.hitbox import Hitbox

from src.entities.coin.coin import Coin
from src.entities.stone.stone import Stone
from src.entities.item.item import Item


class Gameplay(State):
    def __init__(self, states: dict, *args) -> None:
        super().__init__(states, *args)
        self.level_name = args[0]
        self.scene_name = None

        self.player_start_position = args[1]
        self.transition_in = args[2]
        self.transition_out = None
        self.paused = False
        self.text_grow_factor = 0
        self.sine_degrees = 0
        self.onscreen_tile_count = 0
        self.hitboxes = {}
        self.particle_engine = None
        self.new_entity_queue = []
        self.hud = None

        self.time_limit_ticks = TIME_LIMIT_TICK_INTERVAL
        self.time_limit = 0
        self.time_limit_enabled = False
        self.money = 0
        self.stones = 0
        self.quota = 0
        self.player_health = MAX_PLAYER_HEALTH
        
        self.clear_scene()
    
    def clear_scene(self):
        self.hitboxes = {}

        for type in HITBOX_TYPES:
            self.hitboxes[type] = []
            for i in range(MAX_HITBOXES):
                self.hitboxes[type].append(None)

        self.gravity = DEFAULT_GRAVITY
        self.width = None
        self.height = None
        self.tilesets = {}
        self.bg_color = f"#000000"
        self.bg_image = None
        self.bg_1 = None
        self.bg_2 = None
        self.bg_3 = None
        self.ground_1 = {}
        self.ground_2 = {}
        self.main_ground = {}
        self.objects = {}
        self.player = None
        self.entities = []

        for i in range(MAX_ENTITIES):
            self.entities.append(None)

        self.overlay_1 = {}
        self.overlay_2 = {}
        self.fg_1 = {}
        self.fg_2 = {}

    def on_state_enter(self, game):
        self.game = game
        level_data = self.game.get_level_data(self.level_name)
        if level_data:
            if "time_limit" in level_data:
                if level_data["time_limit"] > 0:
                    self.time_limit_enabled = True
                    self.time_limit = level_data["time_limit"]
            if "quota" in level_data:
                self.quota = level_data["quota"]
        self.font = pygame.font.Font(game.load_resource(PAUSE_MENU_FONT), PAUSE_MENU_FONT_SIZE)
        self.camera = Camera(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.transition_overlay = AnimatedSprite(self.game, self.game.get_screen())
        self.transition_overlay.load_spritesheet(TRANSITION_SPRITESHEET)
        self.transition_overlay.load_sprite_data(TRANSITION_ANIMATION)
        self.transition_overlay.set_animation("idle")

        self.hud = Hud(self)
        # self.hud.set_draw_target(self.camera.surface)
        
        self.particle_engine = ParticleEngine(MAX_PARTICLES, self.camera.surface, self.camera)
        self.state = State(level_states)

        # level_name = self.level_name
        self.load_scene(self.level_name, self.player_start_position, None, "money_in")

    def process_events(self, game):
        if game.game_should_quit():
            game.quit_game()
        # self.state.process_events(self)
    
    def update(self, game):
        delta = game.get_delta_time()
        if delta > 1000/FPS:
            delta = 1000/FPS
        self.text_grow_factor = int(math.sin(self.sine_degrees) * MAX_TEXT_GROW)
        self.sine_degrees += TEXT_GROW_STEP_SIZE%MAX_TEXT_GROW

        if self.time_limit_enabled and self.state.get_name() == "level_active":
            self.time_limit_ticks -= delta
            if self.time_limit_ticks <= 0:
                self.time_limit -= 1
                self.time_limit_ticks = TIME_LIMIT_TICK_INTERVAL

        if game.is_button_released(SELECT_BUTTON):
            self.pause_menu()

        if not self.paused:

            self._add_queued_entities_to_scene()

            for hitbox_type in self.hitboxes:
                hitbox_index = 0
                for hitbox in self.hitboxes[hitbox_type]:
                    if hitbox:
                        if hitbox._alive == False:
                            self.hitboxes[hitbox_type][hitbox_index] = None
                    hitbox_index += 1

            
            if self.bg_image:
                self.bg_image.update()

            entity_index = 0
            for entity in self.entities:
                if entity:
                    if entity._alive == False:
                        self.entities[entity_index] = None
                    elif hasattr(entity, "position") and not entity.update_if_not_in_view:
                        if self.camera.update_range.collidepoint(entity.position):
                            entity.update(delta)
                    # else:
                    #     entity.update(delta)
                entity_index += 1

            
            if self.player:
                self.player.update(delta)

        self.state.update(self)
        
        self.particle_engine.update(delta)

        if self.hud:
            self.hud.update(delta)

    def draw(self, game):
        self.onscreen_tile_count = 0
        
        # game.get_screen().fill(self.bg_color)

        self.camera.surface.fill(self.bg_color)

        if self.bg_image:
            self.bg_image.draw()
        
        if self.bg_1:
            camera_pos = self.camera.get_position()
            parallax_x = int(camera_pos[0] * self.bg_1["parallax_x"])
            parallax_y = int(camera_pos[1] * self.bg_1["parallax_y"])

            draw_x = 0 - parallax_x
            draw_y = 0 - parallax_y

            if draw_x < camera_pos[0]:
                draw_x -= self.bg_1["image"].get_width()
            if draw_x > camera_pos[0] + self.bg_1["image"].get_width():
                draw_x += self.bg_1["image"].get_width()

            wrap_x = draw_x + self.bg_1["image"].get_width()  

            self.camera.surface.blit(self.bg_1["image"], [draw_x,draw_y])
            self.camera.surface.blit(self.bg_1["image"], [wrap_x,draw_y])
        
        if self.bg_2:

            camera_pos = self.camera.get_position()

            # print(camera_pos)

            parallax_x = int(camera_pos[0] * self.bg_2["parallax_x"])
            parallax_y = int(camera_pos[1] * self.bg_2["parallax_y"])

            draw_x = 0 - parallax_x
            # draw_y = 0 - parallax_y 
            draw_y = 0 - parallax_y#camera_pos[1]  

            wrap_x = draw_x + self.bg_2["image"].get_width()  

            # print(self.game.get_fps())

                      
            self.camera.surface.blit(self.bg_2["image"], [draw_x,draw_y])
            self.camera.surface.blit(self.bg_2["image"], [wrap_x ,draw_y])

        if self.bg_3:
            camera_pos = self.camera.get_position()

            # print(camera_pos)

            parallax_x = int(camera_pos[0] * self.bg_3["parallax_x"]) % self.bg_3["image"].get_width()  
            parallax_y = int(camera_pos[1] * self.bg_3["parallax_y"])

            draw_x = 1 - parallax_x
            # draw_y = 0 - parallax_y 
            draw_y = 0 - parallax_y#camera_pos[1]  

            wrap_x = draw_x + self.bg_3["image"].get_width()  

                      
            self.camera.surface.blit(self.bg_3["image"], [draw_x,draw_y])
            self.camera.surface.blit(self.bg_3["image"], [wrap_x ,draw_y])
        
        if self.ground_2:
            tileset_path = f"{BASE_PATH}{self.ground_2['tileset']}"

            if tileset_path in self.tilesets:
                tileset_image = self.tilesets[tileset_path]
                for tile in self.ground_2["tiles"]:
                    dest = tile["px"]
                    source = tile["src"]
                    grid_size = self.ground_2["grid_size"]
                    tile_rect = pygame.rect.Rect(dest[0], dest[1], grid_size, grid_size)
                    if tile_rect.colliderect(self.camera.rect):
                        camera_pos = self.camera.get_position()
                        self.onscreen_tile_count += 1
                        draw_x = dest[0] - camera_pos[0]
                        draw_y = dest[1] - camera_pos[1]
                        self.camera.surface.blit(tileset_image,[draw_x,draw_y],[source[0], source[1], grid_size, grid_size])

        if self.main_ground:
            tileset_path = f"{BASE_PATH}{self.main_ground['tileset']}"

            if tileset_path in self.tilesets:
                tileset_image = self.tilesets[tileset_path]
                for tile in self.main_ground["tiles"]:
                    dest = tile["px"]
                    source = tile["src"]
                    grid_size = self.main_ground["grid_size"]
                    tile_rect = pygame.rect.Rect(dest[0], dest[1], grid_size, grid_size)
                    if tile_rect.colliderect(self.camera.rect):
                        self.onscreen_tile_count += 1
                        camera_pos = self.camera.get_position()
                        draw_x = dest[0] - camera_pos[0]
                        draw_y = dest[1] - camera_pos[1]
                        self.camera.surface.blit(tileset_image,[draw_x,draw_y],[source[0], source[1], grid_size, grid_size])
        
        for entity in self.entities:
            if entity:
                entity.draw()

        if self.player:
            self.player.draw()
        
        if self.hitboxes and DEBUG_ENABLED and DEBUG_SHOW_HITBOXES:
            for type in self.hitboxes:
                for hitbox in self.hitboxes[type]:
                    if hitbox is not None:
                        pygame.draw.rect(self.camera.surface, (0,0,255), (hitbox.get_hitbox()[0] - self.camera.x, hitbox.get_hitbox()[1] - self.camera.y, hitbox.get_hitbox()[2], hitbox.get_hitbox()[3]), 1)
                        
        if self.particle_engine:
            self.particle_engine.draw()
        
        if self.hud:
            self.hud.draw()

        self.game.get_screen().blit(self.camera.surface, [0,0])

        self.state.draw(self)

    def pause(self):
        self.paused = True
    
    def unpause(self):
        self.paused = False

    def load_scene(self, scene_name, player_start_position, transition_out=None, transition_in=None):
        self.scene_name = scene_name
        self.player_start_position = player_start_position
        self.transition_out = transition_out
        self.transition_in = transition_in
        if self.transition_out == None:
            self.state.set_state(self,"load_scene", scene_name, self.player_start_position, self.transition_in)
    
    def money_in_transition(self):
        self.state.set_state(self, "money_in_transition")
    
    def start_scene(self):
        self.state.set_state(self, "level_active")
    
    def level_active(self):
        self.unpause()
        self.state.set_state(self, "level_active")
    
    def return_to_title_screen(self):
        self.game.save_game()
        self.state.set_state(self, "return_to_title_screen")

    def return_to_world_map(self):
        self.state.set_state(self, "return_to_world_map")
    
    def pause_menu(self):
        if self.state.get_name() == "level_active":
            self.pause()
            self.state.set_state(self, "pause_menu")

    def get_onscreen_tile_count(self):
        return self.onscreen_tile_count
    
    def generate_particles(self, type, position, properties={}):
        self.particle_engine.generate_particles(type, position, properties)
    
    def add_entity_to_scene(self, entity):
        for attribute in entity.__dict__:
            if isinstance(entity.__dict__[attribute], Hitbox):
                self.register_hitbox(entity.__dict__[attribute])
        self.new_entity_queue.append(entity)

    def spawn_new_entity(self, entity_data):
        new_entity_properties = {properties["__identifier"]: properties["__value"] for properties in entity_data["fieldInstances"]}
        new_entity_properties["iid"] = entity_data["iid"] if "iid" in entity_data else None

        print(new_entity_properties)

        for property in new_entity_properties:
            if property == "type":
                if new_entity_properties[property] in ENTITIES:
                    return ENTITIES[new_entity_properties[property]](self, new_entity_properties)
                else:
                    return None
        
    
    
    def _add_queued_entities_to_scene(self):
        if self.new_entity_queue:
            entity_slot_index = 0
            new_entity_queue_index = 0
            for entity_slot in self.entities:
                if new_entity_queue_index > len(self.new_entity_queue) - 1:
                    break
                if entity_slot == None:
                    self.entities[entity_slot_index] = self.new_entity_queue[new_entity_queue_index]
                    new_entity_queue_index += 1
                entity_slot_index += 1
            self.new_entity_queue = []
    
    def register_hitbox(self, new_hitbox):
        hitbox_type = new_hitbox.get_type()
        if not hitbox_type in self.hitboxes:
            logging.debug(f"could not register hitbox! hitbox type {hitbox_type} is not a valid hitbox type!")
            return
        for i in range(MAX_HITBOXES):
            if self.hitboxes[hitbox_type][i] == None:
                self.hitboxes[hitbox_type][i] = new_hitbox
                return
        logging.debug(f"could not add hitbox! all available hitbox slots are full")
        return
    
    def collect_coin(self, coin):
        self.money += coin.value
    
    def collect_stone(self, stone):
        self.stones += stone.value

    def collect_item(self, item):
        if item.target == "money":
            value = int(item.value)
            if value >= 0:
                self.money += value
            else:
                # something here if you want different behavior if the value is negative
                ...
        elif item.target == "stones":
            value = int(item.value)
            if value >= 0:
                self.stones += value
            else:
                ...
            

        








        