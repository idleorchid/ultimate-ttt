import math
import random
import copy
# https://en.wikipedia.org/wiki/Ultimate_tic-tac-toe#Computer_implementations
# https://en.wikipedia.org/wiki/Monte_Carlo_tree_search
# https://www.baeldung.com/java-monte-carlo-tree-search
# https://en.wikipedia.org/wiki/Monte_Carlo_method#Artificial_intelligence_for_games

# cloning methods for Node and State

class MonteCarloComp():
    def __init__(self):
        self.WIN_SCORE = 10
        self.ITERATIONS = 500

    def monteCarlo(self, current_board, previous_move, mini_board_wins):
        iter_count = 0
        tree = Node(None, True, current_board,
                         mini_board_wins, previous_move)
        while iter_count < self.ITERATIONS:
            tree = self.monteCarloIteration(tree, previous_move, mini_board_wins)
            iter_count += 1
        return tree.getChildWithMaxScore().state.move

    def monteCarloIteration(self, tree, previous_move, mini_board_wins):
        node = tree
        # phase 1 - selection
        while len(node.getChildren()) > 0:
            node = node.getBestNode()

        # phase 2 - expansion
        if not (self.checkWin(node.state.mini_board_wins, node.state.COMP_NO) or self.checkWin(node.state.mini_board_wins, node.state.PLAYER_NO)):
            possible_moves = node.state.getPossibleMoves()  
            # create child node for each possible move from the current node
            for (big, mini) in possible_moves:
                new_child_board = copy.deepcopy(node.state.board)
                new_child_board[big][mini] = node.state.getPlayerNo()

                new_mini_board_wins = copy.deepcopy(node.state.mini_board_wins)
                new_mini_board_wins[big] = self.checkIfWinOnMiniBoard(
                    new_child_board[big])

                new_child = Node(node, node.state.isOpponentComp(),
                                new_child_board, new_mini_board_wins, (big, mini))
                node.addChild(new_child)
        # phase 3 - simulation
        explore_node = node
        if len(node.children) > 0:
            explore_node = random.choice(node.children)
        sim_result = self.simulateRandomGame(explore_node)
        # phase 4 - update (back propagation)
        self.backPropagation(explore_node, sim_result)
        return tree

    def simulateRandomGame(self, node):
        sim_node = node.clone()
        sim_state = sim_node.state
        board_win = 0
        hasGameFinished = self.checkWin(sim_state.mini_board_wins, sim_state.getPlayerNo())
        if hasGameFinished or len(sim_state.getPossibleMoves()) == 0:
            board_win = sim_state.getPlayerNo()

        hasGameFinished = self.checkWin(sim_state.mini_board_wins, sim_state.getOpponentNo())
        if hasGameFinished:
            board_win = sim_state.getOpponentNo()
        if board_win == sim_state.getOpponentNo():
            sim_node.parent.state.win_score = -sim_node.infinity
            return sim_state.getOpponentNo()
        
        while board_win == 0:
            sim_state.swapPlayer()
            possible_moves = sim_state.getPossibleMoves()
            big_move, mini_move = random.choice(possible_moves)
            sim_state.board[big_move][mini_move] = sim_state.getPlayerNo()
            sim_state.mini_board_wins[big_move] = self.checkIfWinOnMiniBoard(sim_state.board[big_move])
            if sim_state.mini_board_wins[mini_move] != 0:
                mini_move = -1
            sim_state.setMove((big_move, mini_move))
            hasGameFinished = self.checkWin(sim_state.mini_board_wins, sim_state.getPlayerNo())
            if hasGameFinished or len(sim_state.getPossibleMoves()) == 0:
                board_win = sim_state.getPlayerNo()
        return board_win

    def backPropagation(self, explore_node, sim_result):
        temp_node = explore_node.clone()
        while temp_node != None:
            temp_node.state.visit_count+=1
            if temp_node.state.getPlayerNo() == sim_result:
                temp_node.state.win_score += self.WIN_SCORE
            temp_node = temp_node.parent

    def getPossibleMoves(self, board, previous_move, mini_board_wins):
        if previous_move[1] == -1:
            # can pick any mini board from the big board
            moves = [[(big, mini) for mini in range(len(board[big])) if (
                (board[big][mini] == 0) and (mini_board_wins[big] == 0))] for big in range(len(board))]
            return [item for sublist in moves for item in sublist]
        else:
            # have to pick a move from a particular mini board
            return [(previous_move[1], x) for x in range(len(board[previous_move[1]])) if board[previous_move[1]][x] == 0]

    def checkIfWinOnMiniBoard(self, mini_board):
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
        # mini_board_wins[mini_board_num] = win
        return win# != 0

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

class Node():
    def __init__(self, parent, is_comp, board=[], mini_board_wins=[], move=(-1, -1)):
        self.infinity = float("inf")
        self.parent = parent
        self.children = []
        self.state = State(is_comp)
        if len(board) > 0:
            self.state.updateBoard(board, mini_board_wins, move)


    def addChild(self, new_child):
        self.children.append(new_child)

    def getChildren(self):
        return self.children

    def getBestNode(self):
        max_uct = 0
        best_node = None
        for node in self.children:
            node_uct = node.calcUCT()
            if node_uct > max_uct:
                max_uct = node_uct
                best_node = node
        return best_node


    def calcUCT(self):
        # should move to State
        exploration_param = 1.41
        if self.state.getVisitCount() == 0:
            return self.infinity
        else:
            return (self.state.getWinScore() / self.state.getVisitCount()) + (exploration_param * math.sqrt(math.log(self.parent.state.getVisitCount()) / self.state.getVisitCount()))

    def getChildWithMaxScore(self):
        best_child = self.children[0]
        for child in self.children:
            if child.state.visit_count > best_child.state.visit_count:
                best_child = child
        return best_child

    def clone(self):
        clone_node = Node(self.parent, self.state.is_comp)
        clone_node_state = self.state.clone()
        clone_node.state = clone_node_state
        for child in self.children:
            clone_node.addChild(child.clone())
        return clone_node


class State():
    def __init__(self, is_comp):
        self.PLAYER_NO = 3
        self.COMP_NO = 5
        self.board = []
        self.mini_board_wins = []
        self.visit_count = 0
        self.win_score = 0
        # if computer is the player that plays next (their potential moves lead from this state into the states of the child nodes)
        self.is_comp = is_comp
        # move required to get to this state from the state of the parent node
        self.move = ()

    def updateBoard(self, board, mini_board_wins, move):
        self.board = board
        self.mini_board_wins = mini_board_wins
        self.move = move

    def setMove(self, move):
        self.move = move

    def getPossibleMoves(self):
        if self.move[1] == -1:
            # can pick any mini board from the big board
            moves = [[(big, mini) for mini in range(len(self.board[big])) if (
                (self.board[big][mini] == 0) and (self.mini_board_wins[big] == 0))] for big in range(len(self.board))]
            return [item for sublist in moves for item in sublist]
        else:
            # have to pick a move from a particular mini board
            return [(self.move[1], x) for x in range(len(self.board[self.move[1]])) if self.board[self.move[1]][x] == 0]

    def getWinScore(self):
        return self.win_score

    def getVisitCount(self):
        return self.visit_count

    def getPlayerNo(self):
        return self.COMP_NO if self.is_comp else self.PLAYER_NO
    
    def getOpponentNo(self):
        return self.PLAYER_NO if self.is_comp else self.COMP_NO

    def isOpponentComp(self):
        return not self.is_comp
    
    def swapPlayer(self):
        self.is_comp = not self.is_comp

    def clone(self):
        clone_state = State(self.is_comp)
        clone_state.updateBoard(copy.deepcopy(self.board), copy.deepcopy(self.mini_board_wins), self.move)
        clone_state.visit_count = self.visit_count
        clone_state.win_score = self.win_score
        return clone_state

