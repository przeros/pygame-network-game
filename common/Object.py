import pygame

from common.Moves import Moves


class Object:
    id = None
    background_color = (255, 255, 255)
    x = None
    y = None
    width = None
    height = None
    image_type = None

    def __init__(self, id, x, y, width, height, image_type):
        self.id = id
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image_type = image_type

    def get_top_y(self):
        return self.y - self.height * 0.5

    def get_bottom_y(self):
        return self.y + self.height * 0.5

    def get_right_x(self):
        return self.x + self.width * 0.5

    def get_left_x(self):
        return self.x - self.width * 0.5

    def move(self, direction, distance):
        match direction:
            case Moves.UP:
                self.y -= distance
            case Moves.LEFT:
                self.x -= distance
            case Moves.DOWN:
                self.y += distance
            case Moves.RIGHT:
                self.x += distance

    def collide(self, object):
        if self.get_top_y() < object.get_bottom_y() and self.get_bottom_y() > object.get_top_y()\
                and self.get_right_x() > object.get_left_x() and self.get_left_x() < object.get_right_x():
            return True
        else:
            return False
