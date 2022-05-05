import json
import socket
import sys
import threading
from time import sleep

class Lixeira:

    def __init__(self):
        self.capacidade_lixeira = 0.0
        self.latitude_lixeira = 0
        self.longitude_lixeira = 0
        self.carga_lixeira = 0.0
        self.status_lixeira = "aberta"
        self.cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.payload = 2048

    #A função principal da Lixeira, é responsável por iniciar os dados da lixeira e então tentar conectá-la ao servidor. Após conectada, fica aguardando
    #mensagens do servidor em uma thread, enquanto possibilita que o usuário possa adicionar mais lixo a ela via terminal
    def main(self):
        latitude = input("Insira o valor da latitude da lixeira: ")
        self.latitude_lixeira = latitude
        longitude = input("Insira o valor da longitude da lixeira: ")
        self.longitude_lixeira = longitude
        capacidade = input("Insira o valor de capacidade máxima de lixo que a lixeira pode comportar: ")
        self.capacidade_lixeira = float(capacidade)
        while True: 
            try:
                ip = input("Insira o endereço de ip que deseja se conectar: ")
                porta = input("Insira a porta que deseja se conectar no ip informado: ")
                self.lixeira_conectar(ip, int(porta))
            except:
                print("Ocorreu um erro ao tentar se conectar ao endereço informado. Insira os dados novamente.")
                continue
            else:
                break
        self.cadastrar_lixeira()        
        thread = threading.Thread(target= self.receber_mensagem)
        thread.daemon = True
        thread.start()
        self.enviar_informacoes_lixeira()
        while True:
            opcao = input("Escolha uma das opções: \n 1-Inserir carga de lixo \n 2-Encerrar programa \n")
            if opcao == '2':
                self.enviar_mensagem("encerrar conexao/")
                break
            elif opcao == '1':
                lixo = input("Insira a quantidade de lixo a ser adicionado a lixeira: ")
                self.inserir_lixo(float(lixo))
        sys.exit()     

    #Faz a conexão da lixeira ao servidor usando o protocolo TCP/IP
    def lixeira_conectar(self,ip, porta):
        #Tenta estabelecer uma conexão com o endereço de IP e a porta informados
        print("Se conectando ao ip ", ip," na porta ",porta,".")
        endereco = (ip, porta)
        try:
            self.cliente_socket.connect(endereco)
            print("Conexão efetuada com sucesso.")   
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
        print("thread sendo executada")
        while True:
            print("Aguardando mensagem.")            
            #Recebe os dados enviados pelo cliente, até o limite do payload em bytes
            dados = self.cliente_socket.recv(self.payload)
            if dados:
                mensagem = dados.decode('utf-8')
                if mensagem.split('/')[0] == 'alterar status':
                    self.alterar_status(mensagem)          
                elif mensagem.split('/')[0] == "esvaziar lixeira":
                    self.esvaziar_lixeira()
                elif mensagem.split('/')[0] == "definir capacidade":
                    self.capacidade_lixeira(mensagem)
                    self.enviar_mensagem('capacidade maxima da lixeira alterada')
                elif mensagem.split('/')[0] == "adicionar lixo":
                    self.adicionar_lixo(mensagem)
                   
    def esvaziar_lixeira(self):
        if self.carga_lixeira > 0:
            self.remover_dados_lixeira_servidor()
            self.definir_carga(0)
            self.enviar_informacoes_lixeira()
            self.informar_lixeira_esvaziada()
            print('lixeira esvaziada')
        else:
            print('lixeira já está vazia')

    def informar_lixeira_esvaziada(self):
        self.enviar_mensagem("notificar lixeira esvaziada/"+self.latitude_lixeira+'/'+self.longitude_lixeira)

    def alterar_status(self, mensagem):
        if mensagem.split('/')[1] != self.status_lixeira and mensagem.split('/')[1] == "aberta" or mensagem.split('/')[1] == "fechada":                      
            self.remover_dados_lixeira_servidor()
            self.definir_status_lixeira(mensagem)
            self.enviar_informacoes_lixeira()    

    def remover_dados_lixeira_servidor(self):
        dados_lixeira = {
            "capacidade": self.capacidade_lixeira,
            "carga": self.carga_lixeira,
            "status": self.status_lixeira,
            "posicao": self.posicao_lixeira()
        }
        response = json.dumps(dados_lixeira)
        self.enviar_mensagem("remover dados da lixeira/"+response)

    def enviar_informacoes_lixeira(self):
        dados_lixeira = {
            "capacidade": self.capacidade_lixeira,
            "carga": self.carga_lixeira,
            "status": self.status_lixeira,
            "posicao": self.posicao_lixeira()
        }
        response = json.dumps(dados_lixeira)
        self.enviar_mensagem("cadastrar dados das lixeiras/"+response)

    #Este método é responsável por alterar a capacidade maxima da lixeira através de uma requisição do servidor
    def definir_capacidade(self, mensagem):
        self.capacidade_lixeira = float(mensagem.split('/')[1])

    #Este método insere mais lixo na lixeira através de dados inseridos pelo terminal
    def inserir_lixo(self, lixo):
        if lixo + self.carga_lixeira <= self.capacidade_lixeira :
            if self.status_lixeira == "aberta":
                self.carga_lixeira = self.carga_lixeira() + lixo
                print("Lixo adicionado com sucesso.")
            elif self.status_lixeira == "fechada":
                print("A lixeira está bloqueada.")
        else:
            print("A carga de lixo ultrapassa a capacidade máxima da lixeira.")

    def adicionar_lixo(self, mensagem):
        if float(mensagem.split('/')[1]) + self.carga_lixeira > self.capacidade_lixeira:
            print('a carga de lixo ultrapassa a capacidade máxima da lixeira')
        elif self.status_lixeira == "fechada":
            print("a lixeira está bloqueada, não é possível adicionar lixo")
        else:
            self.remover_dados_lixeira_servidor()
            self.definir_carga(mensagem)
            self.enviar_informacoes_lixeira()

    #Este método é responsável por adicionar mais lixo a lixeira via uma requisição do servidor
    def definir_carga(self, mensagem):
        if self.carga_lixeira + float(mensagem.split('/')[1]) <= self.capacidade_lixeira:
            self.carga_lixeira = self.carga_lixeira + float(mensagem.split('/')[1])
            print("Lixo adicionado com sucesso.")
        else:
            print('A carga de lixo ultrapassa a capacidade maxima da lixeira.')

    #Este método altera o status atual da lixeira via uma requisição do servidor
    def definir_status_lixeira(self, mensagem):
        self.status_lixeira = mensagem.split('/')[1]
        print("status da lixeira alterado para ",self.status_lixeira)

    def posicao_lixeira(self):
        posicao =  self.latitude_lixeira+','+self.longitude_lixeira
        return posicao

    #Este método cadastra os dados da lixeira no servidor
    def cadastrar_lixeira(self):
        mensagem = "cadastrar lixeira/"+self.latitude_lixeira+'/'+self.longitude_lixeira
        self.enviar_mensagem(mensagem)        

if __name__ == "__main__":
    lixeira = Lixeira()
    lixeira.main()