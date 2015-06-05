# -*- coding: utf-8 -*-



from PyQt4 import QtCore, QtGui
import sys
import time


try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

global a
a='0,0'

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(618, 464)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))

        self.graphicsView = QtGui.QGraphicsView(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(30, 20, 400, 400))
        self.graphicsView.setObjectName(_fromUtf8("graphicsView"))
        
        self.scene = Scene(30, 20, 400, 400, MainWindow)                # Scene upper left corner x = 30, y=30, height = 400, width = 400
        MainWindow.setCentralWidget(self.centralwidget)
        self.graphicsView.setScene(self.scene)

        self.scene.addItem(Circle_BLUE(180, 170 , 100, 100))
        self.scene.addItem(Circle_RED(220, 210, 20, 20))
        self.scene.addLine(50, 220, 410, 220)
        self.scene.addLine(230, 40, 230, 400)

        self.label_virtual_joystick = QtGui.QLabel(self.centralwidget)
        self.label_virtual_joystick.setGeometry(QtCore.QRect(470, 190, 111, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_virtual_joystick.setFont(font)
        self.label_virtual_joystick.setAlignment(QtCore.Qt.AlignCenter)
        self.label_virtual_joystick.setObjectName(_fromUtf8("label_virtual_joystick"))
        self.layoutWidget = QtGui.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(480, 30, 48, 68))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label_encoder1_text = QtGui.QLabel(self.layoutWidget)
        self.label_encoder1_text.setObjectName(_fromUtf8("label_encoder1_text"))
        self.verticalLayout.addWidget(self.label_encoder1_text)
        self.label_encoder2_text = QtGui.QLabel(self.layoutWidget)
        self.label_encoder2_text.setObjectName(_fromUtf8("label_encoder2_text"))
        self.verticalLayout.addWidget(self.label_encoder2_text)
        self.label_encoder3_text = QtGui.QLabel(self.layoutWidget)
        self.label_encoder3_text.setObjectName(_fromUtf8("label_encoder3_text"))
        self.verticalLayout.addWidget(self.label_encoder3_text)
        self.label_encoder4_text = QtGui.QLabel(self.layoutWidget)
        self.label_encoder4_text.setObjectName(_fromUtf8("label_encoder4_text"))
        self.verticalLayout.addWidget(self.label_encoder4_text)
        self.layoutWidget1 = QtGui.QWidget(self.centralwidget)
        self.layoutWidget1.setGeometry(QtCore.QRect(540, 30, 46, 68))
        self.layoutWidget1.setObjectName(_fromUtf8("layoutWidget1"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.label_encoder1_value = QtGui.QLabel(self.layoutWidget1)
        self.label_encoder1_value.setText(_fromUtf8(""))
        self.label_encoder1_value.setObjectName(_fromUtf8("label_encoder1_value"))
        self.verticalLayout_2.addWidget(self.label_encoder1_value)
        self.label_encoder2_value = QtGui.QLabel(self.layoutWidget1)
        self.label_encoder2_value.setText(_fromUtf8(""))
        self.label_encoder2_value.setObjectName(_fromUtf8("label_encoder2_value"))
        self.verticalLayout_2.addWidget(self.label_encoder2_value)
        self.label_encoder3_value = QtGui.QLabel(self.layoutWidget1)
        self.label_encoder3_value.setText(_fromUtf8(""))
        self.label_encoder3_value.setObjectName(_fromUtf8("label_encoder3_value"))
        self.verticalLayout_2.addWidget(self.label_encoder3_value)
        self.label_encoder4_value = QtGui.QLabel(self.layoutWidget1)
        self.label_encoder4_value.setText(_fromUtf8(""))
        self.label_encoder4_value.setObjectName(_fromUtf8("label_encoder4_value"))
        self.verticalLayout_2.addWidget(self.label_encoder4_value)
        self.label_obstacle = QtGui.QLabel(self.centralwidget)
        self.label_obstacle.setGeometry(QtCore.QRect(490, 250, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_obstacle.setFont(font)
        self.label_obstacle.setText(_fromUtf8(""))
        self.label_obstacle.setObjectName(_fromUtf8("label_obstacle"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 618, 20))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "ProBot Control Unit", None))
        self.label_virtual_joystick.setText(_translate("MainWindow", "Virtual Joystick", None))
        self.label_encoder1_text.setText(_translate("MainWindow", "Encoder 1", None))
        self.label_encoder2_text.setText(_translate("MainWindow", "Encoder 2", None))
        self.label_encoder3_text.setText(_translate("MainWindow", "Encoder 3", None))
        self.label_encoder4_text.setText(_translate("MainWindow", "Encoder 4", None))


    def data_send(self, x,y):

        if x in range(50,180):

            v_ang_gui = (230-x)/180

        elif x in range(280,410):
            v_ang_gui = (230-x)/180     # CW rotation gives - value

        else:
            v_ang_gui=0

        if y in range(40,170):
            v_lin_gui= (220-y)/180

        elif y in range(270,400):
            v_lin_gui = (220-y)/180

        else:
            v_lin_gui=0

        return str(v_ang_gui) + ',' + str(v_lin_gui)            # returns angular and linear velocities coming from gui

  
class Scene(QtGui.QGraphicsScene):
    def mousePressEvent(self, e):
        
        QtGui.QGraphicsScene.mousePressEvent(self, e)
    
    def mouseReleaseEvent(self, e):  
        
        QtGui.QGraphicsScene.mouseReleaseEvent(self, e)

        self.clear()

        self.addItem(Circle_BLUE(180, 170 , 100, 100))
        self.addItem(Circle_RED(220, 210, 20, 20))

        self.addLine(50, 220, 410, 220)
        self.addLine(230, 40, 230, 400)

        global a

        a = '0,0'

    def mouseMoveEvent(self, e):
        
        QtGui.QGraphicsScene.mouseMoveEvent(self, e)

        if e.buttons() == QtCore.Qt.LeftButton:                     # checks the mouse button

            position = QtCore.QPointF(e.scenePos())
 
            self.clear()

            self.addItem(Circle_BLUE(180, 170 , 100, 100))
            self.addLine(50, 220, 410, 220)
            self.addLine(230, 40, 230, 400)
            self.addItem(Circle_RED( int(position.x())-10 , int(position.y())-10 , 20,20))
            self.addLine(230, 220 , int(position.x()), int(position.y()))
 
            MainWindow = QtGui.QMainWindow()
            ui = Ui_MainWindow()

            global a
            a=ui.data_send(position.x(),position.y())


class Circle_RED(QtGui.QGraphicsEllipseItem):

    def __init__(self, *args):
        
        QtGui.QGraphicsEllipseItem.__init__(self, *args)

        self.setPen(QtGui.QPen(QtCore.Qt.red, 1))
        self.setBrush(QtGui.QBrush(QtCore.Qt.red,1))

        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable, True)

class Circle_BLUE(QtGui.QGraphicsEllipseItem):

    def __init__(self, *args):
        
        QtGui.QGraphicsEllipseItem.__init__(self, *args)

        self.setPen(QtGui.QPen(QtCore.Qt.cyan, 1))
        self.setBrush(QtGui.QBrush(QtCore.Qt.cyan,1))


def main():

    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)                             # Creating the GUI
    MainWindow.show()
    sys.exit(app.exec_())

if __name__ == "__main__":

    main()



        


