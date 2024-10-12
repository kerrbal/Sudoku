import pygame
def determine_mouse(event):
    pos = event["pos"]
    x = pos[0]
    y = pos[1]
    if x <= 75 and y <= 123:
        return [0, 0]


def change_a_number(the_pos, the_num):
    
    text = comic_font.render(the_num, False, [122, 122, 122], [255,255,204])
    rect = text.get_rect(topleft = (0, 0))
    win.blit(text, rect)



pygame.init()
win = pygame.display.set_mode((1000, 1000))
pygame.display.set_caption("Sudoku")
comic_path = r"C:\Users\addad\Desktop\fonts for sudoku\Action_Man.ttf"
aller_path = r"C:\Users\addad\Desktop\fonts for sudoku\Aller_Bd.ttf"
opensans_path = r"C:\Users\addad\Desktop\fonts for sudoku\OpenSans-Bold.ttf"
comic_font = pygame.font.Font(comic_path, 150)
aller_font = pygame.font.Font(aller_path, 30)
opensans_font = pygame.font.Font(opensans_path, 30),
NUM_VARS = "0123456789"
NUM_VAR = "0"
text = comic_font.render(NUM_VAR, False, [122, 122, 122], [255,255,204])
print(text.get_size())

textrect = text.get_rect(topleft = (0, 0))
print(textrect.size)

original_rect = pygame.Rect(125, 125, 750, 750)
original_rect.fill()
win.fill((255, 204, 204))
win.blit(text, textrect)
pygame.display.update()
run = True
while run:
    pygame.time.delay(500)
    a = pygame.event.get()
    for event in a:
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(event.type)
            print(event.dict)
            if event.dict["button"] == 1:
                cell_pos = determine_mouse(event.dict)
        if event.type == pygame.KEYDOWN:
            key = event.dict["unicode"]
            print(event)
            if key in NUM_VARS:
                NUM_VAR = key
            if cell_pos:
                change_a_number(cell_pos, NUM_VAR)
    pygame.display.update()


