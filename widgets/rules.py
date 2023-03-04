from models import FolderTableModel
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtSql import *
from PyQt5.QtCore import *
from models import RuleTableModel

class RulesWidget(QVBoxLayout):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.setup_model()

    def setup_ui(self):
        icons_hbox = QHBoxLayout()
        self.add_btn = QPushButton()
        self.rm_btn = QPushButton()
        self.add_btn.setIcon(QIcon('icons/add rule.png'))
        self.add_btn.setToolTip('Add rule')
        self.rm_btn.setIcon(QIcon('icons/remove icon.png'))
        self.rm_btn.setToolTip('Remove rule')
        icons_hbox.addWidget(self.add_btn)
        icons_hbox.addWidget(self.rm_btn)
        icons_hbox.addStretch()
        rules_label = QLabel("Rules")
        self.rule_list = QListView()
        self.addLayout(icons_hbox)
        self.addWidget(rules_label)
        self.addWidget(self.rule_list)
        self.setContentsMargins(0, 0, 0, 0)
        self.setSpacing(7)

    def setup_model(self):
        self.model = RuleTableModel(self)
        self.model.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.model.setTable("RULE")
        self.rule_list.setModel(self.model)
        self.rule_list.setModelColumn(1)
        self.rule_list.setEditTriggers(QAbstractItemView.NoEditTriggers)