import pygame   

pygame.init()

# Cores
yellow = (255, 255, 0)
black = (0, 0, 0)
blue = (0, 0, 255)
invisible_color = (0, 0, 0)  # Parede Invisível

# Classe para criar as paredes
class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x, y))

# Criar os blocos
class Block(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(black) 
        self.image.set_colorkey(black) 
        pygame.draw.ellipse(self.image, color, [0, 0, width, height])
        self.rect = self.image.get_rect()

# Classe para criar os bonecos
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, sprite):
        super().__init__()
        self.image = pygame.image.load(sprite).convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, change_x, change_y, walls):
        # Movimentação do jogador
        x, y = self.rect.topleft
        self.rect.x += change_x
        if pygame.sprite.spritecollide(self, walls, False):
            self.rect.x = x
        self.rect.y += change_y
        if pygame.sprite.spritecollide(self, walls, False):
            self.rect.y = y

# Configuração da tela
screen_size = (606, 606)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('Cigarrinho Pacman')

# Sprite do boneco
Cigarrinho = pygame.image.load('Cigarribia.jpg')
pygame.display.set_icon(Cigarrinho)

# Configurar as paredes
def setup_walls(sprites_list):
    wall_list = pygame.sprite.Group()

    walls = [
        [0, 0, 6, 600],
        [0, 0, 600, 6],  
        [0, 600, 606, 6], 
        [600, 0, 6, 606], 
    ]

    # Criar as paredes e colocar na lista dos sprites
    for item in walls:
        wall = Wall(item[0], item[1], item[2], item[3], blue)
        wall_list.add(wall)
        sprites_list.add(wall)

    return wall_list

# Portão 
def _gate(sprites_list):
    gate = pygame.sprite.Group()
    invisible_wall = Wall(282, 242, 42, 2, invisible_color)
    gate.add(invisible_wall)
    sprites_list.add(invisible_wall)
    return gate

def run():
    sprites_list = pygame.sprite.Group()
    wall_list = setup_walls(sprites_list)
    gate = _gate(sprites_list)

    # Criar o boneco
    Cigarrinho = Player(303 - 16, (7 * 60) + 19, "Cigarribia.jpg")
    sprites_list.add(Cigarrinho)

    # Criar as bolinhas
    block_list = pygame.sprite.Group()
    for line in range(19):
        for column in range(19):
            if (line == 7 or line == 8) and (column in [8, 9, 10]):
                continue
            block = Block(yellow, 4, 4)
            block.rect.x = (30 * column + 6) + 26
            block.rect.y = (30 * line + 6) + 26
            block_list.add(block)
            sprites_list.add(block)

    clock = pygame.time.Clock()
    done = False
    change_x = 0
    change_y = 0

    while not done:
        # Veriicar os eventos do jogo
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    change_x = -5
                if event.key == pygame.K_RIGHT:
                    change_x = 5
                if event.key == pygame.K_UP:
                    change_y = -5
                if event.key == pygame.K_DOWN:
                    change_y = 5
            if event.type == pygame.KEYUP:
                if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                    change_x = 0
                if event.key in (pygame.K_UP, pygame.K_DOWN)

        # Atualizar o boneco
        Cigarrinho.update(change_x, change_y, wall_list)

        screen.fill(black)

        # Desenhar os sprites
        sprites_list.draw(screen)

        # Atualizar a tela
        pygame.display.flip()

        # Cravar em 60 FPS
        clock.tick(60)

    pygame.quit()

run()