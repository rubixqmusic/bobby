import pygame
from settings import *
from src.components.animatedsprite import AnimatedSprite

PLAYER_MONEY = "player_money"

LABEL_FONT_1 = f"{FONTS_PATH}/{MENU_FONT_BOLD}"
STAT_FONT_1 = f"{FONTS_PATH}/{MENU_FONT_LIGHT}"
LABEL_FONT_SIZE = 12
LABEL_COLOR_1 = GOLD_COLOR
STAT_COLOR_1 = "#ffffff"
STAT_FONT_SIZE = 10
X_FONT_SIZE = 8

LABELS_Y_POSITION = 8

MONEY_LABEL= "Money"
MONEY_LABEL_POSITION = [8,LABELS_Y_POSITION]
MONEY_SPRITESHEET = f"{GRAPHICS_PATH}/entities/copper_coin.png"
MONEY_ANIMATION = f"{ANIMATIONS_PATH}/coin.json"
MONEY_ICON_ANIMATION = "idle"
MONEY_ICON_POSITION = [39, 18]
MONEY_X_SIGN_POSITION = [38, 21]
MONEY_STAT_POSITION = [8,19]
MONEY_STAT_RIGHT_X = [36, 26]

QUOTA_LABEL= "Quota"
QUOTA_LABEL_POSITION = [68,LABELS_Y_POSITION]
QUOTA_ICON_POSITION = [96, 18]
QUOTA_X_SIGN_POSITION = [95, 21]
QUOTA_STAT_RIGHT_X = [92, 26]

STONES_LABEL = "Stones"
STONES_LABEL_POSITION = [128, LABELS_Y_POSITION]
STONES_SPRITESHEET = f"{GRAPHICS_PATH}/entities/green_stone.png"
STONES_ANIMATION = f"{ANIMATIONS_PATH}/stone.json"
STONES_ICON_ANIMATION = "idle"
STONES_ICON_POSITION = [160, 18]
STONES_X_SIGN_POSITION = [159, 21]
STONES_STAT_RIGHT_X = [156, 26]

HEALTH_LABEL = "Health"
HEALTH_LABEL_POSITION = [192, LABELS_Y_POSITION]

TIME_LABEL = "Time"
TIME_LABEL_POSITION = [460, LABELS_Y_POSITION]
TIME_STAT_RIGHT_SIDE = [489, 26]


class Hud:
    def __init__(self, gameplay) -> None:
        self.gameplay = gameplay
        self.draw_target = gameplay.camera.surface
        self.visible = True

        self.label_font_1 = pygame.font.Font(gameplay.game.load_resource(LABEL_FONT_1), LABEL_FONT_SIZE)
        self.stat_font_1 = pygame.font.Font(gameplay.game.load_resource(STAT_FONT_1), STAT_FONT_SIZE)
        self.x_font = pygame.font.Font(gameplay.game.load_resource(STAT_FONT_1), X_FONT_SIZE)

        self.money_label_surface = self.label_font_1.render(MONEY_LABEL, True, LABEL_COLOR_1)
        self.quota_label_surface = self.label_font_1.render(QUOTA_LABEL, True, LABEL_COLOR_1)
        self.stones_label_surface = self.label_font_1.render(STONES_LABEL, True, LABEL_COLOR_1)
        self.health_label_surface = self.label_font_1.render(HEALTH_LABEL, True, LABEL_COLOR_1)
        self.time_label_surface = self.label_font_1.render(TIME_LABEL, True, LABEL_COLOR_1)
        self.x_surface = self.x_font.render("x", True, STAT_COLOR_1)

        self.money_icon = AnimatedSprite()
        self.money_icon.load_spritesheet(gameplay.game.load_resource(MONEY_SPRITESHEET))
        self.money_icon.load_animation(gameplay.game.load_resource(MONEY_ANIMATION))
        self.money_icon.set_draw_target(self.draw_target)
        self.money_icon.set_animation(MONEY_ICON_ANIMATION)
        self.money_icon.set_position(*MONEY_ICON_POSITION)
        self.money_icon.play()

        self.stones_icon = AnimatedSprite()
        self.stones_icon.load_spritesheet(gameplay.game.load_resource(STONES_SPRITESHEET))
        self.stones_icon.load_animation(gameplay.game.load_resource(STONES_ANIMATION))
        self.stones_icon.set_draw_target(self.draw_target)
        self.stones_icon.set_animation(STONES_ICON_ANIMATION)
        self.stones_icon.set_position(*STONES_ICON_POSITION)
        self.stones_icon.play()
    
    def update(self, delta):
        self.money_icon.update(delta)
        self.stones_icon.update(delta)

    def draw(self):
        if not self.visible:
            return
        if not self.draw_target:
            return
        
        money = str(self.gameplay.money)
        money_surface = self.stat_font_1.render(money, True, STAT_COLOR_1)
        money_rect = money_surface.get_rect(midright=MONEY_STAT_RIGHT_X)

        quota = str(self.gameplay.quota)
        quota_surface = self.stat_font_1.render(quota, True, STAT_COLOR_1)
        quota_rect = quota_surface.get_rect(midright=QUOTA_STAT_RIGHT_X)

        time = str(self.gameplay.time_limit)
        time_surface = self.stat_font_1.render(time, True, STAT_COLOR_1)
        time_rect = time_surface.get_rect(midright=TIME_STAT_RIGHT_SIDE)

        stones = str(self.gameplay.stones)
        stones_surface = self.stat_font_1.render(stones, True, STAT_COLOR_1)
        stones_rect = stones_surface.get_rect(midright=STONES_STAT_RIGHT_X)

        self.draw_target.blit(money_surface, money_rect)
        self.draw_target.blit(quota_surface, quota_rect)
        self.draw_target.blit(time_surface, time_rect)
        self.draw_target.blit(stones_surface, stones_rect)

        self.draw_target.blit(self.money_label_surface, MONEY_LABEL_POSITION)
        self.draw_target.blit(self.quota_label_surface, QUOTA_LABEL_POSITION)
        self.draw_target.blit(self.stones_label_surface, STONES_LABEL_POSITION)
        self.draw_target.blit(self.health_label_surface, HEALTH_LABEL_POSITION)
        self.draw_target.blit(self.time_label_surface, TIME_LABEL_POSITION)

        self.draw_target.blit(self.x_surface, MONEY_X_SIGN_POSITION)
        self.draw_target.blit(self.x_surface, QUOTA_X_SIGN_POSITION)
        self.draw_target.blit(self.x_surface, STONES_X_SIGN_POSITION)

        self.money_icon.set_position(*MONEY_ICON_POSITION)
        self.money_icon.draw()
        self.money_icon.set_position(*QUOTA_ICON_POSITION)
        self.money_icon.draw()
        self.stones_icon.set_position(*STONES_ICON_POSITION)
        self.stones_icon.draw()
    
    def set_draw_target(self, draw_target):
        self.draw_target = draw_target