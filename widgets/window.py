from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtSql import *
import buttons
import os
import conditions
import database
import models
import delegates
import widgets.preview as preview
import widgets.emptylabels as emptylabels
from widgets.folders import FoldersWidget
from widgets.rules import RulesWidget
from widgets.rule_detail import ConditionWidget

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_database()
        self.setWindowTitle('File Organizer')
      
        main_window_vbox = QVBoxLayout()

        self.no_rule_label = emptylabels.EmptyLabel("No Rule Selected", "icons/norule.png")
        self.no_folder_label = emptylabels.EmptyLabel("No Folder Selected", "icons/nofolder.png")
        self.frame2 = QFrame()
        self.frame3 = QFrame()
      
        all_panel_hbox = QHBoxLayout()

        self.panel1 = FoldersWidget()

        # Panel 2 starts from here...

        self.panel2 = RulesWidget()

        # Panel 3 starts from here
        self.panel3 = ConditionWidget()
  
        # Packing layouts into the main window which is in vertical layout...

        all_panel_hbox.addLayout(self.panel1)
        all_panel_hbox.addWidget(self.no_folder_label, Qt.AlignCenter)
        all_panel_hbox.addWidget(self.frame2)
        all_panel_hbox.addWidget(self.no_rule_label, Qt.AlignCenter)

        all_panel_hbox.addWidget(self.frame3)
        self.frame3.hide()

        # Stretch factor of 1,1,3 leads to 20%, 20%, 60% used space
        # for panel 1,2,3 respectively
        all_panel_hbox.setStretchFactor(self.panel1, 1)
        # all_panel_hbox.addWidget(self.progress_bar)

        all_panel_hbox.setStretchFactor(self.frame2, 1)
        all_panel_hbox.setStretchFactor(self.frame3, 3)

        all_panel_hbox.setStretchFactor(self.no_rule_label, 3)
        all_panel_hbox.setStretchFactor(self.no_folder_label, 3)
        # main_window_vbox.addWidget(file_list)
        main_window_vbox.addLayout(all_panel_hbox)

        self.setLayout(main_window_vbox)
        self.setMinimumSize(900, 500)

    def setup_database(self):
        database.init_database()
        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName("database.db")
        db.open()