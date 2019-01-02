import sys
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QGridLayout, QGroupBox
from PyQt5.QtGui import QPixmap
from random import randint
import custom_label as cl

WIDTH = 640
HEIGHT = 480


def displayBoard(board, layout):
    for x in range(9):
        mini_board = board[x]
        mini_layout = QGridLayout()
        group_box = QGroupBox()
        for row in range(3):
            for cell in range(3):
                some_int = randint(0, 150)
                if (some_int < 50):
                    pixmap = QPixmap('./O.png')
                elif (some_int < 100):
                    pixmap = QPixmap('./X.png')
                else:
                    pixmap = QPixmap('./blank.png')
                pixmap = pixmap.scaledToWidth(50)
                label = cl.CustomLabel(x, row, cell)
                label.setPixmap(pixmap)
                mini_layout.addWidget(label, row, cell)
        group_box.setLayout(mini_layout)
        group_box.setObjectName('mini-board')
        group_box.setStyleSheet(
            'QGroupBox#mini-board {border : 5px solid black}')
        layout.addWidget(group_box, x // 3, x % 3)


def isMoveOnBoard(move):
    # checks move is actually on the board, but not whether it is valid by rules

    # move in format (big board, mini board)
    return (0 < move[0] < 3) and (0 < move[1] < 3)


def isValidMoveByRules(move, previous_move, current_board):
    # check move is valid by the rules of the game (i.e. assumes the move is on
    # the board)

    # move and previous_move in the format (big board, mini board)

    # the big board played has to correspond with the location played on the
    # previous mini board (unless previous move is -1)
    # the chosen place can't already have been played by either player in
    # a previous turn
    is_empty = current_board[move[0]][move[1] == 0]
    if (previous_move[1] != 1):
        return is_empty
    else:
        return is_empty and (move[0] == previous_move[1])


if __name__ == "__main__":
    board = {}
    for x in range(9):
        board[x] = [[0 for y in range(3)] for z in range(3)]

    app = QApplication([sys.argv])
    window = QWidget()
    layout = QGridLayout()
    displayBoard(board, layout)
    window.resize(WIDTH, HEIGHT)
    window.setLayout(layout)
    window.setWindowTitle("Ultimate Tic Tac Toe")
    window.show()
    sys.exit(app.exec_())
