import pygame

pygame.init()
win = pygame.display.set_mode((800, 800), pygame.RESIZABLE)
x = pygame.image.load("win_image.png")
x = pygame.transform.scale(x, (400, 400))
win.blit(x, (100, 100))

pygame.display.update()

run = True

previous_screen = win.get_size()

while run:
    for event in pygame.event.get():
        
        if previous_screen != win.get_size():
            win.fill((0, 0, 0))
            win.blit(pygame.transform.scale(x, (win.get_size()[0]/2, win.get_size()[1]/2)), (win.get_size()[0]/8, win.get_size()[1]/8))
            pygame.display.update()

        if event.type == pygame.QUIT:
            run = False

        