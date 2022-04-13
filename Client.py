import socket

class Cliente:
    def __init__(self):
        #Configuração do socket para atender ao protocolo TCP/IP
        self.cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    
    def cliente_conectar(self,ip, porta):
        #Tenta estabelecer uma conexão com o endereço de IP e a porta informados
        print("Se conectando ao ip "+ip+" na porta "+str(porta)+".")
        endereco = (ip, porta)
        self.cliente_socket.connect(endereco)

    def cliente_enviar(self,mensagem):
        try: 
            #Tenta enviar uma mensagem
            self.cliente_conectar("192.168.25.5", 2004)
            while True:
                self.cliente_socket.send(bytes("alterar status/Teste",'utf-8'))
        except socket.error as e: 
            print ("Socket error: ",str(e)) 
        except Exception as e: 
            print ("Ocorreu uma exceção:  ",str(e)) 
        finally: 
            print ("Fechando a conexão com o servidor")
            #Finaliza a conexão com o servidor
            self.cliente_socket.close() 

    def alterar_status_lixeira(self,latitude, longitude, status):
        mensagem = 'alterar status'+'/'+latitude+'/'+longitude+'/'+status
        self.cliente_enviar(self, mensagem)

if __name__ == "__main__":
    cliente = Cliente()
    cliente.cliente_enviar("Teste")
    