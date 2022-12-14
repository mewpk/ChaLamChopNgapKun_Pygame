import pygame
import os
from states.state import State
from states.pause_menu import PauseMenu


class Game_World(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.game = game
        self.load_assets()
        self.player = Player(self.game)
        self.enemy = Enemy(self.game)
    def update(self, delta_time, actions):
        # Check if the game was paused
        if actions["start"]:
            new_state = PauseMenu(self.game)
            new_state.enter_ssate()
        self.player.update(delta_time, actions)

    def render(self, display):
        display.blit(
            self.bg_img, (-self.player.position_x, -self.player.position_y))
        self.enemy.render(display)
        self.player.render(display)
    def load_assets(self):
        self.bg_img = pygame.image.load(os.path.join(
            self.game.assets_dir, "map", "Map.png")).convert_alpha()

class Player():
    def __init__(self, game):
        self.game = game
        self.load_sprites()
        self.position_x, self.position_y = 240, 140
        self.hp, self.mana = "500", "200"
        self.current_frame, self.last_frame_update = 0, 0

    def update(self, delta_time, actions):
        # Get the direction from inputs
        direction_x = actions["right"] - actions["left"]
        direction_y = actions["down"] - actions["up"]
        # Update the position
        self.position_x += 50 * delta_time * direction_x
        self.position_y += 50 * delta_time * direction_y

        # Animate the sprite
        self.animate(delta_time, direction_x, direction_y)

    def render(self, display):
        self.game.draw_text(display, "HP :" + self.hp,
                            (241, 66, 99), 50, 25, 8)
        self.game.draw_text(display, "Mana :" + self.mana,
                            (85, 138, 180), 50, 40, 8)
        display.blit(self.curr_image, (240, 140))

    def animate(self, delta_time, direction_x, direction_y):
        # Compute how much time has passed since the frame last updated
        self.last_frame_update += delta_time
        # If no direction is pressed, set image to idle and return
        if not (direction_x or direction_y):
            self.curr_image = self.curr_anim_list[0]
            return
        # If an image was pressed, use the appropriate list of frames according to direction
        if direction_x:
            if direction_x > 0:
                self.curr_anim_list = self.right_sprites
            else:
                self.curr_anim_list = self.left_sprites
        if direction_y:
            if direction_y > 0:
                self.curr_anim_list = self.front_sprites
            else:
                self.curr_anim_list = self.back_sprites
        # Advance the animation if enough time has elapsed
        if self.last_frame_update > .15:
            self.last_frame_update = 0
            self.current_frame = (self.current_frame +
                                  1) % len(self.curr_anim_list)
            self.curr_image = self.curr_anim_list[self.current_frame]

    def load_sprites(self):
        # Get the diretory with the player sprites
        self.sprite_dir = os.path.join(self.game.sprite_dir, "player")
        self.front_sprites, self.back_sprites, self.right_sprites, self.left_sprites = [], [], [], []
        # Load in the frames for each direction
        for i in range(1, 5):
            self.front_sprites.append(pygame.image.load(os.path.join(
                self.sprite_dir, "player_front" + str(i) + ".png")))
            self.back_sprites.append(pygame.image.load(os.path.join(
                self.sprite_dir, "player_back" + str(i) + ".png")))
            self.right_sprites.append(pygame.image.load(os.path.join(
                self.sprite_dir, "player_right" + str(i) + ".png")))
            self.left_sprites.append(pygame.image.load(os.path.join(
                self.sprite_dir, "player_left" + str(i) + ".png")))
        # Set the default frames to facing front
        self.curr_image = self.front_sprites[0]
        self.curr_anim_list = self.front_sprites




class Enemy():
    def __init__(self, game):
        self.game = game
        self.load_enemy()  
        self.player = Player(self.game)

    def render(self, display):
        display.blit(self.enemy_image, (0 ,0))

    def load_enemy(self):
        self.enemy_dir = os.path.join(self.game.assets_dir, "enemys")
        self.enemy_image = pygame.image.load(os.path.join(
            self.enemy_dir, "Faceset" + ".png")).convert_alpha()


class Gun():
    def __init__(self, game):
        self.game = game
        self.load_gun()

    def load_gun(self):
        self.gun_dir = os.path.join(self.game.assets_dir, "guns")
