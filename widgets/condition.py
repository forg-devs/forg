from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtSql import *

class Condition(QHBoxLayout):
    def __init__(self):
        super().__init__()
        model = QStandardItemModel()
        self.condition = QComboBox()
        self.condition.setModel(model)
        self.operator = QComboBox()
        self.operator.setModel(model)

        # Display Calender Here....

        self.date_edit = QDateEdit(calendarPopup=True)
        self.date_edit.setDateTime(QDateTime.currentDateTime())
        self.date_edit.setHidden(True)

        def update_date():
            self.date_edit.date().toString('yyyyMMdd')

        self.date_edit.editingFinished.connect(update_date)

        condition_combobox_data = {
            'Size': ['is', 'less than', 'greater than'],
            'Extension': ['is', 'is not'],
            'Date Added': ['is', 'is before', 'is after']
        }
        units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
        for condition_combobox_key, condition_combobox_value in condition_combobox_data.items():
            combobox_item = QStandardItem(condition_combobox_key)
            model.appendRow(combobox_item)
            for self.size_value in condition_combobox_value:
                combobox1_item = QStandardItem(self.size_value)
                combobox_item.appendRow(combobox1_item)

        def update_combobox1(index):
            index_value = model.index(index, 0, self.condition.rootModelIndex())
            self.operator.setRootModelIndex(index_value)
            self.operator.setCurrentIndex(0)

        self.condition.currentTextChanged.connect(lambda x: update_combobox1(self.condition.currentIndex()))
        update_combobox1(0)

        self.size_value = QLineEdit()
        self.size_value.setValidator(QDoubleValidator())
        self.ext_value = QLineEdit()
        self.ext_value.setHidden(True)
        self.unit = QComboBox()
        for u in units:
            self.unit.addItem(u)


        def onActivated():
            if self.condition.currentText() == 'Extension':
                self.ext_value.setHidden(False)
                self.size_value.setHidden(True)
                self.unit.setHidden(True)
                self.date_edit.setHidden(True)
            if self.condition.currentText() == 'Date Added':
                self.date_edit.setHidden(False)
                self.size_value.setHidden(True)
                self.ext_value.setHidden(True)
                self.unit.setHidden(True)
            if self.condition.currentText() == 'Size':
                self.size_value.setHidden(False)
                self.unit.setHidden(False)
                self.date_edit.setHidden(True)
                self.ext_value.setHidden(True)

        self.condition.currentIndexChanged.connect(onActivated)

        self.addWidget(self.condition)
        self.addWidget(self.operator)
        self.addWidget(self.size_value)
        self.addWidget(self.unit)
        self.addWidget(self.date_edit)
        self.addWidget(self.ext_value)
        self.addStretch()