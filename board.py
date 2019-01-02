from PyQt5 import QtCore
from PyQt5.QtWidgets import QLabel, QWidget, QGridLayout, QGroupBox, QMessageBox
from PyQt5.QtGui import QPixmap
import custom_label as cl

PLAYER_NO = 3
COMP_NO = 5
CELL_WIDTH = 50


class BoardManager():
    def __init__(self, main_window, main_layout):
        self.main_window = main_window
        self.main_layout = main_layout
        self.board = self.initBoard()
        self.mini_board_wins = [3] * 2 + [0] * 4 + [5] * 2 + [0]
        # previous move dictates that the start move can be in any big cell
        self.previous_move = (0, -1)
        self.player_turn = True

    def initBoard(self):
        return [[0 for y in range(9)] for x in range(9)]

    def displayBoard(self):
        self.clearLayout()
        for x in range(9):
            mini_board = self.board[x]
            mini_layout = QGridLayout()
            group_box = QGroupBox()
            if (self.mini_board_wins[x] == 0):
                for cell in range(9):
                    if (self.board[x][cell] == 3):
                        pixmap = QPixmap('./X.png')
                    elif (self.board[x][cell] == 5):
                        pixmap = QPixmap('./O.png')
                    else:
                        pixmap = QPixmap('./blank.png')
                    pixmap = pixmap.scaledToWidth(CELL_WIDTH)
                    label = cl.CustomLabel(x, cell, self)
                    label.setPixmap(pixmap)
                    mini_layout.addWidget(label, cell // 3, cell % 3)
            else:
                label = QLabel()
                if (self.mini_board_wins[x] == 3):
                    pixmap = QPixmap('./X.png')
                else:
                    pixmap = QPixmap('./O.png')
                pixmap = pixmap.scaledToWidth(CELL_WIDTH * 3)
                label.setPixmap(pixmap)
                label.setAlignment(QtCore.Qt.AlignCenter)
                mini_layout.addWidget(label, 0, 0)
            group_box.setLayout(mini_layout)
            group_box.setObjectName('mini-board')
            group_box.setStyleSheet(
                'QGroupBox#mini-board {border : 5px solid black}')
            self.main_layout.addWidget(group_box, x // 3, x % 3)
        self.main_window.setLayout(self.main_layout)

    def clearLayout(self):
        while self.main_layout.count():
            child = self.main_layout.takeAt(0)
            child.widget().deleteLater()

    def manageMove(self, big_cell, mini_cell):
        if (self.player_turn):
            if self.isMoveOnBoard((big_cell, mini_cell)):
                if (self.isValidMoveByRules((big_cell, mini_cell))):
                    self.previous_move = (big_cell, mini_cell)
                    self.board[big_cell][mini_cell] = PLAYER_NO
                    self.player_turn = not self.player_turn
                    self.displayBoard()
                else:
                    QMessageBox.about(
                        self.main_window, "Invalid Move", "You cannot make this move.")
        else:
            if self.isMoveOnBoard((big_cell, mini_cell)):
                if (self.isValidMoveByRules((big_cell, mini_cell))):
                    self.previous_move = (big_cell, mini_cell)
                    self.board[big_cell][mini_cell] = COMP_NO
                    self.player_turn = not self.player_turn
                    self.displayBoard()
                else:
                    QMessageBox.about(
                        self.main_window, "Invalid Move", "You cannot make this move.")
        self.checkIfWinOnMiniBoard(self.previous_move[0])
        if (self.checkIfWinOnMiniBoard(self.previous_move[1])):
            self.previous_move = (self.previous_move[0], -1)
            self.displayBoard()
            print('Win:', self.checkIfWinOnBigBoard())

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
        is_empty = self.board[move[0]][move[1]] == 0
        if (self.previous_move[1] == -1):
            return is_empty
        else:
            return is_empty and (move[0] == self.previous_move[1])

    def checkIfWinOnMiniBoard(self, mini_board_num):
        if (self.mini_board_wins[mini_board_num] != 0):
            return True
        else:
            mini_board = self.board[mini_board_num]
            win = 0
            if mini_board[0] != 0:
                if mini_board[0] == mini_board[4] == mini_board[8]:
                    win = mini_board[0]
                if mini_board[0] == mini_board[3] == mini_board[6]:
                    win = mini_board[0]
                if mini_board[0] == mini_board[1] == mini_board[2]:
                    win = mini_board[0]
            if mini_board[4] != 0:
                if mini_board[4] == mini_board[2] == mini_board[6]:
                    win = mini_board[4]
                if mini_board[4] == mini_board[3] == mini_board[5]:
                    win = mini_board[4]
                if mini_board[4] == mini_board[1] == mini_board[7]:
                    win = mini_board[4]
            if mini_board[8] != 0:
                if mini_board[8] == mini_board[2] == mini_board[5]:
                    win = mini_board[8]
                if mini_board[8] == mini_board[6] == mini_board[7]:
                    win = mini_board[8]
            self.mini_board_wins[mini_board_num] = win
            return win != 0

    def checkIfWinOnBigBoard(self):
        win = 0
        if self.mini_board_wins[0] != 0:
            if self.mini_board_wins[0] == self.mini_board_wins[4] == self.mini_board_wins[8]:
                win = self.mini_board_wins[0]
            if self.mini_board_wins[0] == self.mini_board_wins[3] == self.mini_board_wins[6]:
                win = self.mini_board_wins[0]
            if self.mini_board_wins[0] == self.mini_board_wins[1] == self.mini_board_wins[2]:
                win = self.mini_board_wins[0]
        if self.mini_board_wins[4] != 0:
            if self.mini_board_wins[4] == self.mini_board_wins[2] == self.mini_board_wins[6]:
                win = self.mini_board_wins[4]
            if self.mini_board_wins[4] == self.mini_board_wins[3] == self.mini_board_wins[5]:
                win = self.mini_board_wins[4]
            if self.mini_board_wins[4] == self.mini_board_wins[1] == self.mini_board_wins[7]:
                win = self.mini_board_wins[4]
        if self.mini_board_wins[8] != 0:
            if self.mini_board_wins[8] == self.mini_board_wins[2] == self.mini_board_wins[5]:
                win = self.mini_board_wins[8]
            if self.mini_board_wins[8] == self.mini_board_wins[6] == self.mini_board_wins[7]:
                win = self.mini_board_wins[8]
        return win

    def getBoard(self):
        return self.board


if __name__ == '__main__':
    board = Board()
    print(board.board)
