import pygame
from settings import *
from src.components.animatedsprite import AnimatedSprite

PLAYER_MONEY = "player_money"

LABEL_FONT_1 = f"{FONTS_PATH}/{MENU_FONT_REGULAR}"
STAT_FONT_1 = f"{FONTS_PATH}/{MENU_FONT_LIGHT}"
LABEL_FONT_SIZE = 8
LABEL_COLOR_1 = "#ffffff"
STAT_FONT_SIZE = 10

LABELS_Y_POSITION = 8

MONEY_LABEL= "MONEY"
MONEY_LABEL_POSITION = [8,LABELS_Y_POSITION]
MONEY_SPRITESHEET = f"{GRAPHICS_PATH}/entities/copper_coin.png"
MONEY_ANIMATION = f"{ANIMATIONS_PATH}/coin.json"
MONEY_ICON_ANIMATION = "idle"
MONEY_ICON_POSITION = [28, 16]
MONEY_X_SIGN_POSITION = [27, 17]
MONEY_STAT_POSITION = [8,17]

QUOTA_LABEL= "QUOTA"
QUOTA_LABEL_POSITION = [62,LABELS_Y_POSITION]
QUOTA_ICON_POSITION = [83, 16]
QUOTA_X_SIGN_POSITION = [82, 19]

HEALTH_LABEL = "HEALTH"
HEALTH_LABEL_POSITION = [116, LABELS_Y_POSITION]


class Hud:
    def __init__(self, gameplay) -> None:
        self.gameplay = gameplay
        self.draw_target = gameplay.camera.surface
        self.visible = True

        self.label_font_1 = pygame.font.Font(gameplay.game.load_resource(LABEL_FONT_1), LABEL_FONT_SIZE)
        self.stat_font_1 = pygame.font.Font(gameplay.game.load_resource(STAT_FONT_1), STAT_FONT_SIZE)

        self.money_label_surface = self.label_font_1.render(MONEY_LABEL, True, LABEL_COLOR_1)
        self.quota_label_surface = self.label_font_1.render(QUOTA_LABEL, True, LABEL_COLOR_1)
        self.health_label_surface = self.label_font_1.render(HEALTH_LABEL, True, LABEL_COLOR_1)
        self.x_surface = self.stat_font_1.render("x", True, LABEL_COLOR_1)

        self.money_icon = AnimatedSprite()
        self.money_icon.load_spritesheet(gameplay.game.load_resource(MONEY_SPRITESHEET))
        self.money_icon.load_animation(gameplay.game.load_resource(MONEY_ANIMATION))
        self.money_icon.set_draw_target(self.draw_target)
        self.money_icon.set_animation(MONEY_ICON_ANIMATION)
        self.money_icon.set_position(*MONEY_ICON_POSITION)
        self.money_icon.play()
    
    def update(self, delta):
        self.money_icon.update(delta)

    def draw(self):
        if not self.visible:
            return
        if not self.draw_target:
            return
        
        money = str(self.gameplay.game.get_save_data(PLAYER_MONEY))
        money_surface = self.stat_font_1.render(money, True, LABEL_COLOR_1)

        self.draw_target.blit(money_surface, MONEY_STAT_POSITION)
        self.draw_target.blit(self.money_label_surface, MONEY_LABEL_POSITION)
        self.draw_target.blit(self.quota_label_surface, QUOTA_LABEL_POSITION)
        self.draw_target.blit(self.health_label_surface, HEALTH_LABEL_POSITION)

        self.draw_target.blit(self.x_surface, MONEY_X_SIGN_POSITION)
        self.draw_target.blit(self.x_surface, QUOTA_X_SIGN_POSITION)

        self.money_icon.set_position(*MONEY_ICON_POSITION)
        self.money_icon.draw()
        self.money_icon.set_position(*QUOTA_ICON_POSITION)
        self.money_icon.draw()
    
    def set_draw_target(self, draw_target):
        self.draw_target = draw_target