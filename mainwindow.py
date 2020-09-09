from PyQt5.QtCore import *
from PyQt5.QtGui import *

from breakout import *
import sys
import datetime

__author__ = "Laszlo Balla"
__version__ = "0.0.3"
__date__ = "2016.10.20"

################################################################
def main():
    app = QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec_())

################################################################
class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("BreakoutGame in Python")
        # create stuff
        self.breakoutwidget = Breakout(540, 800,"Breakout")
        self.setCentralWidget(self.breakoutwidget)
        #self.breakoutwidget.setStyleSheet("background-image:url(\"Traffic.jpg\"); background-position: center;")

        self.createActions()
        self.createMenus()

        # format the main window
        self.setGeometry(100,100,540,800)

        # show windows
        self.show()
        #self.breakoutwidget.show()
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap("bkgnd1.jpg")))
        self.setPalette(palette)

    def about(self):
        QMessageBox.about(self, self.tr("Breakout Game"),
            self.tr("Version: "
                    "%s\n"
                    "%s\n"
                    "%s\n\n"
                    % ( __version__, __date__,__author__)))

    def help(self):
        QMessageBox.information(self, self.tr("Help"),
                          self.tr("<b><u>Brick types:</u></b><p>"
                                  "<b><font color=\"darkMagenta\">Purple:</font></b>"
                                  "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
                                  "simple brick, value: 10 points<p>"
                                  "<b>Black:</b>"
                                  "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
                                  "needs 3 hits to destroy, value: 30 points when destroyed<p>"
                                  "<b><font color=\"white\">White:</font></b>"
                                  "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
                                  "ball is faster for 30 secs, double points<p>"
                                  "<b><font color=\"yellow\">Yellow:</font></b>"
                                  "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
                                  "you are lucky: your score is doubled<p>"
                                  "<b><font color=\"red\">Red:</font></b>"
                                  "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
                                  "paddle shrinks, but faster for 30 secs<p>"
                                  "<b><font color=\"green\">Green:</font></b>"
                                  "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
                                  "three balls on the table<p>"
                                  "<b><font color=\"blue\">Blue:</font></b>"
                                  "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
                                  "paddle grows, but slower for 30 secs<p>"))


    def createActions(self):
        self.restartAct = QAction(self.tr("Restart game"), self)
        # self.connect(self.restartAct, SIGNAL("triggered()"),  self.restartAction)
        self.restartAct.triggered.connect(self.restartAction)

        self.exitAct = QAction(self.tr("Exit"), self)
        self.exitAct.setShortcut(self.tr("Ctrl+Q"))
        self.exitAct.setStatusTip(self.tr("Exit the application"))
       # self.connect(self.exitAct, SIGNAL("triggered()"), self, SLOT("close()"))
        self.exitAct.triggered.connect(self.close)

        self.helpAct = QAction(self.tr("Help"), self)
        self.helpAct.setStatusTip(self.tr("Show the Help"))
       # self.connect(self.helpAct, SIGNAL("triggered()"), self.help)
        self.helpAct.triggered.connect(self.help)

        self.aboutAct = QAction(self.tr("About"), self)
        self.aboutAct.setStatusTip(self.tr("Show the application's About box"))
       # self.connect(self.aboutAct, SIGNAL("triggered()"), self.about)
        self.aboutAct.triggered.connect(self.about)


        self.aboutQtAct = QAction(self.tr("About Qt"), self)
        self.aboutQtAct.setStatusTip(self.tr("Show the Qt library's About box"))
       # self.connect(self.aboutQtAct, SIGNAL("triggered()"), qApp, SLOT("aboutQt()"))
        self.aboutQtAct.triggered.connect(qApp.aboutQt)

        self.skinGroup = QActionGroup(self)
        self.skinGroup.setExclusive (True)

        self.basicAct = self.skinGroup.addAction(QAction(self.tr("Basic"), self))
        self.basicAct.setCheckable(True)
       # self.connect(self.basicAct, SIGNAL("triggered()"), self.basicskinSelected)
        self.basicAct.triggered.connect(self.basicskinSelected)

        self.androidAct = self.skinGroup.addAction(QAction(self.tr("Android"), self))
        self.androidAct.setCheckable(True)
        self.androidAct.setChecked(True)
       # self.connect(self.androidAct, SIGNAL("triggered()"), self.androidskinSelected)
        self.androidAct.triggered.connect(self.androidskinSelected)

        self.arcanoidAct = self.skinGroup.addAction(QAction(self.tr("Arcanoid"), self))
        self.arcanoidAct.setCheckable(True)
       # self.connect(self.arcanoidAct, SIGNAL("triggered()"), self.arcanoidskinSelected)
        self.arcanoidAct.triggered.connect(self.arcanoidskinSelected)

        self.atariAct = self.skinGroup.addAction(QAction(self.tr("Atari"), self))
        self.atariAct.setCheckable(True)
       # self.connect(self.atariAct, SIGNAL("triggered()"), self.atariskinSelected)
        self.atariAct.triggered.connect(self.atariskinSelected)

        self.physicsGroup = QActionGroup(self)
        self.physicsGroup.setExclusive(True)

        self.atariClassicAct = self.physicsGroup.addAction(QAction(self.tr("Atari Classic"), self))
        self.atariClassicAct.setCheckable(True)
       # self.connect(self.atariClassicAct, SIGNAL("triggered()"), self.atariclassicphysicsSelected)
        self.atariClassicAct.triggered.connect(self.atariclassicphysicsSelected)


        self.atariRandomizedAct = self.physicsGroup.addAction(QAction(self.tr("Atari Randomized"), self))
        self.atariRandomizedAct.setCheckable(True)
       # self.connect(self.atariRandomizedAct, SIGNAL("triggered()"), self.atarirandomizedphysicsSelected)
        self.atariRandomizedAct.triggered.connect(self.atarirandomizedphysicsSelected)

        self.RealisticAct = self.physicsGroup.addAction(QAction(self.tr("Realistic"), self))
        self.RealisticAct.setCheckable(True)
        self.RealisticAct.setChecked(True)
       # self.connect(self.RealisticAct, SIGNAL("triggered()"), self.realisticphysicsSelected)
        self.RealisticAct.triggered.connect(self.realisticphysicsSelected)

        self.autoPaddleAct = QAction(self.tr("Enabled"), self)
        self.autoPaddleAct.setCheckable(True)
       # self.connect(self.autoPaddleAct, SIGNAL("triggered()"), self.autopaddletoggled)
        self.autoPaddleAct.triggered.connect(self.autopaddletoggled)

    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu(self.tr("File"))
        self.fileMenu.addAction(self.restartAct)
        self.fileMenu.addAction(self.exitAct)

        self.skinMenu = self.menuBar().addMenu(self.tr("Skin"))

        self.skinMenu.addAction(self.basicAct)
        self.skinMenu.addAction(self.androidAct)
        self.skinMenu.addAction(self.arcanoidAct)
        self.skinMenu.addAction(self.atariAct)

        self.physicsMenu = self.menuBar().addMenu(self.tr("Physics"))
        self.physicsMenu.addAction(self.atariClassicAct)
        self.physicsMenu.addAction(self.atariRandomizedAct)
        self.physicsMenu.addAction(self.RealisticAct)

        self.autopaddleMenu = self.menuBar().addMenu(self.tr("Auto_Paddle"))
        self.autopaddleMenu.addAction(self.autoPaddleAct)

        self.helpMenu = self.menuBar().addMenu(self.tr("Help"))
        self.helpMenu.addAction(self.helpAct)
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.aboutQtAct)

    def createStatusBar(self):
        sb = QStatusBar()
        sb.setFixedHeight(18)
        self.setStatusBar(sb)
        self.statusBar().showMessage(self.tr("Ready"))

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.breakoutwidget.pauseGame()
        else:
            self.breakoutwidget.keyPressEvent(e)

    def keyReleaseEvent(self, e):
        self.breakoutwidget.keyReleaseEvent(e)

    def basicskinSelected(self):
        self.breakoutwidget.changeskin ("basic")
        self.skinMenu.show()

    def androidskinSelected(self):
        self.breakoutwidget.changeskin ("android")
        self.skinMenu.show()

    def arcanoidskinSelected(self):
        self.breakoutwidget.changeskin ("arcanoid")
        self.skinMenu.show()

    def atariskinSelected(self):
        self.breakoutwidget.changeskin ("atari")
        self.skinMenu.show()

    def atariclassicphysicsSelected(self):
        self.breakoutwidget.changephysics ("Classic")
        self.physicsMenu.show()

    def atarirandomizedphysicsSelected(self):
        self.breakoutwidget.changephysics ("Randomized")
        self.physicsMenu.show()

    def realisticphysicsSelected(self):
        self.breakoutwidget.changephysics ("Realistic")
        self.physicsMenu.show()

    def autopaddletoggled(self):
        self.breakoutwidget.autopaddle = self.autoPaddleAct.isChecked()
        self.autopaddleMenu.show()

    def restartAction(self):
        self.breakoutwidget.resetGame()

################################################################
if __name__ == "__main__":
    main()