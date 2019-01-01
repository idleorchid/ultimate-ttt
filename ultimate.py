import sys
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QGridLayout

WIDTH = 640
HEIGHT = 480
def displayBoard(board, layout):
    for x in range(9):
        mini_board = board[x]
        board_string = ''
        for row in mini_board:
            board_string += ''.join(str(i) for i in row) +'\n'
        label = QLabel(str(x) + ':\n' + board_string)
        layout.addWidget(label, x//3, x%3)

if __name__ == "__main__":
    board = {}
    for x in range(9):
        board[x] = [[0 for y in range(3)] for z in range(3)]

    for x in range(9):
        mini_board = board[x]

    app = QApplication([sys.argv])
    window = QWidget()
    layout = QGridLayout()
    displayBoard(board, layout)
    window.resize(WIDTH, HEIGHT)
    window.setLayout(layout)
    window.show()
    sys.exit(app.exec_())
