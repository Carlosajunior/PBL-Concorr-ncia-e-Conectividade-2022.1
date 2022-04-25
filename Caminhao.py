import json
import socket

class Caminhao:

    def __init__(self):
        self.lista_lixeiras = []
        self.cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    
    def caminhao_conectar(self,ip, porta):
        #Tenta estabelecer uma conexão com o endereço de IP e a porta informados
        print("Se conectando ao ip ", ip," na porta ",porta,".")
        endereco = (ip, porta)
        self.cliente_socket.connect(endereco)

    def enviar_mensagem(self, mensagem):
        try: 
            #Tenta enviar uma mensagem
            self.cliente_socket.send(bytes(mensagem,'utf-8'))
        except socket.error as e: 
            print ("Socket error: ",str(e)) 
        except Exception as e: 
            print ("Ocorreu uma exceção:  ",str(e)) 

    def receber_mensagem(self):
        dados = self.cliente_socket.recv(self.payload)
        if dados:
                mensagem = dados.decode('utf-8')   
                if mensagem.split('/')[0] == "alterar trajeto":
                    self.alterar_trajeto_caminhao(mensagem) 

    def alterar_trajeto_caminhao(self, mensagem):
        old_index = mensagem.split('/')[1]
        new_index = mensagem.split('/')[2]
        if old_index > len(self.lista_lixeiras) or old_index < len(self.lista_lixeiras):
            self.enviar_mensagem('index da posição atual da lixeira na lista inválido.')
        elif new_index > len(self.lista_lixeiras) or new_index < len(self.lista_lixeiras):
            self.enviar_mensagem('index da posição nova da lixeira na lista inválido.')
        elif new_index == len(self.lista_lixeiras):
            self.enviar_mensagem('index é referente a posição atual da lixeira.')
        else:
            self.lista_lixeiras.insert(new_index,self.lista_lixeiras.pop(old_index))
            self.enviar_mensagem('posição da lixeira alterada com sucesso.')

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
    