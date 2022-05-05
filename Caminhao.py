import json
import socket
import threading
from time import sleep

class Caminhao:

    def __init__(self):
        self.lista_lixeiras = []
        self.payload = 2048
        self.cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #É a função principal do caminhão, que faz a sua conexão com o servidor, seu cadastro e fica aguardando por novas mensagens do servidor
    def main(self):
        while True: 
            try:
                ip = input("Insira o endereço de ip que deseja se conectar: ")
                porta = input("Insira a porta que deseja se conectar no ip informado: ")
                self.caminhao_conectar(ip, int(porta))
            except:
                print("Ocorreu um erro ao tentar se conectar ao endereço informado. Insira os dados novamente.")
                continue
            else:
                break
        self.cadastrar_caminhao()        
        thread = threading.Thread(target= self.receber_mensagem)
        thread.daemon = True
        thread.start()
        self.realizar_trajeto()

    #Cadastra os dados do caminhão no servidor
    def cadastrar_caminhao(self):
        self.enviar_mensagem("cadastrar caminhao/")
    
    #Realiza a conexão do caminhão ao servidor utilizando o protocolo TCP/IP
    def caminhao_conectar(self,ip, porta):
        #Tenta estabelecer uma conexão com o endereço de IP e a porta informados
        print("Se conectando ao ip ", ip," na porta ",porta,".")
        endereco = (ip, porta)
        try:
            self.cliente_socket.connect(endereco)
        except socket.error as e:
            print(str(e))

    #Este método recebe uma mensagem no formato de string e a codifica no formato utf-8 em bytes para enviar para o servidor
    def enviar_mensagem(self, mensagem):
        try: 
            #Tenta enviar uma mensagem
            self.cliente_socket.send(bytes(mensagem,'utf-8'))
        except socket.error as e: 
            print ("Socket error: ",str(e)) 
        except Exception as e: 
            print ("Ocorreu uma exceção:  ",str(e)) 

    #Este método é responsável por receber as mensagens enviadas pelo servidor, e a partir de seu conteudo, executar algum dos métodos
    def receber_mensagem(self):
        while True:
            try:
                dados = self.cliente_socket.recv(self.payload)
                if dados:
                        mensagem = dados.decode('utf-8')   
                        if mensagem.split('/')[0] == "alterar trajeto":
                            self.alterar_trajeto_caminhao(mensagem)
                        elif mensagem.split('/')[0] == "dados das lixeiras":
                            if mensagem.split('/')[1] != 'não há lixeiras cadastradas.':
                                string_json = mensagem.split('/')[1]
                                lista_lixeiras = json.loads(string_json).get("dados")
                                print("\n")
                                print(lista_lixeiras)
                            else:
                                print("\nNão há lixeiras cadastradas no servidor.")        
            except Exception as e: 
                print ("Ocorreu uma exceção:  ",str(e)) 

    #Esse método é responsavel por receber uma string que contem a posição atual de uma lixeira na lista de percurso do caminhão e a posição
    #nova que essa lixeira deve ser colocada
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

    def realizar_trajeto(self):
        while True:
            for lixeira in self.lista_lixeiras:
                print("Realizando o trajeto.")
                self.lista_lixeiras.pop(0)
                if lixeira.get('status') == 'aberta' and float(lixeira.get("carga") > 0):
                    latitude = lixeira.get('posicao').split(',')[0]
                    longitude = lixeira.get('posicao').split(',')[1]
                    self.enviar_mensagem('esvaziar lixeira/'+latitude+'/'+longitude)  
                    print("lixeira ",lixeira.get('posicao')," foi esvaziada.")
                sleep(2)      

if __name__ == "__main__":
    caminhao = Caminhao()
    caminhao.main()
    