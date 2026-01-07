from PySide6.QtWidgets import QApplication, QWidget, QMainWindow, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QPushButton, QButtonGroup, QComboBox
from PySide6.QtCore import Qt, QSize, QEvent
from PySide6.QtGui import QFont
import math
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Calculations')

        self.hometitle = QLabel('Home page')
        self.homecon = QLabel('A quick and easy calculator to help with electrical and geometical equasions')
        self.homecon.setWordWrap(True)
        self.homepage = QHBoxLayout()
        self.homepage.addWidget(self.hometitle)
        self.homepage.addWidget(self.homecon)
        self.eleccon = QLabel('Elec')
        self.geomcon = QLabel('Geom')
        self.hometitle.show()
        self.eleccon.hide()
        self.geomcon.hide()

        self.input1 = QLineEdit()
        self.input2 = QLineEdit()
        self.input3 = QLineEdit()
        self.input1.show()
        self.input2.hide()
        self.input3.hide()

        buttons = QHBoxLayout()
        self.buttongroup = QButtonGroup()
        self.homeb = QPushButton('Home')
        self.elecb = QPushButton('Elec')
        self.geomb = QPushButton('Geom')
        self.homeb.setCheckable(True)
        self.homeb.setChecked(True)
        self.elecb.setCheckable(True)
        self.geomb.setCheckable(True)
        buttons.addWidget(self.homeb)
        buttons.addWidget(self.elecb)
        buttons.addWidget(self.geomb)
        self.buttongroup.addButton(self.elecb)
        self.buttongroup.addButton(self.geomb)
        self.buttongroup.addButton(self.homeb)
        self.buttongroup.setExclusive(True)

        self.geomtypes = ['2D Area', '3D Volume', '2D Sides']
        self.geomtype = QComboBox()
        self.geomtype.hide()
        self.geomtype.addItems(self.geomtypes)
        self.twodshapes = ['Circle', 'Eclipse', 'Triangle', 'Square', 'Rectangle']
        self.threedshapes = ['Sphere', 'Cylinder', 'pyrmid', 'Cone', 'Cube', 'Cuboid']
        self.shape = QComboBox()
        self.shape.hide()
        self.heightlab = QLabel('Height')
        self.heightlab.hide()
        self.widthlab = QLabel('Width')
        self.widthlab.hide()
        self.radiuslab = QLabel('Radius')
        self.radiuslab.hide()

        self.geomchoice = QHBoxLayout()
        self.geomchoice.addWidget(self.geomtype)
        self.geomchoice.addWidget(self.shape)

        self.elecunits = ['Current(I/Amps)', 'Voltage(V/Volts)', 'Resistance(R/Ohms)', 'Power(P/Watts)']
        self.elecunit1 = QComboBox()
        self.elecunit1.hide()
        self.elecunit1.addItems(self.elecunits)
        self.elecunit2 = QComboBox()
        self.elecunit2.hide()
        self.elecunit2.addItems(self.elecunits)
        self.geomunits = ['None', 'Width', 'Height', 'Depth', 'Radius']
        self.geomunit1 = QComboBox()
        self.geomunit1.hide()
        self.geomunit1.addItems(self.geomunits)
        self.geomunit2 = QComboBox()
        self.geomunit2.hide()
        self.geomunit2.addItems(self.geomunits)
        self.geomunit3 = QComboBox()
        self.geomunit3.hide()
        self.geomunit3.addItems(self.geomunits)

        self.unitlay = QHBoxLayout()
        self.unitlay.addWidget(self.input1)
        self.unitlay.addWidget(self.elecunit1)
        self.unitlay.addWidget(self.geomunit1)
        self.unitlay.addWidget(self.input2)
        self.unitlay.addWidget(self.elecunit2)
        self.unitlay.addWidget(self.geomunit2)
        self.unitlay.addWidget(self.input3)
        self.unitlay.addWidget(self.geomunit3)

        self.calbutton = QPushButton('Calculate')
        self.calbutton.clicked.connect(self.cal)

        leftlayout = QVBoxLayout()
        leftlayout.addLayout(self.geomchoice)
        leftlayout.addLayout(self.homepage)
        leftlayout.addWidget(self.eleccon)
        leftlayout.addWidget(self.geomcon)
        leftlayout.addLayout(self.unitlay)
        leftlayout.addLayout(buttons)
        leftlayout.addWidget(self.calbutton)
        leftcon = QWidget()
        leftcon.setLayout(leftlayout)
        leftcon.setFixedSize(400, 300)

        self.results = QLabel()
        rightlayout = QHBoxLayout()
        rightlayout.addWidget(self.results)
        rightcon = QWidget()
        rightcon.setLayout(rightlayout)
        rightcon.setFixedSize(200, 300)

        mainlayout = QHBoxLayout()
        mainlayout.setContentsMargins(0, 0, 0, 0)
        mainlayout.addWidget(leftcon)
        mainlayout.addWidget(rightcon)

        container = QWidget()
        container.setLayout(mainlayout)
        self.setFixedSize(600, 300)

        self.setCentralWidget(container)
        self.homeb.clicked.connect(self.home)
        self.elecb.clicked.connect(self.elec)
        self.geomb.clicked.connect(self.geom)

        self.input1.installEventFilter(self)
        self.input2.installEventFilter(self)
        self.input3.installEventFilter(self)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()
        elif event.key() == Qt.Key_Return:
            self.cal()
        elif event.key() == Qt.Key_Tab:
            self.switchpage()
        else:
            super().keyPressEvent(event)

    def eventFilter(self, obj, event):
        if obj == self.input1 and event.type() == QEvent.Type.KeyPress:
            if event.key() == Qt.Key_Tab:
                self.switchpage()
                return True
        return False

    def switchpage(self):
        if self.homeb.isChecked():
            self.elecb.setChecked(True)
            self.elec()
            return
        elif self.elecb.isChecked():
            self.geomb.setChecked(True)
            self.geom()
            return
        elif self.geomb.isChecked():
            self.homeb.setChecked(True)
            self.home()
            return

    def elec(self):
        self.hometitle.hide()
        self.homecon.hide()
        self.geomtype.hide()
        self.shape.hide()
        self.geomcon.hide()
        self.geomunit1.hide()
        self.geomunit2.hide()
        self.geomunit3.hide()
        self.input1.show()
        self.input2.show()
        self.input3.hide()
        self.input1.clear()
        self.input2.clear()
        self.input3.clear()
        self.elecunit1.show()
        self.elecunit2.show()
        self.eleccon.show()
        return

    def geom(self):
        self.hometitle.hide()
        self.homecon.hide()
        self.eleccon.hide()
        self.elecunit1.hide()
        self.elecunit2.hide()
        self.geomtype.show()
        self.shape.show()
        self.geomcon.show()
        self.input1.show()
        self.input2.show()
        self.input1.clear()
        self.input2.clear()
        self.input3.clear()
        self.geomunit1.show()
        self.geomunit2.show()
        self.upshapeops()
        self.geomtype.currentIndexChanged.connect(self.upshapeops)
        self.shape.currentIndexChanged.connect(self.upshape)
        return

    def upshape(self):
        if self.shape.currentText() == self.twodshapes[0]:
            
            return
        if self.shape.currentText() == self.twodshapes[1]:
            return
        if self.shape.currentText() == self.twodshapes[2]:
            return
        if self.shape.currentText() == self.twodshapes[3]:
            return
        if self.shape.currentText() == self.twodshapes[4]:
            return
        if self.shape.currentText() == self.threedshapes[0]:
            return
        if self.shape.currentText() == self.threedshapes[1]:
            return
        if self.shape.currentText() == self.threedshapes[2]:
            return
        if self.shape.currentText() == self.threedshapes[3]:
            return
        if self.shape.currentText() == self.threedshapes[4]:
            return
        if self.shape.currentText() == self.threedshapes[5]:
            return


    def upshapeops(self):
        self.shape.blockSignals(True)
        self.shape.clear()

        if self.geomtype.currentText() == self.geomtypes[1]:
            self.input3.show()
            self.geomunit3.show()
            self.shape.addItems(self.threedshapes)
        else:
            self.input3.hide()
            self.geomunit3.hide()
            self.shape.addItems(self.twodshapes)
        self.shape.blockSignals(True)

    def home(self):
        self.geomtype.hide()
        self.shape.hide()
        self.input1.show()
        self.input2.hide()
        self.input1.clear()
        self.input2.clear()
        self.input3.clear()
        self.elecunit1.hide()
        self.elecunit2.hide()
        self.geomunit1.hide()
        self.geomunit2.hide()
        self.hometitle.show()
        self.homecon.show()
        self.geomcon.hide()
        self.eleccon.hide()
        return

    def uptext(self, result):
        currtext = self.results
        newtext = str(self.results.text())+ '\n' + str(result)
        self.results.setText(newtext)

    def getgeomval(self, name):
        if self.geomunit1.currentText() == name:
            return float(self.input1.text())
        if self.geomunit2.currentText() == name:
            return float(self.input2.text())
        if self.geomunit3.currentText() == name:
            return float(self.input3.text())
        return None
    
    def cal(self):
        if self.homeb.isChecked():
            calstr = self.input1.text()
            calcle = calstr.strip().replace(' ', '')
            if '+' in calcle:
                calnums = calcle.split('+')
                result = float(calnums[0]) + float(calnums[1])
            elif '-' in calcle:
                calnums = calcle.split('-')
                result = float(calnums[0]) - float(calnums[1])
            elif '*' in calcle:
                calnums = calcle.split('*')
                result = float(calnums[0]) * float(calnums[1])
            else:
                calnums = calcle.split('/')
                result = float(calnums[0]) / float(calnums[1])
            if str(result).endswith('.0'):
                self.homecon.setText(str(int(result)))
                self.uptext(int(result))
                self.input1.clear()
            else:
                self.homecon.setText(str(result))
                self.uptext(result)
                self.input1.clear()

            return
        elif self.elecb.isChecked():
            ev1 = int(self.input1.text())
            ev2 = int(self.input2.text())
            eu1 = self.elecunit1.currentText()
            eu2 = self.elecunit2.currentText()
            if eu1 == eu2:
                self.eleccon.setText('Invalid')
            elif {eu1, eu2} == {self.elecunits[0], self.elecunits[1]}:
                if eu1 == self.elecunits[0]:
                    self.eleccon.setText(f'{self.elecunits[0]} = {ev1}\n{self.elecunits[1]} = {ev2}\n{self.elecunits[2]} = {ev2 / ev1}\n{self.elecunits[3]} = {ev2 * ev1}')
                else:
                    self.eleccon.setText(f'{self.elecunits[0]} = {ev2}\n{self.elecunits[1]} = {ev1}\n{self.elecunits[2]} = {ev1 / ev2}\n{self.elecunits[3]} = {ev1 * ev2}')
            elif {eu1, eu2} == {self.elecunits[0], self.elecunits[2]}:
                if eu1 == self.elecunits[0]:
                    self.eleccon.setText(f'{self.elecunits[0]} = {ev1}\n{self.elecunits[1]} = {ev1 * ev2}\n{self.elecunits[2]} = {ev2}\n{self.elecunits[3]} = {(ev1 * ev1) * ev2}')
                else:
                    self.eleccon.setText(f'{self.elecunits[0]} = {ev2}\n{self.elecunits[1]} = {ev2 * ev2}\n{self.elecunits[2]} = {ev1}\n{self.elecunits[3]} = {(ev2 * ev2) * ev1}')
            elif {eu1, eu2} == {self.elecunits[0], self.elecunits[3]}:
                if eu1 == self.elecunits[0]:
                    self.eleccon.setText(f'{self.elecunits[0]} = {ev1}\n{self.elecunits[1]} = {ev2 / ev1}\n{self.elecunits[2]} = {ev2 / (ev1 * ev1)}\n{self.elecunits[3]} = {ev2}')
                else:
                    self.eleccon.setText(f'{self.elecunits[0]} = {ev2}\n{self.elecunits[1]} = {ev1 / ev2}\n{self.elecunits[2]} = {ev1 / (ev2 * ev2)}\n{self.elecunits[3]} = {ev1}')
            elif {eu1, eu2} == {self.elecunits[1], self.elecunits[2]}:
                if eu1 == self.elecunits[1]:
                    self.eleccon.setText(f'{self.elecunits[0]} = {ev1 / ev2}\n{self.elecunits[1]} = {ev1}\n{self.elecunits[2]} = {ev2}\n{self.elecunits[3]} = {(ev1 * ev1) / ev2}')
                else:
                    self.eleccon.setText(f'{self.elecunits[0]} = {ev2 / ev1}\n{self.elecunits[1]} = {ev2}\n{self.elecunits[2]} = {ev1}\n{self.elecunits[3]} = {(ev2 * ev2) / ev1}')
            elif {eu1, eu2} == {self.elecunits[1], self.elecunits[3]}:
                if eu1 == self.elecunits[1]:
                    self.eleccon.setText(f'{self.elecunits[0]} = {ev2 / ev1}\n{self.elecunits[1]} = {ev1}\n{self.elecunits[2]} = {ev2 / (ev1 * ev1)}\n{self.elecunits[3]} = {ev2}')
                else:
                    self.eleccon.setText(f'{self.elecunits[0]} = {ev1 / ev2}\n{self.elecunits[1]} = {ev2}\n{self.elecunits[2]} = {ev1 / (ev2 * ev2)}\n{self.elecunits[3]} = {ev1}')
            elif {eu1, eu2} == {self.elecunits[2], self.elecunits[3]}:
                if eu1 == self.elecunits[2]:
                    self.eleccon.setText(f'{self.elecunits[0]} = {(ev2 / ev1) ** .5}\n{self.elecunits[1]} = {(ev2 * ev1) ** .5}\n{self.elecunits[2]} = {ev1}\n{self.elecunits[3]} = {ev2}')
                else:
                    self.eleccon.setText(f'{self.elecunits[0]} = {(ev1 / ev2) ** .5}\n{self.elecunits[1]} = {(ev1 * ev2) ** .5}\n{self.elecunits[2]} = {ev2}\n{self.elecunits[3]} = {ev1}')
            result = self.eleccon.text()
            self.uptext(result)
            return

        elif self.geomb.isChecked():
            pi = math.pi
            geom1 = self.input1.text() + ' ' + self.geomunit1.currentText()
            geom2 = self.input2.text() + ' ' + self.geomunit2.currentText()
            width = self.getgeomval(self.geomunits[1])
            height = self.getgeomval(self.geomunits[2])
            depth = self.getgeomval(self.geomunits[3])
            radius = self.getgeomval(self.geomunits[4])

            if self.geomtype.currentText() == self.geomtypes[0]:
                if self.shape.currentText() == self.twodshapes[0]:
                    preresult = (math.pi * radius * radius)

                elif self.shape.currentText() == self.twodshapes[1]:
                    preresult = (math.pi * height * width)

                elif self.shape.currentText() == self.twodshapes[2]:
                    preresult = (width / 2 * height)

                elif self.shape.currentText() == self.twodshapes[3]:

                    if width:
                        preresult = (width * width)
                    else:
                        preresult = (height * height)

                elif self.shape.currentText() == self.twodshapes[4]:
                    preresult = (height * width)

            if str(preresult).endswith('.0'):
                result = str(int(preresult))
                self.geomcon.setText(result)
            else:
                result = str(preresult)
                self.geomcon.setText(result)

                self.geomcon.setText(result)
            
            self.uptext(result)
            return

app = QApplication(sys.argv)
window = MainWindow()
window.show()

app.exec()
