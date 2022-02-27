# type - a unique id for each piece
# 0 - pawn
# 1 - rook
# 2 - knight
# 3 - bishop
# 4 - queen
# 5 - king

class Pieces:
    color = ''  # char representing color (w - white, b - black)
    uni_char = ''
    id = -1
    has_moved = False

    def __init__(self):
        self.color = '\0'
        self.uni_char = '\0'

    def get(self):
        return self.uni_char

    def get_team(self):
        return self.color

    def get_type(self):
        return self.id

    def moved(self):
        return self.has_moved

    def set_moved(self, move):
        self.has_moved = move

    def reset(self):
        self.color = '\0'
        self.uni_char = '\0'
        self.id = -1
        self.has_moved = False


class Pawn(Pieces):
    def __init__(self, color):
        if color == 'W' or color == 'w':
            self.color = color
            self.uni_char = '\u2659'
        elif color == 'B' or color == 'b':
            self.color = color
            self.uni_char = '\u265F'

        self.id = 0


class Rook(Pieces):
    def __init__(self, color):
        if color == 'W' or color == 'w':
            self.color = color
            self.uni_char = '\u2656'
        elif color == 'B' or color == 'b':
            self.color = color
            self.uni_char = '\u265C'

        self.id = 1


class Knight(Pieces):
    def __init__(self, color):
        if color == 'W' or color == 'w':
            self.color = color
            self.uni_char = '\u2658'
        elif color == 'B' or color == 'b':
            self.color = color
            self.uni_char = '\u265E'

        self.id = 2


class Bishop(Pieces):
    def __init__(self, color):
        if color == 'W' or color == 'w':
            self.color = color
            self.uni_char = '\u2657'
        elif color == 'B' or color == 'b':
            self.color = color
            self.uni_char = '\u265D'

        self.id = 3


class Queen(Pieces):
    def __init__(self, color):
        if color == 'W' or color == 'w':
            self.color = color
            self.uni_char = '\u2655'
        elif color == 'B' or color == 'b':
            self.color = color
            self.uni_char = '\u265B'

        self.id = 4


class King(Pieces):
    is_in_check = False

    def __init__(self, color):
        if color == 'W' or color == 'w':
            self.color = color
            self.uni_char = '\u2654'
        elif color == 'B' or color == 'b':
            self.color = color
            self.uni_char = '\u265A'

        self.id = 5

    def in_check(self):
        self.is_in_check = True
