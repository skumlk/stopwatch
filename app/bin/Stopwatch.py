import sys
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QFrame, QMenu, QMessageBox
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from app.bin.Titlebar import TitleBar
import app.bin.Const
from PyQt5.Qt import QColor, pyqtSignal
from app.bin import ConfigParser
from app.bin.Settings import Settings
from app.bin.ConfigParser import ConfigNoteModel
import time

class Stopwatch(QtWidgets.QFrame):

    #pin to top, undo not working properly
    reopenWindowSignal = pyqtSignal(str)

    bodyColors = {"purple": "#eb00eb", "green": "#D4FC7A","yellow": "#FFE46E","pink": "#FF7BE3" }
    titleColors = {"purple": "#D700D7", "green": "#BFFB33","yellow": "#FFDB3B","pink": "#FF48D8" }

    def __init__(self, stopwatchManager, parent=None):
        
        QtWidgets.QFrame.__init__(self, parent)
        
        self.stopwatchManager = stopwatchManager
        self.m_mouse_down= False
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
       
        self.updateStyleSheet()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.SubWindow | Qt.Tool)
        self.setMouseTracking(True)

        settings = ConfigParser.config_instance.getSettings()
        self.m_titleBar = TitleBar(self, True); # configNote.isPinToTop())
        self.m_content = QtWidgets.QWidget(self)
        vbox=QtWidgets.QVBoxLayout(self)
        vbox.addWidget(self.m_titleBar)
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.setSpacing(0)
        layout=QtWidgets.QVBoxLayout()
        layout.addWidget(self.m_content)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(0)
        vbox.addLayout(layout)
    
        font = QtGui.QFont("Times", 16, QtGui.QFont.Bold) 
        l2 = QtWidgets.QLabel()
        l2.setAlignment(Qt.AlignCenter)
        l2.setFont(font)
        l2.setStyleSheet("font-size: 15px;")
        self.l2 = l2

        l=QtWidgets.QVBoxLayout(self.contentWidget())
        l.addWidget(l2)
        
        lapTextField = QtWidgets.QTextEdit()
        lapTextField.setReadOnly(True)
        lapTextField.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)    
        self.lapTextField = lapTextField
        l.addWidget(lapTextField)

        l.setContentsMargins(0, 0, 0, 0)

        self.m_titleBar.pinToTopChangeSignal.connect(self.actionPinToTopChange)
        self.setPosition(500, 10)
        self.setDimension(250, 150)
        self.setPinToTop(True)
        self.installEventFilter(self)

        self.checkThreadTimer = QtCore.QTimer(self)
        self.checkThreadTimer.setInterval(100) #.1 seconds
        self.checkThreadTimer.timeout.connect(self.readListValues)
        self.reset()

    def readListValues(self): 

        if self.startTime is None:
            self.lapStartTime = self.startTime = int(round(time.time() * 1000))
            timeInMs = 0
        else:
            timeInMs = int(round(time.time() * 1000)) - self.startTime

        timeInMs += self.totalTime
        self.l2.setText(self.formatTime(timeInMs))

    def formatTime(self, timeInMs):
        milliseconds = int((timeInMs%1000)/100)
        tmpTime = int(timeInMs/1000)

        seconds = tmpTime%60
        tmpTime = int(tmpTime/60)
        
        minutes = tmpTime%60
        tmpTime = int(tmpTime/60)

        hours = tmpTime
        return "{hours:02d}:{minutes:02d}:{seconds:02d}:{milli:1d}".format(hours=hours, minutes=minutes, seconds=seconds, milli=milliseconds)

    def eventFilter(self, object, event):
        if event.type() == QtCore.QEvent.FocusIn:
            print("Focused")

        return False # passes this event to the child, i.e. does not block it from the child widgets

    def setPinToTop(self, isPinToTop):
        flag = self.windowFlags()
        if isPinToTop:
            flag |= Qt.WindowStaysOnTopHint
            self.setWindowFlags(flag)
            self.raise_()
            self.show()
            self.activateWindow()
        elif bool(flag & QtCore.Qt.WindowStaysOnTopHint):#is flag set
            self.reopenWindowSignal.emit()

    def start(self):
        self.startTime = None
        self.checkThreadTimer.start(100)

    def reset(self):
        self.lapTotalTime = 0
        self.lapStartTime = 0
        self.lapText = ""
        self.lapCount = 1
        self.checkThreadTimer.stop()
        self.startTime = None
        self.totalTime = 0
        self.l2.setText("00:00:00:0")
        self.lapTextField.setText(self.lapText)

    def pause(self):
        currentTime = int(round(time.time() * 1000))
        self.totalTime += currentTime - self.startTime
        self.lapTotalTime = currentTime - self.lapStartTime
        self.checkThreadTimer.stop()

    def lap(self):
        currentTime = int(round(time.time() * 1000))
        lapTime = self.lapTotalTime + currentTime - self.lapStartTime
        self.lapText = "{count:d}. {time}\r\n".format(count=self.lapCount, time=self.formatTime(lapTime)) + self.lapText
        self.lapTextField.setText(self.lapText)
        self.lapStartTime = currentTime
        self.lapCount += 1
        self.lapTotalTime = 0

    def actionPinToTopChange(self, isPinToTop):
        #ConfigParser.config_instance.updateNotePinToTop(self._id, isPinToTop)
        self.setPinToTop(isPinToTop)

    def contentWidget(self):
        return self.m_content

    def setText(self, text):
        self.textEditor.setText(text)

    def setPosition(self, x, y):
        self.move(x, y)

    def signalTextChanged(self):
        text = self.textEditor.toHtml()
        self.noteManager.updateNoteText(self._id, text)

    def positionChanged(self, x,y):
        pass
        # self.noteManager.updateNotePosition(self._id, x, y)

    def resizeEvent(self, resizeEvent):
        newSize = self.size()
        # self.noteManager.updateNoteDimension(self._id, newSize.width(), newSize.height())

    def setDimension(self, width, height):
        self.resize(width, height)

    def closeNote(self):
        msg = QMessageBox()
        msg.move(self.geometry().x(), self.geometry().y() + 50)
        msg.setIcon(QMessageBox.Information)
        msg.setText("Do you want to delete note?")
        msg.setWindowTitle("Sticky Note")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        retval = msg.exec_()
        if retval == QMessageBox.Ok:  # accepted
            self.close()
            self.noteManager.deleteNote(self._id)

    def createNewNote(self):
        self.noteManager.createNewNote(self._id)

    def updateStyleSheet(self, backgroundColor = app.bin.Const.BODY_BACKGROUND_COLOR):
        css = """
            QFrame{{
                Background:  {0};
                color: black;
                font:13px ;
                font-weight:normal;
                }}
            """.format(backgroundColor)
        self.setStyleSheet(css)

    def setColor(self, color):
        bodyColorCode = self.bodyColors[color]
        titleColorCode = self.titleColors[color]
        self.updateStyleSheet(bodyColorCode)
        #self.noteManager.updateNoteColor(self._id, color)
        self.m_titleBar.updateTitleColor(titleColorCode)

    def updateSettings(self):
        settings = ConfigParser.config_instance.getSettings()
        self.textEditor.setSettings(settings)

        # self.textEditor.setColor(settings.getFontColor())
        # self.textEditor.setFontSize(settings.getFontSize())
        # self.textEditor.setFontFamily(settings.getFontFamily())