import functools
from GUI.Gui import *
from GUI.WindowProjectAdd import *
from GUI.SettingsDialog import *
import sys

class MyWin(QtWidgets.QMainWindow):
    db = dbController()
    list = []
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindo()
        self.ui.setupUi(self)
        self.ui.addButton.clicked.connect(self.AddDialog)
        self.ui.stateEditButton.pressed.connect(self.StateDialog)
        self.ui.platformEditBtn.pressed.connect(self.PlatformDialog)
        self.ui.sortButton.pressed.connect(self.updateChanged)
        self.ui.searchButton.pressed.connect(self.updateChanged)
        self.updateChanged()


    def ChangeDialog(self, PK):
        dialog = WindowProjectAdd(self)
        dialog.setType('Change')
        dialog.change_func(PK)
        dialog.exec_()
        self.ui.updateTable(True, 0, self.list)
        self.updateChanged()
        #print(PK)

    def updateChanged(self):
        connection = self.db.create_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT project_id FROM project ORDER BY project_id")
        list = self.ui.g_list
        self.list = self.ui.g_list
        if len(list) == 0:
            list = cursor.fetchall()
        print(list)
        for i in range(self.ui.list_len):
            btn = self.ui.tableWidget.cellWidget(i, 5)
            btn.pressed.connect(functools.partial(self.ChangeDialog, list[i][0]))
        connection.close()

    def AddDialog(self):
        dialog = WindowProjectAdd(self)
        dialog.setType('Add')
        dialog.exec_()
        self.ui.updateTable(True, 1)
        #self.ui.updateTable(True, 0, self.list)
        self.updateChanged()

    def StateDialog(self):
        dialog = SettingdDialog(self)
        dialog.setType('state')
        dialog.exec_()
        self.ui.updateTable(False, 0)

    def PlatformDialog(self):
        dialog = SettingdDialog(self)
        dialog.setType('platform')
        dialog.exec_()
        self.ui.updateTable(False, 0)

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MyWin()
    window.show()
    sys.exit(app.exec_())
