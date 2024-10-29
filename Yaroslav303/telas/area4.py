import pygame
from telaBase import Base

class AreaQuatro(Base):
    def __init__(self, inventario):
        super().__init__(inventario) 
        self.spritFundo = pygame.image.load("assets/tela4.png").convert_alpha()
        self.play = True

        # Carregar as imagens do armário e mão
        self.spriteArmarioFechado = pygame.image.load("assets/armário.png")
        self.spriteArmarioAberto = pygame.image.load("assets/armario 2.png")
        self.spriteMao1 = pygame.image.load("assets/mao 1.png")
        self.spriteMao2 = pygame.image.load("assets/mao 2.png")  # Mão após o dedo ser removido
        
        # Definir o estado inicial (fechado)
        self.armario_aberto = False  
        self.spriteAtual = self.spriteArmarioFechado
        
        # Definir o retângulo do armário e da mão
        self.armario = self.spriteAtual.get_rect(center=(50, 400))
        self.mao = self.spriteMao1.get_rect(center=(950, 400))  # Corrigido "get_get_rect"
        
        # Controle para verificar se o item já foi adicionado ao inventário
        self.item_adicionado = False
        self.inventario = inventario
        self.dedo_removido = False  # Controle para mudança de sprite da mão

        # Carregar o som do armário
        self.armario_sound = pygame.mixer.Sound("assets/armario.mp3")

    def processar_entrada(self, eventos, teclas_pressionadas):
        # Verificar eventos de clique
        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                # Verifica se o clique foi no armário
                if self.armario.collidepoint(evento.pos):
                    # Tocar som do armário ao abrir/fechar
                    self.armario_sound.play()

                    # Alterna o estado do armário (aberto ou fechado)
                    self.armario_aberto = not self.armario_aberto
                    # Atualiza o sprite de acordo com o estado
                    if self.armario_aberto:
                        self.spriteAtual = self.spriteArmarioAberto
                    else:
                        self.spriteAtual = self.spriteArmarioFechado
                        # Verifica se é a primeira vez que está sendo fechado e adiciona o item
                        if not self.item_adicionado:
                            self.inventario.add_item("fio")
                            print(self.inventario)
                            self.item_adicionado = True  # Impede que o item seja adicionado novamente

                # Verifica se o clique foi na mão
                if self.mao.collidepoint(evento.pos):
                    if "dedo" in self.inventario.items:
                        self.inventario.remove_item("dedo")
                        self.dedo_removido = True  # Marca que o dedo foi removido
                        self.fim = True

    def atualizar(self):
        # Atualiza o sprite da mão se o dedo foi removido
        if self.dedo_removido:
            self.mao = self.spriteMao2.get_rect(center=(950, 400))  # Atualiza o retângulo da nova mão

    def desenhar(self, tela):
        # Desenhar o fundo e o armário
        tela.blit(self.spritFundo, (0, 0))
        tela.blit(self.spriteAtual, self.armario)

        # Desenhar a mão (atualizada se o dedo foi removido)
        if self.dedo_removido:
            tela.blit(self.spriteMao2, self.mao)  # Desenha a mão sem dedo
        else:
            tela.blit(self.spriteMao1, self.mao)  # Desenha a mão com o dedo

        # Desenhar o inventário
        self.inventario.draw(tela)
