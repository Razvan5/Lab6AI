import turtle
from turtle import *

turtle.tracer(1, 0)
turtle_list = []
global chosen_x
global chosen_y
for i in range(0, 9):
    sam = Turtle()
    turtle_list.append(sam)

game_matrix = [
    [1, 1, 1, 1],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [2, 2, 2, 2],
]


def valid_move(piece_x, piece_y, move_x, move_y, current_turn):
    if game_matrix[piece_x][piece_y] != current_turn:
        return False
    if piece_x == move_x and piece_y == move_y:
        return False
    if piece_x > len(game_matrix) or piece_y > len(game_matrix) or move_x > len(game_matrix) or move_y > len(game_matrix):
        return False
    # Enemy or player piece is occupying this move
    if game_matrix[move_x][move_y] != 0:
        return False
    # It can only be 0 for no change in X or 1 for X movement
    if abs(piece_x - move_x) > 1:
        return False
    # It can only be 0 for no change in Y or 1 for Y movement
    if abs(piece_y - move_y) > 1:
        return False

    return True


def pretty_print_color(matrix, reset_turtles):
    speed(30)
    k = 0
    if reset_turtles:
        for t in turtle_list:
            t.clear()
            t.reset()
        return
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] != 0:
                turtle_list[k].shape("circle")
                turtle_list[k].shapesize(5)
                turtle_list[k].penup()
                turtle_list[k].setposition(convert_to_xy(i, j))
                if matrix[i][j] == 1:
                    turtle_list[k].color("blue")
                    if i == chosen_x and j == chosen_y:
                        turtle_list[k].color("purple")
                    k += 1
                if matrix[i][j] == 2:
                    turtle_list[k].color("red")
                    if i == chosen_x and j == chosen_y:
                        turtle_list[k].color("purple")
                    k += 1


def check_winner(matrix):
    if matrix[0] == [2, 2, 2, 2]:
        return 2
    if matrix[3] == [1, 1, 1, 1]:
        return 1
    return 0


def convert_to_ij(x, y):
    i, j = -1, -1

    if 250 > y > 125:
        i = 0
    if 125 > y > 0:
        i = 1
    if 0 > y > -125:
        i = 2
    if -125 > y > -250:
        i = 3

    if 250 > x > 125:
        j = 3
    if 125 > x > 0:
        j = 2
    if 0 > x > -125:
        j = 1
    if -125 > x > -250:
        j = 0

    return i, j


def convert_to_xy(index_i, index_j):
    x, y = -1, -1

    if index_i == 0:
        y = 190
    if index_i == 1:
        y = 63.3
    if index_i == 2:
        y = -63.3
    if index_i == 3:
        y = -190

    if index_j == 0:
        x = -190
    if index_j == 1:
        x = -63.3
    if index_j == 2:
        x = 63.3
    if index_j == 3:
        x = 190

    return x, y


def best_value_function(curr_x, curr_y, next_x, next_y):
    sum_computer = 0
    sum_human = 0
    for i in range(len(game_matrix)):
        for j in range(len(game_matrix[i])):
            if game_matrix[i][j] == 1:
                sum_human += i
            if game_matrix[i][j] == 2:
                sum_computer +=i
    return  sum_computer - sum_human


def transition(x, y, a, b):
    game_matrix[int(a)][int(b)] = game_matrix[int(x)][int(y)]
    game_matrix[int(x)][int(y)] = 0


class Drawer:
    def __init__(self):
        self.first_click = True
        self.no_winner = True
        self.current_turn = 1
        self.x = -1
        self.y = -1
        self.a = -1
        self.b = -1

    def click(self, c_x, c_y):
        if self.first_click:
            global chosen_x
            global chosen_y
            self.x = convert_to_ij(c_x, c_y)[0]
            self.y = convert_to_ij(c_x, c_y)[1]
            self.first_click = False
            chosen_x = self.x
            chosen_y = self.y
            pretty_print_color(game_matrix, False)
        else:
            if self.current_turn == 1:
                if check_winner(game_matrix) == 1:
                    pretty_print_color(game_matrix, True)
                    turtle.bgpic("unu.png")
                    Screen().exitonclick()

                self.a = convert_to_ij(c_x, c_y)[0]
                self.b = convert_to_ij(c_x, c_y)[1]
                print("Turn Player ", self.current_turn)

                if check_winner(game_matrix) == 1:
                    pretty_print_color(game_matrix, True)
                    turtle.bgpic("unu.png")
                    Screen().exitonclick()
                elif valid_move(self.x, self.y, self.a, self.b, self.current_turn):
                    transition(self.x, self.y, self.a, self.b)
                    pretty_print_color(game_matrix, False)
                    self.current_turn = 2
            else:
                if check_winner(game_matrix) == 2:
                    pretty_print_color(game_matrix, True)
                    turtle.bgpic("doi.png")
                    Screen().exitonclick()

                self.a = convert_to_ij(c_x, c_y)[0]
                self.b = convert_to_ij(c_x, c_y)[1]
                print("Turn Player ", self.current_turn)

                if check_winner(game_matrix) == 2:
                    pretty_print_color(game_matrix, True)
                    turtle.bgpic("doi.png")
                    Screen().exitonclick()
                elif valid_move(self.x, self.y, self.a, self.b, self.current_turn):
                    transition(self.x, self.y, self.a, self.b)
                    pretty_print_color(game_matrix, False)
                    self.current_turn = 1

            self.first_click = True
    # print("You clicked:" + str(x) + "," + str(y))
    # print("It converts to:" + str(convert_to_ij(x, y)))
    # print("It converts to:" + str(convert_to_xy((convert_to_ij(x, y))[0], (convert_to_ij(x, y))[1])))


if __name__ == '__main__':

    turtle.bgpic("board.png")
    chosen_x = 1
    chosen_y = 1
    pretty_print_color(game_matrix, False)

    # no_winner = True
    # current_turn = 1
    # while no_winner:
    #     if current_turn == 1:
    #         print("Turn Player 1")
    #
    #         x, y, a, b = input()
    #
    #         while not valid_move(int(x), int(y), int(a), int(b), current_turn):
    #             x, y, a, b = input()
    #
    #         transition(x, y, a, b)
    #
    #         if check_winner(game_matrix) == 1:
    #             pretty_print_color(game_matrix)
    #             print("Player 1 has won!")
    #             no_winner = False
    #         else:
    #             pretty_print_color(game_matrix)
    #             current_turn = 2
    #
    #     else:
    #         print("Turn Player 2")
    #
    #         x, y, a, b = input()
    #         while not valid_move(int(x), int(y), int(a), int(b), current_turn):
    #             x, y, a, b = input()
    #
    #         transition(x, y, a, b)
    #
    #         if check_winner(game_matrix) == 2:
    #             pretty_print_color(game_matrix)
    #             print("Player 2 has won!")
    #             no_winner = False
    #         else:
    #             pretty_print_color(game_matrix)
    #             current_turn = 1
    d = Drawer()
    turtle.onscreenclick(d.click)
    turtle.mainloop()
    turtle.done()
