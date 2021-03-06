

import os
import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QMainWindow, QFrame
from PyQt5 import Qt
#from app.bin.StickyNote import StickyNote
import app.bin.StopwatchManager as StopwatchManager
#from app.bin.SettingsDialog import SettingsDialog
import app.bin.ConfigParser as ConfigParser
import qtmodern.styles
import qtmodern.windows

class SystemTrayIcon(QtWidgets.QSystemTrayIcon):

    def __init__(self, icon, parent=None):
        QtWidgets.QSystemTrayIcon.__init__(self, icon, parent)
        menu = QtWidgets.QMenu(parent)
        create_new_action = menu.addAction('New Stopwatch')
        hide_all_action = menu.addAction('Hide All')
        menu.addSeparator()
        settings_action = menu.addAction('Settings')
        menu.addSeparator()
        exit_action = menu.addAction('Quit')

        self.setContextMenu(menu)

        create_new_action.triggered.connect(self.createStopwatch)
        exit_action.triggered.connect(self.exitAll)
        settings_action.triggered.connect(self.showSettings)
        hide_all_action.triggered.connect(self.hideAll)

    def on_context_menu(self, point):
        print("xxxxx dddd")

    def createStopwatch(self):
        StopwatchManager.stopwatch_manager_instance.createNewStopwatch()

    def hideAll(self):
        StickyNoteManager.stopwatch_manager_instance.hideAll()   

    def exitAll(self):
        QtWidgets.QApplication.quit()

    def showSettings(self):
        settings = ConfigParser.config_instance.getSettings()
        dlg = SettingsDialog(settings)
        dlg.move(self.geometry().x(), self.geometry().y() + 50)
        mw = qtmodern.windows.ModernWindow(dlg)
        ret = mw.show()
