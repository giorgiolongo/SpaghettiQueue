from qrcode.image.base import BaseImage
from qrcode import make as makeqr
from PyQt5.QtGui import QPixmap, QImage, QPainter
from PyQt5.QtCore import Qt

class PixmapImage(BaseImage):
    """
    A way to create Qt-Compatible qr codes and turn them to pixmaps
    """
    def __init__(self, border, width, box_size):
        self.border = border
        self.width = width
        self.box_size = box_size
        size = (width + border * 2) * box_size
        self._image = QImage(
            size, size, QImage.Format_RGB16)
        self._image.fill(Qt.white)

    def pixmap(self):
        return QPixmap.fromImage(self._image)

    def drawrect(self, row, col):
        painter = QPainter(self._image)
        painter.fillRect(
            (col + self.border) * self.box_size,
            (row + self.border) * self.box_size,
            self.box_size, self.box_size,
            Qt.black)

    def save(self, stream, kind=None):
        pass

def genqrpixmap(data: str):
    """
    Creates a qr pixmap with the given data
    """
    return makeqr(data, image_factory=PixmapImage).pixmap().scaled(150,150)