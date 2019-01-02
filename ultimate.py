import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout

import board as b

WIDTH = 640
HEIGHT = 480

if __name__ == "__main__":
    app = QApplication([sys.argv])
    window = QWidget()
    layout = QGridLayout()
    bm = b.BoardManager(window, layout)
    bm.displayBoard()
    window.resize(WIDTH, HEIGHT)
    window.setLayout(layout)
    window.setWindowTitle("Ultimate Tic Tac Toe")
    window.show()
    sys.exit(app.exec_())
