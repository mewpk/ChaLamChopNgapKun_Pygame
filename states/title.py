import os,pygame
from states.state import State
from states.game_world import Game_World

class Title(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.game = game
        self.load_logo()
        

    def update(self, delta_time, actions):
        if actions["start"]:
            new_state = Game_World(self.game)
            new_state.enter_state()
        self.game.reset_keys()
    def load_logo(self):
        self.logo_dir = os.path.join(self.game.assets_dir, "logo")
        self.logo_image = pygame.image.load(os.path.join(self.logo_dir, "Shark.png"))
    def render(self, display):
        display.fill((255,255,255))
        self.game.draw_text(display, "Cha Lam Chop Ngap Kun", (0,0,0), self.game.GAME_W/2, self.game.GAME_H/2,20 )
        self.game.draw_text(display, "65010731 Patsakorn Thong-un", (0,0,0), self.game.GAME_W/2, self.game.GAME_H/2 + 50,10 )
        display.blit(self.logo_image, (self.game.GAME_W/2-80 ,self.game.GAME_H/2 -50))

    