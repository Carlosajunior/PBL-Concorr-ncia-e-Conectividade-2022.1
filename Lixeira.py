import imp


import socket

class Lixeira:

    def __init__(self):
        self.capacidade_lixeira = 0
        self.latitude_lixeira = 0
        self.longitude_lixeira = 0
        self.carga_lixeira = 0
        self.status_lixeira = "aberta"
        self.cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    def lixeira_conectar(self,ip, porta):
        #Tenta estabelecer uma conexão com o endereço de IP e a porta informados
        print("Se conectando ao ip ", ip," na porta ",porta,".")
        endereco = (ip, porta)
        self.cliente_socket.connect(endereco)

    def definir_capacidade(self, capacidade_lixeira):
        self.capacidade_lixeira = capacidade_lixeira

    def capacidade_lixeira(self):
        return self.capacidade_lixeira

    def longitude_lixeira(self):
        return self.longitude_lixeira

    def latitude_lixeira(self):
        return self.latitude_lixeira

    def definir_carga(self, carga_lixeira):
        self.carga_lixeira = carga_lixeira

    def carga_lixeira(self):
        return self.carga_lixeira

    def definir_status_lixeira(self, status_lixeira):
        self.status_lixeira = status_lixeira

    def status_da_lixeira(self):
        return self.status_lixeira

if __name__ == "__main__":
    lixeira = Lixeira()
    lixeira.lixeira_conectar("192.168.43.143", 7777)