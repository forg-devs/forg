from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtSql import *
from PyQt5.QtWidgets import *
from sqlite3 import IntegrityError
import database
import buttons
from widgets.preview import PreviewDialog

class RuleDetailController():

    def __init__(self, rule_detail_widget):

        self.view = rule_detail_widget
        self.mapper = self.view.condition_mapper
        self.model = self.view.condition_model
        self.setup_signals_and_slots()

    def setup_signals_and_slots(self):
        self.view.select_folder_btn.clicked.connect(self.select_folder_clicked)
        self.view.actionscc.currentIndexChanged.connect(self.on_activated)
        self.view.save_btn.clicked.connect(self.save_button_clicked)
        self.view.discard_btn.clicked.connect(self.discard_button_clicked)


    def select_folder_clicked(self):
        selected_path = QFileDialog.getExistingDirectory()
        self.view.select_folder_btn.setToolTip(selected_path)
        if selected_path:
            self.view.select_folder_btn.setText("To {}"
                .format(QDir(selected_path).dirName()))

    def save_button_clicked(self):
        self.mapper.submit()

    def discard_button_clicked(self):
        self.mapper.revert()

    def on_activated(self):
        if self.view.actionscc.currentText() == 'Rename':
            self.view.rename_value.setHidden(False)
            self.view.select_folder_btn.setHidden(True)
        else:
            self.view.rename_value.setHidden(True)
            if self.view.actionscc.currentText() == 'Copy' or self.view.actionscc.currentText() == 'Move':
                self.view.select_folder_btn.setHidden(False)
            elif self.view.actionscc.currentText() == 'Delete' or self.view.actionscc.currentText() == 'Trash Bin':
                self.view.select_folder_btn.setHidden(True)
    

