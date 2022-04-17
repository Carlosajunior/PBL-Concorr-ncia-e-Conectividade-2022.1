import socket
import threading

class Servidor:

    def __init__(self):
        self.lista_de_clientes_conectados = []        
        #Define o tamanho máximo de bytes que podem ser recebidos
        self.payload = 2048
        #Configuração do socket para seguir o protocolo TCP/IP
        self.servidor_socket = socket.socket(socket.AF_INET,  socket.SOCK_STREAM)
        #Configuração para permitir que um endereço de IP e uma porta possam ser reutilizados no caso de um crash da aplicação
        self.servidor_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
        
    def alterar_status_lixeira(self,mensagem):
        response = self.enviar_mensagem(self, mensagem)

    def dados_das_lixeiras(self,mensagem):
        pass

    def esvaziar_lixeira(self, mensagem):
        pass

    def alterar_ordem_lixeiras(self, mensagem):
        pass

    def adicionar_lixo_lixeira(self, mensagem):
        pass

    def alterar_trajeto_caminhao(self, mensagem):
        pass
        
    def iniciar_servidor(self):
        #Incializando o servidor            
            endereco = ('localhost',2004)
            print("Iniciando o servidor no localhost na porta 2004.")
            print("Servidor rodando no endereço ", endereco)
            self.servidor_socket.bind(endereco)
            #Servidor a passar a aguarda por conexões de clientes, num máximo de 10 clientes em uma fila de espera para se conectar
            self.servidor_socket.listen(10)
            print("Aguardando conexão.")
            while True:
                #Aceita a conexão de um cliente
                cliente, endereco = self.servidor_socket.accept()
                print("conexão efetuada com sucesso com o endereço "+str(endereco)+".")
                #Adiciona o cliente conectado a uma lista de clientes conectados
                self.lista_de_clientes_conectados.append(cliente)
                #Incia uma thread para receber mensagens do cliente que se conectou
                thread = threading.Thread(target= self.receber_mensagem, args = [cliente])
                thread.start()        

    def remover_cliente(self, cliente):
        self.lista_de_clientes_conectados.remove(cliente)
    
    def receber_mensagem(self,cliente):                 
        try:
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
                elif mensagem.split('/')[0] == "alterar trajeto":
                    self.alterar_trajeto_caminhao(mensagem)
        except:
            self.remover_cliente(cliente)

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
    servidor.iniciar_servidor()