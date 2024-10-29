import pygame
from telaBase import Base
from telas.senha import Popup

class AreaDois(Base):
    def __init__(self, inventario):
        super().__init__(inventario)
        self.spritFundo = pygame.image.load("assets/tela2.png").convert_alpha()
        self.play = True
        self.senha = False

        self.spriteScanner = pygame.image.load("assets/scanner 1.png")
        self.scanner = self.spriteScanner.get_rect(center=(180, 400))

        self.spriteTVs = [
            pygame.image.load("assets/tv 1.png"),
            pygame.image.load("assets/tv 2.png"),
            pygame.image.load("assets/tv 3.png"),
            pygame.image.load("assets/tv 4.png")
        ]
        self.TV = self.spriteTVs[0].get_rect(center=(776, 570))

        self.tv_sprite_index = 0
        self.tv_last_change_time = 0
        self.tv_switching = False

        # Carregar o som da TV
        self.tv_sound = pygame.mixer.Sound("assets/tvSom.mp3")
        self.tv_sound_playing = False  # Variável para verificar se o som já está tocando

        # Cria uma instância do popup para a senha
        self.popup = None
        self.scanner_ativo = True  # Variável para controlar se o scanner está ativo

    def processar_entrada(self, eventos, teclas_pressionadas):
        if self.popup is None:  # Só permite clicar no scanner se o popup não estiver ativo
            for evento in eventos:
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    if evento.button == 1:
                        if self.TV.collidepoint(evento.pos):
                            if 'fio' in self.inventario.items:
                                self.tv_switching = True
                                self.tv_last_change_time = pygame.time.get_ticks()
                                self.inventario.remove_item('fio')
                                
                                # Iniciar o som da TV
                                if not self.tv_sound_playing:
                                    self.tv_sound.play()
                                    self.tv_sound_playing = True

                        if self.scanner_ativo and self.scanner.collidepoint(evento.pos):  # Clique no scanner
                            self.popup = Popup()  # Cria o popup ao clicar no scanner

        else:
            self.popup.processar_eventos(eventos)  # Processa eventos no popup

    def atualizar(self):
        if self.popup is None:  # Atualiza a TV apenas se o popup não estiver aberto
            if self.tv_switching:
                now = pygame.time.get_ticks()
                if now - self.tv_last_change_time >= 2000:
                    if self.tv_sprite_index < len(self.spriteTVs) - 1:
                        self.tv_sprite_index += 1
                        self.tv_last_change_time = now
                    else:
                        self.tv_switching = False
                        self.tv_sound_playing = False  # Som para de tocar após a transição
                        
        if self.popup and not self.popup.ativo():  # Fecha o popup quando a senha estiver correta
            if self.popup.confirmacao:  # Se a senha estiver correta (popup.confirmacao == True)
                self.spriteScanner = pygame.image.load("assets/scanner 2.png")  # Muda o sprite do scanner
                self.scanner_ativo = False  # Desativa a funcionalidade do scanner
                self.inventario.add_item("lixo")
            self.popup = None  # Fecha o popup

    def desenhar(self, tela):
        tela.blit(self.spritFundo, (0, 0))
        tela.blit(self.spriteScanner, self.scanner)
        tela.blit(self.spriteTVs[self.tv_sprite_index], self.TV)

        self.inventario.draw(tela)

        if self.popup:  # Se o popup estiver ativo, desenha ele
            self.popup.desenhar(tela)
