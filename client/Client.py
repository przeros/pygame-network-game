import pickle
import socket
from threading import Thread

from common.Game import Game
from common.Player import Player


class Client:
    MSG_LENGTH = 4096
    client_socket = None
    ip = None
    port = None
    server_ip = None
    server_port = None
    game: Game = None

    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __copy__(self):
        copy = self
        copy.game = self.game
        return copy

    def shutDown(self):
        if self.client_socket is not None:
            self.client_socket.close()
            print(f"Shutting down client\nIP: {self.ip}\nPORT: {self.port}")

    def connect(self, server_ip, server_port):
        try:
            self.client_socket.connect((server_ip, server_port))
            self.server_ip = server_ip
            self.server_port = server_port
            self.ip = self.client_socket.getsockname()[0]
            self.port = self.client_socket.getsockname()[1]
            self.runThread(self.receive_game, (), f"GAME DATA RECEIVER", True)
            print("Establieshed connection with server: " + server_ip)
            return True
        except socket.error:
            print("Couldn't connect to server: " + server_ip)
            return False

    def runThread(self, methodSignature, args, name, daemon):
        newThread = Thread(target=methodSignature, args=args, name=name, daemon=daemon)
        newThread.start()

    def receive_game(self):
        while True:
            try:
                game_to_string = self.client_socket.recv(self.MSG_LENGTH)
                if len(game_to_string) > 0:
                    self.game = pickle.loads(game_to_string)
                else:
                    print(f"ERROR IN RECEIVING GAME DATA\nIP: {self.ip}\nPORT: {self.port}")
                    break

            except socket.error:
                print(f"ERROR IN CONNECTION WITH SERVER\nIP: {self.server_ip}\nPORT: {self.server_port}")
                break

    def send_game(self):
        game_to_string = pickle.dumps(self.game.__copy__())
        try:
            self.client_socket.send(game_to_string)
        except socket.error:
            print("ERROR WITH SENDING GAME DATA TO SERVER")

    '''def sendMessage(self, message):
        # print(message)
        try:
            self.clientSocket.send(self.encryptMessage(message.encode()))
            self.clientSocket.settimeout(1.0)
            ackMessage = self.clientSocket.recv(MSG_LENGTH).decode()
            if ackMessage is not None:
                self.logger.log(ackMessage)
        except socket.error:
            if self.serverIp is not None:
                self.logger.log("Server " + self.serverIp + " has been disconnected!")
            else:
                self.logger.log("You are not allowed to send a message. Connect to the server!")

    def detectMessage(self, message):
        if message is not None:
            self.sendMessage(message)'''