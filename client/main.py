import time

from client.Client import Client
from client.GUI import GUI
from common.Configuration import Configuration

if __name__ == '__main__':
    client = Client()
    if client.connect(Configuration.SERVER_IP, Configuration.SERVER_PORT) is True:
        while client.game is None:
            pass
        gui = GUI(client.__copy__(), Configuration.WINDOW_WIDTH, Configuration.WINDOW_HEIGHT, Configuration.WINDOW_NAME, Configuration.BACKGROUND_COLOR)
        gui.start()
