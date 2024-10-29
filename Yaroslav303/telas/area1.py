import pygame
from telaBase import Base

class AreaUm(Base):
    def __init__(self, inventario):
        super().__init__(inventario) 
        self.spritFundo = pygame.image.load("assets/tela1.png").convert_alpha()
        
        # Carregar os sprites do baú
        self.spriteBauFechado = pygame.image.load("assets/bau 1.png")
        self.spriteBauAberto = pygame.image.load("assets/bau 2.png")
        
        # Definir o estado inicial (fechado)
        self.bau_aberto = False  
        self.spriteAtualBau = self.spriteBauFechado
        
        # Definir o retângulo do baú
        self.bau = self.spriteAtualBau.get_rect(center=(500, 600))
        
        # Controle para verificar se o item já foi adicionado ao inventário
        self.item_adicionado = False
        self.inventario = inventario

        # Carregar o som do baú
        self.bau_sound = pygame.mixer.Sound("assets/bau.mp3")

        self.play = True

    def processar_entrada(self, eventos, teclas_pressionadas):
        # Verificar eventos de clique
        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                # Verifica se o clique foi no baú
                if self.bau.collidepoint(evento.pos):
                    # Verifica se o jogador possui a "chave" no inventário
                    if 'chave' in self.inventario.items:
                        # Tocar som do baú ao abrir/fechar
                        self.bau_sound.play()

                        # Alterna o estado do baú (aberto ou fechado)
                        self.bau_aberto = not self.bau_aberto
                        
                        # Atualiza o sprite de acordo com o estado
                        if self.bau_aberto:
                            self.spriteAtualBau = self.spriteBauAberto
                            # Remove a "chave" do inventário e adiciona o "dedo" na primeira vez
                            if not self.item_adicionado:
                                self.inventario.remove_item("chave")  # Remove a chave
                                self.inventario.add_item("dedo")  # Adiciona o dedo
                                print(self.inventario)
                                self.item_adicionado = True  # Impede que o item seja adicionado novamente
                        else:
                            self.spriteAtualBau = self.spriteBauFechado

    def atualizar(self):
        pass  # Atualizações da cena, se necessário

    def desenhar(self, tela):
        # Desenhar o fundo e o baú
        tela.blit(self.spritFundo, (0, 0))
        tela.blit(self.spriteAtualBau, self.bau)
        self.inventario.draw(tela)
