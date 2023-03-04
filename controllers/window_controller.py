from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtSql import *
from PyQt5.QtWidgets import *
import database
import buttons
from .rule_controller import RulesController
from .folder_controller import FoldersController
from .rule_detail_controller import RuleDetailController
from widgets.preview import PreviewDialog

class WindowController(QObject):

    def __init__(self, window_widget):
        super().__init__()

        self.view = window_widget
        self.setup_controllers()
        self.setup_signals_and_slots()
        self.folder_unselected()

    def setup_controllers(self):
        self.folder_cont = FoldersController(self.view.panel1)
        self.rule_cont = RulesController(self.view.panel2)
        self.rule_det_cont = RuleDetailController(self.view.panel3)

    

    def setup_signals_and_slots(self):
        self.rule_cont.view.rule_list.selectionModel().currentChanged.connect(self.init_rule_name)
        self.rule_det_cont.view.rule_name.returnPressed.connect(self.update_rule_name)
        self.rule_cont.view.rule_list.selectionModel().currentChanged.connect(self.rule_selected)
        self.folder_cont.view.folder_list.clicked.connect(self.rule_unselected)
        self.rule_cont.view.rm_btn.clicked.connect(self.rule_unselected)
        self.folder_cont.view.folder_list.clicked.connect(self.folder_selected)

        self.rule_cont.view.rule_list.selectionModel().currentChanged.connect(self.change_rule)
        self.folder_cont.view.folder_list.clicked.connect(lambda: self.rule_cont.init_rules(self.folder_cont.selected_folder()))
        self.rule_cont.view.add_btn.clicked.connect(lambda: self.rule_cont.add_rule(self.view, self.folder_cont.selected_folder()))

        self.rule_det_cont.view.run_btn.clicked.connect(self.run_button_clicked)
        self.rule_det_cont.view.prev_btn.clicked.connect(self.show_preview)
        # Errors
        self.folder_cont.folder_error.connect(self.show_folder_error)
        self.rule_cont.rule_error.connect(self.show_rule_error)




    def init_rule_name(self, item):
        self.rule_det_cont.view.rule_name.setText(item.data())

    def update_rule_name(self):
        # Make sure line edit is not blank
        panel3 = self.rule_det_cont.view
        panel2 = self.rule_cont.view
        old_name = self.rule_cont.selected_rule()
        if panel3.rule_name.text():
            # Update in RULE table
            index = panel2.rule_list.selectionModel().currentIndex()
            inserted = panel2.model.setData(index, panel3.rule_name.text())
            # Update in CONDITION table if returns True
            if inserted:
                success = database.update_condition_rule(old_name, panel3.rule_name.text())
                if not success:
                    # If CONDITIONS table updatation fails,
                    # revert RULE table modifications
                    panel2.model.revert()
            # Failed, probably due to being duplicate
            else:
                panel2.model.revert()
                QMessageBox.warning(self.view, "Rename Failed",
                                    "Rule with that name already exists.")
                # Focus rename widget and select text
                panel3.rule_name.setFocus()
                panel3.rule_name.selectAll()
        else:
            # Blank name was given
            QMessageBox.warning(self.view, "Rename Failed",
                                "Rule name can not be blank")

    def rule_selected(self):
        self.view.frame3.setLayout(self.rule_det_cont.view)
        self.view.frame3.show()
        self.view.no_rule_label.hide()

    def rule_unselected(self):
        self.view.frame3.hide()
        self.view.no_rule_label.show()

    def folder_selected(self, _):
        self.view.frame2.setLayout(self.rule_cont.view)
        self.view.frame2.show()
        self.view.no_folder_label.hide()
        self.view.no_rule_label.show()


    def folder_unselected(self):
        self.view.frame2.hide()
        self.view.no_rule_label.hide()
        self.view.no_folder_label.show()
        self.rule_cont.view.rm_btn.setEnabled(False)
        self.rule_cont.view.add_btn.setEnabled(False)
        self.rule_cont.view.rm_btn.setEnabled(False)

    def change_rule(self, index):
        self.rule_det_cont.model.setFilter("Rule = '{}'".format(index.data()))
        self.rule_det_cont.model.select()
        self.rule_det_cont.mapper.toFirst()

    def show_folder_error(self):
        QMessageBox.warning(self.view, "Failed",
                                    "Folder with that path exists")

    def show_rule_error(self):
        QMessageBox.warning(self.view, "Failed",
                                    "Rule with that name already exists")



    def run_button_clicked(self):
        rule = self.rule_cont.selected_rule()
        path = self.folder_cont.selected_folder()
        buttons.resume_pause_clicked(False, path, rule)

    def show_preview(self):
        rule = self.rule_cont.selected_rule()
        path = self.folder_cont.selected_folder()
        file_paths = buttons.resume_pause_clicked(True, path, rule)
        msg = "List of files that satisfy the condition"
        dial = PreviewDialog("Preview Rule", msg, file_paths)
        # It will show dialog and pause the code execution until dialog is closed
        # using dial.open() is recommended in documention but it doesn't work for me.
        dial.exec_()