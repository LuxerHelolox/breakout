from PyQt4.QtCore import *
from PyQt4.QtGui import *


class ScoreItem(QObject):
    def __init__(self, painter, point, score):
        super(ScoreItem, self).__init__()
        self._painter = painter

    def _set_pos(self, pos):
        self._painter.translate(pos)

    pos = pyqtProperty(QPointF, fset=_set_pos)
