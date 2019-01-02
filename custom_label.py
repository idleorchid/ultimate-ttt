from PyQt5.QtWidgets import QLabel

class CustomLabel(QLabel):
    def __init__(self, big_board_num, mini_board_row_num, mini_board_cell_num):
        QLabel.__init__(self)
        self.big_board = big_board_num
        self.mini_board = (mini_board_row_num, mini_board_cell_num)

    def getMiniBoardNum(self):
        return (self.mini_board[0] * 3) + self.mini_board[1]

    def mousePressEvent(self, event):
        print(self.big_board, self.mini_board)
