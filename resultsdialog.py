from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QTreeWidget, QTreeWidgetItem

class ResultsDialog(QDialog):
    def __init__(self, results):
        super().__init__()
        
        self.setWindowTitle("Results")
        self.resize(500, 500)
        
        layout = QVBoxLayout()
        self.setLayout(layout)
        categories = {
            'Images': [],
            'Documents': [],
            'Music': [],
            'Videos': [],
            'Other': []
            # Add more categories as needed
        }
        # Create a tree widget to display the results
        self.tree_widget = QTreeWidget()
        self.tree_widget.setHeaderLabels(['File Path', 'Action'])
        layout.addWidget(self.tree_widget)
        
        for file_path, action, category in results.items():
            categories[category].append((file_path, action))
        
        for category, files in categories.items():
            category_item = QTreeWidgetItem([category])
            self.tree_widget.addTopLevelItem(category_item)
            for file_path, action in files:
                file_item = QTreeWidgetItem([file_path, action])
                category_item.addChild(file_item)
                
        # Expand all items
        self.tree_widget.expandAll()
    
