from PyQt5.QtCore import *
from PyQt5.QtGui import *


class Paddle:

    library = ""

    def __init__(self, library, initial_x,initial_y, right_edge ):
        Paddle.library = library
        self._initial_x = initial_x
        self._initial_y = initial_y
        self._right_edge = right_edge - 80
        self._flash_pos = 0
        self.resetState()

    @property
    def dx(self):
        return self._dx

    @dx.setter
    def dx(self, x):
        self._dx = x

    def move(self):
        self._x += self._speed * self._dx
        if self._x < 0:
            self._x = 0
        elif self._x > self._right_edge:
            self._x = self._right_edge
        y = self._rect.top()
        self._rect.moveTo(int(self._x), y)

    def resetState(self):
        self._x = self._initial_x
        self._dx = 0
        self._image = QImage(Paddle.library +"\paddle.png")  # img = QtGui.QImage()
        self._rect = self.image.rect()
        self._rect.moveTo(self._initial_x, self._initial_y)
        self._speed = 2
        self._tick = 0

    @property
    def rect(self):
        return self._rect

    @property
    def image(self):
        return self._image

    @property
    def tick(self):
        return self._tick

    @tick.setter
    def tick(self, tick):
        self._tick = tick

    @property
    def flash_pos(self):
        return self._flash_pos

    @flash_pos.setter
    def flash_pos(self, flash_pos):
        self._flash_pos = flash_pos