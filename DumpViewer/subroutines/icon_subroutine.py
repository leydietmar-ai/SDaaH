from PySide6.QtGui import QIcon, QPixmap, QPainter, QFont
from PySide6.QtCore import Qt

def emoji_to_icon(emoji: str, size: int = 16) -> QIcon:
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.transparent)

    painter = QPainter(pixmap)
    font = QFont()
    font.setPointSize(size - 2)
    painter.setFont(font)
    painter.drawText(pixmap.rect(), Qt.AlignCenter, emoji)
    painter.end()

    return QIcon(pixmap)
