from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtSql import *
from PyQt5.QtWidgets import *
import database

class RulesController(QObject):
    rule_error = pyqtSignal()
    def __init__(self, rules_widget):
        super().__init__()
        self.view = rules_widget
        self.model = rules_widget.model
        self.setup_signals_and_slots()

    def setup_signals_and_slots(self):
        self.view.rule_list.selectionModel().selectionChanged.connect(self.rule_selection_changed)
        self.view.rm_btn.clicked.connect(self.remove_rule)

    def rule_selection_changed(self, selected, _):
        if selected.indexes():
            self.view.rm_btn.setEnabled(True)
        else:
            self.view.rm_btn.setEnabled(False)

    def add_rule(self, window, folder):
        text, ok = QInputDialog.getText(window, 'New rule', 'Enter name:')
        if ok and text:
            record = self.model.record()
            record.setValue("F_ID", database.get_folder_id(folder))
            record.setValue("Rule_Name", text)
            record.setValue("State", 0)
            if (self.model.insertRecord(-1, record)):
                database.insertCondition(text)
            else:
                self.rule_error.emit()


    def remove_rule(self):
        if self.selected_rule():
            database.remove_rule(self.selected_rule())
            self.model.select()
            self.view.rm_btn.setEnabled(False)

    def init_rules(self, path):
        self.model.setFilter("F_ID = {}".format(database.get_folder_id(path)))
        self.model.select()
        self.view.add_btn.setEnabled(True)   
        
    def selected_rule(self):
        index = self.view.rule_list.selectionModel().currentIndex()
        if index.isValid():
            return index.data()
        else:
            return ""
