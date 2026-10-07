import unittest

from board import Board
from game import DotsAndBoxes


class TestDotsAndBoxes(unittest.TestCase):

    def test_valid_horizontal_move(self):
        game = DotsAndBoxes()

        result = game.process_move(
            "H", 0, 0
        )

        self.assertTrue(result)
        self.assertTrue(
            game.board.horizontal[0][0]
        )

    def test_valid_vertical_move(self):
        game = DotsAndBoxes()

        result = game.process_move(
            "V", 0, 0
        )

        self.assertTrue(result)
        self.assertTrue(
            game.board.vertical[0][0]
        )

    def test_repeated_move(self):
        game = DotsAndBoxes()

        first = game.process_move(
            "H", 0, 0
        )

        second = game.process_move(
            "H", 0, 0
        )

        self.assertTrue(first)
        self.assertFalse(second)

    def test_box_completion(self):
        game = DotsAndBoxes()

        game.process_move("H", 0, 0)
        game.process_move("V", 0, 0)
        game.process_move("H", 1, 0)

        # P2 completes the box
        game.process_move("V", 0, 1)

        self.assertEqual(
            game.scores[1],
            1
        )

        # Same player gets another turn
        self.assertEqual(
            game.current,
            1
        )

    def test_end_of_game(self):
        board = Board()

        # Fill every horizontal line
        for r in range(board.rows + 1):
            for c in range(board.cols):
                board.add_line("H", r, c)

        # Fill every vertical line
        for r in range(board.rows):
            for c in range(board.cols + 1):
                board.add_line("V", r, c)

        self.assertTrue(
            board.is_complete()
        )

    def test_undo(self):
        game = DotsAndBoxes()

        game.process_move(
            "H", 0, 0
        )

        self.assertTrue(
            game.board.horizontal[0][0]
        )

        game.undo()

        self.assertFalse(
            game.board.horizontal[0][0]
        )

        self.assertEqual(
            game.scores,
            [0, 0]
        )

        self.assertEqual(
            game.current,
            0
        )


if __name__ == "__main__":
    unittest.main()