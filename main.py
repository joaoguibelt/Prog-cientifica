import sys
from mywindow import AppWindow
from PyQt5.QtWidgets import *
from OpenGL.GL import *
from PyQt5.QtGui import *


def main():
    app = QApplication(sys.argv)
    gui = AppWindow(scale_factor=1.0)
    gui.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
