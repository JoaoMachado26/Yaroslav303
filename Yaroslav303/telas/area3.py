import pygame
from telaBase import Base

class AreaTres(Base):
    def __init__(self, inventario):
        super().__init__(inventario) 
        self.spritFundo = pygame.image.load("assets/tela3.png").convert_alpha()
        self.play = True

        # Carregando os sprites de lixo
        self.spriteLixo = [
            pygame.image.load("assets/lixo 1.png"),
            pygame.image.load("assets/lixo 2.png"),
            pygame.image.load("assets/lixo 3.png"),
            pygame.image.load("assets/lixo 4.png")
        ]

        self.spriteChave = pygame.image.load("assets/chave.png")
        self.chave_rect = self.spriteChave.get_rect(topleft=(477, 600))  # Posiciona a chave

        # Variáveis para o controle de estado
        self.lixo_atual = 0
        self.lixo_rect = self.spriteLixo[self.lixo_atual].get_rect(center=(500, 400))  # Posiciona o lixo
        self.transicao_iniciada = False
        self.tempo_inicial = 0
        self.intervalo_transicao = 500  # 500 milissegundos de intervalo entre sprites
        self.chave_coletada = False

    def processar_entrada(self, eventos, teclas_pressionadas):
        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                # Verifica se o lixo está no inventário
                if "lixo" in self.inventario.items:
                    # Detecta se o clique está dentro do primeiro sprite de lixo
                    if self.lixo_rect.collidepoint(evento.pos) and not self.transicao_iniciada:
                        self.transicao_iniciada = True
                        self.tempo_inicial = pygame.time.get_ticks()
                else:
                    print("Item 'lixo' não está no inventário.")
                
                # Verifica se a chave foi clicada após a animação do lixo
                if self.chave_rect.collidepoint(evento.pos) and not self.chave_coletada:
                    self.inventario.add_item("chave")  # Adiciona a chave ao inventário
                    self.inventario.remove_item("lixo")
                    self.chave_coletada = True  # Marca a chave como coletada

    def atualizar(self):
        # Se a transição foi iniciada, mudamos o sprite a cada intervalo de tempo
        if self.transicao_iniciada:
            tempo_atual = pygame.time.get_ticks()
            if tempo_atual - self.tempo_inicial >= self.intervalo_transicao:
                # Vai para o próximo sprite de lixo
                self.lixo_atual += 1
                self.tempo_inicial = tempo_atual  # Reinicia o temporizador

                # Se chegou ao último sprite, termina a transição
                if self.lixo_atual >= len(self.spriteLixo):
                    self.lixo_atual = len(self.spriteLixo) - 1
                    self.transicao_iniciada = False  # Impede que a animação reinicie

    def desenhar(self, tela):
    # Desenha o fundo da área
        tela.blit(self.spritFundo, (0, 0)) 

        # Desenha o sprite de lixo atual (se a chave não foi coletada)
        if not self.chave_coletada:
            tela.blit(self.spriteLixo[self.lixo_atual], self.lixo_rect)

        # Desenha a chave somente após a transição dos sprites de lixo ter terminado e a chave não tiver sido coletada
        if not self.chave_coletada and self.lixo_atual == len(self.spriteLixo) - 1:
            tela.blit(self.spriteChave, self.chave_rect)

        # Desenha o inventário
        self.inventario.draw(tela)
