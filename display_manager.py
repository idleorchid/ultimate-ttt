class DisplayManager():
    def __init__(self):
        self.big_board_list = []
        self.mini_board_list = []

    def clearMiniBoardList(self):
        self.mini_board_list = []

    def addToMiniBoardList(self, pos, item):
        self.mini_board_list.insert(pos, item)

    def getIndexInMiniBoardList(self, item):
        return self.mini_board_list.indexOf(item)

    def clearBigBoardList(self):
        self.big_board_list = []

    def addToBigBoardList(self, pos, item):
        self.big_board_list.insert(pos, item)

    def getIndexInBigBoardList(self, item):
        return self.big_board_list.indexOf(item)
