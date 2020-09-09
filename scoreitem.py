from PyQt5.QtCore import *
from PyQt5.QtGui import *


class ScoreItem(QObject):
    def __init__(self, x, y):
        super(ScoreItem, self).__init__()
        self._image = QImage("basic" + "\\" + "ball.png")  # img = QtGui.QImage()
        self._rect = self._image.rect()
        self._rect.moveTo(x, y)

    def _set_pos(self, pos):
        self._rect.moveTo(pos)

    @property
    def rect(self):
        return self._rect

    @property
    def image(self):
        return self._image

    pos = pyqtProperty(QPoint, fset=_set_pos)
