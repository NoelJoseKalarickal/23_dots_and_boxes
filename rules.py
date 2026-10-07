def valid_move(board, orientation, row, col):
    orientation = orientation.upper()

    if orientation not in {"H", "V"}:
        return False

    if not isinstance(row, int) or not isinstance(col, int):
        return False

    if orientation == "H":
        return (
            0 <= row <= board.rows
            and 0 <= col < board.cols
            and not board.horizontal[row][col]
        )

    return (
        0 <= row < board.rows
        and 0 <= col <= board.cols
        and not board.vertical[row][col]
    )


def completed_boxes(board, before):
    return len(board.completed - before)