import sys
from threading import Thread
import hazprac
from PyQt5.QtWidgets import *
import background
import os


app = QApplication(sys.argv)
window = hazprac.Window()
window.show()
daemon = Thread(target=background.main, daemon=True, name='Monitor')
daemon.start()
sys.exit(app.exec_())
