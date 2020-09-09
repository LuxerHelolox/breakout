import random

from PyQt5.QtGui import *
from PyQt5.QtMultimedia import QSound


class Ball:
    physics = ""
    library = ""

    def __init__(self, library, physics, initial_x, initial_y, right_edge):
        self._initial_x = initial_x
        self._initial_y = initial_y
        self._right_edge = right_edge
        Ball.library = library
        Ball.physics = physics
        self.blip = QSound("sounds\Robot_blip_0.wav")
        random.seed()
        self.resetState()

    def resetState(self):
        self._image = QImage(Ball.library + "\\" + "ball.png")  # img = QtGui.QImage()
        self._rect = self._image.rect()
        if Ball.physics == "Classic":
            self._speed = 1
            self._xdir = 1
            self._ydir = -1
        else:
            self._speed = 1.414
            self._xdir = 0.7
            self._ydir = -0.7

        if random.random() - 0.5 < 0:
            self._xdir *= -1

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
        self._left += self._speed * self._xdir
        self._top += self._speed * self._ydir
        self._rect.moveTo(int(self._left), int(self._top))
        if self._rect.left() <= 0:
            self._xdir *= -1
            self.blip.play()
            # QSound.play("sounds\Robot_blip_0.wav")

        if self._rect.right() >= self._right_edge:
            self._xdir *= -1
            self.blip.play()

        if self._rect.top() <= 0:
            self._ydir *= -1
            self.blip.play()

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
