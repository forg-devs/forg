from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtSql import *
from widgets.condition import Condition
import delegates


class ConditionWidget(QVBoxLayout):
    def __init__(self):
        super().__init__()
        self.condition_model = QSqlTableModel(self)
        self.condition_model.setTable("CONDITIONS")
        self.condition_model.setHeaderData
        self.condition_model.setEditStrategy(QSqlTableModel.OnRowChange)
        self.condition_mapper = QDataWidgetMapper(self)
        self.condition_mapper.setSubmitPolicy(QDataWidgetMapper.ManualSubmit)
        self.condition_mapper.setModel(self.condition_model)
        self.condition_mapper.setItemDelegate(delegates.ConditionItemDelegate(self))
        icons_hbox = QHBoxLayout()
        icons_hbox.addStretch()
        self.prev_btn = QPushButton()
        self.prev_btn.setIcon(QIcon('icons/preview.png'))
        self.prev_btn.setToolTip("Preview rule")
        self.run_btn = QPushButton()

        icons_hbox.addWidget(self.prev_btn)
        icons_hbox.addWidget(self.run_btn)
        self.addLayout(icons_hbox)

        self.run_btn.setIcon(QIcon('icons/pause.png'))
        self.run_btn.setToolTip('Pause')


        label_panel3 = QLabel("NAME: ")
        self.rule_name = QLineEdit()
        header_hbox = QHBoxLayout()
        header_hbox.addWidget(label_panel3)
        header_hbox.addWidget(self.rule_name)
        self.addLayout(header_hbox)

        self.condition = Condition()
        panel3_condition_hbox2_layout = QHBoxLayout()

        condition_label = QLabel('If all of the following conditions are met: ')
        

        btm_hbox = QHBoxLayout()
        self.save_btn = QPushButton("Save")
        self.discard_btn = QPushButton("Discard")
        btm_hbox.addStretch()
        btm_hbox.addWidget(self.save_btn)
        btm_hbox.addWidget(self.discard_btn)

        actions_label = QLabel('Do the following to the selected folder/files: ')
        self.actionscc = QComboBox()
        self.actionscc.addItem('Copy')
        self.actionscc.addItem('Move')
        self.actionscc.addItem('Delete')
        self.actionscc.addItem('Trash Bin')
        self.actionscc.addItem('Rename')
        self.select_folder_btn = QPushButton("Select Folder")

        self.rename_value = QLineEdit()
        self.rename_value.setHidden(True)
        panel3_condition_hbox2_layout.addWidget(self.actionscc)
        panel3_condition_hbox2_layout.addWidget(self.select_folder_btn)
        panel3_condition_hbox2_layout.addWidget(self.rename_value)
        panel3_condition_hbox2_layout.addStretch()
        self.addSpacing(30)
        self.addWidget(condition_label)
        self.addLayout(self.condition)
        self.addSpacing(30)
        self.addWidget(actions_label)
        self.addLayout(panel3_condition_hbox2_layout)
        self.addStretch()
        self.addLayout(btm_hbox)
        self.setAlignment(Qt.AlignTop)

        self.setup_mapping()

    def setup_mapping(self):
        self.condition_mapper.addMapping(self.condition.condition, 1, b'currentText')
        self.condition_mapper.addMapping(self.condition.operator, 2, b'currentText')
        self.condition_mapper.addMapping(self.condition.size_value, 3)
        self.condition_mapper.addMapping(self.condition.ext_value, 4)
        self.condition_mapper.addMapping(self.condition.date_edit, 5, b'date')
        self.condition_mapper.addMapping(self.condition.unit, 6, b'currentText')
        self.condition_mapper.addMapping(self.actionscc, 7, b'currentText')
        self.condition_mapper.addMapping(self.select_folder_btn, 8)
        self.condition_mapper.addMapping(self.rename_value, 9)
