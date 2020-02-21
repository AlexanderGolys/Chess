from chessCore import *
import pygame
from pygame.locals import *
import sys
from abc import ABC, abstractmethod


class Colors:
    black = 0x000
    white = 0xFFFFFF
    no_color = (0, 0, 0, 0)

    p1_1 = 0xF3E0EC
    p1_2 = 0xEAD5E6
    p1_3 = 0xF2BEFC
    p1_4 = 0xCA9CE1
    p1_5 = 0x685F74

    chess_com_dark_square_bg = 0x779556
    chess_com_dark_square_bg_selected = 0x577536
    chess_com_light_square_bg = 0xEBECD0
    chess_com_light_square_bg_selected = 0xCBCCB0

    chess_com_bg_color = 0x312e2b
    light_bg_1 = 0xCACD74
    light_bg_2 = 0xABC291

    @staticmethod
    def to_rgba_full_opacity(color):
        return color//0x10000, (color//0x100) % 0x100, color % 0x100, 0xFF


class WindowFrame:
    def __init__(self):
        self.height = 1000
        self.width = 1000
        self.margin_x = 100
        self.margin_y = 100
        self.fps = 30
        self.buttons = ()


class Window(WindowFrame):
    def __init__(self, surface):
        super().__init__()
        self.DISPLAYSURF = surface


class Button(ABC):
    def __init__(self, c_coords, text=""):
        self.img = pygame.image.load('./graphics/button1.png')
        self.width = 400
        self.height = 100
        self.center_coords = c_coords
        self.coords = (self.center_coords[0] - self.width//2, self.center_coords[1] - self.height//2)
        self.text = text

    def click_check(self, coords):
        x = coords[0]
        y = coords[1]
        if self.coords[0] < x < self.coords[0] + self.width and self.coords[1] < y < self.coords[1] + self.height:
            return True
        return False

    @abstractmethod
    def action(self):
        pass


class ActionButton(Button):
    def __init__(self, c_coords, action, text=""):
        super().__init__(c_coords, text)
        self.action = action

    def action(self):
        self.action()


class MenuWindow(Window):
    def __init__(self, surface, choosing_list):
        super().__init__(surface)
        self.button_margin = 200
        self.bg_color = Colors.chess_com_bg_color
        self.buttons = [ActionButton((self.width//2, self.height//2 + i*self.button_margin), action, "Play")
                        for i, action in enumerate(choosing_list)]
        self.DISPLAYSURF = surface

    def draw_button(self, button):
        font_obj = pygame.font.Font('freesansbold.ttf', 30)
        stack_surface = font_obj.render(button.text, True, Colors.to_rgba_full_opacity(Colors.white))
        stack_rect = stack_surface.get_rect()
        stack_rect.center = button.center_coords
        self.DISPLAYSURF.blit(stack_surface, stack_rect)
        self.DISPLAYSURF.blit(button.img, button.coords)

    def draw_buttons(self):
        for button in self.buttons:
            self.draw_button(button)

    def buttons_coords(self):
        return (button.coords for button in self.buttons)


class MainWindow(Window):
    def __init__(self, surface):
        super().__init__(surface)
        self.bg_color = (Colors.light_bg_2, Colors.chess_com_bg_color)
        self.black_bg_color = Colors.chess_com_dark_square_bg
        self.white_bq_color = Colors.chess_com_light_square_bg
        self.bP_img = pygame.image.load('./graphics/bP1.png')
        self.bR_img = pygame.image.load('./graphics/bR1.png')
        self.bB_img = pygame.image.load('./graphics/bB1.png')
        self.bN_img = pygame.image.load('./graphics/bN1.png')
        self.bK_img = pygame.image.load('./graphics/bK1.png')
        self.bQ_img = pygame.image.load('./graphics/bQ1.png')
        self.wP_img = pygame.image.load('./graphics/wP1.png')
        self.wR_img = pygame.image.load('./graphics/wR1.png')
        self.wB_img = pygame.image.load('./graphics/wB1.png')
        self.wN_img = pygame.image.load('./graphics/wN1.png')
        self.wK_img = pygame.image.load('./graphics/wK1.png')
        self.wQ_img = pygame.image.load('./graphics/wQ1.png')
        self.square_len = min(self.height - 2*self.margin_y, self.width - 2*self.margin_x)/8

    def return_piece_img(self, piece, color):
        if color == WH:
            if piece == P:
                return self.wP_img
            if piece == R:
                return self.wR_img
            if piece == N:
                return self.wN_img
            if piece == B:
                return self.wB_img
            if piece == Q:
                return self.wQ_img
            if piece == K:
                return self.wK_img
        if piece == P:
            return self.bP_img
        if piece == R:
            return self.bR_img
        if piece == N:
            return self.bN_img
        if piece == B:
            return self.bB_img
        if piece == Q:
            return self.bQ_img
        if piece == K:
            return self.bK_img

    def start_animation(self):
        pass

    def left_top_squares_coords(self):
        margin = max(self.margin_x, self.margin_y)
        reversed = [[(margin + i*self.square_len, margin + ii*self.square_len) for i in range(8)] for ii in range(8)]
        reversed[0], reversed[-1] = reversed[-1], reversed[0]
        reversed[1], reversed[-2] = reversed[-2], reversed[1]
        reversed[2], reversed[-3] = reversed[-3], reversed[2]
        reversed[3], reversed[-4] = reversed[-4], reversed[3]
        return reversed

    def what_square_clicked(self, coords):
        return int((coords[0] - self.margin_x)//self.square_len), int((coords[1] - self.margin_y)//self.square_len)

    def draw_chessboard(self):
        light = 1
        colors = (self.white_bq_color, self.black_bg_color)
        coords = self.left_top_squares_coords()
        for row in coords:
            for coord in row:
                pygame.draw.rect(self.DISPLAYSURF, colors[light], (coord[0], coord[1], self.square_len, self.square_len))
                light = (light+1) % 2
            light = (light + 1) % 2

    def draw_pieces(self, board):
        coords = self.left_top_squares_coords()
        for i, row in enumerate(board.board):
            for ii, piece in enumerate(row):
                if piece is not None:
                    self.DISPLAYSURF.blit(self.return_piece_img(piece.which, piece.color), coords[i][ii])

    def draw_selected(self, coords):
        x = coords[0]
        y = coords[1]
        tab_coords = self.left_top_squares_coords()
        if ((x % 2) + (y % 2)) % 2 == 0:
            pygame.draw.rect(self.DISPLAYSURF, Colors.chess_com_dark_square_bg_selected, (tab_coords[y][x][0], tab_coords[y][x][1], self.square_len, self.square_len))
        else:
            pygame.draw.rect(self.DISPLAYSURF, Colors.chess_com_light_square_bg_selected, (tab_coords[y][x][0], tab_coords[y][x][1], self.square_len, self.square_len))


def test():
    board = Board(1)
    c = WH
    while True:
        board.print_board()

        print("x1 = ")
        x1 = int(input())
        print("y1 = ")
        y1 = int(input())
        print("x2 = ")
        x2 = int(input())
        print("y2 = ")
        y2 = int(input())

        if board.move(x1, y1, x2, y2, c):
            c = (c+1) % 2


class Application:
    def __init__(self):
        pygame.init()
        self.FPSCLOCK = pygame.time.Clock()
        frame = WindowFrame()
        self.DISPLAYSURF = pygame.display.set_mode((frame.width, frame.height))
        self.window = Window(self.DISPLAYSURF)
        pygame.display.set_caption('Chess')
        self.menu()

    def menu(self):
        self.window = MenuWindow(self.DISPLAYSURF, [self.main_game])
        print(self.window.buttons[0])
        while True:
            self.window.DISPLAYSURF.fill(self.window.bg_color)
            self.window.draw_buttons()
            mouse_clicked = False
            mouse_coords = (0, 0)
            for event in pygame.event.get():  # event handling loop
                if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEMOTION:
                    mouse_coords = event.pos
                elif event.type == MOUSEBUTTONUP:
                    mouse_coords = event.pos
                    mouse_clicked = True

            if mouse_clicked:
                for button in self.window.buttons:
                    if button.click_check(mouse_coords):
                        button.action()
            pygame.display.update()
            self.FPSCLOCK.tick(self.window.fps)

    def main_game(self):
        self.window = MainWindow(self.DISPLAYSURF)
        game = Board()
        selected = False
        selected_square = None
        color_turn = WH
        while True:     # main loop
            mouse_clicked = False
            self.DISPLAYSURF.fill(self.window.bg_color[color_turn])
            self.window.draw_chessboard()
            if selected:
                self.window.draw_selected(selected_square)
            self.window.draw_pieces(game)
            mouse_coords = (0, 0)

            for event in pygame.event.get():  # event handling loop
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYUP and event.key == K_ESCAPE:
                    self.window = MenuWindow(self.DISPLAYSURF, [self.main_game])
                    return
                elif event.type == MOUSEMOTION:
                    mouse_coords = event.pos
                elif event.type == MOUSEBUTTONUP:
                    mouse_coords = event.pos
                    mouse_clicked = True

            if mouse_clicked:
                square_clicked = game.flip_coords(self.window.what_square_clicked(mouse_coords))
                print(square_clicked)
                if not selected:
                    if game.piece_color(square_clicked) == color_turn:
                        selected_square = square_clicked
                        selected = True
                elif game.piece_color(square_clicked) == color_turn:
                    selected_square = square_clicked
                else:
                    game.move(selected_square[0], selected_square[1], square_clicked[0], square_clicked[1], color_turn)
                    if not game.illegal:
                        color_turn = (color_turn+1) % 2
                    selected = False

            pygame.display.update()
            self.FPSCLOCK.tick(self.window.fps)


if __name__ == '__main__':
    app = Application()
