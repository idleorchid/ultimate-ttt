from PyQt5.QtWidgets import QLabel, QWidget, QGridLayout, QGroupBox, QMessageBox
from PyQt5.QtGui import QPixmap
import custom_label as cl

PLAYER_NO = 3
COMP_NO = 5
class BoardManager():
    def __init__(self, main_window, main_layout):
        self.main_window = main_window
        self.main_layout = main_layout
        self.board = self.initBoard()
        # previous move dictates that the start move can be in any big cell
        self.previous_move = (0, -1)
        self.player_turn = True

    def initBoard(self):
        return [[[0 for y in range(3)] for z in range(3)] for x in range(9)]

    def displayBoard(self):
        for x in range(9):
            mini_board = self.board[x]
            mini_layout = QGridLayout()
            group_box = QGroupBox()
            for row in range(3):
                for cell in range(3):
                    if (self.board[x][row][cell] == 3):
                        pixmap = QPixmap('./X.png')
                    elif (self.board[x][row][cell] == 5):
                        pixmap = QPixmap('./O.png')
                    else:
                        pixmap = QPixmap('./blank.png')
                    pixmap = pixmap.scaledToWidth(50)
                    label = cl.CustomLabel(x, row, cell, self)
                    label.setPixmap(pixmap)
                    mini_layout.addWidget(label, row, cell)
            group_box.setLayout(mini_layout)
            group_box.setObjectName('mini-board')
            group_box.setStyleSheet(
                'QGroupBox#mini-board {border : 5px solid black}')
            self.main_layout.addWidget(group_box, x // 3, x % 3)

    def manageMove(self, big_cell, mini_board_coords):
        mini_cell = (mini_board_coords[0] * 3) + mini_board_coords[1]
        if (self.player_turn):
            if self.isMoveOnBoard((big_cell, mini_cell)):
                if (self.isValidMoveByRules((big_cell, mini_cell))):
                    self.previous_move = (big_cell, mini_cell)
                    self.board[big_cell][mini_board_coords[0]][mini_board_coords[1]] = PLAYER_NO
                    self.player_turn = not self.player_turn
                    self.displayBoard()
                else:
                    QMessageBox.about(self.main_window, "Invalid Move", "You cannot make this move.")
        else:
            if self.isMoveOnBoard((big_cell, mini_cell)):
                if (self.isValidMoveByRules((big_cell, mini_cell))):
                    self.previous_move = (big_cell, mini_cell)
                    self.board[big_cell][mini_board_coords[0]][mini_board_coords[1]] = COMP_NO
                    self.player_turn = not self.player_turn
                    self.displayBoard()
                else:
                    QMessageBox.about(self.main_window, "Invalid Move", "You cannot make this move.")

    def isMoveOnBoard(self, move):
        # checks move is actually on the board, but not whether it is valid by rules

        # move in format (big board, mini board)
        return (0 <= move[0] < 9) and (0 <= move[1] < 9)

    def isValidMoveByRules(self, move):
        # check move is valid by the rules of the game (i.e. assumes the move is on
        # the board)

        # move and previous_move in the format (big board, mini board)

        # the big board played has to correspond with the location played on the
        # previous mini board (unless previous move is -1)
        # the chosen place can't already have been played by either player in
        # a previous turn
        is_empty = self.board[move[0]][move[1] == 0]
        if (self.previous_move[1] == -1):
            return is_empty
        else:
            return is_empty and (move[0] == self.previous_move[1])

    def getBoard(self):
        return self.board


if __name__ == '__main__':
    board = Board()
    print(board.board)
