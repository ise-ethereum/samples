from unittest import TestCase
import unittest

import Chess


__author__ = 'jan'


class TestChess(TestCase):
    def setUp(self):
        self.test_black = Chess.Chess()
        self.test_white = Chess.Chess()
        self.test_white.figures[Chess.Flags.CURRENT_PLAYER.value]= Chess.Player.WHITE.value
    def test_print_Game(self):
        self.test_black.print_game_indexes()

    def test_print_board(self):
        self.test_black.print_board()

    def test_set_board(self):
        self.test_black._set_figure(1, 1, -2)
        self.test_black.print_board()

    def test_danger_direction(self):
        self.test_black.print_game_indexes()
        print(self.test_black._get_direction(35, 19))

    def test_danger_fields_normal(self):
        list_fields = self.test_black._danger_fields_normal(0, 7)
        for field in list_fields:
            self.test_black.board[field] = -1
        self.test_black.print_game_indexes()

# general tests should all be checked by the sanity check
    def test_moving_outside_the_field(self):
        self.assertFalse(self.test_black.move(4,-1,Chess.Player.BLACK))

    def test_taking_a_figure_outside_the_field(self):
        self.assertFalse(self.test_black.move(-1,4,Chess.Player.BLACK))

    def test_basic_move_king_own_figure(self):
        self.assertFalse(self.test_black.move(4,20,Chess.Player.BLACK))

    def test_wrong_player_moves(self):
        self.assertFalse(self.test_black.move(4,5,Chess.Player.WHITE))

    def test_payer_is_not_the_owner(self):
        self.assertFalse(self.test_black.move(115,116,Chess.Player.BLACK))

# test for the king
    def test_move_king_valid(self):
        self.assertTrue(self.test_black.move(4, 3, Chess.Player.BLACK))
        self.setUp()
        #castling left
        self.assertTrue(self.test_black.move(4,1,Chess.Player.BLACK))
    def test_move_king_invalid(self):
        # too long move
        self.assertFalse(self.test_black.move(4,2,Chess.Player.BLACK))
        # move the king
        self.assertTrue(self.test_black.move(4,3,Chess.Player.BLACK))
        # let the white player do something
        self.assertTrue(self.test_black.move(119,103,Chess.Player.WHITE))
        # move it back
        self.assertTrue(self.test_black.move(3,4,Chess.Player.BLACK))
        # white has to do something again
        self.assertTrue(self.test_black.move(103,119,Chess.Player.WHITE))
        # black player atempts castling
        self.assertFalse(self.test_black.move(4,1,Chess.Player.BLACK))
#test for bishop
    def test_basic_move_bishop_valid(self):
        self.assertTrue(self.test_black.move(20,50,Chess.Player.BLACK))

    def test_move_bishop_invalid(self):
        # straight move
        self.assertFalse(self.test_black.move(20,21,Chess.Player.BLACK))
        # simply wrong move
        self.assertFalse(self.test_black.move(20,64,Chess.Player.BLACK))

# test for pawn
    def test_move_pawn_valid(self):
        # normal
        self.assertTrue(self.test_black.move(33,49,Chess.Player.BLACK))
        # double move
        self.setUp()
        self.assertTrue(self.test_black.move(16,48,Chess.Player.BLACK))
        # hitting something
        self.setUp()
        self.assertTrue(self.test_white.move(22,7,Chess.Player.WHITE))

    def test_temp(self):
        # en passant hit
        # Black makes double jump
        self.assertTrue(self.test_black.move(16,48,Chess.Player.BLACK))
        # white kills it
        self.assertTrue(self.test_black.move(49,32,Chess.Player.WHITE))

    def test_move_pawn_invalid(self):
        # trying to hit empty field
        self.assertFalse(self.test_white.move(22,5,Chess.Player.WHITE))
        # moving backwards
        self.assertFalse(self.test_white.move(34,50,Chess.Player.WHITE))
        # moving left or right
        self.assertFalse(self.test_white.move(34,33,Chess.Player.WHITE))
        self.assertFalse(self.test_white.move(34,35,Chess.Player.WHITE))
        # double move out of position white / Black
        self.assertFalse(self.test_white.move(34,3,Chess.Player.WHITE))
        self.assertFalse(self.test_black.move(33,65,Chess.Player.BLACK))
# test for knight
    def test_move_knight_valid(self):
        # some jumps
        self.assertTrue(self.test_white.move(68,35,Chess.Player.WHITE))
        self.setUp()
        self.assertTrue(self.test_white.move(68,37,Chess.Player.WHITE))
        self.setUp()
        self.assertTrue(self.test_white.move(68,50,Chess.Player.WHITE))

    def test_move_knight_invalid(self):
        # some invalid jumps
        self.assertFalse(self.test_black.move(68,36,Chess.Player.BLACK))
        self.assertFalse(self.test_black.move(68,52,Chess.Player.BLACK))
        self.assertFalse(self.test_black.move(68,2,Chess.Player.BLACK))
# test for Rook
    def test_move_rook_valid(self):
        self.assertTrue(self.test_black.move(0,1,Chess.Player.BLACK))
        self.setUp()
        self.assertTrue(self.test_black.move(0,2,Chess.Player.BLACK))
        self.setUp()
        self.assertTrue(self.test_black.move(7,39,Chess.Player.BLACK))

    def test_move_rook_invalid(self):
        # something is in the way
        self.assertFalse(self.test_black.move(0,6,Chess.Player.BLACK))
        # moving diagonal
        self.assertFalse(self.test_black.move(0,17,Chess.Player.BLACK))
# test for queen
    def test_move_queen_valid(self):
        # straight hitting something
        self.assertTrue(self.test_white.move(119,55,Chess.Player.WHITE))
        self.setUp()
        # straight hitting nothing
        self.assertTrue(self.test_white.move(119,71,Chess.Player.WHITE))
        self.setUp()
        # diagonal hitting nothing
        self.assertTrue(self.test_white.move(119,85,Chess.Player.WHITE))

    def test_move_queen_invalid(self):
        # moving over own figure
        self.assertFalse(self.test_white.move(119,51,Chess.Player.WHITE))
        #moving over enemy figure
        self.assertFalse(self.test_white.move(119,49,Chess.Player.WHITE))
        # moving that way not possible
        self.assertFalse(self.test_white.move(119,2,Chess.Player.WHITE))

    def test_danger_fields_knight(self):
        list_fields = self.test_black._danger_fields_knight(68, 23)
        for field in list_fields:
            self.test_black.board[field] = -1
        self.test_black.print_game_indexes()

    @unittest.skip
    def test_check(self):
        self.test_black.move(19, 64, Chess.Player.BLACK)
        self.test_black.print_board()
        self.test_black.move(19, 49, Chess.Player.BLACK)
        self.test_black.print_board()

    def test_get_first_figure(self):
        print(self.test_black._get_first_figure(Chess.Direction.DOWN, 19))
        print(self.test_black.print_game_indexes())
        print(self.test_black.print_board())

    def test_is_direction_free(self):
        print(self.test_black._is_direction_free(Chess.Direction.DOWN, 19, 115))
        self.test_black.print_board()
        self.test_black.print_game_indexes()
