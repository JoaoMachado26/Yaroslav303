import pygame
import sys
from inventario import Inventario
from telas.menu import Menu
from telas.area1 import AreaUm
from telas.area2 import AreaDois
from telas.area3 import AreaTres
from telas.area4 import AreaQuatro
from telas.fim import Fim
from filtro import adicionar_estatica, adicionar_ruido, corte_de_tela, aplicar_distorcao
import time

pygame.init()

# Inicializa o mixer de som
pygame.mixer.init()

largura = 1000
altura = 800
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Yaroslav 303")
ultimo_tempo_atualizacao = time.time()

visao = 0  # Controla qual área está sendo exibida

# Carregar a imagem da vinheta
vinheta = pygame.image.load("assets/vinheta.png").convert_alpha()
vinheta.set_alpha(128)  # Define a transparência da vinheta para 50%

# Carregar a música e configurá-la para tocar em loop
pygame.mixer.music.load("assets/musica.mp3")

def tocar_musica():
    """Inicia a música em loop"""
    pygame.mixer.music.play(-1)  # -1 faz com que a música toque em loop infinito

def parar_musica():
    """Para a música"""
    pygame.mixer.music.stop()

def trocar_cena(cena, visao, area1, area2, area3, area4, fim):
    if cena.fim:  # Verifica se o jogo chegou ao fim
        return fim  # Se chegou ao fim, troca para a cena final
    else:
        # Controla a troca de áreas com base na variável 'visao'
        if visao == 0:
            return area1
        elif visao == 1:
            return area2
        elif visao == 2:
            return area3
        elif visao == 3:
            return area4

def reiniciar_cenas(inventario):
    """Reinicializa todas as cenas"""
    area1 = AreaUm(inventario)
    area2 = AreaDois(inventario)
    area3 = AreaTres(inventario)
    area4 = AreaQuatro(inventario)
    fim = Fim(inventario)
    menu = Menu(inventario)
    return area1, area2, area3, area4, fim, menu

def aplicar_filtros(surface):
    surface = adicionar_estatica(surface)
    surface = adicionar_ruido(surface)
    surface = corte_de_tela(surface)
    return surface

def main():
    global visao, ultimo_tempo_atualizacao

    inventario = Inventario()

    # Inicialização das cenas
    menu = Menu(inventario)
    area1, area2, area3, area4, fim, menu = reiniciar_cenas(inventario)

    cena_ativa = menu  # Cena inicial

    # Toca a música ao iniciar o jogo, exceto na cena 'Fim'
    tocar_musica()

    while True:
        eventos = pygame.event.get()
        for event in eventos:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        teclas_pressionadas = pygame.key.get_pressed()

        # Muda a visão ao pressionar as setas esquerda e direita
        if teclas_pressionadas[pygame.K_RIGHT]:
            visao = (visao + 1) % 4
            cena_ativa = trocar_cena(cena_ativa, visao, area1, area2, area3, area4, fim)
            pygame.time.wait(500)

        if teclas_pressionadas[pygame.K_LEFT]:
            visao = (visao - 1) % 4
            cena_ativa = trocar_cena(cena_ativa, visao, area1, area2, area3, area4, fim)
            pygame.time.wait(500)

        # Processa a cena atual
        cena_ativa.processar_entrada(eventos, teclas_pressionadas)
        cena_ativa.atualizar()
        cena_ativa.desenhar(tela)

        # Aplica os filtros se estiver nas áreas 1, 2, 3 ou 4
        if isinstance(cena_ativa, (AreaUm, AreaDois, AreaTres, AreaQuatro)):
            tela_com_filtros = aplicar_filtros(tela.copy())
            tela_com_filtros, ultimo_tempo_atualizacao = aplicar_distorcao(tela_com_filtros, ultimo_tempo_atualizacao)
            tela.blit(tela_com_filtros, (0, 0))
            # Desenha a vinheta sobre a tela
            tela.blit(vinheta, (0, 0))
        else:
            tela.blit(tela, (0, 0))

        # Verifica se o jogo está em andamento
        if cena_ativa.play:
            if cena_ativa == fim:  # Se a cena atual é o fim
                parar_musica()  # Para a música
                fim.processar_entrada(eventos, teclas_pressionadas)  # Processa a entrada na cena final
                fim.atualizar()
                fim.desenhar(tela)

                if fim.retorno:  # Se a cena final terminou, volta ao menu
                    # Reinicia todas as cenas
                    area1, area2, area3, area4, fim, menu = reiniciar_cenas(inventario)
                    cena_ativa = menu
                    menu.play = False
                    fim.retorno = False  # Reseta o retorno para futuras execuções
                    tocar_musica()  # Reinicia a música ao voltar ao menu
            else:
                # Atualiza a cena com base na visão atual
                cena_ativa = trocar_cena(cena_ativa, visao, area1, area2, area3, area4, fim)

        pygame.display.flip()

if __name__ == "__main__":
    main()
