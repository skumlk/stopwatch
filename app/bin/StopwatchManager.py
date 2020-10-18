
from app.bin.Stopwatch import Stopwatch
from PyQt5 import QtWidgets, QtCore, QtGui
import app.bin.ConfigParser as ConfigParser
from PyQt5.Qt import QColor

class StopwatchManager:

    stopwatches = []

    def __init__(self):
        rec = QtWidgets.QApplication.desktop().screenGeometry()
        self.screenWidth = rec.width()

        #for note in ConfigParser.config_instance.getNotes(): 
        #   self.createNote(note)

    def createStopwatch(self):
        # _id = note.getId()
        stopwatch = Stopwatch(self)
        stopwatch.show()
        stopwatch.setColor("purple")
        self.stopwatches.append(stopwatch)
        return stopwatch

    def createNewStopwatch(self, _id = None):

        # x = self.screenWidth - 300
        # y = 250
        # color = "purple"

        # if _id:
        #     note = ConfigParser.config_instance.getNote(_id)
        #     x = note.getX()
        #     y = note.getY() + 100
        #     color = note.getColor()

        #note = ConfigParser.config_instance.createNewNote(x, y, color)
        # self.createNote(note)
        self.createStopwatch()

    def showAll(self):
        for frame in self.stopwatches:
            frame.show()
            frame.activateWindow()     

    def updateNoteText(self, _id, text):
        ConfigParser.config_instance.updateNoteText(_id, text)

    def updateNotePosition(self, _id, x ,y):
        ConfigParser.config_instance.updateNotePosition(_id, x, y)

    def updateNoteDimension(self, _id,  width, height):
        ConfigParser.config_instance.updateNoteDimension(_id, width, height)

    def updateNoteColor(self, _id, color):
        ConfigParser.config_instance.updateNoteColor(_id, color)

    def deleteNote(self, _id):
        self.stopwatches = [x for x in self.stopwatches if x._id != _id]
        ConfigParser.config_instance.deleteNote(_id)       

    def hideAll(self):
        for frame in self.stopwatches:
            frame.hide()     

    def updateSettings(self):
        for stickyNote in self.stopwatches:
            stickyNote.updateSettings()

stopwatch_manager_instance = None