import pygame
from settings import *
from src.components.animatedsprite import AnimatedSprite
from src.utilities.math import linear_conversion

PLAYER_MONEY = "player_money"

LABEL_FONT_1 = f"{FONTS_PATH}/{MENU_FONT_BOLD}"
STAT_FONT_1 = f"{FONTS_PATH}/{MENU_FONT_LIGHT}"
LABEL_FONT_SIZE = 12
LABEL_COLOR_1 = GOLD_COLOR
STAT_COLOR_1 = "#ffffff"
STAT_FONT_SIZE = 10
X_FONT_SIZE = 8
SLASH_FONT_SIZE = 9

LABELS_Y_POSITION = 8

# MONEY_LABEL= "Money"
# MONEY_LABEL_POSITION = [8,LABELS_Y_POSITION]
MONEY_SPRITESHEET = f"{GRAPHICS_PATH}/entities/copper_coin.png"
MONEY_ANIMATION = f"{ANIMATIONS_PATH}/coin.json"
MONEY_ICON_ANIMATION = "idle"
# MONEY_ICON_POSITION = [39, 8]
# MONEY_X_SIGN_POSITION = [38, 11]
MONEY_SLASH_SIGN_POSITION = [34, 11]
MONEY_STAT_POSITION = [12,9]
MONEY_STAT_RIGHT_X = [28, 16]

# QUOTA_LABEL= "Quota"
# QUOTA_LABEL_POSITION = [68,LABELS_Y_POSITION]
QUOTA_ICON_POSITION = [70, 8]
QUOTA_X_SIGN_POSITION = [69, 11]
QUOTA_STAT_RIGHT_X = [66, 16]

# STONES_LABEL = "Stones"
# STONES_LABEL_POSITION = [128, LABELS_Y_POSITION]
STONES_SPRITESHEET = f"{GRAPHICS_PATH}/entities/green_stone.png"
STONES_ANIMATION = f"{ANIMATIONS_PATH}/stone.json"
STONES_ICON_ANIMATION = "idle"
STONES_ICON_POSITION = [118, 8]
STONES_X_SIGN_POSITION = [117, 11]
STONES_STAT_RIGHT_X = [114, 16]

# HEALTH_LABEL = "Health"
# HEALTH_LABEL_POSITION = [192, LABELS_Y_POSITION]
HEALTH_BAR_SPRITESHEET = f"{GRAPHICS_PATH}/hud/health_bar.png"
HEALTH_BAR_ANIMATION = f"{ANIMATIONS_PATH}/health_bar.json"
HEALTH_BAR_POSITION = [162, 11]
MAX_HEALTH_ANIMATION_FRAMES = 12
HEALTH_ICON = f"{GRAPHICS_PATH}/hud/heart.png"
HEALTH_ICON_POSITION = [211, 8]

# TIME_LABEL = "Time"
# TIME_LABEL_POSITION = [460, LABELS_Y_POSITION]
TIME_STAT_RIGHT_SIDE = [489, 16]


class Hud:
    def __init__(self, gameplay) -> None:
        self.gameplay = gameplay
        self.draw_target = gameplay.camera.surface
        self.visible = True

        self.label_font_1 = pygame.font.Font(gameplay.game.load_resource(LABEL_FONT_1), LABEL_FONT_SIZE)
        self.stat_font_1 = pygame.font.Font(gameplay.game.load_resource(STAT_FONT_1), STAT_FONT_SIZE)
        self.x_font = pygame.font.Font(gameplay.game.load_resource(STAT_FONT_1), X_FONT_SIZE)
        self.slash_font = pygame.font.Font(gameplay.game.load_resource(STAT_FONT_1), SLASH_FONT_SIZE)

        # self.money_label_surface = self.label_font_1.render(MONEY_LABEL, True, LABEL_COLOR_1)
        # self.quota_label_surface = self.label_font_1.render(QUOTA_LABEL, True, LABEL_COLOR_1)
        # self.stones_label_surface = self.label_font_1.render(STONES_LABEL, True, LABEL_COLOR_1)
        # self.health_label_surface = self.label_font_1.render(HEALTH_LABEL, True, LABEL_COLOR_1)
        # self.time_label_surface = self.label_font_1.render(TIME_LABEL, True, LABEL_COLOR_1)
        self.x_surface = self.x_font.render("x", True, STAT_COLOR_1)
        self.slash_surface = self.slash_font.render("/", True, STAT_COLOR_1)


        self.money_icon = AnimatedSprite()
        self.money_icon.load_spritesheet(gameplay.game.load_resource(MONEY_SPRITESHEET))
        self.money_icon.load_animation(gameplay.game.load_resource(MONEY_ANIMATION))
        self.money_icon.set_draw_target(self.draw_target)
        self.money_icon.set_animation(MONEY_ICON_ANIMATION)
        self.money_icon.set_position(*QUOTA_ICON_POSITION)
        self.money_icon.play()

        self.stones_icon = AnimatedSprite()
        self.stones_icon.load_spritesheet(gameplay.game.load_resource(STONES_SPRITESHEET))
        self.stones_icon.load_animation(gameplay.game.load_resource(STONES_ANIMATION))
        self.stones_icon.set_draw_target(self.draw_target)
        self.stones_icon.set_animation(STONES_ICON_ANIMATION)
        self.stones_icon.set_position(*STONES_ICON_POSITION)
        self.stones_icon.play()

        self.health_bar = AnimatedSprite()
        self.health_bar.load_spritesheet(gameplay.game.load_resource(HEALTH_BAR_SPRITESHEET))
        self.health_bar.load_animation(gameplay.game.load_resource(HEALTH_BAR_ANIMATION))
        self.health_bar.set_draw_target(self.draw_target)
        animation_number = linear_conversion(self.gameplay.player_health, 0, MAX_PLAYER_HEALTH, 0, MAX_HEALTH_ANIMATION_FRAMES)

        self.health_bar.set_animation(str(int(animation_number)))
        self.health_bar.set_position(*HEALTH_BAR_POSITION)
        self.health_bar.play()

        self.health_icon = pygame.image.load(gameplay.game.load_resource(HEALTH_ICON)).convert_alpha()
    
    def update(self, delta):
        self.money_icon.update(delta)
        self.stones_icon.update(delta)
        self.health_bar.update(delta)

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

        # self.draw_target.blit(self.money_label_surface, MONEY_LABEL_POSITION)
        # self.draw_target.blit(self.quota_label_surface, QUOTA_LABEL_POSITION)
        # self.draw_target.blit(self.stones_label_surface, STONES_LABEL_POSITION)
        # self.draw_target.blit(self.health_label_surface, HEALTH_LABEL_POSITION)
        # self.draw_target.blit(self.time_label_surface, TIME_LABEL_POSITION)

        self.draw_target.blit(self.slash_surface, MONEY_SLASH_SIGN_POSITION)
        self.draw_target.blit(self.x_surface, QUOTA_X_SIGN_POSITION)
        self.draw_target.blit(self.x_surface, STONES_X_SIGN_POSITION)

        # self.money_icon.set_position(*MONEY_ICON_POSITION)
        # self.money_icon.draw()
        self.money_icon.set_position(*QUOTA_ICON_POSITION)
        self.money_icon.draw()
        self.stones_icon.set_position(*STONES_ICON_POSITION)
        self.stones_icon.draw()
        self.health_bar.set_position(*HEALTH_BAR_POSITION)
        self.health_bar.draw()
        self.draw_target.blit(self.health_icon, HEALTH_ICON_POSITION)
    
    def set_draw_target(self, draw_target):
        self.draw_target = draw_target