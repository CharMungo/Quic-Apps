from PySide6.QtWidgets import QApplication, QWidget, QMainWindow, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QPushButton, QButtonGroup, QComboBox
from PySide6.QtCore import Qt, QSize, QEvent
from PySide6.QtGui import QFont
import math
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        bodyFont = QFont()
        bodyFont.setPointSize(8)

        ##Home Page Stuff##
        
        self.setWindowTitle('Calculations')

        self.homepage = QVBoxLayout()
        self.hometitle = QLabel('Home Page')
        self.hometitle.hide()
        self.homecon = QLabel('A quick and easy calculator to help with electrical and geometical equasions')
        self.homecon.hide()
        self.homecon.setWordWrap(True)
        self.homepage.addWidget(self.hometitle)
        self.homepage.addWidget(self.homecon)

        ##Buttons##
        self.buttons = QHBoxLayout()
        self.buttongroup = QButtonGroup()
        self.homebut = QPushButton('Home')
        self.elecbut = QPushButton('Electrical')
        self.geombut = QPushButton('Geometrical')
        self.homebut.setCheckable(True)
        self.elecbut.setCheckable(True)
        self.geombut.setCheckable(True)
        self.buttons.addWidget(self.homebut)
        self.buttons.addWidget(self.elecbut)
        self.buttons.addWidget(self.geombut)
        self.buttongroup.addButton(self.homebut)
        self.buttongroup.addButton(self.elecbut)
        self.buttongroup.addButton(self.geombut)
        self.homebut.clicked.connect(self.home)
        self.elecbut.clicked.connect(self.elec)
        self.geombut.clicked.connect(self.geom)
        self.buttongroup.setExclusive(True)

        ##electrical page stuff##
        self.elecpage = QVBoxLayout()
        self.electitle = QLabel('Electrical')
        self.electitle.hide()
        self.eleccon = QLabel()
        self.elecunits = ['Current(I/Amps)', 'Voltage(V,Volts)', 'Resistance(R/Ohms)', 'Power(P/Watts)']
        self.elecunit1 = QComboBox()
        self.elecunit2 = QComboBox()
        self.elecunit1.addItems(self.elecunits)
        self.elecunit2.addItems(self.elecunits)
        self.elecpage.addWidget(self.electitle)
        self.elecpage.addWidget(self.eleccon)

        ##geometrical page stuff##
        self.geompage = QVBoxLayout()
        self.geomtitle = QLabel('Geometrical')
        self.geomtitle.hide()
        self.geomcon = QLabel()
        self.geomcon.hide()
        self.shapes = ['Circle', 'Eclipse', 'Triangle', 'Square', 'Rectangle', 'Sphere', 'Cylinder', 'Pyrmid', 'Cone', 'Cube', 'Cuboid']
        self.shapeop = QComboBox()
        self.shapeop.hide()
        self.shapeop.addItems(self.shapes)
        self.geompage.addWidget(self.geomtitle)
        self.geompage.addWidget(self.shapeop)
        self.geompage.addWidget(self.geomcon)
       
        ##Inputs and Boxs##
        self.iandus = QHBoxLayout()
        self.input1 = QLineEdit()
        self.input2 = QLineEdit()
        self.input3 = QLineEdit()
        self.input1.hide()
        self.input2.hide()
        self.input3.hide()
        self.iandus.addWidget(self.input1)
        self.iandus.addWidget(self.elecunit1)
        self.iandus.addWidget(self.input2)
        self.iandus.addWidget(self.elecunit2)
        self.iandus.addWidget(self.input3)

        ##Calculate##
        self.calcbut = QPushButton('Calculate')
        self.calcbut.clicked.connect(self.calc)

        ##Left Page##
        leftLayout = QVBoxLayout()
        leftLayout.addLayout(self.homepage)
        leftLayout.addLayout(self.elecpage)
        leftLayout.addLayout(self.geompage)
        leftLayout.addLayout(self.iandus)
        leftLayout.addLayout(self.buttons)
        leftLayout.addWidget(self.calcbut)
        leftCon = QWidget()
        leftCon.setLayout(leftLayout)
        leftCon.setFixedSize(400, 300)

        ##Right Page##
        self.pastResults = QLabel()
        rightLayout = QVBoxLayout()
        rightLayout.addWidget(self.pastResults)
        rightCon = QWidget()
        rightCon.setLayout(rightLayout)
        rightCon.setFixedSize(200, 300)
        
        ##Left and Right Sections together##
        mainLayout = QHBoxLayout()
        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout.addWidget(leftCon)
        mainLayout.addWidget(rightCon)
        container = QWidget()
        container.setLayout(mainLayout)
        self.setFixedSize(600, 300)
        self.setCentralWidget(container)

        ##Start-up##
        self.home()
        self.homebut.setChecked(True)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()
        elif event.key() == Qt.Key_Return:
            self.calc()
        else:
            super().keyPressEvent(event)

    def eventFilter(self, obj, event):
        if obj == self.input1 and event.type() == QEvent.Type.KeyPress:
            if event.key() == Qt.Key_Tab:
                self.switchPage()
                return True
        if obj == self.input2 and event.type() == QEvent.Type.KeyPress:
            if event.key() == Qt.Key_Tab:
                self.switchPage()
                return True
        if obj == self.input3 and event.type() == QEvent.Type.KeyPress:
            if event.key() == Qt.Key_Tab:
                self.switchPage()
                return True
        return False

    def switchPage(self):
        if self.homebut.isChecked():
            self.elecbut.setChecked(True)
            self.elec()
            return
        elif self.elecbut.isChecked():
            self.geombut.setChecked(True)
            self.geom()
            return
        elif self.geombut.isChecked():
            self.homebut.setChecked(True)
            self.home()
            return
        return

    def home(self):
        self.hometitle.show()
        self.homecon.show()
        self.electitle.hide()
        self.eleccon.hide()
        self.geomtitle.hide()
        self.geomcon.hide()
        self.input1.show()
        self.input2.hide()
        self.input3.hide()
        self.elecunit1.hide()
        self.elecunit2.hide()
        self.shapeop.hide()
        return

    def elec(self):
        self.hometitle.hide()
        self.homecon.hide()
        self.electitle.show()
        self.eleccon.show()
        self.geomtitle.hide()
        self.geomcon.hide()
        self.input1.show()
        self.input2.show()
        self.input3.hide()
        self.elecunit1.show()
        self.elecunit2.show()
        self.shapeop.hide()
        return

    def geom(self):
        self.hometitle.hide()
        self.homecon.hide()
        self.electitle.hide()
        self.eleccon.hide()
        self.geomtitle.show()
        self.geomcon.show()
        self.input1.show()
        self.input2.hide()
        self.input3.hide()
        self.elecunit1.hide()
        self.elecunit2.hide()
        self.shapeop.show()
        return

    def pastResultList(self):
        if self.pastResults.text() == '':
            self.pastResults.setText(self.result)
        elif not self.pastResults.text() == '':
            currentResults = self.pastResults.text()
            newResults = f'{currentResults}\n{self.result}'
            self.pastResults.setText(newResults)
        return

    def calc(self):
        calcin1 = self.input1.text()
        calcin2 = self.input2.text()
        calcin3 = self.input3.text()
        self.input1.clear()
        self.input2.clear()
        self.input3.clear()
        if self.homebut.isChecked():
            calccle = calcin1.strip().replace(' ', '')
            self.result = calcin1
        elif self.elecbut.isChecked():
            self.result = 'elec result'
        elif self.geombut.isChecked():
            self.result = 'geom result'
        self.pastResultList()
        return

app = QApplication(sys.argv)
window = MainWindow()
window.show()

app.exec()
