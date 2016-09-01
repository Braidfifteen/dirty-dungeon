import pygame as pg
import prepare

class Player(pg.sprite.DirtySprite):
    """Class that creates the sprite the user will control."""
    def __init__(self, centerpoint, size, *groups):
        super(Player, self).__init__(*groups)
        self.image = pg.Surface(size)
        self.image.fill(pg.Color("green"))
        self.rect = self.image.get_rect(center=centerpoint)
        self.velocity = [0, 0]
        self.speed = 3

    def get_event(self, event):
        """Handles all events that pertains to playable character."""
        if event.type == pg.KEYDOWN:
            if event.key in prepare.CONTROLS:
                direction = prepare.CONTROLS[event.key]
                self.velocity = prepare.DIRECT_DICT[direction]
        elif event.type == pg.KEYUP:
            self.velocity = [0, 0]

    def update(self, room):
        """Update image and position of sprite."""
        old_pos = self.rect.topleft
        move = self.velocity[0] * self.speed, self.velocity[1] * self.speed
        self.rect.move_ip(move)
        self.wall_hit_logic(move, room.walls)
        if self.rect.topleft != old_pos:
            self.dirty = 1

    def wall_hit_logic(self, move, walls):
        wall_hit_list = pg.sprite.spritecollide(self, walls, False)
        for wall in wall_hit_list:
            if move[0] > 0:
                self.rect.right = wall.rect.left
            elif move[0] < 0:
                self.rect.left = wall.rect.right
            elif move[1] > 0:
                self.rect.bottom = wall.rect.top
            elif move[1] < 0:
                self.rect.top = wall.rect.bottom
            break