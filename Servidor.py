import socket

class Servidor:

    def __init__(self):
        self.servidor_socket = socket.socket(socket.AF_INET,  socket.SOCK_STREAM)

    def iniciar_servidor(self, ip, porta):
            self.servidor_socket.setsockopt

