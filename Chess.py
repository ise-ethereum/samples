__author__ = 'jan'
from enum import Enum

import numpy as np


class Direction(Enum):
    UP = -16
    UP_RIGHT = -15
    RIGHT = 1
    DOWN_RIGHT = 17
    DOWN = 16
    DOWN_LEFT = 15
    LEFT = -1
    UP_LEFT = -17


class Piece(Enum):
    WHITE_KING = -6
    WHITE_QUEEN = -5
    WHITE_ROOK = -4
    WHITE_BISHOP = -3
    WHITE_KNIGHT = -2
    WHITE_PAWN = -1
    EMPTY = 0
    BLACK_KING = 6
    BLACK_QUEEN = 5
    BLACK_ROOK = 4
    BLACK_BISHOP = 3
    BLACK_KNIGHT = 2
    BLACK_PAWN = 1


class Player(Enum):
    WHITE = 1
    BLACK = -1

class Flags(Enum):
    KING_WHITE_POS = 8
    KING_BLACK_POS = 9
    CURRENT_PLAYER = 10


class Chess:
    def __init__(self):
        # not needed helper board to better visualize the board indexes
        self.board = [x for x in range(0, 128)]
        # the actual board containing all the figures and flags
        self.figures = [0 for x in range(0, 128)]
        # test setup , later here should be the hole board set
        self.figures[3] = Piece.BLACK_KING.value
        self.figures[115] = Piece.WHITE_KING.value
        self.figures[19] = Piece.BLACK_BISHOP.value
        self.figures[Flags.KING_WHITE_POS] = 115
        self.figures[Flags.KING_BLACK_POS] = 19
        self.figures[Flags.CURRENT_PLAYER] = Player.WHITE.value

    def make_move(self, from_idx, to_idx, player):
        # save the current state of the board
        self.temp = self.figures[:]
        # check if the move is valid
        if self._is_valid(from_idx, to_idx, player):
            self._make_temporal_move(from_idx, to_idx, player)
        # else abort
        else:
            return -1
        #
        if not self._is_legal(from_idx, to_idx, player):
            self._roll_back()
            return -1
        self._test_check(from_idx, to_idx, player)

    def print_board(self):
        print(np.array(self.figures).reshape(8, 16)[:, :8])

    def print_game_indexes(self):
        print(np.array(self.board).reshape(8, 16)[:, :8])

    def _set_figure(self, rank, file, piece):
        index = rank * 16 + file
        self.figures[index] = piece

    def _danger_fields_normal(self, king_idx, figure_idx):
        # get the danger direction
        direction = self._danger_direction(king_idx, figure_idx)

        # add the fields in that direction
        current_idx = king_idx + direction.value
        danger_fields = []
        while not current_idx & 0x88:
            danger_fields.append(self.board[current_idx])
            current_idx += direction.value
        return danger_fields

    def _danger_fields_knight(self, king_idx, figure_idx):
        direction = self._danger_direction(king_idx, figure_idx)
        # take care of the special knight case
        # take the first step for both directions
        current_idx_first = king_idx
        current_idx_second = king_idx
        danger_fields = []
        # move the second step
        if direction == Direction.UP_RIGHT:
            current_idx_first = current_idx_first + Direction.UP.value + direction.value
            current_idx_second = current_idx_second + Direction.RIGHT.value + direction.value
        if direction == Direction.DOWN_RIGHT:
            current_idx_first = current_idx_first + Direction.DOWN.value + direction.value
            current_idx_second = current_idx_second + Direction.RIGHT.value + direction.value
        if direction == Direction.DOWN_LEFT:
            current_idx_first = current_idx_first + Direction.DOWN.value + direction.value
            current_idx_second = current_idx_second + Direction.LEFT.value + direction.value
        if direction == Direction.UP_LEFT:
            current_idx_first = current_idx_first + Direction.UP.value + direction.value
            current_idx_second = current_idx_second + Direction.LEFT.value + direction.value

        # test if the fields are in the array
        if not current_idx_first & 0x88 and current_idx_first != king_idx:
            danger_fields.append(self.board[current_idx_first])
        if not current_idx_second & 0x88 and current_idx_second != king_idx:
            danger_fields.append(self.board[current_idx_second])
        return danger_fields

    def _make_temporal_move(self, from_idx, to_idx, color):
        self.figures[to_idx] = self.figures[from_idx]
        self.figures[from_idx] = 0

    def _test_check(self, from_idx, to_idx, color):
        # TODO: set the check flag if appropriate
        pass

    def _roll_back(self):
        self.figures = self.temp[:]

    def _get_own_king_pos(self, color):
        # black
        if (color):
            return self.figures[Flags.KING_BLACK_POS.value]
        # white
        else:
            return self.figures[Flags.KING_WHITE_POS.value]

    def _get_enemy_king_pos(self, color):
        # black
        if (color):
            return self.figures[Flags.KING_WHITE_POS.value]
        # white
        else:
            return self.figures[Flags.KING_BLACK_POS.value]

    def _is_legal(self, from_idx, to_idx, color):
        king_danger_direction = Chess._danger_direction(from_idx, self._get_own_king_pos(color))
        # we found something
        if (king_danger_direction):
            # TODO: move in the same  direction backwards but only if the figure can move that way
            return True
        # end of the field
        else:
            return False

    def _is_valid(self, from_idx, to_idx, color):
        # TODO: check if a move is valid
        pass

    @staticmethod
    def _danger_direction(king_idx, figure_idx):
        # king can not be at the same location as the figure
        if king_idx == figure_idx:
            return -2

        # king index is outside the game
        if king_idx & 0x88:
            return -2

        # figure index is outside the game
        if figure_idx & 0x88:
            return -2

        # true : figure is left in the same line or above the king 0 figure is right in the same line or below the king
        is_above_left = king_idx >= figure_idx

        # true : figure is on the same line horizontal as the king
        is_same_horizontal = abs(king_idx - figure_idx) < 8

        # true : figure is on the same vertical line  as the king
        is_same_vertical = king_idx % 8 == figure_idx % 8

        # true : figure is on the left side else right side
        is_left_side = king_idx % 8 > figure_idx % 8

        if is_above_left:
            if is_same_vertical:
                return Direction.UP
            if is_same_horizontal:
                return Direction.LEFT
            if is_left_side:
                return Direction.UP_LEFT
            else:
                return Direction.UP_RIGHT
        else:
            if is_same_vertical:
                return Direction.DOWN
            if is_same_horizontal:
                return Direction.RIGHT
            if is_left_side:
                return Direction.DOWN_LEFT
            else:
                return Direction.DOWN_RIGHT

    def _get_first_figure(self, direction, start):
        current_index = start + direction.value
        # as long as we dont reach the end of the board
        while not current_index & 0x88:
            # return the figure idx if there is one
            if self.figures[current_index] != Piece.EMPTY.value:
                return current_index
            # move to the next field in that direction
            current_index = current_index + direction.value
        # end of the board has been reached
        return -1

    def _is_direction_free(self, direction, start, end, color):
        current_index = start + direction.value
        # as long as we dont reach the desired position
        while end != current_index:
            # we reached the end of the field
            if current_index & 0x88:
                return -1
            # the path is blocked
            if self.figures[current_index] != Piece.EMPTY.value:
                return -1
            current_index = current_index + direction.value
        # we are in front of the desired position
        # calculate if the figure on the field is an enemy
        is_enemy = self.figures[current_index] * color.value
        # the field is empty
        if is_enemy == 0:
            return 1
        # the field is an enemy
        if is_enemy < 0:
            return 1
        # the field is a friend
        if is_enemy > 0:
            return -1