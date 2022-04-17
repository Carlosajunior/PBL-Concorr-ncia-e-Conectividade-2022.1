import imp
import json


import socket

class Lixeira:

    def __init__(self):
        self.capacidade_lixeira = 0
        self.latitude_lixeira = 0
        self.longitude_lixeira = 0
        self.carga_lixeira = 0
        self.status_lixeira = "aberta"
        self.cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.payload = 2048


    def lixeira_conectar(self,ip, porta):
        #Tenta estabelecer uma conexão com o endereço de IP e a porta informados
        print("Se conectando ao ip ", ip," na porta ",porta,".")
        endereco = (ip, porta)
        self.cliente_socket.connect(endereco)
        self.receber_mensagem()

    def enviar_mensagem(self,ip, porta, mensagem):
        try: 
            #Tenta enviar uma mensagem
            self.cliente_socket.send(bytes(mensagem,'utf-8'))
        except socket.error as e: 
            print ("Socket error: ",str(e)) 
        except Exception as e: 
            print ("Ocorreu uma exceção:  ",str(e)) 

    def receber_mensagem(self):
        while True:
            print("Aguardando mensagem.")            
            #Aceita a conexão de um cliente
            cliente, endereco = self.cliente_socket.accept()
            print("conexão efetuada com sucesso com o endereço "+str(endereco)+".")
            #Recebe os dados enviados pelo cliente, até o limite do payload em bytes
            dados = cliente.recv(self.payload)
            if dados:
                mensagem = dados.decode('utf-8')
                if mensagem.split('/')[0] == 'alterar status':
                    if mensagem.split('/')[1] == self.status_lixeira():
                        self.cliente_socket.send(bytes('novo status é igual ao atual','utf-8'))
                    else:
                        self.definir_status_lixeira(mensagem)
                        self.cliente_socket.send(bytes('status alterado','utf-8'))                   
                elif mensagem.split('/')[0] == "dados das lixeiras":                                                                
                    dados_lixeira = {
                        "carga": self.carga_lixeira(),
                        "status": self.status_da_lixeira(),
                        "posicao": self.posicao_lixeira()
                    }
                    response = json.dumps(dados_lixeira)
                    self.cliente_socket.send(bytes(response,'utf-8')) 
                elif mensagem.split('/')[0] == "esvaziar lixeira":
                    if self.carga_lixeira() > 0:
                        self.definir_carga(0)
                        self.cliente_socket.send(bytes('lixeira esvaziada','utf-8'))
                    else:
                        self.cliente_socket.send(bytes('lixeira já está vazia','utf-8'))
                elif mensagem.split('/')[0] == "definir capacidade":
                    self.capacidade_lixeira(mensagem)
                    self.cliente_socket.send(bytes('capacidade maxima da lixeira alterada','utf-8'))
                elif mensagem.split('/')[0] == "adicionar lixo":
                    if float(mensagem.split('/')[1]) + self.carga_lixeira() > self.capacidade_lixeira():
                        self.cliente_socket.send(bytes('a carga de lixo ultrapassa a capacidade máxima da lixeira','utf-8'))
                    else:
                        self.definir_carga(mensagem)
                        self.cliente_socket.send(bytes('lixo adicionado a lixeira com sucesso','utf-8'))

    def definir_capacidade(self, mensagem):
        self.capacidade_lixeira = mensagem.split('/')[1]

    def capacidade_lixeira(self):
        return self.capacidade_lixeira

    def definir_carga(self, mensagem):
        self.carga_lixeira = self.carga_lixeira + float(mensagem.split('/')[1])

    def carga_lixeira(self):
        return self.carga_lixeira

    def definir_status_lixeira(self, mensagem):
        self.status_lixeira = mensagem.split('/')[1]

    def status_da_lixeira(self):
        return self.status_lixeira

    def posicao_lixeira(self):
        return self.latitude_lixeira, self.longitude_lixeira

if __name__ == "__main__":
    lixeira = Lixeira()
    lixeira.lixeira_conectar("192.168.43.143", 7777)