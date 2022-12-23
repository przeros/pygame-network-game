import time
from datetime import datetime

import pygame

from client.Client import Client
from common.Configuration import Configuration
from common.Moves import Moves
from common.Player import Player


class GUI:
    client: Client = None
    window = None
    background_color = None
    # key: player_id value: image
    images = {}
    player_id = None

    def __init__(self, client, width, height, window_name, background_color):
        pygame.init()
        self.client = client
        self.background_color = background_color
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption(window_name)
        for key, image_path in Configuration.IMAGE_PATHS.items():
            self.images[key] = pygame.image.load(image_path)
        self.init_player()
        self.client.send_game()

    def init_player(self):
        self.player_id = datetime.now()
        self.client.game.add_player(
            Player(datetime.now(),
            Configuration.PLAYER_START_POS_X,
            Configuration.PLAYER_START_POS_Y,
            self.images[Configuration.PLAYER_IMAGE_KEY].get_width(),
            self.images[Configuration.PLAYER_IMAGE_KEY].get_height(),
            Configuration.PLAYER_IMAGE_KEY,
            Configuration.PLAYER_SPEED_DEFAULT)
        )

    def start(self):
        quit = False
        clock = pygame.time.Clock()
        move_up = False
        move_left = False
        move_down = False
        move_right = False
        while not quit:
            dt = clock.tick(60)
            move_up, move_left, move_down, move_right = self.handle_events(move_up, move_left, move_down, move_right)
            self.move_players(move_up, move_left, move_down, move_right, dt)
            self.drawGame()
            self.update()


    def drawGame(self):
        self.window.fill(self.background_color)
        for player in self.client.game.players:
            self.window.blit(self.images[player.image_type], (player.x - player.width * 0.5, player.y - player.height * 0.5))

    def update(self):
        pygame.display.flip()

    def quit(self):
        for player in self.client.game.players:
            if player.id == self.player_id:
                self.client.game.delete_player(player)
                self.client.send_game()
        pygame.quit()

    def move_players(self, move_up, move_left, move_down, move_right, dt):
        for player in self.client.game.players:
            if player.id == self.player_id:
                if move_down and player.get_bottom_y() < self.window.get_height():
                    player.move(Moves.DOWN, player.speed * dt)
                if move_up and player.get_top_y() > 0:
                    player.move(Moves.UP, player.speed * dt)
                if move_left and player.get_left_x() > 0:
                    player.move(Moves.LEFT, player.speed * dt)
                if move_right and player.get_right_x() < self.window.get_width():
                    player.move(Moves.RIGHT, player.speed * dt)
                self.client.send_game()

    def handle_events(self, move_up, move_left, move_down, move_right):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    move_right = False
                    move_left = True
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    move_left = False
                    move_right = True
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    move_down = False
                    move_up = True
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    move_up = False
                    move_down = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    move_left = False
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    move_right = False
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    move_up = False
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    move_down = False
        return move_up, move_left, move_down, move_right