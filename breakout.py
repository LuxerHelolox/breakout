from PyQt4.QtCore import *
from PyQt4.QtGui import *
from brick import *
from paddle import *
from ball import *
import sys
import random


class Breakout(QWidget):
    N_OF_ROWS = 5
    N_OF_COLUMNS = 6
    N_OF_BRICKS = N_OF_ROWS * N_OF_COLUMNS
    BRICKHIGHT = 40
    BRICKWIDTH = 80
    DELAY = 5

    def __init__(self,breakout_width, breakout_height, breakout_title):
        QWidget.__init__(self)
        self._x = 0
        self._gameOver = False
        self._gameWon = False
        self._paused = False
        self._gameStarted = False
        self._bottom_edge = breakout_height
        self._ball = Ball("android", breakout_width/2+40, breakout_height-60, breakout_width )
        self._paddle = Paddle("android", breakout_width/2, breakout_height-40, breakout_width)
        self._bricks = [Brick("android", j * Breakout.BRICKWIDTH + 30, i * Breakout.BRICKHIGHT + 50)
                        for i in range(Breakout.N_OF_ROWS) for j in range(Breakout.N_OF_COLUMNS)]
        self.setFixedSize(breakout_width, breakout_height)
        self.setWindowTitle(breakout_title)
        # self.setBackgroundRole(QPalette.Dark)
        # self.setAutoFillBackground (True)

        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap("bkgnd.jpg")))
        self.setPalette(palette)

    def paintEvent(self, e):
        painter = QPainter(self)
        if self._gameOver:
            self.finishGame(painter, "Game lost","sounds\Crowd Boo.wav")
        elif self._gameWon:
            self.finishGame(painter, "Victory", "sounds\Audience_Applause.wav")
        else:
            self.drawObjects(painter)

    def finishGame(self, painter, message, soundfile):
        font = QFont("Courier", 24, QFont.Bold)
        fm = QFontMetrics(font)
        textwidth = fm.width(message)
        painter.setFont(font)
        h = self.height()
        w = self.width()
        painter.translate(QPoint(w / 2, h / 2))
        painter.drawText(-textwidth / 2, 0, message)
        QSound.play(soundfile)

    def drawObjects(self, painter):
        painter.drawImage(self._ball.rect, self._ball.image)
        painter.drawImage(self._paddle.rect, self._paddle.image)
        for i in range(Breakout.N_OF_BRICKS):
            if not self._bricks[i].destroyed:
                painter.drawImage(self._bricks[i].rect, self._bricks[i].image)

    def timerEvent(self, e):
        self.moveObjects()
        self.checkCollision()
        self.repaint()

    def moveObjects(self):
        self._ball.automove()
        self._paddle.move()

    def keyReleaseEvent(self, e):
        if e.key() == Qt.Key_Left or e.key() == Qt.Key_Right:
            self._paddle.dx = 0

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Left:
            self._paddle.dx = -1
        elif e.key() == Qt.Key_Right:
            self._paddle.dx = 1
        elif e.key() == Qt.Key_P:
            self.pauseGame()
        elif e.key() == Qt.Key_Space:
            self.startGame()
        elif e.key() == Qt.Key_Escape:
            app.exit()
        else:
            QWidget.keyPressEvent(self, e)

    def startGame(self):
        if not self._gameStarted:
            QSound.play("sounds\Mario_Jumping.wav")
            self._ball.resetState()
            self._paddle.resetState()
            for i in range(Breakout.N_OF_BRICKS):
                self._bricks[i].destroyed = False
            self._gameOver = False
            self._gameWon = False
            self._gameStarted = True
            self._timerId = self.startTimer(Breakout.DELAY)


    def pauseGame(self):
        if self._paused:
            self._timerId = self.startTimer(Breakout.DELAY)
            self._paused = False
        else:
            self._paused = True
            self.killTimer(self._timerId)

    def stopGame(self):
        self.killTimer(self._timerId)
        self._gameOver = True
        self._gameStarted = False

    def victory(self):
        self.killTimer(self._timerId)
        self._gameWon = True
        self._gameStarted = False

    def checkCollision(self):
        if self._ball.rect.bottom() > self._bottom_edge:
            self.stopGame()

        j = 0
        for i in range(Breakout.N_OF_BRICKS):
            if self._bricks[i].destroyed:
                j += 1

        if j == Breakout.N_OF_BRICKS:
            self.victory()

        if self._ball.rect.intersects(self._paddle.rect):
            paddleLPos = self._paddle.rect.left()
            ballLPos = self._ball.rect.left()

            first = paddleLPos + 16
            second = paddleLPos + 32
            third = paddleLPos + 48
            fourth = paddleLPos + 64

            if ballLPos < first:
                self._ball.xdir *= -1
                self._ball.ydir *= -1

            if ballLPos >= first and ballLPos < second:
                pass
                # self._ball.xdir *= -1
                # self._ball.ydir *= -1

            if ballLPos >= second and ballLPos < third:
                self._ball.xdir = 0
                self._ball.ydir = -1

            if ballLPos >= third and ballLPos < fourth:
                self._ball.xdir = 1
                self._ball.ydir *= -1

            if ballLPos > fourth:
                self._ball.xdir = 1
                self._ball.ydir *= -1

            QSound.play("sounds\Mario_Jumping.wav")

        for i in range(Breakout.N_OF_BRICKS):
            if self._ball.rect.intersects(self._bricks[i].rect):
                ballLeft = self._ball.rect.left()
                ballHeight = self._ball.rect.height()
                ballWidth = self._ball.rect.width()
                ballTop = self._ball.rect.top()

                pointRight = QPoint(ballLeft + ballWidth + 1, ballTop)
                pointLeft = QPoint(ballLeft - 1, ballTop)
                pointTop = QPoint(ballLeft, ballTop - 1)
                pointBottom = QPoint(ballLeft, ballTop + ballHeight + 1)

                if not self._bricks[i].destroyed:
                    if self._bricks[i].rect.contains(pointRight):
                        self._ball.xdir = -1
                    elif self._bricks[i].rect.contains(pointLeft):
                        self._ball.xdir = 1

                    if self._bricks[i].rect.contains(pointTop):
                        self._ball.ydir = 1
                    elif self._bricks[i].rect.contains(pointBottom):
                        self._ball.ydir = -1

                    self._bricks[i].destroyed = True
                    QSound.play("sounds\Robot_blip_1.wav")
                    break


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Breakout(540, 800,"Breakout")
    # window.setFixedSize(300, 400)
    # window.setWindowTitle("Breakout")
    window.show()
    app.exec_()
