from PyQt4.QtCore import *
from PyQt4.QtGui import *


class Brick:
    def __init__(self, library, x, y):
        self._destroyed = False
        self._image = QImage(library+"\\purple_brick.png")  # img = QtGui.QImage()
        self._rect = self.image.rect()
        self._rect.translate(x, y)

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
        return self._image  # in C++ it is reference, so the content may change!!!
