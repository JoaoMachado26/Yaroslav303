import pygame
from telaBase import Base

class Fim(Base):
    def __init__(self, inventario):
        super().__init__(inventario)

        self.play = True

        self.retorno = False
        
        # Carregar os sprites de transição final
        self.spriteLixo = [
            pygame.image.load("assets/porta 1.png"),
            pygame.image.load("assets/porta 2.png"),
            pygame.image.load("assets/porta 3.png"),
            pygame.image.load("assets/porta 4.png"),
            pygame.image.load("assets/fim 1.png"),
            pygame.image.load("assets/fim 2.png")
        ]
        
        # Configurações da transição
        self.current_sprite_index = 0
        self.transition_speed = 5  # Velocidade de transição
        self.alpha_value = 0
        self.increasing = True

    def processar_entrada(self, eventos, teclas_pressionadas):
        # Método vazio, pois a cena final não requer entrada do usuário
        pass

    def atualizar(self):
        if not self.retorno:
            # Controle de transição de alpha (fade in/fade out)
            if self.increasing:
                self.alpha_value += self.transition_speed
                if self.alpha_value >= 255:
                    self.alpha_value = 255
                    self.increasing = False
            else:
                self.alpha_value -= self.transition_speed
                if self.alpha_value <= 0:
                    self.alpha_value = 0
                    self.increasing = True
                    self.current_sprite_index += 1

                    # Verifica se todos os sprites foram exibidos
                    if self.current_sprite_index >= len(self.spriteLixo):
                        self.retorno = True  # Ativa a condição de retorno
                        self.fim = False
                        self.current_sprite_index = len(self.spriteLixo) - 1  # Fixa no último sprite

    def desenhar(self, screen):
        # Preencher fundo com preto
        screen.fill((0, 0, 0))

        # Pegar o sprite atual e aplicar o alpha para a transição
        sprite = self.spriteLixo[self.current_sprite_index].convert_alpha()
        sprite.set_alpha(self.alpha_value)

        # Posicionar o sprite no centro da tela
        sprite_rect = sprite.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))

        # Desenhar o sprite no centro da tela
        screen.blit(sprite, sprite_rect)