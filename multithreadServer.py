import json
import socket
from _thread import *

class Server:

    def __init__(self):
        self.local_ip = socket.gethostbyname(socket.gethostname()) 
        self.dados = []
        self.ThreadCount = 0
        self.porta = 2004
        self.payload = 2048
        self.lixeiras = dict()
        self.caminhao = dict()
        self.administrador = dict()   
        #Configuração do socket para seguir o protocolo TCP/IP
        self.servidor_socket = socket.socket(socket.AF_INET,  socket.SOCK_STREAM)
        #Configuração para permitir que um endereço de IP e uma porta possam ser reutilizados no caso de um crash da aplicação
        self.servidor_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def main(self):
        self.iniciar_servidor()

    def iniciar_servidor(self):
        try:
            self.servidor_socket.bind((self.local_ip, self.porta))
        except socket.error as e:
            print(str(e))
        print("O servidor está rodando no ip ",self.local_ip," e na porta ", self.porta,".")
        self.servidor_socket.listen(5)
        print("Aguardando conexão.")
        while True:
            self.aceitar_conexao()
        self.servidor_socket.close()    

    def aceitar_conexao(self):
        cliente, endereco = self.servidor_socket.accept()
        print("conexão efetuada com sucesso com o endereço "+str(endereco)+".")
        start_new_thread(self.handler_connection,(cliente,))
        self.ThreadCount+=1
        print("Thread numero: ", str(self.ThreadCount))

    def handler_connection(self, cliente):
        while True:
            dados = cliente.recv(self.payload)            
            if dados:
                mensagem = dados.decode('utf-8')
                print(mensagem)
                if mensagem.split('/')[0] == "alterar status":
                    self.alterar_status_lixeira(mensagem)
                elif mensagem.split('/')[0] == "cadastrar dados das lixeiras":
                    self.cadastrar_dados_das_lixeiras(mensagem)
                elif mensagem.split('/')[0] == "esvaziar lixeira":
                    self.esvaziar_lixeira(mensagem)
                elif mensagem.split('/')[0] == "alterar trajeto":
                    self.alterar_trajeto_caminhao(mensagem)
                elif mensagem.split('/')[0] == "cadastrar lixeira":
                    self.cadastrar_lixeira(mensagem,cliente)
                elif mensagem.split('/')[0] == "cadastrar caminhao":
                    self.cadastrar_caminhao(cliente)
                elif mensagem.split('/')[0] == "cadastrar administrador":
                    self.cadastrar_administrador(cliente)
                elif mensagem.split('/')[0] == "remover dados da lixeira":
                    self.remover_dados_lixeira(mensagem)
                elif mensagem.split('/')[0] == "adicionar lixo":
                    self.adicionar_lixo_lixeira(mensagem)
                elif mensagem.split('/')[0] == "notificar lixeira esvaziada":
                    self.notificar_administrador_lixeira_esvaziada(mensagem)
                elif mensagem.split('/')[0] == "iniciar trajeto":
                    self.iniciar_trajeto_caminhao()
                elif mensagem.split('/')[0] == "encerrar conexao":
                    break
        cliente.close()

    #Notifica o administrador que uma lixeira foi esvaziada
    def notificar_administrador_lixeira_esvaziada(self, mensagem):
        self.enviar_mensagem("notificar lixeira esvaziada/"+mensagem.split('/')[1]+'/'+mensagem.split('/')[2], self.administrador.get("administrador"))

    #Envia uma mensagem codificada no padrão utf-8 em bytes, usando como parametro uma conexão que é passada como argumento do método
    def enviar_mensagem(self, mensagem, cliente):
        try:
            #Tenta enviar uma mensagem
            cliente.send(bytes(mensagem,'utf-8'))
        except socket.error as e: 
            print ("Socket error: ",str(e)) 
        except Exception as e: 
            print ("Ocorreu uma exceção:  ",str(e)) 

    #Armazena uma conexão com uma lixeira em um dicionário, utilizando como chave a latitude e a longitude da lixeira, no formato de coordenada,
    #e tendo como valor para esta chave a conexão
    def cadastrar_lixeira(self, mensagem,cliente):
        latitude = mensagem.split('/')[1]
        longitude = mensagem.split('/')[2]
        key = latitude+','+longitude
        self.lixeiras.update({key: cliente})
        print("lixeira cadastrada com sucesso.")                

    #Envia uma requisição para uma lixeira com a quantidade de lixo a ser adicionada. Recebe como parametro a coordenada da lixeira e carga de lixo.
    def adicionar_lixo_lixeira(self, mensagem):
        key = mensagem.split('/')[1]+','+mensagem.split('/')[2]
        cliente = self.lixeiras.get(key)
        msg = 'adicionar lixo/'+mensagem.split('/')[3]
        cliente.send(bytes(msg, 'utf-8'))

    #Remove os dados de uma lixeira, salvos na lista de dados das lixeiras
    def remover_dados_lixeira(self, mensagem):
        response = mensagem.split('/')[1]
        self.dados.remove(json.loads(response))
    
    #envia uma requisição para uma determinada lixeira a fim de alterar o seu status
    def alterar_status_lixeira(self,mensagem):
        key = mensagem.split('/')[1]+','+mensagem.split('/')[2]
        cliente = self.lixeiras.get(key)
        msg = 'alterar status/'+mensagem.split('/')[3]
        cliente.send(bytes(msg, 'utf-8'))

    #Envia a lista de informações das lixeiras presentes no servidor, para um administrador cadastrado no servidor
    def atualizar_informacoes_lixeiras_administrador(self):
        if len(self.administrador.keys()) > 0:
            dados_lixeiras = {"dados":self.dados}
            mensagem = "dados das lixeiras/"+json.dumps(dados_lixeiras) 
            self.enviar_mensagem(mensagem, self.administrador.get("administrador"))

    #Envia a lista de informações das lixeiras presentes no servidor, para um caminhão cadastrado no servidor
    def atualizar_informacoes_lixeiras_caminhao(self):
        if len(self.caminhao.keys()) > 0:
            dados_lixeiras = {"dados":self.dados}
            mensagem = "dados das lixeiras/"+json.dumps(dados_lixeiras) 
            self.enviar_mensagem(mensagem, self.caminhao.get("caminhao"))

    #Recebe os dados de uma lixeira, salva-os na lista de dados de lixeiras do servidor, e envia essa lista para o administrador 
    # e caminhão, caso hajam algum deles cadastrados no servidor
    def cadastrar_dados_das_lixeiras(self, mensagem):
        response = mensagem.split('/')[1]
        self.dados.append(json.loads(response))
        self.atualizar_informacoes_lixeiras_administrador()   
        self.atualizar_informacoes_lixeiras_caminhao()     

    #envia a lista de dados de uma lixeira para um determinado cliente conectado ao servidor, que é passado como parâmetro
    def dados_das_lixeiras(self,cliente):        
        if len(self.lixeiras.keys()) > 0:
            dados_lixeiras = {"dados":self.dados}
            mensagem = "dados das lixeiras/"+json.dumps(dados_lixeiras) 
            self.enviar_mensagem(mensagem,cliente)
        elif len(self.lixeiras.keys()) == 0:
            self.enviar_mensagem('dados das lixeiras/não há lixeiras cadastradas.', cliente)

    #Envia uma requisição para uma lixeira, caso haja algum cadastrado no servidor, para que ela tenha sua carga de lixo esvaziada
    def esvaziar_lixeira(self, mensagem):
        key = mensagem.split('/')[1]+','+mensagem.split('/')[2]
        cliente = self.lixeiras.get(key)
        self.enviar_mensagem("esvaziar lixeira/", cliente)

    def alterar_ordem_lixeiras(self, mensagem):
        endereco = self.caminhao.get('caminhao')
        msg = 'alterar trajeto/'+mensagem.split('/')[1]+'/'+mensagem.split('/')[2]
        response = self.servidor_socket.sendto(bytes(msg,'utf-8'), endereco)
        self.enviar_mensagem(response)
    
    #Envia uma requisição para um caminhão, caso haja algum cadastrado no servidor, para iniciar o trajeto das lixeiras
    def iniciar_trajeto_caminhao(self):
        if len(self.caminhao.keys()) > 0:
            cliente = self.caminhao.get("caminhao")
            self.enviar_mensagem("iniciar trajeto/", cliente)
        else:
            print("Não caminhão cadastrado no servidor.")

    #Salva a conexão de uma administrador com o servidor em um dicionário, usando como chave para acessar essa conexão a palavra "adminstrador",
    #e envia a lista de dados das lixeiras para o administrador
    def cadastrar_administrador(self, cliente):
        self.administrador.update({"administrador":cliente})
        print("Administrador cadastrado.")
        self.dados_das_lixeiras(cliente)

    #Salva a conexão de uma caminhão com o servidor em um dicionário, usando como chave para acessar essa conexão a palavra "caminhao"
    #e envia a lista de dados das lixeiras para o caminhão
    def cadastrar_caminhao(self, cliente):
        self.caminhao.update({"caminhao": cliente})
        print("Caminhão cadastrado;")
        self.dados_das_lixeiras(cliente)

if __name__ == "__main__":
    servidor = Server()
    servidor.main()