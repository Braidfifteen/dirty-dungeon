import sys
import random
import pygame as pg

# Importing prepare initializes the display.
import prepare
from player import Player
from room import Room
from room_info import ROOM_INFO


class App(object):
    """This is the main class that runs the program."""
    def __init__(self):
        self.screen = pg.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        self.clock  = pg.time.Clock()
        self.fps = 60
        self.done = False

        self.player = Player(self.screen_rect.center, (32, 32))
        self.make_rooms()
        self.room = self.rooms[0]

        self.all_sprites = pg.sprite.LayeredDirty()
        self.bg = pg.Surface(self.screen.get_size()).convert()
        self.bg.fill(prepare.BACKGROUND_COLOR)
        self.all_sprites.clear(prepare.SCREEN, self.bg)
        self.all_sprites.add(self.room.walls, self.room.doors, self.player)

    def make_rooms(self):
        room_size = prepare.SCREEN_SIZE
        wall_size = (64, 64)
        self.rooms = {}
        for room_num in ROOM_INFO:
            topleft, exits = ROOM_INFO[room_num]
            self.rooms[room_num] = Room(room_num, topleft, exits, room_size, wall_size)

    def change_room(self, door):
        """Change current room and move player accordingly."""
        room = self.rooms[door.exit_to]
        pw, ph = self.player.rect.size
        #where the player should come out of the door in the next room
        arrival_spots = {
            "left": (room.rect.right - (door.rect.w + pw), self.player.rect.top),
            "right": (room.rect.left + door.rect.w, self.player.rect.top),
            "top": (self.player.rect.left, room.rect.bottom - (door.rect.h + ph)),
            "bottom": (self.player.rect.left, room.rect.top + door.rect.h)}
        self.player.rect.topleft = arrival_spots[door.direction]
        self.room = room

        self.all_sprites.empty()
        #adding the sprites to the group automatically sets their dirty flags to 1 
        self.all_sprites.add(self.room.walls, self.room.doors, self.player)

    def event_loop(self):
        """
        Process all events.
        Send event to player so that they can also handle the event.
        """
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
            elif event.type == pg.KEYUP:
                if event.key == pg.K_ESCAPE:
                    self.done = True
            self.player.get_event(event)

    def display_fps(self):
        """Show the program's FPS in the window handle."""
        template = "{} - FPS: {:.2f}"
        caption = template.format(prepare.CAPTION, self.clock.get_fps())
        pg.display.set_caption(caption)

    def update(self):
        now = pg.time.get_ticks()
        self.player.update(self.room)
        for door in self.room.doors:
            if self.player.rect.colliderect(door.rect):
                self.change_room(door)
                break

    def render(self):
        dirty_rects = self.all_sprites.draw(self.screen)
        pg.display.update(dirty_rects)

    def run(self):
        while not self.done:
            self.event_loop()
            self.update()
            self.render()
            self.clock.tick(self.fps)
            self.display_fps()

def main():
    """Create an App and start the program."""
    app = App()
    app.run()
    pg.quit()
    sys.exit()


if __name__ == "__main__":
    main()
