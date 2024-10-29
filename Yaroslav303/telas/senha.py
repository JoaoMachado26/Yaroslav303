import pygame
import random

class Popup:
    def __init__(self):
        self.largura = 400
        self.altura = 300
        self.janela = pygame.Surface((self.largura, self.altura))  # Cria uma superfície para o popup
        self.fonte = pygame.font.Font(None, 36)
        self.caixa_texto = ""
        self.limite_caracteres = 4  # Limite de caracteres na caixa de texto
        self.letras = ["б", "р", "е", "д", "а", "г", "з", "т"]  # Mais letras para o popup
        self.senha = "бред"
        self.entrada_correta = False
        self.popup_ativo = True
        self.botoes = self.embaralhar_botoes()  # Embaralha os botões na criação
        self.botao_enter = {"label": "Enter", "rect": pygame.Rect(50, 200, 150, 50)}  # Botão Enter
        self.botao_fechar = {"label": "Fechar", "rect": pygame.Rect(220, 200, 150, 50)}  # Botão Fechar
        self.confirmacao = False

    def embaralhar_botoes(self):
        random.shuffle(self.letras)  # Embaralha as letras
        botoes = []
        x_inicial = 50
        for i, letra in enumerate(self.letras):
            rect = pygame.Rect(x_inicial + (i % 4) * 60, 100 + (i // 4) * 60, 50, 50)
            botoes.append({"label": letra, "rect": rect})
        return botoes

    def desenhar(self, tela):
        # Desenha o popup
        pygame.draw.rect(self.janela, (200, 200, 200), (0, 0, self.largura, self.altura))
        pygame.draw.rect(self.janela, (0, 0, 0), (0, 0, self.largura, self.altura), 5)
        
        # Desenha a caixa de texto
        texto_superficie = self.fonte.render(self.caixa_texto, True, (0, 0, 0))
        self.janela.blit(texto_superficie, (50, 50))

        # Desenha os botões de letras
        for botao in self.botoes:
            pygame.draw.rect(self.janela, (150, 150, 150), botao["rect"])
            label_superficie = self.fonte.render(botao["label"], True, (0, 0, 0))
            self.janela.blit(label_superficie, botao["rect"].move(10, 10))

        # Desenha o botão Enter
        pygame.draw.rect(self.janela, (100, 200, 100), self.botao_enter["rect"])
        enter_superficie = self.fonte.render(self.botao_enter["label"], True, (0, 0, 0))
        self.janela.blit(enter_superficie, self.botao_enter["rect"].move(10, 10))

        # Desenha o botão Fechar
        pygame.draw.rect(self.janela, (200, 100, 100), self.botao_fechar["rect"])
        fechar_superficie = self.fonte.render(self.botao_fechar["label"], True, (0, 0, 0))
        self.janela.blit(fechar_superficie, self.botao_fechar["rect"].move(10, 10))

        tela.blit(self.janela, (300, 200))  # Posiciona o popup no centro da tela

    def processar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                # Verifica os botões de letras
                for botao in self.botoes:
                    if botao["rect"].collidepoint(evento.pos[0] - 300, evento.pos[1] - 200):  # Ajusta para posição do popup
                        if len(self.caixa_texto) < self.limite_caracteres:  # Verifica o limite de caracteres
                            self.caixa_texto += botao["label"]
                
                # Verifica o botão Enter
                if self.botao_enter["rect"].collidepoint(evento.pos[0] - 300, evento.pos[1] - 200):
                    self.verificar_senha()

                # Verifica o botão Fechar
                if self.botao_fechar["rect"].collidepoint(evento.pos[0] - 300, evento.pos[1] - 200):
                    self.popup_ativo = False  # Fecha o popup manualmente

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_BACKSPACE:  # Apagar texto
                    self.caixa_texto = self.caixa_texto[:-1]

                if evento.key == pygame.K_RETURN:  # Testar a senha
                    self.verificar_senha()

    def verificar_senha(self):
        if self.caixa_texto == self.senha:
            self.entrada_correta = True
            self.confirmacao = True
            self.popup_ativo = False
        else:
            self.caixa_texto = ""  # Limpa a caixa de texto se a senha estiver incorreta

    def ativo(self):
        return self.popup_ativo
