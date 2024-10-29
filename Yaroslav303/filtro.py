import pygame
import random
import time
# Função para adicionar "ruído" simulando o grão de uma câmera antiga
def adicionar_ruido(superficie):
    superficie_ruido = superficie.copy()
    for _ in range(2000):
        x = random.randint(0, superficie.get_width() - 1)
        y = random.randint(0, superficie.get_height() - 1)
        cor = superficie_ruido.get_at((x, y))

        ruido = random.randint(-20, 20)
        nova_cor = (
            max(0, min(255, cor[0] + ruido)),
            max(0, min(255, cor[1] + ruido)),
            max(0, min(255, cor[2] + ruido)),
            cor[3]
        )
        superficie_ruido.set_at((x, y), nova_cor)

    return superficie_ruido

# Função para simular uma leve distorção de "tremulação" da imagem
def aplicar_distorcao(superficie, ultimo_tempo_atualizacao):
    tempo_atual = time.time()
    if tempo_atual - ultimo_tempo_atualizacao > 0.5:
        deslocamento = random.randint(-3, 3)
        superficie_distorcida = pygame.Surface(superficie.get_size())
        superficie_distorcida.blit(superficie, (deslocamento, 0))
        return superficie_distorcida, tempo_atual
    return superficie, ultimo_tempo_atualizacao

# Função para adicionar estática
def adicionar_estatica(superficie):
    superficie_estatica = superficie.copy()
    for _ in range(100):
        x = random.randint(0, superficie.get_width() - 1)
        y = random.randint(0, superficie.get_height() - 1)
        superficie_estatica.set_at((x, y), (random.randint(200, 255), random.randint(200, 255), random.randint(200, 255)))
    return superficie_estatica

# Função para simular "corte de tela"
def corte_de_tela(superficie):
    if random.random() < 0.005:
        superficie_corte = pygame.Surface(superficie.get_size())
        superficie_corte.fill((0, 0, 0))
        return superficie_corte
    return superficie
