from PyQt4.QtCore import *
from PyQt4.QtGui import *


class Brick:

    library = ""

    def __init__(self, library, x, y, color):
        Brick.library = library
        self._color = color
        self.resetState()
        self._rect = self.image.rect()
        self._rect.translate(x, y)

    def resetState(self):
        self._image = QImage(Brick.library +"\\"+self._color+"_brick.png")  # img = QtGui.QImage()
        self._destroyed = False
        self._tick = 0
        self._stage = 1

    @property
    def rect(self):
        return self._rect

    @rect.setter
    def rect(self, rct):
        self._rect = rct

    @property
    def destroyed(self):
        return self._destroyed

    @destroyed.setter
    def destroyed(self, destr):
        self._destroyed = destr

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
    def stage(self):
        return self._stage

    @stage.setter
    def stage(self, stage):
        self._stage = stage

    @property
    def color(self):
        return self._color