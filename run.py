import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox
import uuid
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QInputDialog
from PyQt5.QtWidgets import QTableWidgetItem
from LayoutApp import LayoutApp
from LayoutApp2 import LayoutApp2

class BaseWindow(QMainWindow):
    def redirect_to_layout(self, index):
        widget.setCurrentIndex(index)

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        ui_file_path = os.path.join(os.path.dirname(__file__), 'HomePage.ui')
        loadUi(ui_file_path, self)  # Chargez le fichier UI directement
    
        # Connectez le clic du bouton pb1Button à la fonction de redirection avec l'indice 1
        self.pb1Button.clicked.connect(lambda: BaseWindow.redirect_to_layout(self,1))

        # connecter le clic du bouton pb2Button à la fonction de redirection avec l'indice 2
        self.pb2Button.clicked.connect(lambda: BaseWindow.redirect_to_layout(self,2))   

        layout_app = LayoutApp()
        layout2_app = LayoutApp2()
        # Récupérez le bouton returnHome de LayoutApp
        return_home_button = layout_app.get_return_home_button()
        # return_home_button2 = layout2_app.get_return_home_button()
        print(return_home_button)
        # Connectez le signal clicked du bouton returnHome à redirect_to_layout avec l'indice 0
        return_home_button.clicked.connect(lambda: BaseWindow.redirect_to_layout(self,0))
        # return_home_button2.clicked.connect(lambda: BaseWindow.redirect_to_layout(LayoutApp2,0))
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = QtWidgets.QStackedWidget()
    mainwindow = MyApp()
    layout = LayoutApp()
    layout2 = LayoutApp2()
    widget.addWidget(mainwindow)
    widget.addWidget(layout)
    widget.addWidget(layout2)
    widget.setWindowTitle("RO Application")
    widget.showMaximized()
    sys.exit(app.exec_())
