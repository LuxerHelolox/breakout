from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from brick import *
from paddle import *
from ball import *
from scoreitem import *
import sys
import random
import math

class Breakout(QWidget):
    N_OF_ROWS = 6
    N_OF_COLUMNS = 5
    N_OF_BRICKS = N_OF_ROWS * N_OF_COLUMNS
    BRICKHIGHT = 40
    BRICKWIDTH = 80
    DELAY = 5
    LASTWALL = 2
    LAYOUT = [[["purple", "purple", "purple", "purple", "purple"],
              ["purple", "purple", "purple", "purple", "purple"],
              ["purple", "purple", "yello", "purple", "purple"],
              ["purple", "purple", "purple", "purple", "purple"],
              ["purple", "purple", "purple", "purple", "purple"],
              ["purple", "purple", "purple", "purple", "purple"]],

              [["purple", "purple", "purple", "purple", "purple"],
              ["purple", "black", "black", "black", "purple"],
              ["purple", "black", "yello", "black", "purple"],
              ["purple", "black", "yello", "black", "purple"],
              ["purple", "black", "black", "black", "purple"],
              ["purple", "purple", "purple", "purple", "purple"]]]

    def __init__(self,breakout_width, breakout_height, breakout_title):
        QWidget.__init__(self)
        self._wall = 1
        self._gameOver = False
        self._gameWon = False
        self._paused = False
        self._gameStarted = False
        self._autopaddle = self.autopaddle = False
        self._bottom_edge = breakout_height
        self._physics = "Realistic"
        self._score = 0
        self._lastscore = 0
        self._scoreitems = []
        self._ball = Ball("android", self._physics , breakout_width/2+30, breakout_height-60, breakout_width )
        self._paddle = Paddle("android", breakout_width/2, breakout_height-40, breakout_width)
        self._bricks = [Brick("android", j * Breakout.BRICKWIDTH + 70, i * Breakout.BRICKHIGHT + 50,
                        Breakout.LAYOUT[self._wall -1][i][j])
                        for i in range(Breakout.N_OF_ROWS) for j in range(Breakout.N_OF_COLUMNS)]
        self.setFixedSize(breakout_width, breakout_height)
        self.setWindowTitle(breakout_title)
        self.blip = QSound("sounds\Robot_blip_0.wav")
        self.mario = QSound("sounds\Mario_Jumping.wav")

        # self.setBackgroundRole(QPalette.Dark)
        # self.setAutoFillBackground (True)


        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap("bkgnd.jpg")))
        self.setPalette(palette)

    def paintEvent(self, e):
        painter = QPainter(self)
        if self._gameOver:
            self.finishGame(painter, "Game lost")
            self.drawScore(painter, str(self._score))
        elif self._gameWon:
            self.finishGame(painter, "Victory")
            self.drawScore(painter, str(self._score))
        else:
            self.drawObjects(painter)
            if not self._gameStarted:
                self.drawWallNumber(painter)
            self.drawScore(painter, str(self._score))


    def finishGame(self, painter, message):
        painter.save()
        font = QFont("Courier", 24, QFont.Bold)
        fm = QFontMetrics(font)
        painter.setFont(font)
        textwidth = fm.width(message)
        painter.setPen(QColor(Qt.cyan))
        h = self.height()
        w = self.width()
        painter.translate(QPoint(w / 2, h / 2-30))
        painter.drawText(-textwidth / 2, 0, message)
        painter.restore()

        try:
            fo = open("bestscores.txt", "r")
            highscore = fo.read()
            fo.close()
        except:
            highscore = "0"

        if self._score < int(highscore):
            message ="No new High Score ("+highscore+")"
            painter.save()
            font = QFont("Courier", 18, QFont.Bold)
            painter.setPen(QColor(Qt.magenta))
            fm = QFontMetrics(font)
            painter.setFont(font)
            textwidth = fm.width(message)
            h = self.height()
            w = self.width()
            painter.translate(QPoint(w / 2, h / 2+30))
            painter.drawText(-textwidth / 2, 0, message)
            painter.restore()
        elif self._score == int(highscore):
            message ="You reached the old High Score"
            painter.save()
            font = QFont("Courier", 18, QFont.Bold)
            fm = QFontMetrics(font)
            painter.setPen(QColor(Qt.magenta))
            painter.setFont(font)
            textwidth = fm.width(message)
            h = self.height()
            w = self.width()
            painter.translate(QPoint(w / 2, h / 2+30))
            painter.drawText(-textwidth / 2, 0, message)
            painter.restore()
        else:
            message ="New High Score: "+ str(self._score)
            painter.save()
            font = QFont("Courier", 18, QFont.Bold)
            fm = QFontMetrics(font)
            painter.setPen(QColor(Qt.yellow))
            painter.setFont(font)
            textwidth = fm.width(message)
            h = self.height()
            w = self.width()
            painter.translate(QPoint(w / 2, h / 2+30))
            painter.drawText(-textwidth / 2, 0, message)
            painter.restore()
            fo = open("bestscores.txt", "w+")
            fo.write(str(self._score))
            fo.close()


    def drawScore(self, painter, score):
        font = QFont("Fantasy", 16, QFont.Bold)
        fm = QFontMetrics(font)
        textwidth = fm.width(score)
        painter.setFont(font)
        h = self.height()
        w = self.width()
        painter.save()
        painter.setPen(QColor(Qt.yellow))
        painter.translate(QPoint(w - 25, 25))
        painter.drawText(-textwidth / 2, 0, score)
        painter.restore()
        painter.setPen(QColor(Qt.red))
        if not self._gameOver and not self._gameWon:
            for scoreitem in self._scoreitems:
                painter.save()
                font = QFont("Fantasy", 14, QFont.Bold)
                painter.translate(QPoint(scoreitem[1], scoreitem[2]))
                painter.drawText(0, - 10, str(scoreitem[0]))
                painter.restore()
                scoreitem[3] -= 1
                if scoreitem[3] <= 0:
                    self._scoreitems.remove(scoreitem)


    def drawObjects(self, painter):
        painter.drawImage(self._ball.rect, self._ball.image)
        painter.drawImage(self._paddle.rect, self._paddle.image)
        if self._paddle.tick > 0:
            self._paddle.tick -= 1
            painter.drawImage(self._paddle.rect.left() + 16* self._paddle.flash_pos,self._paddle.rect.top(),
                              QImage("pow-low.png"))
        for i in range(Breakout.N_OF_BRICKS):
            if not self._bricks[i].destroyed:
                painter.drawImage(self._bricks[i].rect, self._bricks[i].image)

    def drawWallNumber(self, painter):
        message = "Wall n." + str(self._wall)
        font = QFont("Fantasy", 24, QFont.Bold)
        fm = QFontMetrics(font)
        textwidth = fm.width(message)
        painter.setFont(font)
        h = self.height()
        w = self.width()
        painter.save()
        painter.setPen(QColor(Qt.red))
        painter.translate(QPoint(w / 2, h / 2-30))
        painter.drawText(-textwidth / 2, 0, message)
        painter.restore()

    def timerEvent(self, e):
        self.moveObjects()
        self.checkCollision()
        self.repaint()

    def moveObjects(self):
        self._ball.automove()
        self._paddle.move()

    def keyReleaseEvent(self, e):
        if not self._autopaddle and(e.key() == Qt.Key_Left or e.key() == Qt.Key_Right):
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
            if self._gameWon:
                if self._wall <Breakout.LASTWALL:
                    self._wall +=1
                    self._bricks = [Brick("android", j * Breakout.BRICKWIDTH + 70, i * Breakout.BRICKHIGHT + 50,
                                          Breakout.LAYOUT[self._wall - 1][i][j])
                                    for i in range(Breakout.N_OF_ROWS) for j in range(Breakout.N_OF_COLUMNS)]
                    self._ball.resetState()
                    self._paddle.resetState()
                    for i in range(Breakout.N_OF_BRICKS):
                        self._bricks[i].resetState()
                    self._gameOver = False
                    self._gameWon = False
                    self._lastscore = self._score
                    self._scoreitems = []
                    self.repaint()

            else:
                #QSound.play("sounds\Mario_Jumping.wav")
                self.mario.play()
                self._ball.resetState()
                self._paddle.resetState()
                for i in range(Breakout.N_OF_BRICKS):
                    self._bricks[i].resetState()
                self._gameOver = False
                self._gameWon = False
                self._gameStarted = True
                self._timerId = self.startTimer(Breakout.DELAY)
                self._autopaddle = self.autopaddle
                self._score = self._lastscore

    def resetGame(self):
        if self._paused:
            self._paused = False
        else:
            self.killTimer(self._timerId)
        self.killTimer(self._timerId)
        self._ball.resetState()
        self._paddle.resetState()
        for i in range(Breakout.N_OF_BRICKS):
            self._bricks[i].resetState()
        self._gameOver = False
        self._gameWon = False
        self._gameStarted = False
        self._score = 0
        self.repaint()

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
        QSound.play("sounds\Crowd Boo.wav")

    def victory(self):
        self.killTimer(self._timerId)
        self._gameWon = True
        self._gameStarted = False
        QSound.play("sounds\Audience_Applause.wav")

    def checkCollision(self):
        if self._ball.rect.bottom() > self._bottom_edge:
            self.stopGame()

        if not self._ball.rect.bottom() > self._bottom_edge-38:
            j = 0
            for i in range(Breakout.N_OF_BRICKS):
                if self._bricks[i].destroyed:
                    if self._wall== Breakout.LASTWALL:
                        self._bricks[i].tick += 1
                        if self._bricks[i].tick > 20000:
                            # ez igy nagyon nem koser mert ott lehet a labda!!!
                            self._bricks[i].destroyed = False
                            self._bricks[i].tick = 0
                            self._bricks[i].stage += 1
                            #QSound.play("sounds\Robot_blip_0.wav")
                            self.blip.play()

                    else:
                        j += 1

            if j == Breakout.N_OF_BRICKS:
                self.victory()

            if self._ball.rect.intersects(self._paddle.rect):

                self._scoreitems.append([-5,self._ball.rect.left(),self._ball.rect.top(),30])
                self._paddle.tick = 30

                self._score -= 5
                if self._score <0:
                    self._score = 0

                paddleLPos = self._paddle.rect.left()
                ballMiddle = self._ball.rect.left() + self._ball.rect.width()/2

                first = paddleLPos + 16
                second = paddleLPos + 32
                third = paddleLPos + 48
                fourth = paddleLPos + 64

                if self._physics == "Classic":

                    if ballMiddle < first:
                        self._ball.xdir = -1
                        self._ball.ydir = -1
                        self._paddle.flash_pos = 0
                    elif ballMiddle >= first and ballMiddle < second:
                        self._ball.xdir = -1
                        self._ball.ydir *= -1
                        self._paddle.flash_pos = 1
                    elif ballMiddle >= second and ballMiddle < third:
                        self._ball.xdir = 0
                        self._ball.ydir = -1
                        self._paddle.flash_pos = 2
                    elif ballMiddle >= third and ballMiddle < fourth:
                        self._ball.xdir = 1
                        self._ball.ydir *= -1
                        self._paddle.flash_pos = 3
                    else :
                        self._ball.xdir = 1
                        self._ball.ydir = -1
                        self._paddle.flash_pos = 4

                elif self._physics == "Randomized":

                    if ballMiddle < first:
                        self._ball.xdir = -0.866
                        self._ball.ydir = - 0.5
                        self._paddle.flash_pos = 0
                    elif ballMiddle >= first and ballMiddle < second:
                        self._ball.xdir = - 0.7
                        self._ball.ydir = -0.7
                        self._paddle.flash_pos = 1
                    elif ballMiddle >= second and ballMiddle < third:
                        self._ball.xdir = 0.5
                        self._ball.ydir = - 0.866
                        if random.random() - 0.5 < 0:
                            self._ball.xdir *= -1
                        self._paddle.flash_pos = 2
                    elif ballMiddle >= third and ballMiddle < fourth:
                        self._ball.xdir = 0.7
                        self._ball.ydir = - 0.7
                        self._paddle.flash_pos = 3
                    else:
                        self._ball.xdir = 0.866
                        self._ball.ydir = - 0.5
                        self._paddle.flash_pos = 4
                else:
                    if ballMiddle < first:
                        self._paddle.flash_pos = 0
                    elif ballMiddle >= first and ballMiddle < second:
                        self._paddle.flash_pos = 1
                    elif ballMiddle >= second and ballMiddle < third:
                        self._paddle.flash_pos = 2
                    elif ballMiddle >= third and ballMiddle < fourth:
                        self._paddle.flash_pos = 3
                    else:
                        self._paddle.flash_pos = 4

                    if self._paddle.dx == 0:
                        self._ball.ydir *= -1
                    elif  self._paddle.dx < 0:
                        if self._ball.xdir == -0.866 or self._ball.xdir == - 0.7:
                            self._ball.xdir = -0.866
                            self._ball.ydir = - 0.5
                        elif self._ball.xdir == -0.5:
                            self._ball.xdir = - 0.7
                            self._ball.ydir = -0.7
                        elif self._ball.xdir == 0.866:
                            self._ball.xdir = 0.7
                            self._ball.ydir = - 0.7
                        else:
                            self._ball.xdir = 0.5
                            self._ball.ydir = - 0.866
                    else:
                        if self._ball.xdir == 0.866 or self._ball.xdir == 0.7:
                            self._ball.xdir = 0.866
                            self._ball.ydir = - 0.5
                        elif self._ball.xdir == 0.5:
                            self._ball.xdir =  0.7
                            self._ball.ydir = -0.7
                        elif self._ball.xdir == - 0.866:
                            self._ball.xdir = - 0.7
                            self._ball.ydir = - 0.7
                        else:
                            self._ball.xdir = - 0.5
                            self._ball.ydir = - 0.866

                #QSound.play("sounds\Mario_Jumping.wav")
                self.mario.play()


        for i in range(Breakout.N_OF_BRICKS):
            if self._ball.rect.intersects(self._bricks[i].rect):
                if not self._bricks[i].destroyed:
                    self._score, scoredelta = self._bricks[i].collision_behavior(self._score)
                    self._scoreitems.append([scoredelta, self._ball.rect.left(), self._ball.rect.top(), 30])

                    ballLeft = self._ball.rect.left()
                    ballHeight = self._ball.rect.height()
                    ballWidth = self._ball.rect.width()
                    ballTop = self._ball.rect.top()

                    pointTopMiddle = QPoint(ballLeft + ballWidth / 2, ballTop - 1)
                    pointBottomMiddle = QPoint(ballLeft + ballWidth / 2, ballTop + ballHeight + 1)
                    pointLeftMiddle = QPoint(ballLeft - 1, ballTop + ballHeight / 2)
                    pointRightMiddle = QPoint(ballLeft + ballWidth + 1, ballTop + ballHeight / 2)

                    if self._bricks[i].rect.contains(pointTopMiddle):
                        self._ball.ydir *= -1
                    elif self._bricks[i].rect.contains(pointBottomMiddle):
                        self._ball.ydir *= -1
                    elif self._bricks[i].rect.contains(pointLeftMiddle):
                        self._ball.xdir *= -1
                    elif self._bricks[i].rect.contains(pointRightMiddle):
                        self._ball.xdir *= -1
                    else:

                        pointTopRight = QPoint(ballLeft + ballWidth + 1, ballTop)
                        pointTopLeft = QPoint(ballLeft - 1, ballTop)
                        pointLeftTop = QPoint(ballLeft, ballTop - 1)
                        pointLeftBottom = QPoint(ballLeft, ballTop + ballHeight + 1)

                        pointBottomRight = QPoint(ballLeft + ballWidth + 1, ballTop + ballHeight)
                        pointBottomLeft = QPoint(ballLeft - 1, ballTop + ballHeight)
                        pointRightTop = QPoint(ballLeft + ballWidth, ballTop - 1)
                        pointRightBottom = QPoint(ballLeft + ballWidth, ballTop + ballHeight + 1)


                        if self._bricks[i].rect.contains(pointTopRight) and self._ball.xdir > 0:
                            self._ball.xdir = -1 * math.fabs(self._ball.xdir)
                        if self._bricks[i].rect.contains(pointTopLeft)and self._ball.xdir < 0 :
                            self._ball.xdir = math.fabs(self._ball.xdir)
                        if self._bricks[i].rect.contains(pointLeftTop)and self._ball.ydir < 0:
                            self._ball.ydir = math.fabs(self._ball.ydir)
                        if self._bricks[i].rect.contains(pointLeftBottom)and self._ball.ydir > 0:
                            self._ball.ydir = -1 * math.fabs(self._ball.ydir)
                        if self._bricks[i].rect.contains(pointBottomRight) and self._ball.xdir > 0:
                            self._ball.xdir = -1 * math.fabs(self._ball.xdir)
                        if self._bricks[i].rect.contains(pointBottomLeft)and self._ball.xdir < 0 :
                            self._ball.xdir = math.fabs(self._ball.xdir)
                        if self._bricks[i].rect.contains(pointRightTop)and self._ball.ydir < 0:
                            self._ball.ydir = math.fabs(self._ball.ydir)
                        if self._bricks[i].rect.contains(pointRightBottom)and self._ball.ydir > 0:
                            self._ball.ydir = -1 * math.fabs(self._ball.ydir)

                    break

    def changeskin(self,library):
        Ball.library = library
        Brick.library = library
        Paddle.library = library

    def changephysics(self,physics):
        self._physics = Ball.physics = physics

    def scoreItemAnimation(self):
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Breakout(540, 800,"Breakout")
    # window.setFixedSize(300, 400)
    # window.setWindowTitle("Breakout")
    window.show()
    app.exec_()
