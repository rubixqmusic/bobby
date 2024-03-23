import pygame
from res.framework.animatedsprite import AnimatedSprite

INCOMPLETE_ANIMATION = "incomplete"
COMPLETE_ANIMATION = "complete"

class LevelTile:
    def __init__(self, game, level_name, x, y, tile_size, spritesheet, animation, draw_target, camera) -> None:
        self.game = game
        self.camera = camera
        self.complete = False
        self.level_name = level_name
        self.x = x
        self.y = y
        self.rect = pygame.rect.Rect(x, y, tile_size, tile_size )
        self.animated_sprite = AnimatedSprite(game,draw_target)
        self.animated_sprite.load_spritesheet(game.load_resource(spritesheet))
        self.animated_sprite.load_sprite_data(game.load_resource(animation))
        self.animated_sprite.set_position(self.x, self.y)

        level_data = game.get_level_data(self.level_name)
        if level_data is not None:
            if level_data["money"] > level_data["quota"]:
                self.complete = True
                self.animated_sprite.set_animation(COMPLETE_ANIMATION)
            else:
                self.complete = False
                self.animated_sprite.set_animation(INCOMPLETE_ANIMATION)
        else:
            self.complete = True
            self.animated_sprite.set_animation(COMPLETE_ANIMATION)
        
        self.animated_sprite.play()
    
    def update(self):
        self.animated_sprite.update()
    
    def draw(self):
        # print(self.animated_sprite.position)
        # print(self.animated_sprite.draw_target)
        self.animated_sprite.set_position(self.x - self.camera.x, self.y - self.camera.y)
        self.animated_sprite.draw()