from abc import ABC, abstractmethod
import pygame


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

    make_darker = (0, 0, 0, .2)

    @staticmethod
    def to_rgba_full_opacity(color):
        return color//0x10000, (color//0x100) % 0x100, color % 0x100, 0xFF


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


class NonActionButton(Button):
    def action(self):
        pass


class BarButton(NonActionButton):
    def __init__(self, c_coords):
        super().__init__(c_coords)
        self.width = 100
        self.height = 100
        self.coords = (self.center_coords[0] - self.width//2, self.center_coords[1] - self.height//2)


class BackButton(BarButton):
    def __init__(self, c_coords):
        super().__init__(c_coords)
        self.img = pygame.image.load('./graphics/back_arrow.png')


class PrevMoveButton(BarButton):
    def __init__(self, c_coords):
        super().__init__(c_coords)
        self.img = pygame.image.load('./graphics/last_move_arrow.png')


class SaveButton(BarButton):
    def __init__(self, c_coords):
        super().__init__(c_coords)
        self.img = pygame.image.load('./graphics/save_arrow.png')


class DeleteButton(BarButton):
    def __init__(self, c_coords):
        super().__init__(c_coords)
        self.img = pygame.image.load('./graphics/delete_icon.png')