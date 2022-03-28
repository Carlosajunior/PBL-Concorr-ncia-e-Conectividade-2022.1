class Lixeira:

    def __init__(self):
        self.capacidade_lixeira = 0
        self.latitude_lixeira = 0
        self.longitude_lixeira = 0
        self.carga_lixeira = 0
        self.status_lixeira = "aberta"

    def definir_capacidade(self, capacidade_lixeira):
        self.capacidade_lixeira = capacidade_lixeira

    def capacidade_lixeira(self):
        return self.capacidade_lixeira

    def longitude_lixeira(self):
        return self.longitude_lixeira

    def latitude_lixeira(self):
        return self.latitude_lixeira

    def definir_carga(self, carga_lixeira):
        self.carga_lixeira = carga_lixeira

    def carga_lixeira(self):
        return self.carga_lixeira

    def definir_status_lixeira(self, status_lixeira):
        self.status_lixeira = status_lixeira

    def status_da_lixeira(self):
        return self.status_lixeira