from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtSql import *
from PyQt5.QtWidgets import *
from sqlite3 import IntegrityError
import database
import buttons

class FoldersController(QObject):
    folder_error = pyqtSignal()
    def __init__(self, folders_widget):
        super().__init__()
        self.view = folders_widget
        self.model = folders_widget.model
        self.setup_signals_and_slots()

    def setup_signals_and_slots(self):
        self.view.folder_list.selectionModel().selectionChanged.connect(self.folder_selection_changed)
        self.view.add_btn.clicked.connect(self.add_folder)
        self.view.rm_btn.clicked.connect(self.remove_folder)

    def folder_selection_changed(self, selected, deselected):
        if selected.indexes():
            self.view.rm_btn.setEnabled(True)
        else:
            self.view.rm_btn.setEnabled(False)

    def add_folder(self):
        added = buttons.add_folder_clicked()
        if not added:
            # Folder dialog was closed without selecting folder
            if (added is None):
                pass
            else:
                self.folder_error.emit()
        self.model.select()


    def remove_folder(self):
        folder = self.selected_folder()
        if folder:
            database.remove_folder(folder)
            self.model.select()

    def selected_folder(self):
        index = self.view.folder_list.selectionModel().currentIndex()
        if index.isValid():
            path = index.sibling(index.row(), 2).data()
            return path
        else:
            return ""
    
