from calendar import c
import socket

class Cliente:
    def __init__(self):
        #Configuração do socket para atender ao protocolo TCP/IP
        self.cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    
    def cliente_conectar(self,ip, porta):
        #Tenta estabelecer uma conexão com o endereço de IP e a porta informados
        print("Se conectando ao ip ", ip," na porta ",porta,".")
        endereco = (ip, porta)
        self.cliente_socket.connect(endereco)

def cliente_enviar(self,mensagem):
    try: 
        #Tenta enviar uma mensagem

        self.cliente_socket.sendall(mensagem.encode('utf-8')) 
        # Look for the response 
        quantidade_recebida = 0 
        quantidade_enviada = len(mensagem)
        #Verifica se a quantidade de bytes recebidas é correspondente ao tamanho da mensagem enviada 
        while quantidade_recebida < quantidade_enviada: 
            dados = self.cliente_socket.recv(16) 
            quantidade_recebida += len(dados) 
            print ("Recebido: ",dados) 
    except socket.error as e: 
        print ("Socket error: ",str(e)) 
    except Exception as e: 
        print ("Ocorreu uma exceção:  ",str(e)) 
    finally: 
        print ("Fechando a conexão com o servidor")
        #Finaliza a conexão com o servidor
        self.cliente_socket.close() 

if __name__ == "__main__":
    cliente = Cliente()
    cliente.cliente_conectar("192.168.43.143", 7777)