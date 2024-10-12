import pygame
import pygame.freetype


pygame.freetype.init()
pygame.init()

win = pygame.display.set_mode((400, 400))

image = pygame.image.load("back.png")
image = pygame.transform.scale(image, (50, 25))

win.blit(image, (100, 100))

pygame.display.update()

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        