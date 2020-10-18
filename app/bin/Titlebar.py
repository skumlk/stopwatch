import sys
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QFrame
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
import app.bin.Const
import app.shared.util as util
from PyQt5.Qt import pyqtSignal

class TitleBar(QtWidgets.QDialog):

    pinToTopChangeSignal = pyqtSignal(bool)

    def __init__(self, parent=None, isPinToToggle = False):
        QtWidgets.QDialog.__init__(self, parent)
        self.parent = parent
        self.setWindowFlags(Qt.FramelessWindowHint)
        
        self.setAutoFillBackground(True)
        self.setBackgroundRole(QtGui.QPalette.Highlight)
        self.updateCss()
        hbox=QtWidgets.QHBoxLayout(self)

        btnPinToggle=QtWidgets.QToolButton(self)
        self.btnPinToggle = btnPinToggle
        btnPinToggle.setMinimumHeight(10)
        btnPinToggle.clicked.connect(self.actionPinToggle)
        hbox.addWidget(btnPinToggle)
        self.setPinToToggle(isPinToToggle)
        
        self.isStartOrPause = True
        self.btnStartPause=QtWidgets.QToolButton(self)
        self.btnStartPause.setMinimumHeight(10)
        self.btnStartPause.clicked.connect(self.onStartPause)
        hbox.addWidget(self.btnStartPause)
        self.setIsStartOrPause(True)

        btnLap=QtWidgets.QToolButton(self)
        btnLap.setIcon(util.createQIcon("app", 'img/lap.png'))
        btnLap.setToolTip("New Lap")
        btnLap.setMinimumHeight(20)
        btnLap.clicked.connect(self.onLap)
        hbox.addWidget(btnLap)

        btnReset=QtWidgets.QToolButton(self)
        btnReset.setIcon(util.createQIcon("app", 'img/reset.png'))
        btnReset.setMinimumHeight(20)
        btnReset.setToolTip("Reset")
        btnReset.clicked.connect(self.onReset)
        hbox.addWidget(btnReset)

        btnClose=QtWidgets.QToolButton(self)
        btnClose.setIcon(util.createQIcon("app", 'img/close.png'))
        btnClose.setMinimumHeight(20)
        btnClose.clicked.connect(self.close)
        hbox.addWidget(btnClose)

        hbox.insertStretch(1,500)
        hbox.insertStretch(5,500)
        hbox.setSpacing(8)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Fixed)
        self.maxNormal=False

    def setIsStartOrPause(self, isStart):
        self.isStart = isStart
        if isStart:
            icon = 'img/start.png'
            toolTip = "Start/Continue"
        else:
            icon = 'img/pause.png'
            toolTip = "Pause"

        self.btnStartPause.setIcon(util.createQIcon("app", icon))
        self.btnStartPause.setToolTip(toolTip)

    def onReset(self):
        self.parent.reset()
        self.setIsStartOrPause(True)

    def onLap(self):
        self.parent.lap()
 
    def onStartPause(self):
        if self.isStart:
            self.parent.start()
        else:
            self.parent.pause()

        self.setIsStartOrPause(not self.isStart)

    def close(self):
        self.parent.closeNote()

    def setPinToToggle(self, isPinToToggle):
        self.isPinToToggle = isPinToToggle
        iconPath = 'img/pin-off.png'
        if self.isPinToToggle:
            iconPath = "img/pin-on.png"

        self.btnPinToggle.setIcon(util.createQIcon("app", iconPath))
        self.pinToTopChangeSignal.emit(self.isPinToToggle)

    def actionPinToggle(self):
        self.setPinToToggle(not self.isPinToToggle)

    def mousePressEvent(self,event):
        if event.button() == Qt.LeftButton:
            self.parent.moving = True
            self.parent.offset = event.pos()

    def mouseMoveEvent(self,event):
        if self.parent.moving: 
            newPosition = event.globalPos()-self.parent.offset
            self.parent.move(newPosition)
            self.parent.positionChanged(newPosition.x(), newPosition.y())
    
    def updateCss(self, backgroundColor=app.bin.Const.TITLE_BACKGROUND_COLOR):
        css = """
            QWidget{{
                Background: {0};
                color:white;
                font:12px bold;
                font-weight:bold;
                border-radius: 1px;
                height: 11px;
            }}
            QDialog{{
                font-size:12px;
                color: black;
            }}
            QToolButton{{
                Background: {0};
                font-size:11px;
            }}
            QToolButton:hover{{
            }}
        """.format(backgroundColor)
        self.setStyleSheet(css)


    def updateTitleColor(self, color):
        self.updateCss(color)