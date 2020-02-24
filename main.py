from pygame.locals import *
import sys
from windows import *


class PositionTree:
    def __init__(self):
        self.root = PositionNode()
        self.iterator = self.root

    def add_node(self, board):
        new_node = PositionNode(self.iterator, board=board)
        self.iterator.children[new_node.id] = new_node
        self.iterator = new_node

    def prev(self):
        self.iterator = self.iterator.parent

    def delete_node(self):
        if self.iterator != self.root:
            del_id = self.iterator.id
            self.iterator = self.iterator.parent
            del self.iterator.children[del_id]


class PositionNode:
    no_created = 0

    def __init__(self, parent=None, board=None):
        if board is not None:
            self.board = board
        else:
            self.board = Board()
        self.children = {}
        self.parent = parent
        self.id = self.no_created
        PositionNode.no_created += 1

    def __eq__(self, other):
        return self.id == other.id


class Application:
    def __init__(self):
        pygame.init()
        self.FPSCLOCK = pygame.time.Clock()
        frame = WindowFrame()
        self.DISPLAYSURF = pygame.display.set_mode((frame.width, frame.height))
        self.window = Window(self.DISPLAYSURF)
        self.menu_window = MenuWindow(self.DISPLAYSURF, ((self.main_game, "2 Players"), (self.passing, "1 Player"),
                                                         (self.learn, "Learning"), (self.about, "About")))
        self.about_window = AboutWindow(self.DISPLAYSURF)
        pygame.display.set_caption('Chess')
        self.menu()

    @staticmethod
    def passing():
        pass

    def menu(self):
        self.window = self.menu_window
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

    def about(self):
        self.window = self.about_window
        while True:
            self.window.DISPLAYSURF.fill(self.window.bg_color)
            self.window.draw()
            mouse_clicked = False
            mouse_coords = (0, 0)
            for event in pygame.event.get():  # event handling loop
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYUP and event.key == K_ESCAPE:
                    self.window = self.menu_window
                    return
                elif event.type == MOUSEMOTION:
                    mouse_coords = event.pos
                elif event.type == MOUSEBUTTONUP:
                    mouse_coords = event.pos
                    mouse_clicked = True

            if mouse_clicked:
                if self.window.button.click_check(mouse_coords):
                    self.window = self.menu_window
                    return

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
            self.window.draw_button()
            if selected:
                self.window.draw_selected(selected_square)
            self.window.draw_pieces(game)
            mouse_coords = (0, 0)

            for event in pygame.event.get():  # event handling loop
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYUP and event.key == K_ESCAPE:
                    self.window = self.menu_window
                    return
                elif event.type == MOUSEMOTION:
                    mouse_coords = event.pos
                elif event.type == MOUSEBUTTONUP:
                    mouse_coords = event.pos
                    mouse_clicked = True

            if mouse_clicked:
                square_clicked = self.window.what_square_clicked(mouse_coords)
                if square_clicked is not None:
                    square_clicked = game.flip_coords(square_clicked)
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
                if self.window.button.click_check(mouse_coords):
                    self.window = self.menu_window
                    return

            pygame.display.update()
            self.FPSCLOCK.tick(self.window.fps)

    def learn(self):
        tree = PositionTree()
        self.window = LearnWindow(self.DISPLAYSURF)
        selected = False
        selected_square = None
        color_turn = WH
        while True:     # main loop
            game = tree.iterator.board
            mouse_clicked = False
            self.DISPLAYSURF.fill(self.window.bg_color)
            self.window.draw_chessboard()
            self.window.top_bar.draw()
            self.window.move_list.draw(tree.iterator.children)
            if selected:
                self.window.draw_selected(selected_square)
            self.window.draw_pieces(game)
            mouse_coords = (0, 0)

            for event in pygame.event.get():  # event handling loop
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYUP and event.key == K_ESCAPE:
                    self.window = self.menu_window
                    return
                elif event.type == MOUSEMOTION:
                    mouse_coords = event.pos
                elif event.type == MOUSEBUTTONUP:
                    mouse_coords = event.pos
                    mouse_clicked = True

            if mouse_clicked:
                square_clicked = self.window.what_square_clicked(mouse_coords)
                if square_clicked is not None:
                    square_clicked = game.flip_coords(square_clicked)
                    if not selected:
                        if game.piece_color(square_clicked) == color_turn:
                            selected_square = square_clicked
                            selected = True
                    elif game.piece_color(square_clicked) == color_turn:
                        selected_square = square_clicked
                    else:
                        temp_game = deepcopy(game)
                        game.move(selected_square[0], selected_square[1], square_clicked[0], square_clicked[1], color_turn)
                        if not game.illegal:
                            color_turn = (color_turn+1) % 2
                            tree.add_node(game)
                        tree.iterator.parent.board = temp_game

                        selected = False
                if self.window.top_bar.back_button.click_check(mouse_coords):
                    self.window = self.menu_window
                    return

                if self.window.top_bar.prev_move_button.click_check(mouse_coords):
                    if tree.iterator.parent is not None:
                        tree.prev()
                        color_turn = (color_turn + 1) % 2

                if self.window.top_bar.save_button.click_check(mouse_coords):
                    pass

                if self.window.top_bar.delete_button.click_check(mouse_coords):
                    tree.delete_node()

            pygame.display.update()
            self.FPSCLOCK.tick(self.window.fps)


if __name__ == '__main__':
    app = Application()

