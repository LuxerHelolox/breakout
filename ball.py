from PyQt4.QtCore import *
from PyQt4.QtGui import *
import random
import math

class Ball():

    def __init__(self,library,initial_x,initial_y, right_edge):
        self._initial_x = initial_x
        self._initial_y = initial_y
        self._right_edge = right_edge
        self._image = QImage(library +"\\"+"ball.png")  # img = QtGui.QImage()
        self._rect = self.image.rect()
        self.resetState()

    def resetState(self):
        self._xdir = 0.5 + random.random()/2
        self._ydir = -(math.sqrt ( 2- self._xdir*self._xdir))
        self._left = self._initial_x
        self._top = self._initial_y
        self._rect.moveTo(self._initial_x, self._initial_y)

    @property
    def rect(self):
        return self._rect

    @property
    def image(self):
        return self._image

    def automove(self):
        self._left += self._xdir
        self._top += self._ydir
        self._rect.moveTo(int(self._left), int(self._top))
        if self._rect.left() == 0:
            self._xdir *= -1
            QSound.play("sounds\Robot_blip_0.wav")

        if self._rect.right() == self._right_edge:
            self._xdir *= -1
            QSound.play("sounds\Robot_blip_0.wav")

        if self._rect.top() == 0:
            self._ydir *= -1
            QSound.play("sounds\Robot_blip_0.wav")

    @property
    def xdir(self):
        return self._xdir

    @xdir.setter
    def xdir(self, x):
        self._xdir = x

    @property
    def ydir(self):
        return self._ydir

    @ydir.setter
    def ydir(self, y):
        self._ydir = y
