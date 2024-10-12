import pygame
import game_logic
import random
pygame.init()

class Game:
    def __init__(self, board, hint_num = 3):
        if not (self.board_test):
            print("board is not valid.")
            quit()
        
        self.hint_num = hint_num
        self.actions = []
        self.board_info = board
        solution = game_logic.Sudoku(board)
        solution.solve_recursively()
        self.solution = solution.output_solution("str")
        self.deel_board = game_logic.Sudoku(board).board
        self.wrong_guesses = []
        self.game_situation = "notfinished"
        self.empty_cells = self.get_empty_cell_num()
        self.empty_cell_num = len(self.empty_cells)
        self.load_images()
        self.init_the_game()
        self.load_the_board()
        self.load_cells()
        self.create_game_visual()
        self.run()
    def get_empty_cell_num(self):
        empty_cells = []
        for i in range(9):
            for j in range(9):
                if self.board_info[i][j] == "0":
                    empty_cells.append([i, j])
        return empty_cells.copy()
    def load_images(self):
        self.soft_surface = pygame.image.load("soft.png")
        self.zero_image = pygame.image.load("win_image.png")
        self.images = [pygame.image.load("win_image" + str(i) + ".png") for i in range(1, 10)]
        self.back = pygame.image.load("back.png")
        self.hint = pygame.image.load("hint.png")

    def init_the_game(self):
        self.win = pygame.display.set_mode((600, 600))
        self.set_resolution(self.win.get_size())

    def load_the_board(self):
        win_x = self.win.get_size()[0]
        win_y = self.win.get_size()[1]
        self.board = pygame.Surface((win_x*0.75, win_y*0.75))

    def load_cells(self):
        board_x = self.board.get_size()[0]
        board_y = self.board.get_size()[1]
        #106x is the width of the board. and x is the interval between cells.
        #10x is the width of the board. The same holds for the y too.

        cell_width = 10*self.x
        cell_height = 10*self.y
        self.cells = [pygame.Surface((cell_width, cell_height)) for i in range(81)]
        self.cells_blits_info = self.get_blits_info()


    def get_blits_info(self):
        blits_info = []

        blank_space_x = self.x
        blank_space_y = self.y
        image_space_x = self.x * 10
        image_space_y = self.y * 10

        self.x_positions = []
        self.y_positions = []

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
        
        

                blits_info.append((self.cells[i*9 + j], (x_alignment, y_alignment)))
                if i == 0:
                    self.x_positions.append(self.win.get_size()[0]*0.125 + x_alignment)
                if j == 0:
                    self.y_positions.append(self.win.get_size()[1]*0.125 + y_alignment)
        return blits_info

    #sets minimum space, and images
    def set_resolution(self, resolution):
        board_x = resolution[0]*0.75
        image_x = board_x/10.6
        board_y = resolution[1]*0.75
        image_y = board_y/10.6
        self.x = image_x / 10
        self.y = image_y / 10
        self.zero_image = pygame.transform.scale(self.zero_image, (image_x, image_y))
        self.soft_surface = pygame.transform.scale(self.soft_surface, resolution)
        self.back = pygame.transform.scale(self.back, (120, 60))
        self.hint = pygame.transform.scale(self.hint, (120, 60))
        for i in range(len(self.images)):
            self.images[i] = pygame.transform.scale(self.images[i], (image_x, image_y))
        

    def board_test(self):
        includes = list("0123456789")
        if type(self.board) == list and len(self.board) == 9:
            for i in range(9):
                if type(self.board) == list and len(self.board[i]) == 9:
                    continue
                else:
                    return False
        else:
            return False
        
        for row in self.board:
            for i in row:
                if i in includes:
                    continue
                else:
                    return False
        
        return True

    #Just creating the visual
    def create_game_visual(self):
        self.win.fill((0, 0, 0))
        self.win.blit(self.soft_surface, (0, 0))
        self.board.fill((185,226,245))
        self.paste_pictures()
        self.board.blits(self.cells_blits_info)
        self.win.blit(self.board, (self.win.get_size()[0]*0.125, self.win.get_size()[1]*0.125))
        self.win.blit(self.back, (600*0.125, 540))
        x = 600 - 600*0.125 - 120
        self.win.blit(self.hint, (x, 540))

    def paste_pictures(self):
        cell_index = 0
        self.occupied_cells = []
        row_num = 0
        for row in self.board_info:
            for cell in row:
                if cell == "0":
                    self.cells[row_num*9 + cell_index].blit(self.zero_image, (0, 0))
                else:
                    self.cells[row_num*9 + cell_index].blit(self.images[int(cell) - 1], (0, 0))
                    self.occupied_cells.append([cell_index, row_num])
                cell_index += 1
            cell_index = 0
            row_num += 1

    def get_cell_index(self, pos):
        x_index = pos[0]
        y_index = pos[1]
        image_space_x = self.x * 10
        image_space_y = self.y * 10
        return_x = -1
        return_y = -1
        for i in range(8, -1, -1):
            if x_index >= self.x_positions[i]:
                if x_index <= self.x_positions[i] + image_space_x:
                    return_x = i
                    break
        for i in range(8, -1, -1):
            if y_index >= self.y_positions[i]:
                if y_index <= self.y_positions[i] + image_space_y:
                    return_y = i
                    break
        
        if 600*0.125<=x_index<=600*0.125 + 120:
            if 540<=y_index<=600:
                return_x = -2
                return_y = -2

        x = 600 - 600*0.125 - 120
        if x <=x_index<=x + 120:
            if 540<=y_index<=600:
                return_x = -3
                return_y = -3


        return return_x, return_y
    
    def update_the_cell(self, index, num, is_hint = False):
        cell_index = index[1]*9 + index[0]




        self.cells[cell_index].fill((0, 0, 0))
        self.cells[cell_index].blit(self.images[int(num) - 1], (0, 0))

        self.board.blit(self.cells[cell_index], (self.x_positions[index[0]] - self.win.get_size()[0]*0.125, self.y_positions[index[1]] - self.win.get_size()[1]*0.125))

        self.win.blit(self.board, (self.win.get_size()[0]*0.125, self.win.get_size()[1]*0.125))

        self.rule_violation([index[1], index[0]], num)

        

        pygame.display.update()
        if self.board_info[index[1]][index[0]] == "0":
            self.empty_cell_num -= 1
        self.board_info[index[1]][index[0]] = str(num)
        if not is_hint:
            self.actions.append([[index[1], index[0]], str(num)])
    
    def run(self):
        command = True
        pygame.display.flip()
        true_cell = False
        
        while command:
            
            if self.empty_cell_num == 0:
                command = False
                
                self.game_situation = "lose"
                if len(self.wrong_guesses) == 0:
                    self.game_situation = "win"
                print(self.game_situation)
                continue
            
            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    command = False



                if event.type == pygame.MOUSEBUTTONDOWN:
                    index = self.get_cell_index(event.dict["pos"])
                    if index[0] == -1:
                        true_cell = False
                    else:
                        true_cell = True
                    if index[0] == -2:
                        self.go_back()
                    
                    if index[0] == -3:
                        self.give_hint()
                if event.type == pygame.KEYDOWN:
                    if not true_cell:
                        continue
                    the_key = event.dict["unicode"]
                    if list(index) in self.occupied_cells:
                        continue
                    if the_key not in list("123456789"):
                        self.remove_from_board(index)

                    else:
                        self.update_the_cell(index, the_key)

                

    def remove_from_board(self, index):
        _81index = index[1] * 9 + index[0]
        original_index = [index[1], index[0]]
        if self.board_info[index[1]][index[0]] != "0":
            self.empty_cell_num += 1
        self.board_info[index[1]][index[0]] = "0"
        self.cells[_81index].blit(self.zero_image, (0, 0))
        self.board.blit(self.cells[_81index], (self.x_positions[index[0]] - self.win.get_size()[0]*0.125, self.y_positions[index[1]] - self.win.get_size()[1]*0.125))
        self.win.blit(self.board, (self.win.get_size()[0]*0.125, self.win.get_size()[1]*0.125))

        if original_index in self.wrong_guesses:
            self.wrong_guesses.remove(original_index)

        pygame.display.update()
        
        self.actions.append([[index[1], index[0]], "0"])

    def rule_violation(self, cell_index, target_num):

        if int(target_num) not in self.deel_board[cell_index[0]][cell_index[1]].possibilities:

            self.wrong_guesses.append(cell_index)

    def go_back(self):
        if len(self.actions) == 0:
            return
        x = self.actions[-1][0][1]
        y = self.actions[-1][0][0]
        cell = self.cells[y * 9 + x]
        cell.blit(self.zero_image, (0, 0))
        x = self.actions[-1][0][1]
        y = self.actions[-1][0][0]
        if len(self.actions) > 1:
            if self.actions[-1][0] == self.actions[-2][0]:
                
                if self.actions[-1][1] != "0" and self.actions[-2][1] == "0":
                    self.empty_cell_num += 1
                elif self.actions[-1][1] == "0" and self.actions[-2][1] != "0":
                    self.empty_cell_num -= 1
                    cell.blit(self.images[int(self.actions[-2][1]) - 1], (0, 0))
                self.board_info[y][x] = self.actions[-2][1]
            else:
                if self.actions[-1][1] != "0":
                    self.empty_cell_num += 1
        else:
            if self.actions[-1][1] != "0":
                self.empty_cell_num += 1
        self.board.blit(cell, (self.x_positions[x] - 600*0.125, self.y_positions[y] - 600*0.125))
        self.win.blit(self.board, (600*0.125, 600*0.125))
        pygame.display.update()
        self.actions = self.actions[:-1]

    def give_hint(self):
        if self.hint_num<=0:
            print("no more hint!")
            return
        random_index = random.randint(0, self.empty_cell_num - 1)
        row_num = self.empty_cells[random_index][0]
        col_num = self.empty_cells[random_index][1]

        true_value = self.solution[row_num][col_num]
        self.update_the_cell([col_num, row_num], true_value, True)
        self.hint_num -= 1
        

    
    def game_over(self):
        if empty_cell_num == 0:
            return True
        return False
        




board = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]
for row in board:
    for i in range(9):
        row[i] = str(row[i])


sud1 = Game(board)