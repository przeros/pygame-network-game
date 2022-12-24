import time
from datetime import datetime

from common.Configuration import Configuration
from common.Game import Game
from common.Object import Object
from server.Server import Server

if __name__ == '__main__':
    game = Game()
    server = Server(Configuration.SERVER_IP, Configuration.SERVER_PORT, game)
    server.run()
    while len(server.client_sockets) < 1:
        pass
    server.object_generator()
