import pygame

pygame.init()

def change_resolution(resolution):

    for i in range(81):
        surfaces[i] = pygame.transform.scale(surfaces[i], resolution)
    for i in range(9):
        image_surfaces[i] = pygame.transform.scale(image_surfaces[i], resolution)

def determine_cell(pos):
    x_index = pos[0]
    y_index = pos[1]
    return_x = -1
    return_y = -1
    for i in range(8, -1, -1):
        if x_index >= x_positions[i]:
            if x_index <= x_positions[i] + image_space_x:
                return_x = i
                break
    
    for i in range(8, -1, -1):
        if y_index >= y_positions[i]:
            if y_index <= y_positions[i] + image_space_y:
                return_y = i
                break

    return return_x, return_y
    

def init_sudoku(nums):
    if len(nums) == 0:
        for i in surfaces:
            i.blit(blank_image, (0, 0))

    row_num = 0
    col_num = 0

    for row in nums:
        for cell in row:
            if cell == "0":
                surfaces[row_num*9 + col_num].blit(blank_image, (0, 0))
            else:
                surfaces[row_num*9 + col_num].blit(image_surfaces[int(cell) - 1], (0, 0))

            col_num += 1
        row_num +=1
        col_num = 0


blank_image = pygame.image.load("win_image.png")
image_surfaces = [pygame.image.load("win_image" + str(i) + ".png") for i in range(1, 10)]


win = pygame.display.set_mode((600, 600))

soft_surface = pygame.transform.scale(pygame.image.load("soft.png"), (600, 600))
win.blit(soft_surface, (0, 0))


board = pygame.Surface((600*0.75, 600*0.75))
board.fill((185,226,245))
blank_space_x = board.get_size()[0]/106
blank_space_y = board.get_size()[1]/106
image_space_x = blank_space_x * 10
image_space_y = blank_space_y * 10


surfaces = [pygame.Surface((600, 600)) for i in range(81)]
init_sudoku([])
x_positions = []
y_positions = []
change_resolution((image_space_x, image_space_y))


blits_info = []
for i in range(9):
    for j in range(9):

        x_alignment = blank_space_x * 3 + blank_space_x * j + image_space_x * j
        y_alignment = blank_space_y * 3 + blank_space_y * i + image_space_y * i
        if j >= 6:
            x_alignment += blank_space_x * 2
        elif j >= 3:
            x_alignment += blank_space_x

        if i >= 6:
            y_alignment += blank_space_y * 2
        elif i >= 3:
            y_alignment += blank_space_y
        
        

        blits_info.append((surfaces[i*9 + j], (x_alignment, y_alignment)))
        if i == 0:
            x_positions.append(600*0.125 + x_alignment)
        if j == 0:
            y_positions.append(600*0.125 + y_alignment)

board.blits(blits_info)
win.blit(board, (600*0.125, 600*0.125))

pygame.display.update()

run = True
key_on = False
search = list("123456789")
key = -1

while run:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.dict["pos"]
            corresponding_cell_indexes = determine_cell(pos)
            if corresponding_cell_indexes[0] == -1 or corresponding_cell_indexes[1] == -1:
                print("not in the cell.")
                key_on = False
            else:
                key_on = True
        
        if key_on:
            if event.type == pygame.KEYDOWN:
                key = event.dict["unicode"]
                if key in search:
                    target_index = corresponding_cell_indexes[1] * 9 + corresponding_cell_indexes[0]

                    surfaces[target_index].fill((0, 0, 0))
                    surfaces[target_index].blit(image_surfaces[int(key) - 1], (17, 59))
                    board.fill((185,226,245))
                    board.blits(blits_info)
                    win.blit(soft_surface, (0, 0))
                    win.blit(board, (600*0.125 + 10, 600*0.125 + 50))
            key = -1



        
        pygame.time.delay(10)

        pygame.display.flip()