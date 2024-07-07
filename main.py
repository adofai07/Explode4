import pygame

BD_SIZE = 5
SQ_SIZE = 75

pygame.init()

pygame.display.set_caption('Explode4')
window_surface = pygame.display.set_mode((BD_SIZE * SQ_SIZE, BD_SIZE * SQ_SIZE))

background = pygame.Surface((BD_SIZE * SQ_SIZE, BD_SIZE * SQ_SIZE))
background.fill(pygame.Color('#000000'))

is_running = True

while is_running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

    window_surface.blit(background, (0, 0))

    pygame.display.update()