import json
import socket

class Administrador:
    def __init__(self):
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
        self.cadastrar_administrador()
        # thread = threading.Thread(target= self.receber_mensagem)
        # thread.start()
        while True:
            self.dados_das_lixeiras()
            opcao = input("Escolha uma das opções:\n 1-Alterar status de uma lixeira \n 2-Alterar o trajeto do caminhão")
            if opcao == '1':
                print("Informe os dados da lixeira que deseja modificar o status: \n")
                latitude = input("Latitude: \n")
                longitude = input("Longitude: \n")
                status = input("Novo status da lixeira: \n")
                self.alterar_status_lixeira(latitude, longitude, status)

    #Realiza a conexão do administrador ao servidor utilizando o protocolo TCP/IP
    def administrador_conectar(self,ip, porta):
        #Tenta estabelecer uma conexão com o endereço de IP e a porta informados
        print("Se conectando ao ip "+ip+" na porta "+str(porta)+".")
        endereco = (ip, porta)
        self.administrador_socket.connect(endereco)

    #Este método recebe uma mensagem no formato de string e a codifica no formato utf-8 em bytes para enviar para o servidor
    def administrador_enviar(self,mensagem):
        try:             
            self.administrador_socket.send(bytes(mensagem,'utf-8'))
            response = self.administrador_socket.recv(2048)
            return response
        except socket.error as e: 
            print ("Socket error: ",str(e)) 
        except Exception as e: 
            print ("Ocorreu uma exceção:  ",str(e)) 

    #Este método cadastra os dados do administrador no servidor
    def cadastrar_administrador(self):
        self.administrador_enviar("cadastrar administrador/")

    #Envia uam requisição para alterar o status de uma lixeira, usando como identificador sua latitude e longitude
    def alterar_status_lixeira(self,latitude, longitude, status):
        mensagem = 'alterar status/'+latitude+'/'+longitude+'/'+status
        response = self.administrador_enviar(self, mensagem)
        if response == 'status alterado':
            print('status alterado com sucesso.')
        else:
            print('ocorreu um erro ao tentar alterar o status.')

    #Altera a posição de uma lixeira no percurso do caminhão, usando como identificador sua latitude e longitude e informando a nova posição
    def alterar_percurso(self, latitude, longitude, posicao):
        mensagem = 'alterar trajeto/'+latitude+'/'+longitude+'/'+posicao
        response = self.administrador_enviar(self, mensagem)
        if response == 'posição da lixeira alterada':
            print('posição da lixeira alterada com sucesso.')
        else:
            print(response)

    #Busca os dados de todas as lixeiras cadastradas no servidor ao enviar uma requisição destes dados para o mesmo
    def dados_das_lixeiras(self): 
        print('buscando dados das lixeiras.\n')
        response = self.administrador_enviar("dados das lixeiras/")
        print('dados recebidos.\n')
        string_json = response.decode('utf-8')
        lista_lixeiras = json.loads(string_json).get("dados")
        print(lista_lixeiras)

if __name__ == "__main__":
    administrador = Administrador()
    administrador.main()
    