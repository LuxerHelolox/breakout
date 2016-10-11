from PyQt4.QtCore import *
from PyQt4.QtGui import *


class Brick:

    library = ""

    def __init__(self, library, x, y):
        Brick.library = library
        self.resetState()
        self._rect = self.image.rect()
        self._rect.translate(x, y)

    def resetState(self):
        self._image = QImage(Brick.library +"\\"+"purple_brick.png")  # img = QtGui.QImage()
        self._destroyed = False

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
