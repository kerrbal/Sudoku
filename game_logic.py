class Sudoku():
    def __init__(self, board):
        one_board = Block(board)
        self.board = one_board.cells



    def print_board(self):
        for row in self.board:
            for cell_object in row:
                
                print(cell_object.value, end = " ")
            print()


    def solve_recursively(self):
        smallest = 10
        smallest_cell = None
        for row in self.board:
            for a_cell in row:
                if a_cell.value != 0:
                    continue
                if len(a_cell.possibilities) == 0:
                    return False
                if len(a_cell.possibilities) < smallest:
                    smallest_cell = a_cell
                    smallest = len(a_cell.possibilities)

        if smallest == 10:
            return True
        
        for number in smallest_cell.possibilities.copy():
            smallest_cell.remove_from_possibilities(number)
            finish = self.solve_recursively()
            if finish:
                return True
            smallest_cell.add_to_possibilities()

    def output_solution(self, mode = "int"):
        return_this = []
        roow = []
        if mode == "int":
            for row in self.board:
                for i in row:
                    roow.append(i.value)
                return_this.append(roow.copy())
                roow.clear()
        elif mode == "str":
            for row in self.board:
                for i in row:
                    roow.append(str(i.value))
                return_this.append(roow.copy())
                roow.clear()
        else:
            print("something wrong")
            return
        return return_this

            
 


class Cell():

    def __init__(self, value, position):
        self.value = value
        self.position = position
        self.horizontal_block = None
        self.vertical_block = None
        self.square_block = None
        self.possibilities = None
        self.original_possibilities = None
        self.used_possibilities = None


    def set_other_features(self, cell_list):
        if self.value != 0:
            return
        

        self.set_blocks(cell_list)
        self.possibilities = self.possibility_list()
        self.original_possibilities = tuple(self.possibilities)
        self.used_possibilities = []


    def set_blocks(self, cell_list):
        self.horizontal_block = self.written_nums(((self.position[0], 0), (self.position[0], 8)), cell_list)
        self.vertical_block = self.written_nums(((0, self.position[1]), (8, self.position[1])), cell_list)
        square_row = 0
        square_col = 0
        if self.position[0]<3:
            square_row = 0
        elif self.position[0]<6:
            square_row = 3
        else:
            square_row = 6
        
        if self.position[1]<3:
            square_col = 0
        elif self.position[1]<6:
            square_col = 3
        else:
            square_col = 6
        self.square_block = self.written_nums(((square_row, square_col), (square_row + 2, square_col + 2)), cell_list)

    def written_nums(self, pos, cell_list):
        the_cells = []
        start = pos[0]
        end = pos[1]
        if start[0] == end[0]:
            #the line is horizontal.
            for i in range(9):
                the_cells.append(cell_list[start[0]][i])
        elif start[1] == end[1]:
            #the line is vertical.
            for i in range(9):
                the_cells.append(cell_list[i][start[1]])

        else:
            #it is square.
            for i in range(3):
                for j in range(3):
                    the_cells.append(cell_list[start[0] + i][start[1] + j])

        return the_cells
    

    def intersect(self, *lists):
        intersection_list = []
        first_list = lists[0]
        value = True
        for i in first_list:
            
            value = True
            for j in range(1, len(lists)):
                if i not in lists[j]:
                    value = False
                    break
            if (value):
                intersection_list.append(i)
        
        return intersection_list

    def difference(self, the_list, target = [1, 2, 3, 4, 5, 6, 7, 8, 9]):
        number_list = [a_cell.value for a_cell in the_list]
        the_difference = []
        for i in target:
            if i not in number_list:

                the_difference.append(i)
        return the_difference

    def possibility_list(self):

        horizontal_possibility = self.difference(self.horizontal_block)
        vertical_possibility = self.difference(self.vertical_block)
        square_possibility = self.difference(self.square_block)

        possibilities = self.intersect(horizontal_possibility, vertical_possibility, square_possibility)


        return possibilities

    def remove_from_possibilities(self, the_number):
        if self.horizontal_block == None:
            print("assigned a value V2")
            return

        corresponding_cells = self.horizontal_block + self.vertical_block + self.square_block
        for a_cell in corresponding_cells:

            if a_cell == self:
                continue
            if a_cell.value != 0:
                continue
            if the_number not in a_cell.original_possibilities:
                continue
            if the_number in a_cell.possibilities:
                a_cell.possibilities.remove(the_number)
            a_cell.used_possibilities.append(the_number)
        self.value = the_number

    def add_to_possibilities(self):
        if self.value == 0:
            print("HATAAAAAAAAAAAAA")
            return

        if self.horizontal_block == None:
            print("hattaaaaaaa2")
            return

        the_value = self.value
        self.value = 0
        corresponding_cells = self.horizontal_block + self.vertical_block + self.square_block

        for cell in corresponding_cells:
            if cell == self:
                continue
            
            if cell.value != 0:
                continue
            if the_value in cell.used_possibilities:
                cell.used_possibilities.remove(the_value)
                if the_value not in cell.possibilities:
                    if cell.used_possibilities.count(the_value) == 0:
                        cell.possibilities.append(the_value)
            

    def __str__(self):
        return str(self.value)

class Block():
    def __init__(self, board):
        self.cells = self.return_cells(board) 
        self.activate_cells()

    def activate_cells(self):
        for row in self.cells:
            for one_cells in row:
                one_cells.set_other_features(self.cells)


    def return_cells(self, board):
        cells = []
        one_row = []
        pos = [0, 0]
        for row in board:
            for element in row:
                element = int(element)
                one_row.append(Cell(element, pos.copy()))
                pos[1] += 1
            cells.append(one_row.copy())
            one_row = []
            pos[1] = 0

            pos[0] += 1
    
        return cells

