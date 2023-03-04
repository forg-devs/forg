from models import FolderTableModel
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtSql import *
from PyQt5.QtCore import *

class FoldersWidget(QVBoxLayout):
    """Forg's folder widget containing list of added folders"""
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.setup_model()
    
    def setup_ui(self):
        icons_hbox = QHBoxLayout()
        self.add_btn = QPushButton()
        self.rm_btn = QPushButton()
        self.add_btn.setIcon(QIcon('icons/add folder.png'))
        self.add_btn.setToolTip('Add Folder')
        self.rm_btn.setIcon(QIcon('icons/remove icon.png'))
        self.rm_btn.setToolTip('Remove Folder')
        icons_hbox.addWidget(self.add_btn)
        icons_hbox.addWidget(self.rm_btn)
        icons_hbox.addStretch()
        folders_label = QLabel("Folders")
        self.folder_list = QListView()
        self.addLayout(icons_hbox)
        self.addWidget(folders_label)
        self.addWidget(self.folder_list)
        self.setSpacing(7)

    # Initialise database model
    def setup_model(self):
        self.model = FolderTableModel(self)
        self.model.setTable("FOLDER")
        self.folder_list.setModel(self.model)
        self.folder_list.setModelColumn(1)
        self.folder_list.setEditTriggers(QListView.NoEditTriggers)
        self.model.setData(self.folder_list.selectionModel().currentIndex(), Qt.DecorationRole)
        self.model.select()
