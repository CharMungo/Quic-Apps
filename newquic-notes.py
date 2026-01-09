import os
import sys
from PySide6.QtWidgets import QApplication, QWidget, QMainWindow, QMenu, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QPushButton
from pathlib import Path
from PySide6.QtCore import Qt, QSize, QEvent
from PySide6.QtGui import QFont
from dotenv import load_dotenv, dotenv_values

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
		
        self.setWindowTitle('Quick Notes')
        self.setFixedSize(300, 500)
		
        font = QFont()
		
        self.currentNoteNum = QLabel()
        self.input = QLineEdit()
        self.settingsButton = QPushButton("")
        self.settingsButton.setFixedSize(20, 20)
        self.note = QLabel()
        self.note.setFont(font)
        self.note.setWordWrap(True)
        self.addLineButton = QPushButton('Add')
        self.addLineButton.clicked.connect(self.addLine)
        self.remLineButton = QPushButton('Remove')
        self.remLineButton.clicked.connect(self.remLine)
        self.cycleListButton = QPushButton('Cycle Lists')
        self.cycleListButton.clicked.connect(self.cycleList)
        self.newListButton = QPushButton('New List')
        self.newListButton.clicked.connect(self.newList)
		
        topLayout = QHBoxLayout()
        topLayout.addWidget(self.currentNoteNum)
        topLayout.addWidget(self.input)
        topLayout.addWidget(self.settingsButton)

        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.addLineButton)
        buttonLayout.addWidget(self.remLineButton)
        buttonLayout.addWidget(self.cycleListButton)
        buttonLayout.addWidget(self.newListButton)

        self.currentNoteContents = QLabel()

        pageLayout = QVBoxLayout()
        pageLayout.addLayout(topLayout)
        pageLayout.addLayout(buttonLayout)
        pageLayout.addWidget(self.currentNoteContents)
		
        container = QWidget()
        container.setLayout(pageLayout)

        load_dotenv()
        self.directory = os.getenv("DIRECTORY")

        self.setCentralWidget(container)
    
        print(f"Searching for .todo files in {self.directory}")
        self.allFilesInDirectory = os.listdir(self.directory)
        if not self.allFilesInDirectory:
            print('No todo files found - creating .todo1')
            with open (f"{self.directory}.todo1.txt", 'x'):
                pass
            self.allFilesInDirectory = os.listdir(self.directory)
        
        self.indexFiles()
        self.fileIndexNum = 0
        self.currentNoteNum.setText(str(self.fileIndexNum))
        self.currentFile = f"{self.directory}.todo{self.fileNumList[self.fileIndexNum]}.txt"
        self.readFile()


    def indexFiles(self):
        self.fileList = []
        self.fileNumList = []
        self.allFilesInDirectory = os.listdir(self.directory)
        for filename in self.allFilesInDirectory:
            if filename.startswith('.todo') and filename.endswith('.txt'):
                self.fileList.append(filename)
                self.fileList.sort()
                self.fileNumList.append(filename[5:-4])
                self.fileNumList.sort()
        print(f".todo files:{self.fileList}")
        print(f".todo file numbers{self.fileNumList}")

    def cycleList(self):
        self.fileIndexNum = (self.fileIndexNum + 1) % len(self.fileNumList)
        self.currentFile = f"{self.directory}.todo{self.fileNumList[self.fileIndexNum]}.txt"
        self.currentNoteNum.setText(str(self.fileIndexNum))
        self.checkEmptyLists()
        self.readFile()

    def checkEmptyLists(self):
        for file in self.allFilesInDirectory:
            with open(f"{self.directory}{file}", "r") as f:
                contents = f.read()
            if contents == "":
                os.remove(f"{self.directory}{file}")
                self.indexFiles()

    def readFile(self):
        with open(self.currentFile, "r") as f:
            lines = f.read()
            array = lines.splitlines()
            listed = []
            num = 1
            for line in array:
                listed.append(f'{str(num)}.{line}')
                num +=1
            self.currentNoteContents.setText('\n'.join(listed))

    def newList(self):
        if ".todo1.txt" not in self.fileList:
            with open(f"{self.directory}.todo1.txt", "x"):
                print(f"New file made: {self.directory}.todo1.txt")
                self.currentFile = f"{self.directory}.todo1.txt"
                self.indexFiles()
                self.readFile()
                return
        else:

            for x in self.fileNumList:
                if str(int(x) + 1) not in self.fileNumList:
                    with open(f"{self.directory}.todo{int(x) + 1}.txt", "x"):
                        print(f"New file made: {self.directory}.todo{int(x) + 1}.txt")
                        self.currentFile = f"{self.directory}.todo{int(x) + 1}.txt"
                        self.indexFiles()
                        self.readFile()
                        return
    def addLine(self):
        with open(self.currentFile, 'a') as f:
            f.write(f'\n{self.input.text()}')
        self.input.clear()
        self.readFile()

    def remLine(self):
        with open(self.currentFile, 'r') as f:
            lines = f.read()
            line = lines.splitlines()
            line.pop(int(self.input.text())-1)
            self.newLines = '\n'.join(line)
        with open(self.currentFile, 'w') as f:
            f.write(self.newLines)
        self.readFile()


app = QApplication(sys.argv)
window = MainWindow()
window.show()

app.exec()
