from PyQt5 import QtCore
from PyQt5.QtWidgets import QLabel, QWidget, QGridLayout, QGroupBox, QMessageBox, QVBoxLayout
from PyQt5.QtGui import QPixmap
import custom_label as cl
import minimax_comp as mc
import monte_carlo_comp as mcc
import copy

PLAYER_NO = 3
COMP_NO = 5
CELL_WIDTH = 50

# add move history
# highlight cell that the next move should be played in
# display the giant pieces slightly transparent to see the board underneath


class BoardManager():
    def __init__(self, main_window, main_layout):
        self.main_window = main_window
        self.main_layout = QVBoxLayout()
        self.board = self.initBoard()
        self.mini_board_wins = [0] * 9
        # previous move dictates that the start move can be in any big cell
        self.previous_move = (0, -1)
        self.player_turn = True
        self.comp_player = mcc.MonteCarloComp()
        self.grid_dict = {
            0 : "top left",
            1 : "top middle",
            2 : "top right",
            3 : "middle Left",
            4 : "centre",
            5 : "middle right",
            6 : "bottom left",
            7 : "bottom middle",
            8 : "bottom right",
        }
        self.just_finished_grid = -1

    def initBoard(self):
        return [[0 for y in range(9)] for x in range(9)]

    def displayBoard(self):
        self.clearLayout()
        main_grid_layout = QGridLayout()
        for x in range(9):
            mini_layout = QGridLayout()
            group_box = QGroupBox()
            if (self.mini_board_wins[x] == 0):
                for cell in range(9):
                    if (self.board[x][cell] == 3):
                        pixmap = QPixmap('X.png')
                    elif (self.board[x][cell] == 5):
                        pixmap = QPixmap('O.png')
                    else:
                        pixmap = QPixmap('blank.png')
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
            main_grid_layout.addWidget(group_box, x // 3, x % 3)
        last_move_label = QLabel()
        last_move_string = 'Last move: ' + self.grid_dict[self.previous_move[0]] + ' of '
        if self.previous_move[1] < 0:
            if self.just_finished_grid < 0:
                last_move_string = 'No previous move - play anywhere.'
            else:
                last_move_string += self.grid_dict[self.just_finished_grid] + ' (play anywhere)'
        else:
            last_move_string += '<u>' + self.grid_dict[self.previous_move[1]] + '</u>'
        last_move_label.setText(last_move_string)
        last_move_label.setStyleSheet('color: white; font-size:15px;')
        last_move_label.setAlignment(QtCore.Qt.AlignCenter)
        v_group_box = QGroupBox()
        v_group_box.setLayout(main_grid_layout)
        self.main_layout.addWidget(last_move_label)
        self.main_layout.addWidget(v_group_box)
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
                    self.updateWinStatus(big_cell)
                    self.player_turn = not self.player_turn
                    self.displayBoard()
                    comp_move = self.comp_player.monteCarlo(copy.deepcopy(self.board), self.previous_move, copy.deepcopy(self.mini_board_wins))
                    # score, comp_move = self.comp_player.chooseMove(self.board[:], 5, True, self.previous_move, self.mini_board_wins[:])
                    self.previous_move = comp_move
                    self.board[comp_move[0]][comp_move[1]] = COMP_NO
                    self.updateWinStatus(comp_move[0])
                    self.player_turn = not self.player_turn
                    self.displayBoard()
                else:
                    QMessageBox.about(
                        self.main_window, "Invalid Move", "You cannot make this move.")
        # else:
        #     if self.isMoveOnBoard((big_cell, mini_cell)):
        #         if (self.isValidMoveByRules((big_cell, mini_cell))):
        #             self.previous_move = (big_cell, mini_cell)
        #             self.board[big_cell][mini_cell] = COMP_NO
        #             self.player_turn = not self.player_turn
        #             self.displayBoard()
        #         else:
        #             QMessageBox.about(
        #                 self.main_window, "Invalid Move", "You cannot make this move.")
        # self.checkIfWinOnMiniBoard(self.previous_move[0])
        # if (self.checkIfWinOnMiniBoard(self.previous_move[1])):
        #     self.previous_move = (self.previous_move[0], -1)
        #     self.displayBoard()
        #     print('Win:', self.checkIfWinOnBigBoard())

    def updateWinStatus(self, big_cell):
        self.checkIfWinOnMiniBoard(big_cell)
        print(self.mini_board_wins)
        if (self.checkIfWinOnMiniBoard(self.previous_move[1])):
            self.just_finished_grid = self.previous_move[1]
            self.previous_move = (self.previous_move[0], -1)

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
            print('board:', self.board)
            mini_board = self.board[mini_board_num]
            win = 0
            print('mini board:', mini_board)
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
            print('win:', win)
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

# if __name__ == '__main__':
#     board = Board()
#     print(board.board)
