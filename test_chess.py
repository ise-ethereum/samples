from unittest import TestCase
import unittest

import Chess


__author__ = 'jan'


class TestChess(TestCase):
    def setUp(self):
        self.test_black = Chess.Chess(False)
        self.test_white = Chess.Chess(False)
        self.test_white.figures[Chess.Flags.CURRENT_PLAYER.value]= Chess.Player.WHITE.value
        self.test_empty_start = Chess.Chess(True)

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
        self.assertTrue(self.test_black.move(16,32,Chess.Player.BLACK))
        # double move
        self.setUp()
        self.assertTrue(self.test_black.move(16,48,Chess.Player.BLACK))
        # hitting something
        self.setUp()
        self.assertTrue(self.test_white.move(22,7,Chess.Player.WHITE))
        self.test_white.print_board()

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

    def test_checkmate_valid(self):
        self.test_empty_start._set_figure(4,4,Chess.Piece.BLACK_ROOK.value)
        self.test_empty_start._set_figure(4,5,Chess.Piece.BLACK_ROOK.value)
        self.test_empty_start._set_figure(6,2,Chess.Piece.BLACK_QUEEN.value)
        # king attacked by a rook far away
        self.assertTrue(self.test_empty_start.check_for_checkmate(Chess.Player.WHITE))
        # king attacked by a rook that he could hit but would still be in check
        self.test_empty_start._set_figure(4,5,Chess.Piece.EMPTY.value)
        self.test_empty_start._set_figure(7,4,Chess.Piece.BLACK_ROOK.value)
        self.assertTrue(self.test_empty_start.check_for_checkmate(Chess.Player.WHITE))
        # checkmate by something that hits diagional
        self.test_empty_start._set_figure(7,4,Chess.Piece.EMPTY.value)
        self.test_empty_start._set_figure(4,1,Chess.Piece.BLACK_BISHOP.value)
        self.assertTrue(self.test_empty_start.check_for_checkmate(Chess.Player.WHITE))

    def test_checkmate_invalid(self):
        self.test_empty_start._set_figure(4,5,Chess.Piece.BLACK_ROOK.value)
        self.test_empty_start._set_figure(6,2,Chess.Piece.BLACK_QUEEN.value)
        # king not attacked
        self.assertFalse(self.test_empty_start.check_for_checkmate(Chess.Player.WHITE))
        # king attaked but something can be moved in the way
        self.test_empty_start._set_figure(4,4,Chess.Piece.BLACK_ROOK.value)
        self.assertTrue(self.test_empty_start.check_for_checkmate(Chess.Player.WHITE))
        self.test_empty_start._set_figure(3,2,Chess.Piece.WHITE_BISHOP.value)
        self.assertFalse(self.test_empty_start.check_for_checkmate(Chess.Player.WHITE))
        # king attacked but the attacker can be killed
        self.test_empty_start._set_figure(3,2,Chess.Piece.EMPTY.value)
        self.test_empty_start._set_figure(3,3,Chess.Piece.WHITE_BISHOP.value)
        self.assertFalse(self.test_empty_start.check_for_checkmate(Chess.Player.WHITE))
        # something can be moved in the way vertically
        self.test_empty_start._set_figure(3,3,Chess.Piece.EMPTY.value)
        self.test_empty_start._set_figure(5,0,Chess.Piece.WHITE_ROOK.value)
        self.assertFalse(self.test_empty_start.check_for_checkmate(Chess.Player.WHITE))

    def test_stallmate_valid(self):
        # stallmate just the king cant move
        self.test_empty_start._set_figure(4,5,Chess.Piece.BLACK_ROOK.value)
        self.test_empty_start._set_figure(6,2,Chess.Piece.BLACK_QUEEN.value)
        self.assertTrue(self.test_empty_start.check_for_stallmate(Chess.Player.WHITE))
        # pawn cant move
        self.test_empty_start._set_figure(7,2,Chess.Piece.WHITE_PAWN.value)
        self.assertTrue(self.test_empty_start.check_for_stallmate(Chess.Player.WHITE))
        # could move but would be check again
        self.test_empty_start._set_figure(7,0,Chess.Piece.BLACK_QUEEN.value)
        self.test_empty_start._set_figure(7,1,Chess.Piece.WHITE_ROOK.value)
        self.test_empty_start.check_for_stallmate(Chess.Player.WHITE)

    def test_stallmate_invalid(self):
        # king can move
        self.assertFalse(self.test_empty_start.check_for_checkmate(Chess.Player.WHITE))
        self.test_empty_start._set_figure(4,5,Chess.Piece.BLACK_ROOK.value)
        self.test_empty_start._set_figure(6,2,Chess.Piece.BLACK_QUEEN.value)
        # something can move
        self.test_empty_start._set_figure(7,7,Chess.Piece.WHITE_QUEEN.value)
        self.assertFalse(self.test_empty_start.check_for_checkmate(Chess.Player.WHITE))
        # king is in check
        self.test_empty_start._set_figure(4,4,Chess.Piece.BLACK_ROOK.value)
        self.assertFalse(self.test_empty_start.check_for_checkmate(Chess.Player.WHITE))

    def test_move_count(self):
        self.setUp()
        self.assertEqual(self.test_white.getMoveCount(), 0)
        self.assertTrue(self.test_white.move(68,37,Chess.Player.WHITE))
        self.assertEqual(self.test_white.getMoveCount(), 1)


if __name__ == '__main__':
    unittest.main()
