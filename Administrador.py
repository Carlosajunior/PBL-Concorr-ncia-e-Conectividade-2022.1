import json
import socket
import threading

class Administrador:
    def __init__(self):
        self.payload = 2048
        #Configuração do socket para atender ao protocolo TCP/IP
        self.administrador_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    #É a função principal do administrador, que faz a sua conexão com o servidor, seu cadastro e fica aguardando por novas mensagens do servidor
    #e envia mensagens ao servidor
    def main(self):
        while True: 
            try:
                ip = input("Insira o endereço de ip que deseja se conectar: ")
                porta = input("Insira a porta que deseja se conectar no ip informado: ")
                self.administrador_conectar(ip, int(porta))
                print("Conectado ao servidor.")
            except:
                print("Ocorreu um erro ao tentar se conectar ao endereço informado. Insira os dados novamente.")
                continue
            else:
                break        
        thread = threading.Thread(target= self.receber_mensagem)
        thread.daemon = True
        thread.start()
        self.cadastrar_administrador()
        while True:
            opcao = input("Escolha uma das opções:\n 1-Alterar status de uma lixeira \n 2-Alterar o trajeto do caminhão \n 3-Adicionar lixo a uma lixeira")
            if opcao == '1':
                print("Informe os dados da lixeira que deseja modificar o status: \n")
                latitude = input("Latitude: \n")
                longitude = input("Longitude: \n")
                status = input("Novo status da lixeira: \n")
                self.alterar_status_lixeira(latitude, longitude, status)
            if opcao == '3':
                print("Informe os dados da lixeira que deseja adicionar lixo: \n")
                latitude = input("Latitude: \n")
                longitude = input("Longitude: \n")
                lixo = input("Quantidade de lixo a ser adicionada: \n")
                self.adicionar_lixo_lixeira(latitude,longitude,lixo)

    #Realiza a conexão do administrador ao servidor utilizando o protocolo TCP/IP
    def administrador_conectar(self,ip, porta):
        #Tenta estabelecer uma conexão com o endereço de IP e a porta informados
        print("Se conectando ao ip "+ip+" na porta "+str(porta)+".")
        endereco = (ip, porta)
        try:
            self.administrador_socket.connect(endereco)
        except socket.error as e:
            print(str(e))

    def receber_mensagem(self):
        while True:
            try:
                dados = self.administrador_socket.recv(self.payload)
                if dados:
                    mensagem = dados.decode('utf-8')
                    if mensagem.split('/')[0] == "dados das lixeiras":
                        if mensagem.split('/')[1] != 'não há lixeiras cadastradas.':
                            string_json = mensagem.split('/')[1]
                            lista_lixeiras = json.loads(string_json).get("dados")
                            print("\n")
                            print(lista_lixeiras)
                        else:
                            print("\nNão há lixeiras cadastradas no servidor.")            
            except Exception as e: 
                print ("Ocorreu uma exceção:  ",str(e)) 

    #Este método recebe uma mensagem no formato de string e a codifica no formato utf-8 em bytes para enviar para o servidor
    def administrador_enviar(self,mensagem):
        try:             
            self.administrador_socket.send(bytes(mensagem,'utf-8'))
        except socket.error as e: 
            print ("Socket error: ",str(e)) 
        except Exception as e: 
            print ("Ocorreu uma exceção:  ",str(e)) 

    #Este método cadastra os dados do administrador no servidor
    def cadastrar_administrador(self):
        self.administrador_enviar("cadastrar administrador/")

    def adicionar_lixo_lixeira(self,latitude,longitude,lixo):
        mensagem = 'adicionar lixo/'+latitude+'/'+longitude+'/'+lixo
        self.administrador_enviar(mensagem)

    #Envia uam requisição para alterar o status de uma lixeira, usando como identificador sua latitude e longitude
    def alterar_status_lixeira(self,latitude, longitude, status):
        mensagem = 'alterar status/'+latitude+'/'+longitude+'/'+status
        self.administrador_enviar(mensagem)

    #Altera a posição de uma lixeira no percurso do caminhão, usando como identificador sua latitude e longitude e informando a nova posição
    def alterar_percurso(self, latitude, longitude, posicao):
        mensagem = 'alterar trajeto/'+latitude+'/'+longitude+'/'+posicao
        response = self.administrador_enviar(self, mensagem)
        if response == 'posição da lixeira alterada':
            print('posição da lixeira alterada com sucesso.')
        else:
            print(response)
                

if __name__ == "__main__":
    administrador = Administrador()
    administrador.main()
    