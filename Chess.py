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

    def is_diagonal(self):
        if abs(self.value) == 16:
            return False
        if abs(self.value) == 1:
            return False
        return True


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
    WHITE_KING_POS = 115 + 8
    BLACK_KING_POS = 3 + 8
    CURRENT_PLAYER = 48 + 8
    WHITE_LEFT_CASTLING = 70 + 8
    WHITE_RIGHT_CASTLING = 71 + 8
    BLACK_LEFT_CASTLING = 54 + 8
    BLACK_RIGHT_CASTLING = 55 + 8
    BLACK_EN_PASSANT = 53
    WHITE_EN_PASSANT = 69


class Chess:
    def __init__(self):
        # not needed helper board to better visualize the board indexes
        self.board = [x for x in range(0, 128)]
        # the actual board containing all the figures and flags
        self.figures = [0 for _ in range(0, 128)]
        # test setup , later here should be the hole board set
        # black
        self.figures[0] = Piece.BLACK_ROOK.value
        self.figures[4] = Piece.BLACK_KING.value
        self.figures[Flags.BLACK_KING_POS.value] = 4
        self.figures[7] = Piece.BLACK_ROOK.value
        self.figures[16] = Piece.BLACK_PAWN.value
        self.figures[20] = Piece.BLACK_BISHOP.value
        self.figures[33] = Piece.BLACK_PAWN.value
        self.figures[55] = Piece.BLACK_BISHOP.value

        self.figures[22] = Piece.WHITE_PAWN.value
        self.figures[34] = Piece.WHITE_PAWN.value
        self.figures[38] = Piece.WHITE_ROOK.value
        self.figures[49] = Piece.WHITE_PAWN.value
        self.figures[64] = Piece.WHITE_BISHOP.value
        self.figures[68] = Piece.WHITE_KNIGHT.value
        self.figures[96] = Piece.WHITE_KNIGHT.value
        self.figures[97] = Piece.WHITE_PAWN.value
        self.figures[112] = Piece.WHITE_ROOK.value
        self.figures[116] = Piece.WHITE_KING.value
        self.figures[Flags.WHITE_KING_POS.value] = 116
        self.figures[118] = Piece.WHITE_ROOK.value
        self.figures[119] = Piece.WHITE_QUEEN.value

        self.figures[Flags.CURRENT_PLAYER.value] = Player.BLACK.value

    def make_move(self, from_idx, to_idx, player):
        # get the figures at the beginning
        to_fig = self.figures[to_idx]
        from_fig = self.figures[from_idx]

        # sanity check about the move
        if not self._sanity_checks(from_idx, to_idx, from_fig, to_fig, player):
            return False
        # save the board
        self.temp = self.figures[:]

        if self._is_valid(from_idx, to_idx, from_fig, to_fig, player):
            self._make_temporal_move(from_idx, to_idx, from_fig, to_fig, player)
        else:
            self._roll_back()
            return False
        if not self._is_legal(from_idx, to_idx, from_fig, to_fig, player):
            self._roll_back()
            return False
        self._test_check(from_idx, to_idx, player)
        # change player
        self.figures[Flags.CURRENT_PLAYER.value] = -self.figures[Flags.CURRENT_PLAYER.value]

        return True

    def print_board(self):
        print(np.array(self.figures).reshape(8, 16)[:, :8])

    def print_game_indexes(self):
        print(np.array(self.board).reshape(8, 16)[:, :8])

    def _set_figure(self, rank, file, piece):
        index = rank * 16 + file
        self.figures[index] = piece

    def _danger_fields_normal(self, king_idx, figure_idx):
        # get the danger direction
        direction = self._get_direction(king_idx, figure_idx)

        # add the fields in that direction
        current_idx = king_idx + direction.value
        danger_fields = []
        while not current_idx & 0x88:
            danger_fields.append(self.board[current_idx])
            current_idx += direction.value
        return danger_fields

    def _danger_fields_knight(self, king_idx, figure_idx):
        direction = self._get_direction(king_idx, figure_idx)
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

    def _make_temporal_move(self, from_idx, to_idx, from_fig, to_fig, color):

        # remove all en passant flags
        self.figures[Flags.BLACK_EN_PASSANT.value] = -1
        self.figures[Flags.WHITE_EN_PASSANT.value] = -1
        # castling
        # it already passed valid we just need to move the rook
        if from_fig == Piece.BLACK_KING.value:
            if from_idx == 4 and to_idx == 1:
                self.figures[0] = 0
                self.figures[2] = Piece.BLACK_ROOK.value
            if from_idx == 4 and to_idx == 6:
                self.figures[7] = 0
                self.figures[5] = Piece.BLACK_ROOK.value
        if from_fig == Piece.WHITE_KING.value:
            if from_idx == 116 and to_idx == 112:
                self.figures[112] = 0
                self.figures[114] = Piece.WHITE_ROOK.value
            if from_idx == 116 and to_idx == 118:
                self.figures[118] = 0
                self.figures[117] = Piece.WHITE_ROOK.value
        # taking care of the en passant hit
        if from_fig == Piece.BLACK_PAWN.value:
            temp = from_fig * to_fig
            direction = self._get_direction(from_idx, to_idx)
            if direction.is_diagonal():
                if (temp == 0):
                    self.figures[to_idx + Direction.UP.value] = 0
        if from_fig == Piece.WHITE_PAWN.value:
            temp = from_fig * to_fig
            direction = self._get_direction(from_idx, to_idx)
            if direction.is_diagonal():
                if (temp == 0):
                    self.figures[to_idx + Direction.DOWN.value] = 0
        # take care of the double step
        if from_fig == Piece.BLACK_PAWN.value:
            # diffrence in index should be higher than 17 -> moved at least 2 squares
            if abs(to_idx - from_idx) > 20:
                self.figures[Flags.BLACK_EN_PASSANT.value] = to_idx + Direction.UP.value
        if from_fig == Piece.WHITE_PAWN.value:
            # diffrence in index should be higher than 17 -> moved at least 2 squares
            if abs(to_idx - from_idx) > 20:
                self.figures[Flags.BLACK_EN_PASSANT.value] = to_idx + Direction.DOWN.value

        # main move
        self.figures[to_idx] = self.figures[from_idx]
        self.figures[from_idx] = 0

        # remove castling flag if king or Rook moves. But only at the first move for better performance
        if from_fig == Piece.BLACK_KING.value:
            if from_idx == 4:
                self.figures[Flags.BLACK_LEFT_CASTLING.value] = -1
                self.figures[Flags.BLACK_RIGHT_CASTLING.value] = -1
        if from_fig == Piece.BLACK_ROOK.value:
            if from_idx == 0:
                self.figures[Flags.BLACK_LEFT_CASTLING.value] = -1
            if from_idx == 7:
                self.figures[Flags.BLACK_RIGHT_CASTLING.value] = -1
        if from_fig == Piece.WHITE_KING.value:
            if from_idx == 116:
                self.figures[Flags.WHITE_LEFT_CASTLING.value] = -1
                self.figures[Flags.WHITE_RIGHT_CASTLING.value] = -1
        if from_fig == Piece.WHITE_ROOK.value:
            if from_idx == 112:
                self.figures[Flags.WHITE_LEFT_CASTLING.value] = -1
            if from_idx == 119:
                self.figures[Flags.WHITE_RIGHT_CASTLING.value] = -1


    def _test_check(self, from_idx, to_idx, color):
        # TODO: set the check flag if appropriate
        pass

    def _roll_back(self):
        self.figures = self.temp[:]

    def _get_own_king_pos(self, color):
        if color:
            return self.figures[Flags.WHITE_KING_POS.value]
        else:
            return self.figures[Flags.BLACK_KING_POS.value]

    def _get_enemy_king_pos(self, color):
        if color:
            return self.figures[Flags.BLACK_KING_POS.value]
        else:
            return self.figures[Flags.WHITE_KING_POS.value]

    def _is_legal(self, from_idx, to_idx, from_fig, to_fig, color):
        # the king gets already checked when he moves
        if abs(from_fig) == Piece.BLACK_KING:
            return True
        king_danger_direction = Chess._get_direction(from_idx, self._get_own_king_pos(color))
        # we found something
        if king_danger_direction:
            # TODO: move in the same  direction backwards but only if the figure can move that way
            return True
        # end of the field
        else:
            return False

    def _is_valid(self, from_idx, to_idx, from_fig, to_fig, color):
        direction = self._get_direction(from_idx, to_idx)
        # see if the figure has the capability to move there
        if self._is_move_possible(from_idx, to_idx, from_fig, to_fig, direction):
            # see if the way for the figure is free
            if abs(from_fig) == Piece.BLACK_KNIGHT.value:
                return True
            if self._is_direction_free(direction, from_idx, to_idx):
                if abs(from_fig) == Piece.BLACK_KING.value:
                    current = from_idx
                    while True:
                        if self.is_check(current, to_fig):
                            return False
                        if current == to_idx:
                            return True
                        current += direction.value
                    return True
                return True
            else:
                return False
        else:
            return False

    @staticmethod
    def _get_direction(from_idx, to_idx):
        is_above_left = from_idx >= to_idx
        is_same_horizontal = abs(from_idx - to_idx) < 8
        is_same_vertical = from_idx % 8 == to_idx % 8
        is_left_side = from_idx % 8 > to_idx % 8

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
        # as long as we do not reach the end of the board
        while not current_index & 0x88:
            # return the figure idx if there is one
            if self.figures[current_index] != Piece.EMPTY.value:
                return current_index
            # move to the next field in that direction
            current_index = current_index + direction.value
        # end of the board has been reached
        return -1

    def _is_direction_free(self, direction, from_idx, to_idx):
        current_index = from_idx + direction.value
        # as long as we do not reach the desired position
        while to_idx != current_index:
            # we reached the end of the field
            if current_index & 0x88:
                return False
            # the path is blocked
            if self.figures[current_index] != Piece.EMPTY.value:
                return False
            current_index = current_index + direction.value
        return True

    def _is_move_possible(self, from_idx, to_idx, from_fig, to_fig, direction):
        # Kings
        if from_fig == Piece.BLACK_KING.value:
            if from_idx + direction.value == to_idx:
                return True
            else:
                if (4 == from_idx):
                    if to_idx == 1:
                        if Flags.BLACK_LEFT_CASTLING:
                            return True
                    if to_idx == 6:
                        if Flags.BLACK_RIGHT_CASTLING:
                            return True
            return False

        if from_fig == Piece.WHITE_KING.value:
            if from_idx + direction.value == to_idx:
                return True
            else:
                if from_idx == 116:
                    if to_idx == 113:
                        if Flags.WHITE_LEFT_CASTLING:
                            return True
                    if to_idx == 118:
                        if Flags.WHITE_RIGHT_CASTLING:
                            return True
            return False

        # Bishops
        if abs(from_fig) == Piece.BLACK_BISHOP.value:
            if direction.is_diagonal():
                temp = from_idx
                while not temp & 0x88:
                    if temp == to_idx:
                        return True
                    temp += direction.value
            return False
        # Qeens
        if abs(from_fig) == Piece.BLACK_QUEEN.value:
            temp = from_idx
            while not temp & 0x88:
                if temp == to_idx:
                    return True
                temp += direction.value
            return False
        # Rooks
        if abs(from_fig) == Piece.BLACK_ROOK.value:
            if not direction.is_diagonal():
                temp = from_idx
                while not temp & 0x88:
                    if temp == to_idx:
                        return True
                    temp += direction.value
            return False
        # pawns
        if from_fig == Piece.BLACK_PAWN.value:
            # Pawn has to move in negative direction
            if direction.value < 0:
                return False
            # forward move
            if not direction.is_diagonal():
                if abs(direction.value) < 2:
                    return False
                # simple move
                if from_idx + direction.value == to_idx:
                    return True
                # double move
                else:
                    if from_idx + direction.value + direction.value == to_idx:
                        if 1 == int(from_idx / 16):
                            return True
                return False
            # sidewards move
            else:
                if from_idx + direction.value == to_idx:
                    temp = to_fig * from_fig
                    # if empty the en passant flag needs to be set
                    if temp == 0:
                        if self.figures[Flags.WHITE_EN_PASSANT.value] == to_idx:
                            return True
                        else:
                            return False
                    return True
                else:
                    return False

        if from_fig == Piece.WHITE_PAWN.value:
            # Pawn has to move in positive direction
            if direction.value > 0:
                return False
            # forward move
            if not direction.is_diagonal():
                if abs(direction.value) < 2:
                    return False
                # simple move
                if from_idx + direction.value == to_idx:
                    return True
                # double move
                else:
                    if from_idx + direction.value + direction.value == to_idx:
                        if int(from_idx / 16) == 6:
                            return True
                return False
            # sidewards move
            else:
                # sidewards need to be just one step
                if from_idx + direction.value == to_idx:
                    temp = to_fig * from_fig
                    # if empty the en passant flag needs to be set
                    if temp == 0:
                        if self.figures[Flags.BLACK_EN_PASSANT.value] == to_idx:
                            return True
                        else:
                            return False
                    return True
                else:
                    return False
        # knights:
        if abs(from_fig) == Piece.BLACK_KNIGHT.value:
            if direction.is_diagonal():
                base = from_idx + direction.value
                if direction == Direction.DOWN_LEFT:
                    if base + Direction.LEFT.value == to_idx:
                        return True
                    if base + Direction.DOWN.value == to_idx:
                        return True
                    return False
                if direction == Direction.DOWN_RIGHT:
                    if base + Direction.RIGHT.value == to_idx:
                        return True
                    if base + Direction.DOWN.value == to_idx:
                        return True
                    return False
                if direction == Direction.UP_LEFT:
                    if base + Direction.LEFT.value == to_idx:
                        return True
                    if base + Direction.UP.value == to_idx:
                        return True
                    return False
                if direction == Direction.UP_RIGHT:
                    if base + Direction.RIGHT.value == to_idx:
                        return True
                    if base + Direction.UP.value == to_idx:
                        return True
                    return False
            else:
                return False

    def is_check(self, current_idx, to_fig):
        # TODO: if the current field is check
        return False
        pass

    def _sanity_checks(self, from_idx, to_idx, from_fig, to_fig, player):
        # the starting point is not in the field
        if from_idx & 0x88:
            return False
        # the end point is not in the field
        if to_idx & 0x88:
            return False
        # we have to move something
        if from_idx == to_idx:
            return False
        # there has to be a enemy figure or an empty field
        if from_fig * to_fig > 0:
            return False
        # check if the player is the owner of the figure, also tests for empty figure
        if self.figures[Flags.CURRENT_PLAYER.value] * from_fig > 0:
            return False
        # check if its the players turn
        if self.figures[Flags.CURRENT_PLAYER.value] != player.value:
            return False
        return True
