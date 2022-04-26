import json
import socket
import threading

class Servidor:

    def __init__(self):
        self.lista_de_clientes_conectados = []
        self.lixeiras = dict()
        self.caminhao = dict()
        self.administrador = dict()   
        #Define o tamanho máximo de bytes que podem ser recebidos
        self.payload = 2048
        #Configuração do socket para seguir o protocolo TCP/IP
        self.servidor_socket = socket.socket(socket.AF_INET,  socket.SOCK_STREAM)
        #Configuração para permitir que um endereço de IP e uma porta possam ser reutilizados no caso de um crash da aplicação
        self.servidor_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    def cadastrar_lixeira(self, mensagem):
        latitude = mensagem.split('/')[1]
        longitude = mensagem.split('/')[2]
        key = latitude+','+longitude
        self.lixeiras.update({key: self.lista_de_clientes_conectados.pop()})
        print(self.lixeiras)
        print("lixeira cadastrada com sucesso.")                
        
    def alterar_status_lixeira(self,mensagem):
        key = mensagem.split('/')[1]+','+mensagem.split('/')[2]
        endereco = self.lixeiras.get(key)
        msg = 'alterar status/'+mensagem.split('/')[3]
        response = self.servidor_socket.sendto(bytes(msg,'utf-8'), endereco)
        self.enviar_mensagem(response)

    def dados_das_lixeiras(self):
        dados = []
        if self.lixeiras.keys():
            for value in self.lixeiras.values():
                print("buscando dados da lixeira ", value)
                response = self.servidor_socket.sendto(bytes('dados das lixeiras/','utf-8'), value)
                print('dados recebidos.')
                dados.append(json.loads(response))
            dados_lixeiras = {"dados":dados}
            mensagem = json.dumps(dados_lixeiras)
            self.enviar_mensagem(mensagem)
        else:
            self.enviar_mensagem('não há lixeira cadastradas.')

    def esvaziar_lixeira(self, mensagem):
        key = mensagem.split('/')[1]+','+mensagem.split('/')[2]
        endereco = self.lixeiras.get(key)
        msg = "esvaziar lixeira/"
        request = self.servidor_socket.sendto(bytes(msg,'utf-8'), endereco)
        self.enviar_mensagem(request)

    def alterar_ordem_lixeiras(self, mensagem):
        endereco = self.caminhao.get('caminhao')
        msg = 'alterar trajeto/'+mensagem.split('/')[1]+'/'+mensagem.split('/')[2]
        response = self.servidor_socket.sendto(bytes(msg,'utf-8'), endereco)
        self.enviar_mensagem(response)
     
    def cadastrar_administrador(self):
        self.administrador.update({"administrador":self.lista_de_clientes_conectados.pop()})
        print("Administrador cadastrado")

    def cadastrar_caminhao(self):
        self.caminhao.update({"caminhao":self.lista_de_clientes_conectados.pop()})

    def iniciar_servidor(self):
        #Incializando o servidor
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)            
        endereco = (local_ip,2004)
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
            self.lista_de_clientes_conectados.append(endereco)
            #Incia uma thread para receber mensagens do cliente que se conectou
            thread = threading.Thread(target= self.receber_mensagem, args = [cliente])
            thread.start()        

    def remover_cliente(self, cliente):
        self.lista_de_clientes_conectados.remove(cliente)
    
    def receber_mensagem(self,cliente):                 
        #Recebe os dados enviados pelo cliente, até o limite do payload em bytes
        dados = cliente.recv(self.payload)        
        if dados:
            mensagem = dados.decode('utf-8')
            if mensagem.split('/')[0] == 'alterar status':
                self.alterar_status_lixeira(mensagem)
            elif mensagem.split('/')[0] == "dados das lixeiras":
                self.dados_das_lixeiras()
            elif mensagem.split('/')[0] == "esvaziar lixeira":
                self.esvaziar_lixeira(mensagem)
            elif mensagem.split('/')[0] == "alterar trajeto":
                self.alterar_trajeto_caminhao(mensagem)
            elif mensagem.split('/')[0] == "cadastrar lixeira":
                self.cadastrar_lixeira(mensagem)
            elif mensagem.split('/')[0] == "cadastrar caminhao":
                self.cadastrar_caminhao()
            elif mensagem.split('/')[0] == "cadastrar administrador":
                self.cadastrar_administrador()

    def enviar_mensagem(self, mensagem):
        try: 
            #Tenta enviar uma mensagem
            self.servidor_socket.send(bytes(mensagem,'utf-8'))
        except socket.error as e: 
            print ("Socket error: ",str(e)) 
        except Exception as e: 
            print ("Ocorreu uma exceção:  ",str(e)) 

if __name__ == "__main__":
    servidor = Servidor()
    servidor.iniciar_servidor()