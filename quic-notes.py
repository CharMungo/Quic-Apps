from PySide6.QtWidgets import QApplication, QWidget, QMainWindow, QMenu, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QPushButton
from pathlib import Path
from PySide6.QtCore import Qt, QSize, QEvent
from PySide6.QtGui import QFont
import os
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle('Quick Notes')
        self.setFixedSize(300, 500)

        font = QFont()
        font.setPointSize(12)

        self.input = QLineEdit()
        self.notenum = QLabel()
        self.note = QLabel()
        self.note.setFont(font)
        self.note.setWordWrap(True)
        self.var = QLabel()
        self.input.textChanged.connect(self.var.setText)
        self.addb = QPushButton('Add Line')
        self.remb = QPushButton('Remove Line')
        self.lisb = QPushButton('Cycle Lists')
        
        header = QHBoxLayout()
        header.addWidget(self.notenum)
        header.addWidget(self.input)

        buttonlay = QHBoxLayout()
        buttonlay.addWidget(self.addb)
        buttonlay.addWidget(self.remb)
        buttonlay.addWidget(self.lisb)
        
        layout = QVBoxLayout()
        layout.addLayout(header)
        layout.addLayout(buttonlay)
        layout.addWidget(self.note)
        

        container = QWidget()
        container.setLayout(layout)

        self.directory = '/home/mungo/'

        self.setCentralWidget(container)
        
        self.filenum = 1
        self.file = f'/home/mungo/.todo{self.filenum}.txt'

        self.total()
        self.read()

        self.addb.clicked.connect(self.add)        
        self.remb.clicked.connect(self.rem)
        self.lisb.clicked.connect(self.switchlist)
        self.input.installEventFilter(self)
    
    def total(self):
        files = os.listdir(self.directory)
        self.amount = 0
        for file in files:
            if '.todo' and '.txt' in file:
                self.amount += 1
        return

    def eventFilter(self, obj, event):
        if obj == self.input and event.type() == QEvent.Type.KeyPress:
            if event.key() == Qt.Key_A and event.modifiers() == Qt.ControlModifier:
                self.add()
                self.input.clear()
                return True
            elif event.key() == Qt.Key_A and event.modifiers() == Qt.AltModifier:
                self.add()
                return True
            elif event.key() == Qt.Key_D and event.modifiers() == Qt.ControlModifier:
                self.rem()
                self.input.clear()
                return True
            elif event.key() == Qt.Key_D and event.modifiers() == Qt.AltModifier:
                self.rem()
                return True
            elif event.key() == Qt.Key_Tab:
                self.switchlist()
                return True
        return super().eventFilter(obj, event)


    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()
        elif event.key() == Qt.Key_Return:
            self.add()
            self.input.clear()
        else:
            super().keyPressEvent(event)
        
    def switchlist(self):
        if self.filenum == self.amount:
            self.filenum = 1
        else:
            self.filenum += 1
        self.file = f'/home/mungo/.todo{self.filenum}.txt'
        self.read()

    def autorm(self):
        return

    def new(self, line):
        self.amount += 1
        file = f'/home/mungo/.todo{self.amount}.txt'
        with open(file, 'x'):
            pass
        with open(file, 'a') as f:
            f.write(line)
        self.file = f'/home/mungo/.todo{self.amount}.txt'
        print(self.file)
        self.notenum.setText(str(self.amount))
        self.filenum = self.amount
        self.read()

    def read(self):
        path = Path('self.file' + str(self.filenum))
        file = self.file
        self.notenum.setText(str(self.filenum))
        with open(file, 'r') as f:
            lines = f.readlines()
        
        cline = [line.strip() for line in lines if line.strip() != '']

        with open(file, 'w') as f:
            for line in cline:
                f.write(line + '\n')

        if not cline:
            self.note.setText('No lines to display')
        else:
            text = ''
            for num, line in enumerate(cline, start=1):
                text += f'{num}. {line.strip()}\n'
            self.note.setText(text)

    def rem(self):
        torem = int(self.var.text())
        file = self.file 
        with open(file, 'r') as f:
            lines = f.readlines()
            index = torem - 1
            lines.pop(index)

        with open(file, 'w') as f:
            for num, line in enumerate(lines, start=1):
                f.write(line)
        self.read()

    def add(self):
        toadd = self.var.text()
        if ':' in toadd:
            preline = toadd.split(':')
            line = preline[0]
            print(line)
            self.new(line)
            return True
        else:
            file = self.file
            with open(file, 'a') as f:
                f.write(f'\n{toadd}')
            self.read()


app = QApplication(sys.argv)
window = MainWindow()
window.show()

app.exec()

