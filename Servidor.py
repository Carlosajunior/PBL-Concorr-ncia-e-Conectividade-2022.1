from re import S
import socket

class Servidor:

    def __init__(self):
        #Define o tamanho máximo de bytes que podem ser recebidos
        self.payload = 2048
        #Configuração do socket para seguir o protocolo TCP/IP
        self.servidor_socket = socket.socket(socket.AF_INET,  socket.SOCK_STREAM)
        #Configuração para permitir que um endereço de IP e uma porta possam ser reutilizados no caso de um crash da aplicação
        self.servidor_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    def alterar_status_lixeira(self,mensagem):
        print("entrou no método certo.")
        print('\n')
        print(mensagem)
        print('\n')

    def dados_das_lixeiras(self,mensagem):
        print(mensagem)

    def esvaziar_lixeira(self, mensagem):
        print(mensagem)

    def alterar_ordem_lixeiras(self, mensagem):
        print(mensagem)

    def adicionar_lixo_lixeira(self, mensagem):
        print(mensagem)

    def iniciar_servidor(self, ip, porta):
        #Incializando o servidor
            print("Iniciando o servidor no IP ",ip," e na porta ",porta,".")
            endereco = (ip,porta)
            print("Servidor rodando no endereço ", endereco)
            self.servidor_socket.bind(endereco)
            #Servidor a passar a aguarda por conexões de clientes, num máximo de 5 clientes em uma fila de espera para se conectar
            self.servidor_socket.listen(5)

    def receber_mensagem(self):
        self.iniciar_servidor("192.168.25.5", 2004)
        while True:
            print("Aguardando conexão.")            
            #Aceita a conexão de um cliente
            cliente, endereco = self.servidor_socket.accept()
            print("conexão efetuada com sucesso com o endereço "+str(endereco)+".")
            #Recebe os dados enviados pelo cliente, até o limite do payload em bytes
            dados = cliente.recv(self.payload)
            if dados:
                mensagem = dados.decode('utf-8')
                if mensagem.split('/')[0] == 'alterar status':
                    self.alterar_status_lixeira(mensagem)
                elif mensagem.split('/')[0] == "dados das lixeiras":
                    self.dados_das_lixeiras(mensagem)
                elif mensagem.split('/')[0] == "esvaziar lixeira":
                    self.esvaziar_lixeira(mensagem)
                #Caso haja dados, eles são printados no terminal
                print("Dados: %s" %dados.decode('utf-8'))
                #Fecha a conexão
                cliente.close()

    
    def enviar_mensagem(self, mensagem):
        try: 
            #Tenta enviar uma mensagem
            self.servidor_socket.send(bytes(mensagem,'utf-8'))
        except socket.error as e: 
            print ("Socket error: ",str(e)) 
        except Exception as e: 
            print ("Ocorreu uma exceção:  ",str(e)) 
        finally: 
            print ("Fechando a conexão com o servidor")
            #Finaliza a conexão com o servidor
            self.servidor_socket.close() 

if __name__ == "__main__":
    servidor = Servidor()
    servidor.receber_mensagem()