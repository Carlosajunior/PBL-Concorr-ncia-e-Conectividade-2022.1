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
        #Pega os dados base da lixeira, do usuário através do terminal para configurá-la
        latitude = input("Insira o valor da latitude da lixeira: ")
        self.latitude_lixeira = latitude
        longitude = input("Insira o valor da longitude da lixeira: ")
        self.longitude_lixeira = longitude
        capacidade = input("Insira o valor de capacidade máxima de lixo que a lixeira pode comportar: ")
        self.capacidade_lixeira = float(capacidade)
        while True: 
            #Permance no loop até que uma conexão seja estabelecida com sucesso
            try:
                ip = input("Insira o endereço de ip que deseja se conectar: ")
                porta = input("Insira a porta que deseja se conectar no ip informado: ")
                self.lixeira_conectar(ip, int(porta))
            except:
                print("Ocorreu um erro ao tentar se conectar ao endereço informado. Insira os dados novamente.")
                continue
            else:
                break
        #Após a conexão ser estabelicida, envia uma requisição ao servidor para salvar a conexão desta lixeira ao servidor
        self.cadastrar_lixeira() 
        #Inicia em uma thread o método que irá ser responsável por receber as mensagens enviadas pelo servidor e processá-las       
        thread = threading.Thread(target= self.receber_mensagem)
        thread.daemon = True
        thread.start()
        #Após a lixeira ser cadastrada, envia uma requisição ao servidor com os dados atuais da lixeira para serem cadastrados no mesmo
        self.enviar_informacoes_lixeira()
        while True:
            #Inicia um loop onde dá ao usuário as opções de ou adicionar lixo a lixeira (caso possível), ou encerrar o programa
            opcao = input("Escolha uma das opções: \n 1-Inserir carga de lixo \n 2-Encerrar programa \n")            
            if opcao == '1':
                lixo = input("Insira a quantidade de lixo a ser adicionado a lixeira: ")
                self.inserir_lixo(float(lixo))
            elif opcao == '2':
                self.enviar_mensagem("encerrar conexao/")
                break
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
        while True:
            print("Aguardando mensagem.")            
            #Recebe os dados enviados pelo cliente, até o limite do payload em bytes
            dados = self.cliente_socket.recv(self.payload)
            if dados:
                #Decodifica a mensagem recebida utilizando o padrão utf-8 para transformá-la de bytes para uma string
                mensagem = dados.decode('utf-8')
                #Verifica a qual método a parte inicial da string, se refere em sua requisição e então o executa
                if mensagem.split('/')[0] == 'alterar status':
                    self.alterar_status(mensagem)          
                elif mensagem.split('/')[0] == "esvaziar lixeira":
                    self.esvaziar_lixeira()
                elif mensagem.split('/')[0] == "definir capacidade":
                    self.capacidade_lixeira(mensagem)
                    self.enviar_mensagem('capacidade maxima da lixeira alterada')
                elif mensagem.split('/')[0] == "adicionar lixo":
                    self.adicionar_lixo(mensagem)

    #Esvazia a lixeira e então envia três requisições ao servidor para atualizar os dados dela no servidor e 
    #notificar ao administrador e caminhão a atualização de seus dados
    def esvaziar_lixeira(self):
        if self.carga_lixeira > 0.0:
            self.remover_dados_lixeira_servidor()
            self.carga_lixeira = 0.0
            self.enviar_informacoes_lixeira()            
            sleep(1)
            self.informar_lixeira_esvaziada()
            print('lixeira esvaziada')
        else:
            print('lixeira já está vazia')

    #Envia requisição ao servidor para informar ao administrador que a lixeira foi esvaziada
    def informar_lixeira_esvaziada(self):
        self.enviar_mensagem("notificar lixeira esvaziada/"+self.latitude_lixeira+'/'+self.longitude_lixeira)

    #Altera o status da lixeira, no caso de o status ser diferente do atual e seguir o padrão de status, então faz as requisições
    #para atualizar os dados dessa lixeira no servidor e notificar o administrador e caminhão sobre essa atualização
    def alterar_status(self, mensagem):
        if mensagem.split('/')[1] == "aberta" or mensagem.split('/')[1] == "fechada": 
            if mensagem.split('/')[1] != self.status_lixeira:                     
                self.remover_dados_lixeira_servidor()
                self.definir_status_lixeira(mensagem)
                self.enviar_informacoes_lixeira()
            else:
                print("O novo status é igual ao atual.")
        else:
            print("O status informado é inválido.")    

    #Envia uma requisição para o servidor para remover os dados atuais da lixeira, dele
    def remover_dados_lixeira_servidor(self):
        dados_lixeira = {
            "capacidade": self.capacidade_lixeira,
            "carga": self.carga_lixeira,
            "status": self.status_lixeira,
            "posicao": self.posicao_lixeira()
        }
        response = json.dumps(dados_lixeira)
        self.enviar_mensagem("remover dados da lixeira/"+response)
    
    #Envia uma requisição para o servidor para cadastrar os dados atuai da lixeira, nele
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
                self.remover_dados_lixeira_servidor()
                self.carga_lixeira = self.carga_lixeira + lixo
                print("Lixo adicionado com sucesso.")
                self.enviar_informacoes_lixeira()
            elif self.status_lixeira == "fechada":
                print("A lixeira está bloqueada.")
        else:
            print("A carga de lixo ultrapassa a capacidade máxima da lixeira.")

    #Recebe a requsição do servidor para adicionar lixo a lixeira, caso não ultrapasse a capacidade máxima da lixeira e/ou ela não esteja bloqueada.
    #Caso seja possivel adicionar lixo, adiciona-o e atualiza os dados no servidor e notifica o administrador e o caminhão.
    def adicionar_lixo(self, mensagem):
        if float(mensagem.split('/')[1]) + self.carga_lixeira > self.capacidade_lixeira:
            print('a carga de lixo ultrapassa a capacidade máxima da lixeira')
        elif self.status_lixeira == "fechada":
            print("a lixeira está bloqueada, não é possível adicionar lixo")
        else:
            self.remover_dados_lixeira_servidor()
            self.carga_lixeira = self.carga_lixeira + float(mensagem.split('/')[1])
            print("Lixo adicionado com sucesso.")
            self.enviar_informacoes_lixeira()

    #Este método altera o status atual da lixeira via uma requisição do servidor
    def definir_status_lixeira(self, mensagem):
        self.status_lixeira = mensagem.split('/')[1]
        print("status da lixeira alterado para ",self.status_lixeira)

    #Retorna os dados da lixeira de latitude e longitude como uma posição geográfica
    def posicao_lixeira(self):
        posicao =  self.latitude_lixeira+','+self.longitude_lixeira
        return posicao

    #Este método cadastra a conexão da lixeira com o servidor no mesmo
    def cadastrar_lixeira(self):
        mensagem = "cadastrar lixeira/"+self.latitude_lixeira+'/'+self.longitude_lixeira
        self.enviar_mensagem(mensagem)        

if __name__ == "__main__":
    lixeira = Lixeira()
    lixeira.main()