class Estacao_de_Transbordo:

    def __init__(self):
        self.capacidade_estacao=0
        self.latitude_estacao=0
        self.longitude_estacao=0
        self.carga_estacao=0

    def definir_capacidade_estacao(self, capacidade_estacao):
        self.capacidade_estacao = capacidade_estacao
    
    def capacidade_da_estacao(self):
        return self.capacidade_da_estacao

    def definir_longitude_estacao(self, longitude_estacao):
        self.longitude_estacao = longitude_estacao

    def longitude_da_estacao(self):
        return self.longitude_estacao

    def definir_latitude_estacao(self, latitude_estacao):
        self.latitude_estacao = latitude_estacao

    def latitude_da_estacao(self):
        return self.latitude_estacao

    def definir_carga_estacao(self, carga_estacao):
        self.carga_estacao = carga_estacao

    def carga_da_estacao(self):
        return self.carga_estacao
