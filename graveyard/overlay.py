import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow
from PyQt5.QtCore import Qt, QTimer

class Overlay(QMainWindow):
    def __init__(self, message="Working…"):
        super().__init__()

        self.setWindowFlags(
            Qt.WindowStaysOnTopHint |
            Qt.FramelessWindowHint
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("background: rgba(0, 0, 0, 160);")

        label = QLabel(message, self)
        label.setStyleSheet("color: white; font: 20pt monotype; padding: 30px 30px;")
        label.adjustSize()
        margin = 0
        self.setFixedSize(
            label.sizeHint().width() + margin,
            label.sizeHint().height() + margin
        )
        self.move(50, 50)

        # Automatically close after timeout
        QTimer.singleShot(3000, self.close)

def main(message="Working…"):
    app = QApplication(sys.argv)
    w = Overlay(message)
    w.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    # Basic CLI interface: overlay.py "Message..."
    msg = sys.argv[1]
    main(msg)
