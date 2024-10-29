import pygame

class Inventario:
    def __init__(self):
        self.items = []  # Lista para armazenar itens
        self.font = pygame.font.Font(None, 36)

        # Dicionário de sprites dos itens
        self.item_images = {
            "fio": pygame.image.load("assets/fio.png"),  # Adicionar sprite para o fio
            "chave": pygame.image.load("assets/chave.png"),
            "dedo": pygame.image.load("assets/dedo.png")
        }

        # Carregar imagem de fundo para o inventário
        self.background_image = pygame.image.load("assets/inventario_bg.png")  # Sprite de fundo do inventário

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)

    def draw(self, surface):
        # Desenha o inventário no canto superior esquerdo da tela
        inventory_rect = pygame.Rect(10, 10, 220, 100 + len(self.items) * 50)  # Aumentar altura dinamicamente

        # Desenhar a imagem de fundo do inventário
        surface.blit(self.background_image, inventory_rect.topleft)

        # Desenha os itens no inventário (imagens, se disponíveis)
        for i, item in enumerate(self.items):
            if item in self.item_images:
                # Desenha a imagem do item
                surface.blit(self.item_images[item], (20, 20 + i * 50))
# Certifique-se de que a imagem de fundo "inventario_bg.png" está na pasta "assets"
