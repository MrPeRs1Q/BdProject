from Controllers.dbController import *
from PyQt5 import QtWidgets, QtCore

class SettingdDialog(QtWidgets.QDialog):
    type = ''
    style = "font-family: 'Segoe UI', sans-serif; font-size: 21px; font-style: bold;"
    db = dbController()

    def __init__(self, parent=None):
        super(SettingdDialog, self).__init__(parent)
        self.setFixedSize(721, 414)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.resize(721, 414)
        self.centralwidget.setObjectName("centralwidget")
        self.setWindowTitle("Добавить проект")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.listView = QtWidgets.QListWidget(self.centralwidget)
        self.listView.setObjectName("listView")
        self.horizontalLayout.addWidget(self.listView)

        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label.setText("Добавить элемент")
        self.Addline = QtWidgets.QLineEdit(self.centralwidget)
        self.Addline.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.Addline, 0, 1, 1, 1)

        self.verticalLayout.addLayout(self.gridLayout)
        self.addButton = QtWidgets.QPushButton(self.centralwidget)
        self.addButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.addButton)
        self.addButton.setText("Добавить")
        self.addButton.pressed.connect(self.add_in_list)

        self.btnDelete = QtWidgets.QPushButton(self.centralwidget)
        self.btnDelete.setObjectName("pushButton_2")
        self.verticalLayout.addWidget(self.btnDelete)
        self.btnDelete.setText("Удалить")
        self.btnDelete.pressed.connect(self.delete)
        self.listView.setSelectionBehavior(QtWidgets.QListView.SelectItems)
        self.listView.selectionModel().selectionChanged.connect(self.on_selection_changed)
        self.on_selection_changed()
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.horizontalLayout.addLayout(self.verticalLayout)

        #self.retranslateUi(self.centralwidget)

    def on_selection_changed(self):
        self.btnDelete.setEnabled(
            bool(self.listView.selectionModel().selectedRows())
        )

    def setType(self, type):
        self.type = type
        self.update_list()

    def update_list(self):
        list =[]
        connection = self.db.create_connection()
        self.listView.clear()
        if self.type == 'state':
            list = self.db.get_state()
        if self.type == 'platform':
            list = self.db.get_platform()
        print(list)
        for item in list:
            self.listView.addItem(QtWidgets.QListWidgetItem(item[1]))
        connection.close()

    def add_in_list(self):
        connection = self.db.create_connection()
        if self.Addline.text() != '':
            if self.type == 'state':
                self.db.add_state(self.Addline.text())
            if self.type == 'platform':
                self.db.add_platform(self.Addline.text())
        self.update_list()
        self.Addline.clear()
        connection.close()

    def delete(self):
        connection = self.db.create_connection()
        if self.type == 'state':
            self.db.delete_state(self.listView.currentItem().text())
        if self.type == 'platform':
            self.db.delete_platform(self.listView.currentItem().text())
        self.update_list()
        connection.close()