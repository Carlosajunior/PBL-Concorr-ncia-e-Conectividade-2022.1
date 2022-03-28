from http import server
import socket
from time import sleep

class Servidor:

    def __init__(self):
        #Define o tamanho máximo de bytes que podem ser recebidos
        self.payload = 2048
        #Configuração do socket para seguir o protocolo TCP/IP
        self.servidor_socket = socket.socket(socket.AF_INET,  socket.SOCK_STREAM)
        #Configuração para permitir que um endereço de IP e uma porta possam ser reutilizados no caso de um crash da aplicação
        self.servidor_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def iniciar_servidor(self, ip, porta):
        #Incializando o servidor
            print("Iniciando o servidor no IP ",ip," e na porta ",porta,".")
            endereco = (ip,porta)
            print("Servidor rodando no endereço ", endereco)
            self.servidor_socket.bind(endereco)
            #Servidor a passar a aguarda por conexões de clientes, num máximo de 5 clientes em uma fila de espera para se conectar
            self.servidor_socket.listen(5)

    def receber_mensagem(self):
        self.iniciar_servidor('192.168.43.56', 2004)
        i = 0
        while True:
            print("Aguardando conexão.")
            sleep(2)
            #Aceita a conexão de um cliente
            cliente, endereço = self.servidor_socket.accept()
            print("conexão efetuada com sucesso com o endereço ", endereço)
            #Recebe os dados enviados pelo cliente, até o limite do payload em bytes
            dados = cliente.recv(self.payload)
            if dados:
                #Caso haja dados, eles são printados no terminal
                print("Dados: %s" %dados)
                #Envia os dados recebidos de volta para o cliente
                cliente.send(dados)
                print("Enviado os dados recebidos de volta ao cliente com endereço ",endereço,".")
                #Fecha a conexão
                cliente.close()
                i +=1
            if i == 3:
                break

if __name__ == "__main__":
    servidor = Servidor()
    servidor.receber_mensagem()