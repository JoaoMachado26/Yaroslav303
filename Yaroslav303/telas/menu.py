import pygame
from telaBase import Base

class Menu(Base):
    def __init__(self, inventario):
        super().__init__(inventario) 
        self.spritBotaoPlay = pygame.image.load("assets/play.png").convert_alpha()
        self.spritMensagem = pygame.image.load("assets/mensagem.jpg").convert_alpha()
        self.botaoPlay = self.spritBotaoPlay.get_rect(center=(500, 400))
        self.mensagem = self.spritMensagem.get_rect(center=(500, 300))  # Ajuste a posição da mensagem

        self.spritFundo = pygame.image.load("assets/fundo.png").convert_alpha()

        self.mostrar_mensagem = True  # Controla a exibição da mensagem
        self.play = False

    def processar_entrada(self, eventos, teclas_pressionadas):
        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:
                    if self.mostrar_mensagem and self.mensagem.collidepoint(evento.pos):
                        print("Mensagem clicada! Agora você pode jogar.")
                        self.mostrar_mensagem = False  # Oculta a mensagem
                    elif not self.mostrar_mensagem and self.botaoPlay.collidepoint(evento.pos):
                        print("Botão 'Play' foi clicado!")
                        self.play = True

    def atualizar(self):
        pass  # Nenhuma lógica de atualização necessária para o menu

    def desenhar(self, tela):
        # Desenha o fundo na tela
        tela.blit(self.spritFundo, (0, 0))  # Posição (0, 0) para cobrir toda a tela
        # Desenha a mensagem se deve ser exibida
        if self.mostrar_mensagem:
            tela.blit(self.spritMensagem, self.mensagem)
        else:
            # Desenha o botão na tela
            tela.blit(self.spritBotaoPlay, self.botaoPlay)
