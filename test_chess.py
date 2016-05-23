from unittest import TestCase
import unittest

import Chess


__author__ = 'jan'


class TestChess(TestCase):
    def test_print_Game(self):
        test = Chess.Chess()
        test.print_game_indexes()

    def test_print_board(self):
        test = Chess.Chess()
        test.print_board()

    def test_set_board(self):
        test = Chess.Chess()
        test._set_figure(1, 1, -2)
        test.print_board()

    def test_danger_direction(self):
        test = Chess.Chess()
        test.print_game_indexes()
        print(test._get_direction(35, 19))

    def test_danger_fields_normal(self):
        test = Chess.Chess()
        list_fields = test._danger_fields_normal(0, 7)
        for field in list_fields:
            test.board[field] = -1
        test.print_game_indexes()

    def test_danger_fields_knight(self):
        test = Chess.Chess()
        list_fields = test._danger_fields_knight(68, 23)
        for field in list_fields:
            test.board[field] = -1
        test.print_game_indexes()

    @unittest.skip
    def test_basic_move_test(self):
        test = Chess.Chess()
        test.make_move(3, 4, Chess.Player.BLACK)
        test.print_board()
        test.print_game_indexes()

    @unittest.skip
    def test_check(self):
        test = Chess.Chess()
        test.make_move(19, 64, Chess.Player.BLACK)
        test.print_board()
        test.make_move(19, 49, Chess.Player.BLACK)
        test.print_board()

    def test_get_first_figure(self):
        test = Chess.Chess()
        print(test._get_first_figure(Chess.Direction.DOWN, 19))
        print(test.print_game_indexes())
        print(test.print_board())

    def test_is_direction_free(self):
        test = Chess.Chess()
        print(test._is_direction_free(Chess.Direction.DOWN, 19, 115, Chess.Player.BLACK))
        test.print_board()
        test.print_game_indexes()
