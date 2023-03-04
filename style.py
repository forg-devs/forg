style = """ 

QComboBox {
  border: 1px solid #c9c9c9;
  border-radius: 4px;
  background-color: #fff;
  padding: 4px 24px 4px 8px;
  font-family: "Lucida Grande", "Helvetica Neue", "Helvetica", "Arial", sans-serif;
  font-size: 13px;
  color: #333;
}

QComboBox:hover {
  border: 1px solid #999;
}

QComboBox:focus {
  border: 1px solid #5c9efa;
  outline: none;
}

QComboBox::drop-down {
  subcontrol-origin: padding;
  subcontrol-position: top right;
  width: 24px;
  border-left-width: 1px;
  border-left-color: #c9c9c9;
  border-left-style: solid;
  border-top-right-radius: 4px;
  border-bottom-right-radius: 4px;
  background-color: #fff;
}

QComboBox::down-arrow {
  image: url(/home/lorem/forg/icons/arrow.png);
  width: 12px;
  height: 12px;
}

QComboBox QAbstractItemView {
  border: 1px solid #c9c9c9;
  border-radius: 4px;
  background-color: #fff;
  font-family: "Lucida Grande", "Helvetica Neue", "Helvetica", "Arial", sans-serif;
  font-size: 13px;
  color: #333;
}

QComboBox QAbstractItemView::item {
  height: 20px;
  padding: 4px 8px;
}

QComboBox QAbstractItemView::item:selected {
  background-color: #99c1e6;
  color: #fff;
}

QDateEdit {
border: 1px solid #c9c9c9;
border-radius: 4px;
background-color: #fff;
padding: 2px 4px 2px 4px;
font-family: "Lucida Grande", "Helvetica Neue", "Helvetica", "Arial", sans-serif;
font-size: 13px;
color: #333;
min-width: 100px;}

QDateEdit:hover {
border: 1px solid #999;
}

QDateEdit:focus {
border: 1px solid #5c9efa;
outline: none;
}

QDateEdit::drop-down {
subcontrol-origin: padding;
subcontrol-position: top right;
width: 24px;
border-left-width: 1px;
border-left-color: #c9c9c9;
border-left-style: solid;
border-top-right-radius: 4px;
border-bottom-right-radius: 4px;
background-color: #fff;
}

QDateEdit::down-arrow {
image: url(/home/lorem/forg/icons/arrow.png);
width: 12px;
height: 12px;
}

QDateEdit QAbstractItemView {
border: 1px solid #c9c9c9;
border-radius: 4px;
background-color: #fff;
font-family: "Lucida Grande", "Helvetica Neue", "Helvetica", "Arial", sans-serif;
font-size: 13px;
color: #333;
}

QDateEdit QAbstractItemView::item {
height: 20px;
padding: 4px 8px;
}

QDateEdit QAbstractItemView::item:selected {
background-color: #99c1e6;
color: #fff;
}

QPushButton {
  border: 1px solid #c9c9c9;
  border-radius: 4px;
  background-color: qlineargradient(spread:pad, x1:0.5, y1:0, x2:0.5, y2:1, stop:0 #f5f5f5, stop:1 #e8e8e8);
  color: #333;
  font-family: "Lucida Grande", "Helvetica Neue", "Helvetica", "Arial", sans-serif;
  font-size: 13px;
  padding: 5px 10px;
}

QPushButton:hover {
  background-color: qlineargradient(spread:pad, x1:0.5, y1:0, x2:0.5, y2:1, stop:0 #e1e1e1, stop:1 #d8d8d8);
}

QPushButton:pressed {
  background-color: qlineargradient(spread:pad, x1:0.5, y1:0, x2:0.5, y2:1, stop:0 #d1d1d1, stop:1 #c8c8c8);
  border: 1px solid #c1c1c1;
  padding: 5px 10px 3px 10px;
}

/* QLineEdit */
QLineEdit {
border: 1px solid #c9c9c9;
border-radius: 4px;
background-color: qlineargradient(spread:pad, x1:0.5, y1:0, x2:0.5, y2:1, stop:0 #fff, stop:1 #f2f2f2);
padding: 2px 2px;
font-family: "Lucida Grande", "Helvetica Neue", "Helvetica", "Arial", sans-serif;
font-size: 13px;
color: #333;
}

QLineEdit:hover {
border: 1px solid #999;
}

QLineEdit:focus {
border: 1px solid #5c9efa;
outline: none;
}

QListView {
  background-color: #ffffff;
  border-radius: 8px;
  border: none;
  padding: 0;
  outline: none;
  color: #444444;
  font-size: 16px;
  background-clip: padding-box;
}

QListView::item {
  border: none;
  color: #444444;
  padding: 6px 10px;
  border-radius: 8px;
}

QListView::item:selected {
  background-color: #99b9d5f4;
  color: #444444;
}

QListView::item:hover {
  background-color: #f0f0f0;
}

QListView::indicator {
  width: 24px;
  height: 24px;
  border-radius: 12px;
  border: 1px solid #cccccc;
}

QListView::indicator:checked {
  image: url(./icons/checked_checkbox.png);
  border: 0px;
}

# QListView::indicator:unchecked {
#   image: url(:/icons/unchecked_checkbox.png);
# }

# QListView::indicator:checked:hover, QListView::indicator:unchecked:hover {
#   image: url(:/icons/mixed_checkbox.png);
# }

# QListView::indicator:checked:disabled {
#   image: url(:/icons/checked_checkbox_disabled.png);
# }

# QListView::indicator:unchecked:disabled {
#   image: url(:/icons/unchecked_checkbox_disabled.png);
# }

/* QDateEdit */

"""
  