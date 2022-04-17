import socket

class Administrador:
    def __init__(self):
        #Configuração do socket para atender ao protocolo TCP/IP
        self.administrador_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def administrador_conectar(self,ip, porta):
        #Tenta estabelecer uma conexão com o endereço de IP e a porta informados
        print("Se conectando ao ip "+ip+" na porta "+str(porta)+".")
        endereco = (ip, porta)
        self.administrador_socket.connect(endereco)

    def administrador_enviar(self,mensagem):
        try:             
            self.administrador_socket.send(bytes("alterar status/Teste",'utf-8'))
            response = self.administrador_socket.recv(2048)
        except socket.error as e: 
            print ("Socket error: ",str(e)) 
        except Exception as e: 
            print ("Ocorreu uma exceção:  ",str(e)) 
        finally: 
            print ("Fechando a conexão com o servidor")
            #Finaliza a conexão com o servidor
            self.administrador_socket.close()
            return response.decode('utf-8') 

    def alterar_status_lixeira(self,latitude, longitude, status):
        mensagem = 'alterar status'+'/'+latitude+'/'+longitude+'/'+status
        response = self.administrador_enviar(self, mensagem)
        if response == 'status alterado':
            print('status alterado com sucesso.')
        else:
            print('ocorreu um erro ao tentar alterar o status.')

    def alterar_percurso(self, latitude, longitude, posicao):
        mensagem = 'alterar trajeto'+'/'+latitude+'/'+longitude+'/'+posicao
        response = self.administrador_enviar(self, mensagem)
        if response == 'posição da lixeira alterada':
            print('posição da lixeira alterada com sucesso.')
        else:
            print(response)
if __name__ == "__main__":
    administrador = Administrador()
    administrador.administrador_enviar("Teste")
    