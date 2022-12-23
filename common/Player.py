import pygame

from common.Object import Object


class Player(Object):
    speed = None

    def __init__(self, id, x, y, width, height, image_type, speed):
        super().__init__(id, x, y, width, height, image_type)
        self.speed = speed
