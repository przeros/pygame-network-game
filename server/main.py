from common.Configuration import Configuration
from common.Game import Game
from server.Server import Server

if __name__ == '__main__':
    game = Game()
    server = Server(Configuration.SERVER_IP, Configuration.SERVER_PORT, game)
    server.run()

