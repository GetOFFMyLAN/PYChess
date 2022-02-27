# import statements
from Pieces import *
import Player

# class definitions


class SessionManger:
    SESSION_ID = 0

    def __init__(self):
        self.SESSION_ID = 1

    def save_session(self):
        raise NotImplementedError

    def load_session(self, id):
        raise NotImplementedError

    def gen_id(self):
        raise NotImplementedError


class Engine:
    num_players = 0
    board = [[]]
    piece_container = [[], [], [], [], [], [], [], []]
    players = []

    def __init__(self, np, pl_list):
        self.num_players = np
        self.players = pl_list

    def load_pieces(self):
        """
        load pieces into piece_container. Piece container keeps track of where the pieces are w/out
        interfering with the original board. Works like an overlay
        :return: void
        """
        w_bot = [Rook('w'), Knight('w'), Bishop('w'), Queen('w'), King('w'), Bishop('w'), Knight('w'), Rook('w')]
        b_bot = [Rook('b'), Knight('b'), Bishop('b'), Queen('b'), King('b'), Bishop('b'), Knight('b'), Rook('b')]
        self.piece_container[0] = b_bot
        self.piece_container[7] = w_bot
        self.players[0].set_king(w_bot[4])
        self.players[1].set_king(b_bot[4])

        for i in range(2, 6):  # adds empty pieces to middle 4 rows of board, act as placeholders
            tmp = []
            for j in range(0, 8):
                tmp.append(Pieces())
            self.piece_container[i] = tmp

        w_p = []
        b_p = []
        for i in range(0, len(self.board)):
            w_p.append(Pawn('w'))
            b_p.append(Pawn('b'))

        self.piece_container[6] = w_p
        self.piece_container[1] = b_p

    def load_board(self, b):
        """
        loads board into game engine from input. Sets the engine's board var
        :param b: 2d array of tile chars (unicode)
        :return: void
        """
        if len(b) != 8:
            raise ValueError("invalid board passed")
        for row in b:
            if len(row) != 8:
                raise ValueError("invalid board passed")

        self.board = b

        # load pieces
        self.load_pieces()

    def display_board(self):  # TODO: add dynamic formatting
        """
        outputs board to console
        :return: void
        """
        line_num = 8
        for (b_row, p_row) in zip(self.board, self.piece_container):
            print('{} |'.format(line_num), end=" ")
            for (tile, piece) in zip(b_row, p_row):
                if piece.get() != '\0':
                    print(piece.get(), end=" ")
                else:
                    print(tile, end=" ")
            print('|')
            line_num -= 1
        print("    A B C D E F G H")

    @staticmethod
    def convert_move(pos):
        if len(pos) != 2:
            raise ValueError("invalid position passed as argument")
        if int(pos[1]) > 8 or int(pos[1]) < 0:
            raise ValueError("bad coordinate received")

        x = pos[0]
        y = 7 - (int(pos[1]) - 1)
        if x.lower() == 'a':
            x = 0
        elif x.lower() == 'b':
            x = 1
        elif x.lower() == 'c':
            x = 2
        elif x.lower() == 'd':
            x = 3
        elif x.lower() == 'e':
            x = 4
        elif x.lower() == 'f':
            x = 5
        elif x.lower() == 'g':
            x = 6
        elif x.lower() == 'h':
            x = 7
        else:
            raise ValueError("first component of coordinate invalid")

        equiv = (x, y)
        return equiv

    @staticmethod
    def check_attacks(player, piece):
        """
        checks the pieces that a move could attack
        :param player: the player that is doing the move
        :param piece: the piece being moved
        :return: void, sets king in_check property if king is attacked
        """
        raise NotImplementedError

    # TODO: add support for Queen and King moves

    def check_move(self, team, begin, end):
        """
        checks an inputted move to see if its valid
        :param team: the team (b/w) of the player doing the move
        :param begin: starting position using standard chess position cords ie. (A1)
        :param end: ending position of the piece in standard chess cords
        :return: bool, valid move or not
        """

        piece_loc = self.convert_move(begin)
        end_loc = self.convert_move(end)
        piece = self.piece_container[piece_loc[1]][piece_loc[0]]
        end_piece = self.piece_container[end_loc[1]][end_loc[0]]
        if piece.get_type() < 0 or piece.get_team() != team:
            raise ValueError("No/Invalid piece selected")
        # check if there's already a piece at the end location that is of the same team
        if end_piece.get_type() != -1 and end_piece.get_team() == team:
            raise ValueError("Can't move piece on top of piece of the same team")

        # create possible moves from selected piece and match to end location
        piece_type = piece.get_type()
        x_move_dist = end_loc[0] - piece_loc[0]
        y_move_dist = end_loc[1] - piece_loc[1]
        if piece_type == 0:  # TODO: add support for en pasant
            # movement along y axis (columns)
            if end_loc[0] == piece_loc[0]:
                if not piece.moved() and abs(end_loc[1] - piece_loc[1]) == 2:
                    return True
                elif abs(end_loc[1] - piece_loc[1]) == 1 and end_piece.get_type() == -1:
                    return True
                else:
                    return False
            # movement along x axis (rows)
            elif abs(x_move_dist) == 1:
                if abs(y_move_dist) != 1:
                    return False
                elif end_piece.get_type() == -1:
                    return False
                elif end_piece.get_team() == team:
                    return False
                else:
                    return True
            else:  # either didn't move the pawn or the move was completely invalid
                return False

        elif piece_type == 1:  # rook
            # movement along x axis (columns)
            if abs(x_move_dist) > 0:
                if y_move_dist != 0:
                    return False
                # check if theres piece in the way of move on x axis
                elif x_move_dist < 0:
                    i = piece_loc[0] - 1
                    pieces_taken = 0
                    while i > end_loc[0]:
                        tile = self.piece_container[piece_loc[1]][i]
                        # if there is still distance to end loc and a piece has already been taken then invalid
                        if pieces_taken >= 1:
                            return False
                        # invalid move since moving over/on a piece of the same team
                        if tile.get_type() != -1 and tile.get_team() == team:
                            return False
                        # hit piece that isn't same team, should not be any moves left after
                        if tile.get_type() != -1:
                            pieces_taken += 1
                        i -= 1
                    return True
                elif x_move_dist > 0:
                    i = piece_loc[0] + 1
                    pieces_taken = 0
                    while i < end_loc[0]:
                        tile = self.piece_container[piece_loc[1]][i]
                        # if there is still distance to end loc and a piece has already been taken then invalid
                        if pieces_taken >= 1:
                            return False
                        # invalid move since moving over/on a piece of the same team
                        if tile.get_type() != -1 and tile.get_team() == team:
                            return False
                        # hit piece that isn't same team, should not be any moves left after
                        if tile.get_type() != -1:
                            pieces_taken += 1
                        i += 1
                    return True
                else:
                    return False
            # movement along y axis (rows)
            elif abs(y_move_dist) > 0:
                if x_move_dist != 0:
                    return False
                # check if theres piece in the way of move on y axis
                elif y_move_dist < 0:
                    i = piece_loc[1] - 1
                    pieces_taken = 0
                    while i > end_loc[1]:
                        tile = self.piece_container[i][piece_loc[0]]
                        # if there is still distance to end loc and a piece has already been taken then invalid
                        if pieces_taken >= 1:
                            return False
                        # invalid move since moving over/on a piece of the same team
                        if tile.get_type() != -1 and tile.get_team() == team:
                            return False
                        # hit piece that isn't same team, should not be any moves left after
                        if tile.get_type() != -1:
                            pieces_taken += 1
                        i -= 1
                    return True
                elif y_move_dist > 0:
                    i = piece_loc[1] + 1
                    pieces_taken = 0
                    while i < end_loc[1]:
                        tile = self.piece_container[i][piece_loc[0]]
                        # if there is still distance to end loc and a piece has already been taken then invalid
                        if pieces_taken >= 1:
                            return False
                        # invalid move since moving over/on a piece of the same team
                        if tile.get_type() != -1 and tile.get_team() == team:
                            return False
                        # hit piece that isn't same team, should not be any moves left after
                        if tile.get_type() != -1:
                            pieces_taken += 1
                        i += 1
                    return True
                else:
                    return False

        elif piece_type == 2:  # knight
            if abs(x_move_dist) == 2 and abs(y_move_dist) != 1:  # did not move in L shape
                return False
            elif abs(y_move_dist) == 2 and abs(x_move_dist) != 1:
                return False
            elif end_piece.get_type() != -1 and end_piece.get_team() == team:  # move lands on same team piece
                return False
            else:
                return True

        elif piece_type == 3:  # bishop
            if abs(x_move_dist) != abs(y_move_dist):  # has to move by same length on x and y
                return False

            i = piece_loc[0]
            j = piece_loc[1]
            pieces_taken = 0
            if x_move_dist < 0 and y_move_dist > 0:
                i -= 1
                j += 1
                while i >= end_loc[0] and j <= end_loc[1]:
                    tile = self.piece_container[j][i]
                    if pieces_taken >= 1:
                        return False
                    if tile.get_type() != -1 and tile.get_team() == team:
                        return False
                    if tile.get_type() != -1:
                        pieces_taken += 1

                    i -= 1
                    j += 1
                return True
            elif x_move_dist > 0 and y_move_dist > 0:
                i += 1
                j += 1
                while i <= end_loc[0] and j <= end_loc[1]:
                    tile = self.piece_container[j][i]
                    if pieces_taken >= 1:
                        return False
                    if tile.get_type() != -1 and tile.get_team() == team:
                        return False
                    if tile.get_type() != -1:
                        pieces_taken += 1

                    i += 1
                    j += 1
                return True
            elif x_move_dist > 0 and y_move_dist < 0:
                i += 1
                j -= 1
                while i < end_loc[0] and j > end_loc[1]:
                    tile = self.piece_container[j][i]
                    if pieces_taken >= 1:
                        print("took to many pieces")
                        return False
                    if tile.get_type() != -1 and tile.get_team() == team:
                        print("hit same team")
                        return False
                    if tile.get_type() != -1:
                        pieces_taken += 1

                    i += 1
                    j -= 1
                return True
            elif x_move_dist < 0 and y_move_dist < 0:
                i -= 1
                j -= 1
                while i >= end_loc[0] and j >= end_loc[1]:
                    tile = self.piece_container[j][i]
                    if pieces_taken >= 1:
                        return False
                    if tile.get_type() != -1 and tile.get_team() == team:
                        return False
                    if tile.get_type() != -1:
                        pieces_taken += 1

                    i -= 1
                    j -= 1
                return True
            else:
                return False

        elif piece_type == 4:  # queen
            # moves only along x
            if abs(x_move_dist) > 0 and y_move_dist == 0:
                # check if theres piece in the way of move on x axis
                if x_move_dist < 0:
                    i = piece_loc[0] - 1
                    pieces_taken = 0
                    while i > end_loc[0]:
                        tile = self.piece_container[piece_loc[1]][i]
                        # if there is still distance to end loc and a piece has already been taken then invalid
                        if pieces_taken >= 1:
                            return False
                        # invalid move since moving over/on a piece of the same team
                        if tile.get_type() != -1 and tile.get_team() == team:
                            return False
                        # hit piece that isn't same team, should not be any moves left after
                        if tile.get_type() != -1:
                            pieces_taken += 1
                        i -= 1
                    return True
                elif x_move_dist > 0:
                    i = piece_loc[0] + 1
                    pieces_taken = 0
                    while i < end_loc[0]:
                        tile = self.piece_container[piece_loc[1]][i]
                        # if there is still distance to end loc and a piece has already been taken then invalid
                        if pieces_taken >= 1:
                            return False
                        # invalid move since moving over/on a piece of the same team
                        if tile.get_type() != -1 and tile.get_team() == team:
                            return False
                        # hit piece that isn't same team, should not be any moves left after
                        if tile.get_type() != -1:
                            pieces_taken += 1
                        i += 1
                    return True
                else:
                    return False

            # movement only along y
            elif abs(y_move_dist) > 0 and x_move_dist == 0:
                # check if theres piece in the way of move on y axis
                if y_move_dist < 0:
                    i = piece_loc[1] - 1
                    pieces_taken = 0
                    while i > end_loc[1]:
                        tile = self.piece_container[i][piece_loc[0]]
                        # if there is still distance to end loc and a piece has already been taken then invalid
                        if pieces_taken >= 1:
                            return False
                        # invalid move since moving over/on a piece of the same team
                        if tile.get_type() != -1 and tile.get_team() == team:
                            return False
                        # hit piece that isn't same team, should not be any moves left after
                        if tile.get_type() != -1:
                            pieces_taken += 1
                        i -= 1
                    return True
                elif y_move_dist > 0:
                    i = piece_loc[1] + 1
                    pieces_taken = 0
                    while i < end_loc[1]:
                        tile = self.piece_container[i][piece_loc[0]]
                        # if there is still distance to end loc and a piece has already been taken then invalid
                        if pieces_taken >= 1:
                            return False
                        # invalid move since moving over/on a piece of the same team
                        if tile.get_type() != -1 and tile.get_team() == team:
                            return False
                        # hit piece that isn't same team, should not be any moves left after
                        if tile.get_type() != -1:
                            pieces_taken += 1
                        i += 1
                    return True
                else:
                    return False

            # diagonal
            if abs(x_move_dist) == abs(y_move_dist):
                i = piece_loc[0]
                j = piece_loc[1]
                pieces_taken = 0
                if x_move_dist < 0 and y_move_dist > 0:
                    i -= 1
                    j += 1
                    while i >= end_loc[0] and j <= end_loc[1]:
                        tile = self.piece_container[j][i]
                        if pieces_taken >= 1:
                            return False
                        if tile.get_type() != -1 and tile.get_team() == team:
                            return False
                        if tile.get_type() != -1:
                            pieces_taken += 1

                        i -= 1
                        j += 1
                    return True
                elif x_move_dist > 0 and y_move_dist > 0:
                    i += 1
                    j += 1
                    while i <= end_loc[0] and j <= end_loc[1]:
                        tile = self.piece_container[j][i]
                        if pieces_taken >= 1:
                            return False
                        if tile.get_type() != -1 and tile.get_team() == team:
                            return False
                        if tile.get_type() != -1:
                            pieces_taken += 1

                        i += 1
                        j += 1
                    return True
                elif x_move_dist > 0 and y_move_dist < 0:
                    i += 1
                    j -= 1
                    while i < end_loc[0] and j > end_loc[1]:
                        tile = self.piece_container[j][i]
                        if pieces_taken >= 1:
                            print("took to many pieces")
                            return False
                        if tile.get_type() != -1 and tile.get_team() == team:
                            print("hit same team")
                            return False
                        if tile.get_type() != -1:
                            pieces_taken += 1

                        i += 1
                        j -= 1
                    return True
                elif x_move_dist < 0 and y_move_dist < 0:
                    i -= 1
                    j -= 1
                    while i >= end_loc[0] and j >= end_loc[1]:
                        tile = self.piece_container[j][i]
                        if pieces_taken >= 1:
                            return False
                        if tile.get_type() != -1 and tile.get_team() == team:
                            return False
                        if tile.get_type() != -1:
                            pieces_taken += 1

                        i -= 1
                        j -= 1
                    return True
                else:
                    return False
            else:
                return False

        elif piece_type == 5:  # king
            if abs(x_move_dist) > 1 or abs(y_move_dist) > 1:
                return False
            return True
            # TODO: add condition for when king is in check that checks the attacks on the piece

    def perform_move(self, player_id, start, end):
        start_loc = self.convert_move(start)
        end_loc = self.convert_move(end)
        player_team = self.players[player_id].get_team()

        if not self.check_move(player_team, start, end):
            raise ValueError("invalid move made")

        # replace piece in piece container and replace old spot with empty piece
        self.piece_container[end_loc[1]][end_loc[0]] = self.piece_container[start_loc[1]][start_loc[0]]
        self.piece_container[start_loc[1]][start_loc[0]].set_moved(True)
        new_tile = Pieces()
        self.piece_container[start_loc[1]][start_loc[0]] = new_tile
