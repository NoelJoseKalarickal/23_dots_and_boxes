from board import Board
from rules import valid_move, completed_boxes


class DotsAndBoxes:
    def __init__(self):
        self.board = Board()
        self.current = 0
        self.scores = [0, 0]

        # Stores previous game states for the undo feature
        self.history = []

    def save_state(self):
        """
        Save the current game state before making a move.
        """

        state = {
            "horizontal": [
                row[:] for row in self.board.horizontal
            ],
            "vertical": [
                row[:] for row in self.board.vertical
            ],
            "completed": set(self.board.completed),
            "current": self.current,
            "scores": self.scores[:]
        }

        self.history.append(state)

    def undo(self):
        """
        Undo the most recent valid move.
        """

        if not self.history:
            print("Nothing to undo.")
            return False

        state = self.history.pop()

        self.board.horizontal = [
            row[:] for row in state["horizontal"]
        ]

        self.board.vertical = [
            row[:] for row in state["vertical"]
        ]

        self.board.completed = set(
            state["completed"]
        )

        self.current = state["current"]
        self.scores = state["scores"][:]

        print("Last move undone.")
        return True

    def process_move(self, orientation, row, col):
        """
        Process one move.

        Returns True if the move was successful.
        """

        orientation = orientation.upper()

        if not valid_move(
            self.board,
            orientation,
            row,
            col
        ):
            print("Invalid or already-used move.")
            return False

        # Save state BEFORE changing the board
        self.save_state()

        before = set(self.board.completed)

        success = self.board.add_line(
            orientation,
            row,
            col
        )

        if not success:
            # Safety fallback
            self.history.pop()
            print("Invalid move.")
            return False

        newly_completed = completed_boxes(
            self.board,
            before
        )

        if newly_completed:

            self.scores[self.current] += newly_completed

            print(
                f"Player {self.current + 1} "
                f"completed {newly_completed} "
                f"box(es) and plays again."
            )

        else:
            self.current = 1 - self.current

        return True

    def run(self):

        print("Dots and Boxes")
        print(
            "Enter moves as H row col or V row col."
        )
        print("Rows and columns start at 0.")
        print("Example: H 0 1")
        print("Type 'undo' to undo the last move.")

        while not self.board.is_complete():

            self.board.display(
                self.scores,
                self.current
            )

            raw = input(
                f"Player {self.current + 1}, move: "
            ).strip().upper()

            # NEW FEATURE
            if raw == "UNDO":
                self.undo()
                continue

            parts = raw.split()

            # Validate number of arguments
            if len(parts) != 3:
                print(
                    "Invalid format. "
                    "Use H row col or V row col."
                )
                continue

            orientation, row, col = parts

            # Validate orientation
            if orientation not in {"H", "V"}:
                print(
                    "Invalid orientation. "
                    "Use H or V."
                )
                continue

            # Validate numbers
            if not row.isdigit() or not col.isdigit():
                print(
                    "Row and column must be numbers."
                )
                continue

            row = int(row)
            col = int(col)

            self.process_move(
                orientation,
                row,
                col
            )

        self.board.display(
            self.scores,
            self.current
        )

        print("Game over!")

        if self.scores[0] == self.scores[1]:

            print("The game is a draw.")

        else:

            winner = (
                1
                if self.scores[0] > self.scores[1]
                else 2
            )

            print(
                f"Player {winner} wins!"
            )