from copy import deepcopy, copy

WH = 0
BL = 1

P = 0
N = 1
B = 2
R = 3
Q = 4
K = 5


def piece_to_char(piece):
    ret = ' '
    if piece is None:
        return ret
    if piece.which == P:
        ret = 'p'
    if piece.which == N:
        ret = 'n'
    if piece.which == B:
        ret = 'b'
    if piece.which == Q:
        ret = 'q'
    if piece.which == K:
        ret = 'k'
    if piece.which == R:
        ret = 'r'
    if piece.color == WH:
        return ret.capitalize()
    return ret


def in_chess_board(x, y):
    if 0 > x or x > 7:
        return False
    if 0 > y or y > 7:
        return False
    return True


def swap(a, b):     # swaps 2 variables
    return b, a


def opposite_color(color):
    return (color+1) % 2


def rook_x_squares(x1, y1, x2, y2):     # returns squares passed by rook on x axis
    squares = []
    if y1 > y2:
        y1, y2 = swap(y1, y2)
        x1, x2 = swap(x1, x2)
    while y1 != y2:
        y1 += 1
        squares.append((x1, y1))
    return squares[:-1]


def rook_y_squares(x1, y1, x2, y2):     # returns squares passed by rook on x axis
    squares = []
    if x1 > x2:
        y1, y2 = swap(y1, y2)
        x1, x2 = swap(x1, x2)
    while x1 != x2:
        x1 += 1
        squares.append((x1, y1))
    return squares[:-1]


def bishop_squares(x1, y1, x2, y2):     # returns squares passed by bishop
    squares = []
    if y1 > y2:
        y1, y2 = swap(y1, y2)
        x1, x2 = swap(x1, x2)
    while y1 != y2:
        if x1 < x2:
            y1 += 1
            x1 += 1
        else:
            y1 += 1
            x1 -= 1
        squares.append((x1, y1))
    return squares[:-1]


class Piece:
    def __init__(self, which, color):
        self.which = which
        self.color = color

    def to_str(self):
        piece_str = "piece: "
        if self.which == P:
            piece_str += "pawn"
        if self.which == B:
            piece_str += "bishop"
        if self.which == N:
            piece_str += "knight"
        if self.which == Q:
            piece_str += "queen"
        if self.which == R:
            piece_str += "rook"
        if self.which == K:
            piece_str += "king"
        piece_str += " color: "
        if self.color == WH:
            piece_str += "white"
        else:
            piece_str += "black"
        return piece_str


class Move:
    def __init__(self, x1, y1, x2, y2, piece):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.piece = piece
        if piece.which == P and abs(y1-y2) == 2:    # check if move was long pawn move
            self.double_pawn = True
        else:
            self.double_pawn = False


class Board:
    def __init__(self, a=0):
        self.moves = []
        self.king_moved = [False, False]
        self.right_rook_moved = [False, False]
        self.left_rook_moved = [False, False]
        self.el_passant = None
        self.long_castling = False
        self.short_castling = False
        self.illegal = False
        if a == 0:
            self.board = [
                [Piece(R, WH), Piece(N, WH), Piece(B, WH), Piece(Q, WH), Piece(K, WH), Piece(B, WH), Piece(N, WH), Piece(R, WH)],
                [Piece(P, WH), Piece(P, WH), Piece(P, WH), Piece(P, WH), Piece(P, WH), Piece(P, WH), Piece(P, WH), Piece(P, WH)],
                [None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None],
                [Piece(P, BL), Piece(P, BL), Piece(P, BL), Piece(P, BL), Piece(P, BL), Piece(P, BL), Piece(P, BL), Piece(P, BL)],
                [Piece(R, BL), Piece(N, BL), Piece(B, BL), Piece(Q, BL), Piece(K, BL), Piece(B, BL), Piece(N, BL), Piece(R, BL)],
            ]
        elif a == 1:
            self.board = [
                [Piece(R, WH), None, None, None, Piece(K, WH), None, None, Piece(R, WH)],
                [Piece(P, WH), Piece(P, WH), None, Piece(P, WH), Piece(B, WH), Piece(P, WH), Piece(P, WH), Piece(P, WH)],
                [None, None, None, Piece(P, WH), None, Piece(N, WH), None, None],
                [None, Piece(P, WH), Piece(Q, WH), None, Piece(N, WH), Piece(B, WH), None, None],
                [None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None],
                [Piece(P, BL), Piece(P, BL), Piece(P, BL), Piece(P, BL), Piece(P, BL), Piece(P, BL), Piece(P, BL), Piece(P, BL)],
                [Piece(R, BL), Piece(N, BL), Piece(B, BL), Piece(Q, BL), Piece(K, BL), Piece(B, BL), Piece(N, BL), Piece(R, BL)],
            ]

    def flip(self, y1, y2):     # flips the board if black to check white only
        self.board[0], self.board[-1] = swap(self.board[0], self.board[-1])
        self.board[1], self.board[-2] = swap(self.board[1], self.board[-2])
        self.board[2], self.board[-3] = swap(self.board[2], self.board[-3])
        self.board[3], self.board[-4] = swap(self.board[3], self.board[-4])
        return 7-y1, 7-y2

    def piece_color(self, coords):
        if self.board[coords[1]][coords[0]] is None:
            return None
        else:
            return self.board[coords[1]][coords[0]].color

    @staticmethod
    def flip_coords(coord):
        return coord[0], 7-coord[1]

    def find_king(self, color):     # returns king's coords
        for y, sublist in enumerate(self.board):
            for x, piece in enumerate(sublist):
                if piece is not None and piece.which == K and piece.color == color:
                    return x, y

    def is_there_this_piece(self, x, y, color, piece):
        if in_chess_board(x, y):
            # print(x, y)
            if self.board[y][x] is not None and self.board[y][x].which == piece and self.board[y][x].color == color:
                return True
        return False

    def check_in_this_square(self, x, y, color):    # return true if sth is attacking this square
        # pawn
        if self.is_there_this_piece(x-1, y+1, opposite_color(color), P):
            return True
        if self.is_there_this_piece(x+1, y+1, opposite_color(color), P):
            return True
        # print("No P checks")
        # knight
        if self.is_there_this_piece(x+1, y+2, opposite_color(color), N):
            return True
        if self.is_there_this_piece(x-1, y+2, opposite_color(color), N):
            return True
        if self.is_there_this_piece(x+1, y-2, opposite_color(color), N):
            return True
        if self.is_there_this_piece(x-1, y-2, opposite_color(color), N):
            return True
        if self.is_there_this_piece(x+2, y+1, opposite_color(color), N):
            return True
        if self.is_there_this_piece(x-2, y+1, opposite_color(color), N):
            return True
        if self.is_there_this_piece(x+2, y-1, opposite_color(color), N):
            return True
        if self.is_there_this_piece(x-2, y-1, opposite_color(color), N):
            return True
        # print("No N checks")

        # bishop (and partly queen)
        x1 = x + 1
        y1 = y + 1
        while in_chess_board(x1, y1) and self.board[y1][x1] is None:        # right up
            x1 += 1
            y1 += 1
            if self.is_there_this_piece(x1, y1, opposite_color(color), B):
                return True
            if self.is_there_this_piece(x1, y1, opposite_color(color), Q):
                return True

        x1 = x - 1
        y1 = y + 1
        while in_chess_board(x1, y1) and self.board[y1][x1] is None:        # left up
            x1 -= 1
            y1 += 1
            if self.is_there_this_piece(x1, y1, opposite_color(color), B):
                return True
            if self.is_there_this_piece(x1, y1, opposite_color(color), Q):
                return True

        x1 = x + 1
        y1 = y - 1
        while in_chess_board(x1, y1) and self.board[y1][x1] is None:        # right bottom
            x1 += 1
            y1 -= 1
            if self.is_there_this_piece(x1, y1, opposite_color(color), B):
                return True
            if self.is_there_this_piece(x1, y1, opposite_color(color), Q):
                return True

        x1 = x - 1
        y1 = y - 1
        while in_chess_board(x1, y1) and self.board[y1][x1] is None:        # left bottom
            x1 -= 1
            y1 -= 1
            if self.is_there_this_piece(x1, y1, opposite_color(color), B):
                return True
            if self.is_there_this_piece(x1, y1, opposite_color(color), Q):
                return True

        # print("No B checks")

        # rook (and partly queen)
        x1 = x + 1
        while in_chess_board(x1, y) and self.board[y][x1] is None:  # right
            x1 += 1
            if self.is_there_this_piece(x1, y, opposite_color(color), R):
                return True
            if self.is_there_this_piece(x1, y, opposite_color(color), Q):
                return True

        x1 = x - 1
        while in_chess_board(x1, y) and self.board[y][x1] is None:  # right
            x1 -= 1
            if self.is_there_this_piece(x1, y, opposite_color(color), R):
                return True
            if self.is_there_this_piece(x1, y, opposite_color(color), Q):
                return True

        y1 = y + 1
        while in_chess_board(x, y1) and self.board[y1][x] is None:  # right
            y1 += 1
            if self.is_there_this_piece(x, y1, opposite_color(color), R):
                return True
            if self.is_there_this_piece(x, y1, opposite_color(color), Q):
                return True

        y1 = y - 1
        while in_chess_board(x, y1) and self.board[y1][x] is None:  # right
            y1 -= 1
            if self.is_there_this_piece(x, y1, opposite_color(color), R):
                return True
            if self.is_there_this_piece(x, y1, opposite_color(color), Q):
                return True

        # print("No R & Q checks")

        # king
        if self.is_there_this_piece(x+1, y, opposite_color(color), K):
            return True
        if self.is_there_this_piece(x+1, y+1, opposite_color(color), K):
            return True
        if self.is_there_this_piece(x, y+1, opposite_color(color), K):
            return True
        if self.is_there_this_piece(x+1, y-1, opposite_color(color), K):
            return True
        if self.is_there_this_piece(x-1, y+1, opposite_color(color), K):
            return True
        if self.is_there_this_piece(x-1, y, opposite_color(color), K):
            return True
        if self.is_there_this_piece(x, y-1, opposite_color(color), K):
            return True
        if self.is_there_this_piece(x-1, y-1, opposite_color(color), K):
            return True
        # print("No checks")

        return False

    def check(self, color):     # check if given player is under check
        x, y = self.find_king(color)
        print("king: ", x, y)
        return self.check_in_this_square(x, y, color)

    def check_after_move(self, x1, y1, x2, y2, color):       # check if making move is possible due to checks conditions
        # its not necessary to make full castling, so we can just move the king in this case
        board_copy = deepcopy(self.board)
        self.board[y2][x2] = self.board[y1][x1]
        self.board[y1][x1] = None
        return_value = self.check(color)
        self.board = board_copy
        return return_value

    def legal(self, x1, y1, x2, y2, color):     # check if move is legal
        if x1 < 0 or x2 < 0 or y1 < 0 or y2 < 0 or x1 > 7 or x2 > 7 or y1 > 7 or y2 > 7:    # is in the chessboard
            print('not in chessboard')
            return False
        if self.board[y1][x1] is None:  # is there a piece here?
            print('square is empty')
            return False
        print(self.board[y1][x1].to_str())

        if self.board[y1][x1].color != color:   # is this your color?
            print("it's not your color")
            return False
        if self.board[y2][x2] is not None and self.board[y2][x2].which == K:      # cannot grab a king
            print("you cannot grab a king")
            return False
        if self.check_after_move(x1, y1, x2, y2, color):
            print("it's a check")
            return False
        if x1 == x2 and y1 == y2:   # cannot be the same square
            print("you have to move a piece")
            return False
        if self.board[y2][x2] is not None and self.board[y2][x2].color == color:   # cannot grab own piece
            print("cannot grab own piece")
            return False
        if self.board[y1][x1].which == P:     # piece is a pawn
            if x1 == x2 and y2 == y1 + 1 and self.board[y2][x2] is None:    # move one up
                return True
            if x1 == x2 and y2 == y1 + 2 and self.board[y1+1][x1] is None and self.board[y2][x2] is None:    # want to make move 2 up
                return True
            if abs(x1-x2) == 1 and y2 == y1 + 1 and self.board[y2][x2] is not None:   # grab sth
                return True
            if abs(x1-x2) == 1 and y1 == 4 and y2 == 5 and self.moves[-1].double_pawn and self.moves[-1].x2 == x2: # el passant
                self.el_passant = (x2, y1)
                return True

        if self.board[y1][x1].which == N:  # piece is a knight
            if (abs(x1-x2) == 2 and abs(y1-y2) == 1) or (abs(x1-x2) == 1 and abs(y1-y2) == 2):
                return True

        if self.board[y1][x1].which == B:  # piece is a knight
            print(bishop_squares(x1, y1, x2, y2))
            if abs(x1 - x2) == abs(y1 - y2):
                for i in bishop_squares(x1, y1, x2, y2):
                    if self.board[i[1]][i[0]] is not None:
                        print("there is a piece on bishop's path")
                        return False
                return True

        if self.board[y1][x1].which == R: # rook
            if x1 == x2:
                print(rook_x_squares(x1, y1, x2, y2))
                for i in rook_x_squares(x1, y1, x2, y2):
                    if self.board[i[1]][i[0]] is not None:
                        print("there is a piece on rook's path")
                        return False
                return True
            if y1 == y2:
                print(rook_y_squares(x1, y1, x2, y2))
                for i in rook_y_squares(x1, y1, x2, y2):
                    if self.board[i[1]][i[0]] is not None:
                        print("there is a piece on rook's path")
                        return False
                return True

        if self.board[y1][x1].which == Q:     # queen
            if abs(x1 - x2) == abs(y1 - y2):
                for i in bishop_squares(x1, y1, x2, y2):
                    if self.board[i[1]][i[0]] is not None:
                        print("there is a piece on queen's path")
                        return False
                return True
            if x1 == x2:
                for i in rook_x_squares(x1, y1, x2, y2):
                    if self.board[i[1]][i[0]] is not None:
                        print("there is a piece on queen's path")
                        return False
                return True
            if y1 == y2:
                for i in rook_y_squares(x1, y1, x2, y2):
                    if self.board[i[1]][i[0]] is not None:
                        print("there is a piece on queen's path")
                        return False
                return True
        print(self.board[y1][x1].to_str())

        if self.board[y1][x1].which == K:     # king
            if abs(x1-x2) < 2 and abs(y1-y2) < 2:      # normal move
                return True
            if y1 == 0 and y2 == 0 and x1 == 4 and x2 == 6:     # short castling
                if self.check(color) or self.check_in_this_square(5, 0, color)\
                        or self.check_in_this_square(6, 0, color):  # look for checks inside castling
                    print("king is traveling through check during castling")
                    return False
                if self.board[0][5] is not None or self.board[0][6] is not None:  # check if space is empty between
                    print("there are some pieces between the king and the rook")
                    return False
                if self.king_moved[color] or self.right_rook_moved[color]:  # check if king or rook were moved
                    print("king or rook was moved before")
                    return False
                self.short_castling = True
                return True
            if y1 == 0 and y2 == 0 and x1 == 4 and x2 == 2:     # long castling
                if self.check(color) or self.check_in_this_square(3, 0, color)\
                        or self.check_in_this_square(2, 0, color):
                    print("king is traveling through check during castling")
                    return False
                if self.board[0][3] is not None or self.board[0][2] is not None or self.board[0][1] is not None:
                    print("there are some pieces between the king and the rook")
                    return False    # check if there is space between
                if self.king_moved[color] or self.left_rook_moved[color]:  # check if king or rook were moved
                    print("king or rook was moved before")
                    return False
                self.long_castling = True
                return True

        print("something unidentified went wrong with your move")
        return False

    def move(self, x1, y1, x2, y2, color, promote=None):
        self.illegal = False
        if color == BL:
            y1, y2 = self.flip(y1, y2)
        if self.legal(x1, y1, x2, y2, color):
            if self.short_castling:
                self.board[0][7] = None
                self.board[0][6] = Piece(K, color)
                self.board[0][5] = Piece(R, color)
                self.board[0][4] = None
                self.short_castling = False
            elif self.long_castling:
                self.board[0][4] = None
                self.board[0][3] = Piece(R, color)
                self.board[0][2] = Piece(K, color)
                self.board[0][1] = None
                self.board[0][0] = None
                self.long_castling = False
            elif self.el_passant is not None:
                self.board[y2][x2] = self.board[y1][x1]
                self.board[y1][x1] = None
                self.board[self.el_passant[1]][self.el_passant[0]] = None
                self.el_passant = None
            elif promote is not None:
                self.board[y2][x2] = Piece(promote, color)
                self.board[y1][x1] = None
            else:
                self.board[y2][x2] = self.board[y1][x1]
                self.board[y1][x1] = None

            if (x1 == 0 and y1 == 0) or (x2 == 0 and y2 == 0):     # check if left rook was moved
                self.left_rook_moved[color] = True

            if (x1 == 7 and y1 == 0) or (x2 == 0 and y2 == 7):     # check if left rook was moved
                self.right_rook_moved[color] = True

            if x1 == 4 and y1 == 0:      # check if king was moved
                self.king_moved[color] = True

            self.moves.append(Move(x1, y1, x2, y2, self.board[y2][x2]))
            if color == BL:
                self.flip(y1, y2)
            return True
        else:
            print("Move is illegal")
            self.illegal = True
            if color == BL:
                self.flip(y1, y2)
            return False

    def print_board(self):
        self.flip(0, 0)
        for row in self.board:
            for piece in row:
                print(piece_to_char(piece), end=' ')
            print('')
        self.flip(0, 0)


