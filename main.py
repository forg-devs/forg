import sys
from threading import Thread
import widgets.window as window
from PyQt5.QtWidgets import *
import background
import os
import style
from controllers.window_controller import WindowController
from widgets.window import Window
import database

app = QApplication(sys.argv)
app.setStyleSheet(style.style)
win_widget = Window()
win_controller = WindowController(win_widget)
win_controller.view.show()
daemon = Thread(target=background.main, daemon=True, name='Monitor')
daemon.start()
sys.exit(app.exec_())
