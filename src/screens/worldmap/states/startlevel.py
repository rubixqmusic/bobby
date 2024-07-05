import pygame
from src.state import State
from src.screens.worldmap.resources import *

class StartLevel(State):
    def on_state_enter(self, world_map):
        self.rectangle_height = 16
        self.rectangle_width = SCREEN_WIDTH + 128
        self.x_step_size = 10
        self.x_step = 0
        self.max_x = SCREEN_WIDTH 
        self.num_rectangles = int(SCREEN_HEIGHT/self.rectangle_height)
        
        self.go_bobby_text_surface = world_map.font.render(GO_BOBBY_TEXT, True, GOLD_COLOR)

        self.timer = 20

        self.status = "wait"
    
    def update(self, world_map):
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
            
    
    def draw(self, world_map):
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