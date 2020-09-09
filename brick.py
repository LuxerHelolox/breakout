from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtMultimedia import QSound

class Brick:

    library = ""

    def __init__(self, library, x, y, color):
        Brick.library = library
        self._color = color
        self.resetState()
        self._rect = self.image.rect()
        self._rect.translate(x, y)
        Brick.blip = QSound("sounds\Robot_blip_1.wav")

    def resetState(self):
        self._image = QImage(Brick.library +"\\"+self._color+"_brick.png")  # img = QtGui.QImage()
        self._destroyed = False
        self._tick = 0
        self._stage = 1
        self._blackhit = 0

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

    def collision_behavior(self, score):
        if self._color == "purple":
            self._destroyed = True
            Brick.blip.play()
            #QSound.play("sounds\Robot_blip_1.wav")
            return score + 10, 10
        elif self._color == "yello":
            self._destroyed = True
            Brick.blip.play()
            return score * 2, score
        elif self._color == "black":
            if  self._blackhit<2:
                self._blackhit += 1
                self._image = QImage(Brick.library +"\\"+self._color+"_brick"+str(self._blackhit)+".png")
                return score, 0
            else:
                self._destroyed = True
                Brick.blip.play()
                return score + 30, 30
        else:
            self._destroyed = True
            Brick.blip.play()
            return score + 10, 10