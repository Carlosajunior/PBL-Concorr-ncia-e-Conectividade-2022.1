import json
import socket

class Caminhao:

    def __init__(self):
        self.lista_lixeiras = list
        self.cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    
    def caminhao_conectar(self,ip, porta):
        #Tenta estabelecer uma conexão com o endereço de IP e a porta informados
        print("Se conectando ao ip ", ip," na porta ",porta,".")
        endereco = (ip, porta)
        self.cliente_socket.connect(endereco)

    def caminhao_enviar(self,ip, porta, mensagem):
        try: 
            #Tenta enviar uma mensagem
            self.caminhao_conectar(ip, porta)
            self.cliente_socket.send(bytes(mensagem,'utf-8'))
            dados = self.cliente_socket.recv(16)
            response_json = json.loads(dados.decode('utf-8'))
        except socket.error as e: 
            print ("Socket error: ",str(e)) 
        except Exception as e: 
            print ("Ocorreu uma exceção:  ",str(e)) 
        finally: 
            print ("Fechando a conexão com o servidor")
            #Finaliza a conexão com o servidor
            self.cliente_socket.close()
            return response_json 

    def definir_percurso_lixeiras(self,ip,porta):
        response = self.caminhao_enviar(ip, porta,"percurso das lixeiras/")
        self.lista_lixeiras = response.get("lista_lixeiras")

    def percurso_das_lixeiras(self):
        return self.lista_lixeiras

    def esvaziar_lixeira(self,ip,porta):
        response = self.caminhao_enviar(ip, porta,"esvaziar lixeira/")
        if response.get("lixeira_response") == 'ok':
            self.lista_lixeiras.pop()
            print("lixeira esvaziada.")
        print("Ocorreu um erro ao tentar esvaziar a lixeira.")


if __name__ == "__main__":
    caminhao = Caminhao()
    caminhao.caminhao_conectar("192.168.43.143", 7777)
    