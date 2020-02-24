from buttons import *
from chess_core import *


class WindowFrame:
    height = 1000
    width = 1000
    margin_x = 100
    margin_y = 100
    fps = 30

    def __init__(self):
        self.buttons = ()


class Window(WindowFrame):
    def __init__(self, surface):
        super().__init__()
        self.DISPLAYSURF = surface

    def blit_text(self, text, center_coords):
        font_obj = pygame.font.Font('freesansbold.ttf', 30)
        stack_surface = font_obj.render(text, True, Colors.to_rgba_full_opacity(Colors.white))
        stack_rect = stack_surface.get_rect()
        stack_rect.center = center_coords
        self.DISPLAYSURF.blit(stack_surface, stack_rect)

    def blit_button_text(self, button):
        font_obj = pygame.font.Font('freesansbold.ttf', 30)
        stack_surface = font_obj.render(button.text, True, Colors.to_rgba_full_opacity(Colors.white))
        stack_rect = stack_surface.get_rect()
        stack_rect.center = button.center_coords
        self.DISPLAYSURF.blit(stack_surface, stack_rect)


class MenuWindow(Window):
    def __init__(self, surface, choosing_list):
        super().__init__(surface)
        self.button_margin = 110
        self.bg_color = Colors.chess_com_bg_color
        self.buttons = [ActionButton((self.width//2, self.height//2 + i*self.button_margin), action[0], action[1])
                        for i, action in enumerate(choosing_list)]
        self.DISPLAYSURF = surface

    def draw_buttons(self):
        for button in self.buttons:
            self.DISPLAYSURF.blit(button.img, button.coords)
            self.blit_button_text(button)

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
        self.button = BackButton((50, 50))
        self.square_len = min(self.height - 2*self.margin_y, self.width - 2*self.margin_x)/8

    def draw_button(self):
        self.DISPLAYSURF.blit(self.button.img, self.button.coords)

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
        _reversed = [[(margin + i*self.square_len, margin + ii*self.square_len) for i in range(8)] for ii in range(8)]
        _reversed[0], _reversed[-1] = _reversed[-1], _reversed[0]
        _reversed[1], _reversed[-2] = _reversed[-2], _reversed[1]
        _reversed[2], _reversed[-3] = _reversed[-3], _reversed[2]
        _reversed[3], _reversed[-4] = _reversed[-4], _reversed[3]
        return _reversed

    def what_square_clicked(self, coords):
        x = (coords[0] - self.margin_x)//self.square_len
        y = (coords[1] - self.margin_y)//self.square_len
        if 0 <= x < 8 and 0 <= y < 8:
            return int(x), int(y)
        return None

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


class LearnWindow(MainWindow):
    class TopBar:
        def __init__(self, learn_window):
            self.learn_win = learn_window
            self.back_button = BackButton((50, 50))
            self.prev_move_button = PrevMoveButton((150, 50))
            self.save_button = SaveButton((250, 50))
            self.delete_button = DeleteButton((350, 50))

        def draw(self):
            self.learn_win.DISPLAYSURF.blit(self.back_button.img, self.back_button.coords)
            self.learn_win.DISPLAYSURF.blit(self.prev_move_button.img, self.prev_move_button.coords)
            self.learn_win.DISPLAYSURF.blit(self.save_button.img, self.save_button.coords)
            self.learn_win.DISPLAYSURF.blit(self.delete_button.img, self.delete_button.coords)

    class MoveList:
        def __init__(self, learn_window):
            self.learn_win = learn_window
            self.margin_top = 50
            self.margin_right = 50
            self.margin_left = 50
            self.bar_height = 20
            self.bar_width = self.learn_win.width//2 - self.margin_left - self.margin_right
            self.x_center = 3*self.learn_win.width//4

        def draw(self, _list):
            for i, node in enumerate(_list):    # node - id
                print(i, _list[node])
                font_obj = pygame.font.Font('freesansbold.ttf', 30)
                stack_surface = font_obj.render(str(node), True,
                                                Colors.to_rgba_full_opacity(Colors.white), Colors.make_darker)
                stack_rect = stack_surface.get_rect()
                stack_rect.center = (self.x_center, self.margin_top + i*self.bar_height)
                self.learn_win.DISPLAYSURF.blit(stack_surface, stack_rect)

    def __init__(self, surface):
        super().__init__(surface)
        self.bg_color = Colors.chess_com_bg_color
        self.board_margin_left = 50
        self.board_margin_right = 550
        self.board_margin_x = self.board_margin_left + self.board_margin_right
        self.board_margin_top = self.height//2 - (self.width - self.board_margin_x)//2
        self.board_margin_bottom = self.board_margin_top
        self.board_margin_y = 2*self.board_margin_top
        self.square_len = (self.width - self.board_margin_x)//8
        self.bP_img = self.resize_piece(self.bP_img)
        self.bR_img = self.resize_piece(self.bR_img)
        self.bB_img = self.resize_piece(self.bB_img)
        self.bN_img = self.resize_piece(self.bN_img)
        self.bK_img = self.resize_piece(self.bK_img)
        self.bQ_img = self.resize_piece(self.bQ_img)
        self.wP_img = self.resize_piece(self.wP_img)
        self.wR_img = self.resize_piece(self.wR_img)
        self.wB_img = self.resize_piece(self.wB_img)
        self.wN_img = self.resize_piece(self.wN_img)
        self.wK_img = self.resize_piece(self.wK_img)
        self.wQ_img = self.resize_piece(self.wQ_img)
        self.top_bar = self.TopBar(self)
        self.move_list = self.MoveList(self)

    def resize_piece(self, img):
        return pygame.transform.scale(img, (self.square_len, self.square_len))

    def left_top_squares_coords(self):
        _reversed = [[(self.board_margin_left + i*self.square_len, self.board_margin_top + ii*self.square_len)
                     for i in range(8)] for ii in range(8)]
        _reversed[0], _reversed[-1] = _reversed[-1], _reversed[0]
        _reversed[1], _reversed[-2] = _reversed[-2], _reversed[1]
        _reversed[2], _reversed[-3] = _reversed[-3], _reversed[2]
        _reversed[3], _reversed[-4] = _reversed[-4], _reversed[3]
        return _reversed

    def what_square_clicked(self, coords):
        x = (coords[0] - self.board_margin_left)//self.square_len
        y = (coords[1] - self.board_margin_top)//self.square_len
        if 0 <= x < 8 and 0 <= y < 8:
            return int(x), int(y)
        return None


class AboutWindow(Window):
    def __init__(self, surface):
        super().__init__(surface)
        self.bg_color = Colors.chess_com_bg_color
        self.text_img = pygame.image.load('./graphics/about_text.png')
        self.button = NonActionButton((self.width//2, 3*self.height//4), "Back")
        self.DISPLAYSURF = surface
        self.top_margin = 200
        self.left_margin = 200

    def draw(self):
        self.DISPLAYSURF.blit(self.text_img, (0, 0))        # about text
        self.DISPLAYSURF.blit(self.button.img, self.button.coords)
        self.blit_button_text(self.button)