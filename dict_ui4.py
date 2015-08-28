__author__ = 'zhyuey'

#!/usr/bin/env python


#############################################################################
##
## Copyright (C) 2013 Riverbank Computing Limited.
## All rights reserved.
##
## This file is part of the examples of PyQt.
##
## You may use this file under the terms of the BSD license as follows:
##
## "Redistribution and use in source and binary forms, with or without
## modification, are permitted provided that the following conditions are
## met:
##   * Redistributions of source code must retain the above copyright
##     notice, this list of conditions and the following disclaimer.
##   * Redistributions in binary form must reproduce the above copyright
##     notice, this list of conditions and the following disclaimer in
##     the documentation and/or other materials provided with the
##     distribution.
##   * Neither the name of Riverbank Computing Limited nor the names of
##     its contributors may be used to endorse or promote products
##     derived from this software without specific prior written
##     permission.
##
## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
## "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
## LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
## A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
## OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
## SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
## LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
## DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
## THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
## (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
## OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
##
#############################################################################


import sys, time

from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QApplication, QDialog, QSystemTrayIcon, QMenu, QAction, QShortcut
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt, QThread, QEvent
from PyQt5.QtGui import QIcon, QKeySequence

from baidu_dict import BaiduDict
from youdao_dict import YoudaoDict
import multiprocessing


class WorkThread(QThread):
    received = pyqtSignal(['QString'])
    def __init__(self, word, providerId):
        QThread.__init__(self)
        self.word = word
        self.providerId = providerId

    def run(self):
        if self.providerId == 0:
            result = YoudaoDict.searchDict(self.word)
        elif self.providerId == 1:
            result = BaiduDict.searchDict(self.word)
        self.received.emit(result)
    



class DemoImpl(QDialog):
	
	
    def __init__(self, *args):
        super(DemoImpl, self).__init__(*args)

        loadUi('dict2.ui',self)
		
        self.setLayout(self.verticalLayout)
        self.plainTextEdit.setReadOnly(True)
        self.setWindowFlags(self.windowFlags() |
                            Qt.WindowSystemMenuHint |
                            Qt.WindowMinMaxButtonsHint)
        self.trayicon = QSystemTrayIcon()
        self.traymenu = QMenu()

        self.quitAction = QAction('GQuit', self)
        self.quitAction.triggered.connect(self.close)
        self.quitAction.setShortcut(QKeySequence('Ctrl+q'))
        self.addAction(self.quitAction)

        self.traymenu.addAction('&Normal', self.showNormal, QKeySequence('Ctrl+n'))
        self.traymenu.addAction('Mi&nimize', self.showMinimized, QKeySequence('Ctrl+i'))
        self.traymenu.addAction('&Maximum', self.showMaximized, QKeySequence('Ctrl+m'))
        self.traymenu.addAction('&Quit',self.close, QKeySequence('Ctrl+q'))

        self.trayicon.setContextMenu(self.traymenu)

        self.ticon = QIcon('icon_dict2.ico')
        self.trayicon.setIcon(self.ticon)
        self.trayicon.setToolTip('YYDict')
        self.trayicon.activated.connect(self.on_systemTrayIcon_activated)
        self.traymsg_firstshow = True

        self.button1.clicked.connect(self.searchword)
        self.comboBox.activated.connect(self.searchword)

    def changeEvent(self, event):
        if event.type() == QEvent.WindowStateChange:
            if self.isMinimized():
                self.hide()
                self.trayicon.show()
                if self.traymsg_firstshow:
                    self.trayicon.showMessage('', 'YYDict is running', QSystemTrayIcon.Information, 2000)
                    self.traymsg_firstshow = False
            else:
                self.trayicon.hide()
				
    def closeEvent(self, event):
        self.trayicon.hide()

    @pyqtSlot(QSystemTrayIcon.ActivationReason)
    def on_systemTrayIcon_activated(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.activateWindow()	
            self.showNormal()



    @pyqtSlot()
    def searchword(self):
        word = self.lineEdit.text().strip()
        if not len(word):
            self.plainTextEdit.setPlainText('')
            self.lineEdit.setFocus(Qt.MouseFocusReason)
        else:
            self.workThread = WorkThread(word, self.comboBox.currentIndex())
            self.workThread.received.connect(self.updateResult)
            self.workThread.start()
            self.workThread.wait()


    @pyqtSlot('QString')
    def updateResult(self, rt):
        self.plainTextEdit.setPlainText(rt)
        self.lineEdit.selectAll()
        self.lineEdit.setFocus(Qt.MouseFocusReason)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = DemoImpl()
    widget.show()
    sys.exit(app.exec_())

