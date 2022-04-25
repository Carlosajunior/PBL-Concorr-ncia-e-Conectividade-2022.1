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
                elif mensagem.split('/')[0] == "trajeto das lixeiras":
                    self.percurso_das_lixeiras()

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

    def definir_percurso_lixeiras(self):
        response = self.caminhao_enviar("dados das lixeiras/")
        mensagem = response.decode('utf-8')
        if mensagem == 'não há lixeira cadastradas.':
            print("Não há lixeiras cadastradas no sistema.")
        else:
            lixeiras_json = json.loads(mensagem)
            self.lista_lixeiras = lixeiras_json.get('dados')
            print('percurso das lixeiras obtido.')

    def percurso_das_lixeiras(self):
        percuso_lixeiras = {"dados":self.lista_lixeiras}
        trajeto_lixeiras = json.dumps(percuso_lixeiras)
        self.enviar_mensagem(trajeto_lixeiras)

    def esvaziar_lixeira(self):
        dados_lixeira = self.lista_lixeiras.pop(0)
        if dados_lixeira.get('status') == 'aberta':
            latitude = dados_lixeira.get('posicao').split(',')[0]
            longitude = dados_lixeira.get('posicao').split(',')[0]
            response = self.enviar_mensagem('esvaziar lixeira/'+latitude+'/'+longitude)
            if response.decode('utf-8') == 'lixeira esvaziada':
                print("lixeira esvaziada.")
            else:
                print("Não foi possivel esvaziar a lixeira.")
        else:
            print("A lixeira na posicao ",dados_lixeira.get('posicao')," está bloqueada.")

if __name__ == "__main__":
    caminhao = Caminhao()
    caminhao.caminhao_conectar("192.168.43.143", 7777)
    