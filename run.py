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

class LayoutApp(QMainWindow):
    def __init__(self):
        super().__init__()
        ui_file_path = os.path.join(os.path.dirname(__file__), 'layout.ui')
        loadUi(ui_file_path, self)  # Load the UI file directly

        # Connectez le bouton returnHome à la fonction de redirection avec l'indice 0
        self.returnHome.clicked.connect(lambda: BaseWindow.redirect_to_layout(self,0))


        self.graph = {
            'nodes': {},
            'edges': {},
        }
        self.node_lables = {}


        self.add_node_button.clicked.connect(self.add_node)
        self.add_edge_button.clicked.connect(self.add_edge)

        self.result_info_display.hide()
        self.error_display.hide()

        self.node_input_table.setHorizontalHeaderLabels(
            ["Node ID", "Label", "Entry", "Exit", ""])
        self.edge_input_table.setHorizontalHeaderLabels(
            ["Edge ID", "Start Node", "End Node", "Weight", "Duration", ""])
        self.calculate_button.clicked.connect(self.calculate_shortest_path)

        self.add_node_button.setFixedWidth(
            self.add_node_button.sizeHint().width()+10)
        self.add_edge_button.setFixedWidth(
            self.add_edge_button.sizeHint().width()+10)

        self.calculate_button.setFixedHeight(
            self.calculate_button.sizeHint().height()+10)

        self.clear_button.setFixedHeight(
            self.clear_button.sizeHint().height()+10)

    def add_node(self):

        while True:
            label, ok = QInputDialog.getText(self, "Input", "Enter node label:")
            if not ok:
                return
            
            if label in self.node_lables.values():
                QMessageBox.warning(
                    self, "Error", "This label already exists.")
                continue

            break

        x, ok = QInputDialog.getInt(self, "Input", "Enter entry constraint:")
        if not ok:
            return

        y, ok = QInputDialog.getInt(self, "Input", "Enter exit constraint:")
        if not ok:
            return

        node_id = str(uuid.uuid4())

        self.graph['nodes'][node_id] = (x, y)
        self.node_lables[node_id] = label

        self.start_node_combo.addItem(label)
        self.end_node_combo.addItem(label)

        row_position = self.node_input_table.rowCount()
        self.node_input_table.insertRow(row_position)

        # Set the values for the new row
        self.node_input_table.setItem(
            row_position, 0, QTableWidgetItem(node_id))
        self.node_input_table.setItem(
            row_position, 1, QTableWidgetItem(label))
        self.node_input_table.setItem(
            row_position, 2, QTableWidgetItem(str(x)))
        self.node_input_table.setItem(
            row_position, 3, QTableWidgetItem(str(y)))

        remove_node_button = QtWidgets.QPushButton("Remove Node")
        remove_node_button.clicked.connect(
            lambda: self.remove_node(row_position))

        self.node_input_table.setCellWidget(
            row_position, 4, remove_node_button)
        print(self.graph)
        print(self.node_lables)

    def add_edge(self):

        if len(self.graph['nodes']) < 2:
            QMessageBox.warning(
                self, "Error", "You need to add at least two nodes before adding edges.")
            return

        nodes = list(self.node_lables.values())

        while True:
            start_node, ok = QInputDialog.getItem(
                self, "Input", "Select start node:", nodes, 0, False)
            if not ok:
                return

            while True:
                end_node, ok = QInputDialog.getItem(
                    self, "Input", "Select end node:", nodes, 0, False)
                if not ok:
                    return

                if start_node == end_node:
                    QMessageBox.warning(
                        self, "Error", "The start node and end node cannot be the same.")
                    continue

                # Check if the edge already exists in the graph
                if (start_node, end_node) in self.graph['edges']:
                    QMessageBox.warning(
                        self, "Error", "This edge already exists.")
                    break

                # If the edge doesn't exist, exit the loop
                break

            # If the edge exists, start over from the beginning
            if (start_node, end_node) in self.graph['edges']:
                continue

            # If the edge doesn't exist, exit the loop
            break

        weight, ok = QInputDialog.getDouble(self, "Input", "Enter weight:")
        if not ok:
            return

        duration, ok = QInputDialog.getDouble(self, "Input", "Enter duration:")
        if not ok:
            return

        edge_id = str(uuid.uuid4())

        # Add the edge to the graph
        self.graph['edges'][(start_node, end_node)] = {
            'weight': weight, 'duration': duration}

        row_position = self.edge_input_table.rowCount()
        self.edge_input_table.insertRow(row_position)

        # Set the values for the new row
        self.edge_input_table.setItem(
            row_position, 0, QTableWidgetItem(edge_id))
        self.edge_input_table.setItem(
            row_position, 1, QTableWidgetItem(start_node))
        self.edge_input_table.setItem(
            row_position, 2, QTableWidgetItem(end_node))
        self.edge_input_table.setItem(
            row_position, 3, QTableWidgetItem(str(weight)))
        self.edge_input_table.setItem(
            row_position, 4, QTableWidgetItem(str(duration)))

        remove_edge_button = QtWidgets.QPushButton("Remove Edge")
        remove_edge_button.clicked.connect(
            lambda: self.remove_edge(row_position))

        self.edge_input_table.setCellWidget(
            row_position, 5, remove_edge_button)
        print(self.graph)

    def remove_edge(self, row_position):
        # Get the start and end nodes of the edge from the table
        start_node = self.edge_input_table.item(row_position, 1).text()
        end_node = self.edge_input_table.item(row_position, 2).text()

        # Remove the edge from the graph
        del self.graph['edges'][(start_node, end_node)]

        # Remove the row from the table
        self.edge_input_table.removeRow(row_position)

        print(self.graph)

    def remove_node(self, row_position):
        node_id = self.node_input_table.item(row_position, 0).text()
        label = self.node_input_table.item(row_position, 1).text()

        del self.graph['nodes'][node_id]
        del self.node_lables[node_id]

        self.start_node_combo.removeItem(
            self.start_node_combo.findText(label))
        self.end_node_combo.removeItem(self.end_node_combo.findText(label))

        self.node_input_table.removeRow(row_position)
        print(self.node_lables)
        print(self.graph)

    def calculate_shortest_path(self):
        print(self.graph)
        try:

            self.result_info_display.show()
            self.error_display.hide()
        except Exception as e:
            self.error_display.setText(str(e))
            self.error_display.show()
            self.result_info_display.hide()

class LayoutApp2(QMainWindow):
    def __init__(self):
        super().__init__()
        ui_file_path = os.path.join(os.path.dirname(__file__), 'layout2.ui')
        loadUi(ui_file_path, self)  # Chargez le fichier UI directement

        # Connectez le bouton returnHome à la fonction de redirection avec l'indice 0
        # self.returnHome.clicked.connect(lambda: BaseWindow.redirect_to_layout(self,0))

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
