import pickle
import socket
import threading
import time

import select
from threading import Thread

from common.Game import Game


class Server:
    server_socket = None
    ip = None
    port = None
    MSG_LENGTH = 4096
    MAX_CLIENTS_NUMBER = 2
    client_sockets: socket.SocketType.type = []
    client_ips = []
    client_ports = []
    clients_lock = threading.Lock()
    game: Game = None

    def __init__(self, server_ip, server_port, game):
        self.ip = server_ip
        self.port = server_port
        self.game = game
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def shutDown(self):
        for socket in self.client_sockets:
            if socket is not None:
                print("Disconnecting client " + socket)
                socket.close()
        if self.server_socket is not None:
            print("Shutting down server " + self.ip)
            self.server_socket.close()

    def run(self):
        try:
            self.server_socket.bind((self.ip, self.port))
            self.server_socket.listen(self.MAX_CLIENTS_NUMBER)
            print("Start listening...")
            self.runThread(self.listen, (), "Server Listener", False)
            return True
        except:
            return False

    def listen(self):
        while True:
            try:
                (client_socket, client_ip_port) = self.server_socket.accept()
                print(f"New client connected\nIP: {client_ip_port[0]}\nPORT: {client_ip_port[1]}")
                self.register_client(client_socket, client_ip_port)
                self.broadcast_game()
            except socket.error:
                break

    def runThread(self, methodSignature, args, name, daemon):
        newThread = Thread(target=methodSignature, args=args, name=name, daemon=daemon)
        newThread.start()

    def register_client(self, client_socket, client_ip_port):
        with self.clients_lock:
            self.client_sockets.append(client_socket)
            self.client_ips.append(client_ip_port[0])
            self.client_ports.append(client_ip_port[1])
        self.runThread(self.receive_controller, (client_socket, client_ip_port[0], client_ip_port[1]),
                       f"Server Receiver {client_ip_port[0]} + {client_ip_port[1]}", False)

    def broadcast_game(self):
        game_to_string = pickle.dumps(self.game.__copy__())
        if len(self.client_sockets) > 0:
            try:
                for socket in self.client_sockets:
                    socket.sendall(game_to_string)

            except socket.error:
                print("ERROR WITH SENDING GAME DATA TO CLIENTS")

    def receive_controller(self, client_socket, client_ip, client_port):
        while True:
            try:
                (ready_to_read, ready_to_write, connection_error) = select.select([client_socket], [], [])
                with self.clients_lock:
                    game_to_string = client_socket.recv(self.MSG_LENGTH)
                    if len(game_to_string) > 0:
                        self.game = pickle.loads(game_to_string)
                        self.broadcast_game()
                    else:
                        self.client_sockets.remove(client_socket)
                        self.client_ips.remove(client_ip)
                        self.client_ports.remove(client_port)
                        print(f"Client has DISCONNECTED\nIP: {client_ip}\nPORT: {client_port}")
                        break

            except select.error:
                client_socket.close()
                self.client_sockets.remove(client_socket)
                self.client_ips.remove(client_ip)
                self.client_ports.remove(client_port)
                print(f"Client has DISCONNECTED\nIP: {client_ip}\nPORT: {client_port}")
                break