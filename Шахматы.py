import tkinter as tk
from tkinter import Button

game = tk.Tk()
game.title("Шахматы")
game.geometry('640x640')

canvas = tk.Canvas(game, bg='black', width=80 * 8, height=80 * 8)

WHITE = 1
BLACK = 2
King_b_flag = 0
King_w_flag = 0
Rook_b_flag1 = 0
Rook_w_flag1 = 0
Rook_b_flag2 = 0
Rook_w_flag2 = 0
oval_flag = 0


def correct_coords(row, col):
    return 0 <= row < 8 and 0 <= col < 8


class Figure:
    def __init__(self, color, image, name):
        self.image = image
        self.color = color
        self.name = name

    def get_color(self):
        return self.color

    def get_image(self):
        return self.image

    def get_name(self):
        return self.name


class Pawn(Figure):
    def char(self):
        return 'P'

    def can_move(self, board, row, col, row1, col1):
        if col != col1:
            return False
        if self.color == WHITE:
            direction = 1
            start_row = 1
        else:
            direction = -1
            start_row = 6
        if row + direction == row1:
            return True
        if row == start_row and row + direction * 2 == row1 and \
                board.field[row + direction][col] is None:
            return True
        return False

    def can_attack(self, board, row, col, row1, col1):
        if self.color == WHITE:
            direction = 1
        else:
            direction = -1
        return row + direction == row1 and abs(col - col1) == 1


class Rook(Figure):
    def char(self):
        return "R"

    def can_move(self, board, row, col, row1, col1):
        global Rook_b_flag1
        global Rook_w_flag1
        global Rook_b_flag2
        global Rook_w_flag2

        if row != row1 and col != col1:
            return False
        if col == col1:
            step = 1 if row1 >= row else -1
            for r in range(row + step, row1 - 2 * step, step):
                if not (board.get_piece(r, col) is None):
                    return False
        elif row == row1:
            step = 1 if col1 >= col else -1
            for c in range(col + step, col1, step):
                if not (board.get_piece(row, c) is None):
                    return False
        return True

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)


class Knight(Figure):
    def char(self):
        return 'N'

    def can_move(self, board, row, col, row1, col1):
        if row == row1 and col == col1:
            return False
        if not correct_coords(row1, col1):
            return False
        if row + abs(row - row1) == row + 2 and \
                col - abs(col - col1) == col - 1:
            return True
        elif row + abs(row - row1) == row + 1 and \
                col - abs(col - col1) == col - 2:
            return True
        elif row + abs(row - row1) == row + 2 and \
                col + abs(col - col1) == col + 1:
            return True
        elif row + abs(row - row1) == row + 1 and \
                col + abs(col - col1) == col + 2:
            return True
        elif row - abs(row - row1) == row - 1 and \
                col - abs(col - col1) == col - 2:
            return True
        elif row - abs(row - row1) == row - 2 and \
                col - abs(col - col1) == col - 1:
            return True
        elif row - abs(row - row1) == row - 1 and \
                col + abs(col - col1) == col + 2:
            return True
        elif row - abs(row - row1) == row - 2 and \
                col + abs(col - col1) == col + 1:
            return True
        return False

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)


class Bishop(Figure):
    def char(self):
        return 'B'

    def can_move(self, board, row, col, row1, col1):
        if row == row1 and col == col1:
            return False
        if not correct_coords(row1, col1):
            return False
        if abs(row - row1) != abs(col - col1):
            return False
        step = 1 if row1 > row else -1
        step2 = 1 if col1 > col else -1
        for r in range(row + step, row1 - 2, step):
            for c in range(col + step2, col, step2):
                if not (board.get_piece(r, c) is None):
                    return False
        return True

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)


class Queen(Figure):
    def char(self):
        return 'Q'

    def can_move(self, board, row, col, row1, col1):
        if row == row1 and col == col1:
            return False
        if not correct_coords(row1, col1):
            return False
        if abs(row - row1) == abs(col - col1):
            step = 1 if row1 > row else -1
            step2 = 1 if col1 > col else -1
            for r in range(row + step, row1 - 2, step):
                for c in range(col + step2, col, step2):
                    if not (board.get_piece(r, c) is None):
                        return False
            return True
        else:
            if row != row1 and col != col1:
                return False
            step = 1 if row1 >= row else -1
            for r in range(row + step, row1, step):
                if not (board.get_piece(r, col) is None):
                    return False
            step = 1 if col1 >= col else -1
            for c in range(col + step, col1, step):
                if not (board.get_piece(row, c) is None):
                    return False
            return True

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)


class King(Figure):
    def char(self):
        return 'K'

    def can_move(self, board, row, col, row1, col1):
        global King_w_flag
        global King_b_flag
        if row == row1 and col == col1:
            return False
        if not correct_coords(row1, col1):
            return False

        # проверка на ладью и ферзя

        for r in range(row1 + 1, 8, 1):
            if type(board.get_piece(r, col1)) is Rook and \
                    board.get_piece(r, col1).get_color() != board.current_player_color() or \
                    type(board.get_piece(r, col1)) is Queen and \
                    board.get_piece(r, col1).get_color() != board.current_player_color():
                return False
            elif board.get_piece(r, col1) is not None:
                break
        for c in range(col1 + 1, 8, 1):
            if type(board.get_piece(row1, c)) is Rook and \
                    board.get_piece(row1, c).get_color() != board.current_player_color() or \
                    type(board.get_piece(row1, c)) is Queen and \
                    board.get_piece(row1, c).get_color() != board.current_player_color():
                return False
            elif board.get_piece(row1, c) is not None:
                break
        for r in range(row1 - 1, -1, -1):
            if type(board.get_piece(r, col1)) is Rook and \
                    board.get_piece(r, col1).get_color() != board.current_player_color() or \
                    type(board.get_piece(r, col1)) is Queen and \
                    board.get_piece(r, col1).get_color() != board.current_player_color():
                return False
            elif board.get_piece(r, col1) is not None:
                break
        for c in range(col1 - 1, -1, -1):
            if type(board.get_piece(row1, c)) is Rook and \
                    board.get_piece(row1, c).get_color() != board.current_player_color() or \
                    type(board.get_piece(row1, c)) is Queen and \
                    board.get_piece(row1, c).get_color() != board.current_player_color():
                return False
            elif board.get_piece(row1, c) is not None:
                break

        # проверка на коня

        if correct_coords(row1 + 2, col1 - 1) and \
                type(board.get_piece(row1 + 2, col1 - 1)) is \
                Knight and \
                board.get_piece(row1 + 2, col1 - 1).get_color() != board.current_player_color():
            return False
        elif correct_coords(row1 + 1, col1 - 2) and \
                type(board.get_piece(row1 + 1, col1 - 2)) is \
                Knight and \
                board.get_piece(row1 + 1, col1 - 2).get_color() != board.current_player_color():
            return False
        elif correct_coords(row1 + 2, col1 + 1) and \
                type(board.get_piece(row1 + 2, col1 + 1)) is \
                Knight and \
                board.get_piece(row1 + 2, col1 + 1).get_color() != board.current_player_color():
            return False
        elif correct_coords(row1 + 1, col1 + 2) and \
                type(board.get_piece(row1 + 1, col1 + 2)) is \
                Knight and \
                board.get_piece(row1 + 1, col1 + 2).get_color() != board.current_player_color():
            return False
        elif correct_coords(row1 - 1, col1 - 2) and \
                type(board.get_piece(row1 - 1, col1 - 2)) is \
                Knight and \
                board.get_piece(row1 - 1, col1 - 2).get_color() != board.current_player_color():
            return False
        elif correct_coords(row1 - 2, col1 + 1) and \
                type(board.get_piece(row1 - 2, col1 + 1)) is \
                Knight and \
                board.get_piece(row1 - 2, col1 + 1).get_color() != board.current_player_color():
            return False
        elif correct_coords(row1 - 1, col1 + 2) and \
                type(board.get_piece(row1 - 1, col1 + 2)) is \
                Knight and \
                board.get_piece(row1 - 1, col1 + 2).get_color() != board.current_player_color():
            return False
        elif correct_coords(row1 - 2, col1 - 1) and \
                type(board.get_piece(row1 - 2, col1 - 1)) is \
                Knight and \
                board.get_piece(row1 - 2, col1 - 1).get_color() != board.current_player_color():
            return False

        # проверка на слона и ферзя
        c = col1 + 1
        for r in range(row1 + 1, 8, 1):
            if correct_coords(r, c) and type(board.get_piece(r, c)) is Bishop and \
                    board.get_piece(r, c).get_color() != board.current_player_color() or \
                    correct_coords(r, c) and type(board.get_piece(r, c)) is Queen and \
                    board.get_piece(r, c).get_color() != board.current_player_color():
                return False
            elif correct_coords(r, c) and board.get_piece(r, c) is not None:
                break
            c += 1

        c = col1 + 1
        for r in range(row1 + 1, 8, 1):
            if correct_coords(r, c) and type(board.get_piece(r, c)) is Bishop and \
                    board.get_piece(r, c).get_color() != board.current_player_color() or \
                    correct_coords(r, c) and type(board.get_piece(r, c)) is Queen and \
                    board.get_piece(r, c).get_color() != board.current_player_color():
                return False
            elif correct_coords(r, c) and board.get_piece(r, c) is not None:
                break
            c -= 1

        c = col1 + 1
        for r in range(row1 - 1, -1, -1):
            if correct_coords(r, c) and type(board.get_piece(r, c)) is Bishop and \
                    board.get_piece(r, c).get_color() != board.current_player_color() or \
                    correct_coords(r, c) and type(board.get_piece(r, c)) is Queen and \
                    board.get_piece(r, c).get_color() != board.current_player_color():
                return False
            elif correct_coords(r, c) and board.get_piece(r, c) is not None:
                break
            c += 1

        c = col1 + 1
        for r in range(row1 - 1, -1, -1):
            if correct_coords(r, c) and type(board.get_piece(r, c)) is Bishop and \
                    board.get_piece(r, c).get_color() != board.current_player_color() or \
                    correct_coords(r, c) and type(board.get_piece(r, c)) is Queen and \
                    board.get_piece(r, c).get_color() != board.current_player_color():
                return False
            elif correct_coords(r, c) and board.get_piece(r, c) is not None:
                break
            c -= 1

        # проверка на пешку

        if board.current_player_color() == WHITE:
            if correct_coords(row1 + 1, col1 + 1) and \
                    type(board.get_piece(row1 + 1, col1 + 1)) is Pawn and \
                    board.get_piece(row1 + 1, col1 + 1).get_color() != board.current_player_color():
                return False
            if correct_coords(row1 + 1, col1 - 1) and \
                    type(board.get_piece(row1 + 1, col1 - 1)) is Pawn and \
                    board.get_piece(row1 + 1, col1 - 1).get_color() != board.current_player_color():
                return False
        else:
            if correct_coords(row1 - 1, col1 + 1) and \
                    type(board.get_piece(row1 - 1, col1 + 1)) is Pawn and \
                    board.get_piece(row1 - 1, col1 + 1).get_color() != board.current_player_color():
                return False
            if correct_coords(row1 - 1, col1 - 1) and \
                    type(board.get_piece(row1 - 1, col1 - 1)) is Pawn and \
                    board.get_piece(row1 - 1, col1 - 1).get_color() != board.current_player_color():
                return False

        # проверка на короля

        for c in range(col1 - 1, col1 + 2):
            if correct_coords(row1 + 1, c) and \
                    type(board.get_piece(row1 + 1, c)) is King and \
                    board.get_piece(row1 + 1, c).get_color() != board.current_player_color():
                return False
        for c in range(col1 - 1, col1 + 2):
            if correct_coords(row1 - 1, c) and \
                    type(board.get_piece(row1 - 1, c)) is King and \
                    board.get_piece(row1 - 1, c).get_color() != board.current_player_color():
                return False
        if correct_coords(row1, col1 - 1) and \
                type(board.get_piece(row, col1 - 1)) is King and \
                board.get_piece(row1, col1 - 1).get_color() != board.current_player_color():
            return False
        if correct_coords(row1, col1 + 1) and \
                type(board.get_piece(row1, col1 + 1)) is King and \
                board.get_piece(row1, col1 + 1).get_color() != board.current_player_color():
            return False

        # конечная проверка

        if abs(row - row1) <= 1 and abs(col - col1) <= 1:
            return True
        return False

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)


class Board:
    def __init__(self):
        self.color = WHITE
        BP1 = 0
        BP2 = 0
        BP3 = 0
        BP4 = 0
        BP5 = 0
        BP6 = 0
        BP7 = 0
        BP8 = 0

        WP1 = 0
        WP2 = 0
        WP3 = 0
        WP4 = 0
        WP5 = 0
        WP6 = 0
        WP7 = 0
        WP8 = 0

        BR1 = 0
        BR2 = 0
        BN1 = 0
        BN2 = 0
        BB1 = 0
        BB2 = 0
        BQ = 0
        BK = 0

        WR1 = 0
        WR2 = 0
        WN1 = 0
        WN2 = 0
        WB1 = 0
        WB2 = 0
        WQ = 0
        WK = 0

        figura = 'fresca'

        Black_Pawn_1 = \
            Pawn(BLACK, tk.PhotoImage(file=f'{figura}/bP.png'), BP1)
        Black_Pawn_2 \
            = Pawn(BLACK, tk.PhotoImage(file=f'{figura}/bP.png'), BP2)
        Black_Pawn_3 \
            = Pawn(BLACK, tk.PhotoImage(file=f'{figura}/bP.png'), BP3)
        Black_Pawn_4 \
            = Pawn(BLACK, tk.PhotoImage(file=f'{figura}/bP.png'), BP4)
        Black_Pawn_5 \
            = Pawn(BLACK, tk.PhotoImage(file=f'{figura}/bP.png'), BP5)
        Black_Pawn_6 \
            = Pawn(BLACK, tk.PhotoImage(file=f'{figura}/bP.png'), BP6)
        Black_Pawn_7 \
            = Pawn(BLACK, tk.PhotoImage(file=f'{figura}/bP.png'), BP7)
        Black_Pawn_8 \
            = Pawn(BLACK, tk.PhotoImage(file=f'{figura}/bP.png'), BP8)

        White_Pawn_1 \
            = Pawn(WHITE, tk.PhotoImage(file=f'{figura}/wP.png'), WP1)
        White_Pawn_2 \
            = Pawn(WHITE, tk.PhotoImage(file=f'{figura}/wP.png'), WP2)
        White_Pawn_3 \
            = Pawn(WHITE, tk.PhotoImage(file=f'{figura}/wP.png'), WP3)
        White_Pawn_4 \
            = Pawn(WHITE, tk.PhotoImage(file=f'{figura}/wP.png'), WP4)
        White_Pawn_5 \
            = Pawn(WHITE, tk.PhotoImage(file=f'{figura}/wP.png'), WP5)
        White_Pawn_6 \
            = Pawn(WHITE, tk.PhotoImage(file=f'{figura}/wP.png'), WP6)
        White_Pawn_7 \
            = Pawn(WHITE, tk.PhotoImage(file=f'{figura}/wP.png'), WP7)
        White_Pawn_8 \
            = Pawn(WHITE, tk.PhotoImage(file=f'{figura}/wP.png'), WP8)

        Black_Rook_1 \
            = Rook(BLACK, tk.PhotoImage(file=f'{figura}/bR.png'), BR1)
        Black_Rook_2 \
            = Rook(BLACK, tk.PhotoImage(file=f'{figura}/bR.png'), BR2)
        Black_Knight_1 \
            = \
            Knight(BLACK, tk.PhotoImage(file=f'{figura}/bN.png'), BN1)
        Black_Knight_2 \
            = \
            Knight(BLACK, tk.PhotoImage(file=f'{figura}/bN.png'), BN2)
        Black_Bishop_1 \
            =\
            Bishop(BLACK, tk.PhotoImage(file=f'{figura}/bB.png'), BB1)
        Black_Bishop_2 \
            = \
            Bishop(BLACK, tk.PhotoImage(file=f'{figura}/bB.png'), BB2)
        Black_Queen \
            = \
            Queen(BLACK, tk.PhotoImage(file=f'{figura}/bQ.png'), BQ)
        Black_King \
            = \
            King(BLACK, tk.PhotoImage(file=f'{figura}/bK.png'), BK)

        White_Rook_1 \
            = \
            Rook(WHITE, tk.PhotoImage(file=f'{figura}/wR.png'), WR1)
        White_Rook_2 \
            = \
            Rook(WHITE, tk.PhotoImage(file=f'{figura}/wR.png'), WR2)
        White_Knight_1 \
            = \
            Knight(WHITE, tk.PhotoImage(file=f'{figura}/wN.png'), WN1)
        White_Knight_2 \
            = \
            Knight(WHITE, tk.PhotoImage(file=f'{figura}/wN.png'), WN2)
        White_Bishop_1 \
            = \
            Bishop(WHITE, tk.PhotoImage(file=f'{figura}/wB.png'), WB1)
        White_Bishop_2 \
            = \
            Bishop(WHITE, tk.PhotoImage(file=f'{figura}/wB.png'), WB2)
        White_Queen \
            = \
            Queen(WHITE, tk.PhotoImage(file=f'{figura}/wQ.png'), WQ)
        White_King \
            = \
            King(WHITE, tk.PhotoImage(file=f'{figura}/wK.png'), WK)

        self.field = [[White_Rook_1, White_Knight_1,
                       White_Bishop_1, White_Queen,
                       White_King, White_Bishop_2,
                       White_Knight_2, White_Rook_2],

                      [White_Pawn_1, White_Pawn_2,
                       White_Pawn_3, White_Pawn_4,
                       White_Pawn_5, White_Pawn_6,
                       White_Pawn_7, White_Pawn_8],

                      [None, None, None, None, None, None, None, None],
                      [None, None, None, None, None, None, None, None],
                      [None, None, None, None, None, None, None, None],
                      [None, None, None, None, None, None, None, None],

                      [Black_Pawn_1, Black_Pawn_2,
                       Black_Pawn_3, Black_Pawn_4,
                       Black_Pawn_5, Black_Pawn_6,
                       Black_Pawn_7, Black_Pawn_8],

                      [Black_Rook_1, Black_Knight_1,
                       Black_Bishop_1, Black_Queen,
                       Black_King, Black_Bishop_2,
                       Black_Knight_2, Black_Rook_2]]

    def cell(self, row, col):
        piece = self.field[row][col]
        if piece is not None:
            return piece
        return ' '

    def current_player_color(self):
        return self.color

    def move_piece(self, row, col, row1, col1):
        global Rook_w_flag1
        global Rook_w_flag2
        global Rook_b_flag1
        global Rook_b_flag2
        global King_w_flag
        global King_b_flag
        figura = 'fresca'
        WK = 0
        BK = 0
        if not correct_coords(row, col) or not correct_coords(row1, col1):
            return False
        if row == row1 and col == col1:
            return False
        piece = self.field[row][col]
        if piece is None:
            return False
        if piece.get_color() != self.color:
            return False
        if type(self.field[row1][col1]) is King:
            return False
        if self.field[row1][col1] is None:
            if not piece.can_move(self, row, col, row1, col1):
                return False
        elif self.field[row1][col1].get_color() == opponent(piece.get_color()):
            if not piece.can_attack(self, row, col, row1, col1):
                return False
        else:
            return False
        if type(piece) is Rook:
            if row == 0 and col == 0:
                if Rook_w_flag1 == 0:
                    if King_w_flag == 0 and \
                            row1 == 0 and col1 == 3 and \
                            self.get_piece(0, 1) is None and self.get_piece(0, 2) is None and \
                            self.get_piece(0, 3) is None:
                        self.field[row][col] = None
                        self.field[row1][col1] = piece
                        canvas.delete(self.field[0][4].get_name)
                        self.field[0][2] \
                            = \
                            King(WHITE,
                                 tk.PhotoImage(file=f''
                                                    f'{figura}/wK.png'),
                                 WK)
                        img = self.cell(0, 2)
                        img.get_name = canvas.create_image(2 * 80, 7 * 80, anchor='nw',
                                                           image=img.get_image())
                        self.field[0][4] = None
                        Rook_w_flag1 = 1
                        King_w_flag = 1
                    else:
                        Rook_w_flag1 = 1
            elif row == 7 and col == 0:
                if Rook_b_flag1 == 0:
                    if King_b_flag == 0 and row1 == 7 and col1 == 3 and \
                            self.get_piece(7, 1) is None and self.get_piece(7, 2) is None and \
                            self.get_piece(7, 3) is None:
                        self.field[row][col] = None
                        self.field[row1][col1] = piece
                        canvas.delete(self.field[7][4].get_name)
                        self.field[7][2] = \
                            King(BLACK,
                                 tk.PhotoImage(file=f''
                                                    f'{figura}/bK.png'),
                                 BK)
                        img = self.cell(7, 2)
                        img.get_name = canvas.create_image(2 * 80, 0, anchor='nw',
                                                           image=img.get_image())
                        self.field[7][4] = None
                        Rook_b_flag1 = 1
                        King_b_flag = 1
                    else:
                        Rook_w_flag1 = 1
            elif row == 0 and col == 7:
                if Rook_w_flag2 == 0:
                    if King_w_flag == 0 and row1 == 0 and col1 == 5 and \
                            self.get_piece(0, 6) is None and self.get_piece(0, 5) is None:
                        self.field[row][col] = None
                        self.field[row1][col1] = piece
                        canvas.delete(self.field[0][4].get_name)
                        self.field[0][6] = \
                            King(WHITE,
                                 tk.PhotoImage(file=f''
                                                    f'{figura}/wK.png'),
                                 WK)
                        img = self.cell(0, 6)
                        img.get_name = canvas.create_image(6 * 80, 7 * 80, anchor='nw',
                                                           image=img.get_image())
                        self.field[0][4] = None
                        Rook_w_flag2 = 1
                        King_w_flag = 1
                    else:
                        Rook_w_flag2 = 1
            elif row == 7 and col == 7:
                if Rook_b_flag2 == 0:
                    if King_b_flag == 0 and row1 == 7 and col1 == 5 and \
                            self.get_piece(7, 6) is None and self.get_piece(7, 5) is None:
                        self.field[row][col] = None
                        self.field[row1][col1] = piece
                        canvas.delete(self.field[7][4].get_name)
                        self.field[7][6] = \
                            King(BLACK,
                                 tk.PhotoImage(file=f''
                                                    f'{figura}/bK.png'),
                                 BK)
                        img = self.cell(7, 6)
                        img.get_name = canvas.create_image(6 * 80, 0, anchor='nw',
                                                           image=img.get_image())
                        self.field[7][4] = None
                        Rook_b_flag2 = 1
                        King_b_flag = 1
                    else:
                        Rook_b_flag2 = 1
            else:
                self.field[row][col] = None
                self.field[row1][col1] = piece
        else:
            if type(piece) is King:
                if row == 0 and col == 4:
                    King_w_flag = 1
                elif row == 7 and col == 4:
                    King_b_flag = 1
            self.field[row][col] = None
            self.field[row1][col1] = piece
        self.color = opponent(self.color)
        print(self.field)
        return True

    def may_change(self, row, col, row1, col1):
        if type(self.field[7][col1]) is Pawn or type(self.field[0][col1]) is Pawn:
            return True
        return False

    def change(self, row, col, row1, col1, text):
        BQ = 0
        WQ = 0
        BR = 0
        WR = 0
        BN = 0
        WN = 0
        BB = 0
        WB = 0
        figura = 'fresca'
        if text == 'ферзь':
            if self.field[row1][col1].get_color() == BLACK:
                self.field[0][col1] = \
                    Queen(BLACK,
                          tk.PhotoImage(file=f'{figura}/bQ.png'), BQ)
            else:
                self.field[7][col1] = \
                    Queen(WHITE,
                          tk.PhotoImage(file=f'{figura}/wQ.png'), WQ)
        elif text == 'ладья':
            if self.field[row1][col1].get_color() == BLACK:
                self.field[0][col1] = \
                    Rook(BLACK,
                         tk.PhotoImage(file=f'{figura}/bR.png'), BR)
            else:
                self.field[7][col1] = \
                    Rook(WHITE,
                         tk.PhotoImage(file=f'{figura}/wR.png'), WR)
        elif text == 'конь':
            if self.field[row1][col1].get_color() == BLACK:
                self.field[0][col1] = \
                    Knight(BLACK,
                           tk.PhotoImage(file=f'{figura}/bN.png'), BN)
            else:
                self.field[7][col1] = \
                    Knight(WHITE,
                           tk.PhotoImage(file=f'{figura}/wN.png'), WN)
        elif text == 'слон':
            if self.field[row1][col1].get_color() == BLACK:
                self.field[0][col1] = \
                    Bishop(BLACK,
                           tk.PhotoImage(file=f'{figura}/bB.png'), BB)
            else:
                self.field[7][col1] = \
                    Bishop(WHITE,
                           tk.PhotoImage(file=f'{figura}/wB.png'), WB)
        self.field[row][col] = None

    def get_piece(self, row, col):
        return self.field[row][col]


def opponent(color):
    if color == WHITE:
        return BLACK
    return WHITE


def print_board(board):
    cell_colors = ['peach puff', 'salmon3']
    ci = 0
    for row in range(8):
        for col in range(8):
            x1, y1 = col * 80, row * 80
            x2, y2 = col * 80 + 80, row * 80 + 80
            canvas.create_rectangle((x1, y1), (x2, y2), fill=cell_colors[ci])
            ci = not ci
        ci = not ci

    for row in range(8):
        for col in range(8):
            x1, y1 = col * 80, (7 - row) * 80
            if board.cell(row, col) != ' ':
                img = board.cell(row, col)
                img.get_name = canvas.create_image(x1, y1, anchor='nw', image=img.get_image())
                canvas.grid(row=1, column=0)


def main():
    board = Board()
    print_board(board)
    while True:
        def choose_object(event):
            global object
            global oval
            global oval_flag
            if oval_flag == 1:
                canvas.delete(oval)
            mouse_x = canvas.winfo_pointerx() - canvas.winfo_rootx()
            mouse_y = canvas.winfo_pointery() - canvas.winfo_rooty()
            x1, y1 = mouse_x // 80, mouse_y // 80
            oval \
                = \
                canvas.create_oval((x1 * 80 + 5, y1 * 80 + 5), (x1 * 80 + 20, y1 * 80 + 20),
                                   fill='red')
            oval_flag = 1
            object = board.field[7 - y1][x1]

        def drag(event):
            global origin_x
            global origin_y
            x, y = canvas.coords(object.get_name)
            x, y = int(x), int(y)
            mouse_x = canvas.winfo_pointerx() - canvas.winfo_rootx()
            mouse_y = canvas.winfo_pointery() - canvas.winfo_rooty()
            if x > mouse_x:
                x_crd = -abs(x - mouse_x)
            else:
                x_crd = abs(x - mouse_x)
            if y > mouse_y:
                y_crd = -abs(y - mouse_y)
            else:
                y_crd = abs(y - mouse_y)
            canvas.move(object, x_crd - 40, y_crd - 40)
            origin_x, origin_y = x, y

        def release(event):
            mouse_x = canvas.winfo_pointerx() - canvas.winfo_rootx()
            mouse_y = canvas.winfo_pointery() - canvas.winfo_rooty()
            x1, y1 = mouse_x // 80 * 80, mouse_y // 80 * 80
            x, y = canvas.coords(object.get_name)
            x, y = int(x), int(y)

            if board.move_piece((7 - origin_y // 80), (origin_x // 80), (7 - y1 // 80), (x1 // 80)):
                if board.may_change((7 - origin_y // 80), (origin_x // 80), (7 - y1 // 80),
                                    (x1 // 80)):

                    def send_queen():
                        board.change((7 - origin_y // 80),
                                     (origin_x // 80), (7 - y1 // 80), (x1 // 80), 'ферзь')
                        color = board.current_player_color()
                        if color == WHITE:
                            c = 'b'
                        else:
                            c = 'w'
                        img = board.cell((7 - y1 // 80), (x1 // 80))
                        if c == 'w':
                            img.get_name = canvas.create_image((7 - y1 // 80) * 80, 0, anchor='nw',
                                                               image=img.get_image())
                        else:
                            img.get_name = canvas.create_image((y1 // 80) * 80, 7 * 80, anchor='nw',
                                                               image=img.get_image())

                    def send_knight():
                        board.change((7 - origin_y // 80),
                                     (origin_x // 80), (7 - y1 // 80), (x1 // 80), 'конь')
                        color = board.current_player_color()
                        if color == WHITE:
                            c = 'b'
                        else:
                            c = 'w'
                        img = board.cell((7 - y1 // 80), (x1 // 80))
                        if c == 'w':
                            img.get_name = canvas.create_image((7 - y1 // 80) * 80, 0, anchor='nw',
                                                               image=img.get_image())
                        else:
                            img.get_name = canvas.create_image((y1 // 80) * 80, 7 * 80, anchor='nw',
                                                               image=img.get_image())

                    def send_rook():
                        board.change((7 - origin_y // 80),
                                     (origin_x // 80), (7 - y1 // 80), (x1 // 80), 'ладья')
                        color = board.current_player_color()
                        if color == WHITE:
                            c = 'b'
                        else:
                            c = 'w'
                        img = board.cell((7 - y1 // 80), (x1 // 80))
                        if c == 'w':
                            img.get_name = canvas.create_image((7 - y1 // 80) * 80, 0, anchor='nw',
                                                               image=img.get_image())
                        else:
                            img.get_name = canvas.create_image((y1 // 80) * 80, 7 * 80, anchor='nw',
                                                               image=img.get_image())

                    def send_bishop():
                        board.change((7 - origin_y // 80),
                                     (origin_x // 80), (7 - y1 // 80), (x1 // 80), 'слон')
                        color = board.current_player_color()
                        if color == WHITE:
                            c = 'b'
                        else:
                            c = 'w'
                        img = board.cell((7 - y1 // 80), (x1 // 80))
                        if c == 'w':
                            img.get_name = canvas.create_image((7 - y1 // 80) * 80, 0, anchor='nw',
                                                               image=img.get_image())
                        else:
                            img.get_name = canvas.create_image((y1 // 80) * 80, 7 * 80, anchor='nw',
                                                               image=img.get_image())

                    change_menu = tk.Tk()
                    queen \
                        = \
                        Button(change_menu, text="Ферзь",
                               bg="peach puff", fg="salmon3", command=send_queen)
                    queen.grid(row=1, column=0)

                    knight \
                        = \
                        Button(change_menu, text="Конь",
                               bg="peach puff", fg="salmon3", command=send_knight)
                    knight.grid(row=1, column=1)

                    rook \
                        = \
                        Button(change_menu, text="Ладья",
                               bg="peach puff", fg="salmon3", command=send_rook)
                    rook.grid(row=1, column=2)

                    bishop \
                        = \
                        Button(change_menu, text="Слон",
                               bg="peach puff", fg="salmon3", command=send_bishop)
                    bishop.grid(row=1, column=3)
                    step_x = 100000000
                    step_y = 100000000
                else:
                    if x > x1:
                        step_x = -abs(x - x1)
                    else:
                        step_x = abs(x - x1)
                    if y > y1:
                        step_y = -abs(y - y1)
                    else:
                        step_y = abs(y - y1)
            else:
                if x > origin_x:
                    step_x = -abs(x - origin_x)
                else:
                    step_x = abs(x - origin_x)
                if y > origin_y:
                    step_y = -abs(y - origin_y)
                else:
                    step_y = abs(y - origin_y)
            canvas.delete(oval)
            canvas.move(object.get_name, step_x, step_y)

        canvas.bind('<Button-3>', choose_object)
        canvas.bind('<Button-1>', drag)
        canvas.bind('<ButtonRelease-1>', release)
        game.mainloop()


main()
