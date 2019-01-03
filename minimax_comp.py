PLAYER_NO = 3
COMP_NO = 5


class MinimaxComp():
    def __init__(self):
        pass

    def getPossibleMoves(self, board, previous_move, mini_board_wins):
        if previous_move[1] == -1:
            # can pick any mini board from the big board
            moves = [[(big, mini) for mini in range(len(board[big])) if (
                (board[big][mini] == 0) and (mini_board_wins[big] == 0))] for big in range(len(board))]
            return [item for sublist in moves for item in sublist]
        else:
            # have to pick a move from a particular mini board
            return [(previous_move[1], x) for x in range(len(board[previous_move[1]])) if board[previous_move[1]][x] == 0]

    def chooseMove(self, board, depth, isMaximising, previous_move, mini_board_wins):
        best_move = None
        possible_moves = self.getPossibleMoves(board, previous_move)
        if self.checkWin(board, COMP_NO):
            return (+10 + depth), best_move
        elif self.checkWin(mini_board_wins, PLAYER_NO):
            return (-10 - depth), best_move
        elif len(possible_moves) == 0 or depth == 0:
            mini_count = len(list(filter(lambda x: x == COMP_NO, mini_board_wins))) if isMaximising else -len(
                list(filter(lambda x: x == PLAYER_NO, mini_board_wins)))
            return mini_count, best_move
        else:
            if isMaximising:
                best_score = -self.infinity
                for move in possible_moves:
                    board[move[0]][move[1]] = COMP_NO
                    if self.checkWin(board[move[0]], COMP_NO):
                        mini_board_wins[move[1]] = COMP_NO
                        score, best_move_at_lower_level = self.chooseMove(
                            board, depth - 1, (not isMaximising), (-1, move[1]), mini_board_wins)
                    else:
                        score, best_move_at_lower_level = self.chooseMove(
                            board, depth - 1, (not isMaximising), move, mini_board_wins)
                    board[move[0]][move[1]] = 0
                    mini_board_wins[move[1]] = 0
                    if score > best_score:
                        best_score = score
                        best_move = move
            else:
                best_score = +self.infinity
                for move in possible_moves:
                    board[move[0]][move[1]] = PLAYER_NO
                    if self.checkWin(board[move[0]], PLAYER_NO):
                        mini_board_wins[move[1]] = PLAYER_NO
                        score, best_move_at_lower_level = self.chooseMove(
                            board, depth - 1, (not isMaximising), (-1, move[1]), mini_board_wins)
                    else:
                        score, best_move_at_lower_level = self.chooseMove(
                            board, depth - 1, (not isMaximising), move, mini_board_wins)
                    board[move[0]][move[1]] = 0
                    mini_board_wins[move[1]] = 0
                    if score < best_score:
                        best_score = score
                        best_move = move
            return best_score, best_move

    def checkWin(self, board, player):
        win_score = 3 * player
        return (
            (board[0] + board[1] + board[2] == win_score) or
            (board[3] + board[4] + board[5] == win_score) or
            (board[6] + board[7] + board[8] == win_score) or
            (board[0] + board[3] + board[6] == win_score) or
            (board[1] + board[4] + board[7] == win_score) or
            (board[2] + board[5] + board[8] == win_score) or
            (board[0] + board[4] + board[8] == win_score) or
            (board[2] + board[4] + board[6] == win_score)
        )


if __name__ == '__main__':
    board = [
        [3, 5, 0, 3, 0, 0],
        [4, 5, 6, 0, 2, 0],
        [0, 0, 0, 0, 0, 0],
        [1, 2, 3, 4, 5, 6]
    ]
    mc = MinimaxComp()
    print(mc.getPossibleMoves(board, (0, -1)))
    print(mc.getPossibleMoves(board, (0, 0)))
