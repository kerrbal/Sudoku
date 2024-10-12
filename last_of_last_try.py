import pygame

pygame.init()

win = pygame.display.set_mode((600, 600))
a = pygame.Surface((300, 300))
a.fill((244, 0, 0))
b = pygame.Surface((300, 300))
b.fill((0, 200, 0))
blits_info = [(a, (0, 0)), (b, (300, 300))]
win.blits(blits_info)

pygame.display.update()

run = True

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False