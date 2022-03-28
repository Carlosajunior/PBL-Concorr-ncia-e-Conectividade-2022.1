import re


class Caminhao:

    def __init__(self):
        self.capacidade = 0
        self.carga = 0
        self.lista_lixeiras = list

    def definir_capacidade_caminhao(self,capacidade):
        self.capacidade = capacidade

    def capacidade_do_caminhao(self):
        return self.capacidade

    def definir_carga_caminhao(self, carga):
        self.carga = carga

    def definir_percurso_lixeiras(self, percurso_lixeiras):
        self.lista_lixeiras = percurso_lixeiras

    def percurso_das_lixeiras(self):
        return self.lista_lixeiras