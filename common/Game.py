from common.Object import Object
from common.Player import Player


class Game:
    objects: Object.__class__ = []
    players: Player.__class__ = []

    def __init__(self):
        pass

    def __copy__(self):
        copy = self
        copy.objects = self.objects
        copy.players = self.players
        return copy

    def add_object(self, object):
        self.objects.append(object)

    def delete_object(self, object):
        self.objects.remove(object)

    def add_player(self, player):
        self.players.append(player)

    def delete_player(self, player):
        self.players.remove(player)
