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
            self.cliente_socket.send(bytes("alterar status/Teste",'utf-8'))
            response = self.cliente_socket.recv(2048)
        except socket.error as e: 
            print ("Socket error: ",str(e)) 
        except Exception as e: 
            print ("Ocorreu uma exceção:  ",str(e)) 
        finally: 
            print ("Fechando a conexão com o servidor")
            #Finaliza a conexão com o servidor
            self.cliente_socket.close()
            return response.decode('utf-8') 

    def alterar_status_lixeira(self,latitude, longitude, status):
        mensagem = 'alterar status'+'/'+latitude+'/'+longitude+'/'+status
        response = self.cliente_enviar(self, mensagem)
        if response == 'status alterado':
            print('status alterado com sucesso.')
        else:
            print('ocorreu um erro ao tentar alterar o status.')

    def alterar_percurso(self):
if __name__ == "__main__":
    cliente = Cliente()
    cliente.cliente_enviar("Teste")
    