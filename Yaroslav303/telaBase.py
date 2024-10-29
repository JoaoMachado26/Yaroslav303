class Base:
    def __init__(self, inventario):
        self.proxima_cena = self
        self.fim = False
        self.inventario = inventario  # Salva o inventário para uso nas classes filhas

    def entrada(self, eventos, teclas_pressionadas):
        pass

    def atualizar(self):
        pass

    def desenhar(self, tela):
        pass

    def mudarcena(self, proxima_cena):
        self.proxima_cena = proxima_cena

    def terminar(self):
        self.mudarcena(None)
