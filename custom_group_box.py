from PyQt5.QtWidgets import QGroupBox

class CustomGroupBox(QGroupBox):
    def __init__(self, cell_num):
        QGroupBox.__init__(self)
        self.cell_num = cell_num

    def mousePressEvent(self, event):
        print(self.cell_num)
