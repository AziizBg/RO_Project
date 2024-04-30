import sys
import uuid
import os
from plne import validate_graph, solve_shortest_path

from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QGraphicsEllipseItem, QGraphicsLineItem, QGraphicsScene, QInputDialog, QTableWidgetItem, QMessageBox, QApplication, QMainWindow, QGraphicsTextItem, QAction, QFileDialog
from PyQt5.QtGui import QPen, QColor, QFont
from PyQt5.QtCore import QPointF, QLineF
from PyQt5.QtWidgets import QPushButton

import json
import csv
import math
import random


class LayoutApp(QMainWindow):
    def __init__(self):
        super().__init__()
        ui_file_path = os.path.join(os.path.dirname(__file__), 'layout.ui')
        loadUi(ui_file_path, self)  # Load the UI file directly
        self.setWindowTitle("My PyQt Application")  # Set window title
        self.setup_menu()
        

        self.graph = {
            'nodes': {},
            'edges': {},
        }
        self.node_labels = {}

        # total_size = self.splitter.width()
        # self.splitter.setSizes([int(total_size / 2), int(total_size / 2)])

        self.splitter.setSizes([400, 100])

        self.add_node_button.clicked.connect(self.add_node)
        self.add_edge_button.clicked.connect(self.add_edge)
        self.calculate_button.clicked.connect(self.calculate_shortest_path)
        self.clear_button.clicked.connect(self.clear)

        self.result_info_display.hide()
        self.error_display.hide()

        self.node_input_table.setHorizontalHeaderLabels(
            ["Node ID", "Label", "Entry", "Exit", ""])
        self.edge_input_table.setHorizontalHeaderLabels(
            ["Edge ID", "Start", "End", "Weight", "Duration", ""])

        self.add_node_button.setFixedWidth(
            self.add_node_button.sizeHint().width()+30)
        self.add_edge_button.setFixedWidth(
            self.add_edge_button.sizeHint().width()+30)

        self.result_info_display.setFixedHeight(
            self.result_info_display.sizeHint().height()+10)
        self.error_display.setFixedHeight(
            self.error_display.sizeHint().height()+10)
        # self.calculate_button.setFixedHeight(
        #     self.calculate_button.sizeHint().height()+10)

        # self.clear_button.setFixedHeight(
        #     self.clear_button.sizeHint().height()+10)

    def get_return_home_button(self):
        return self.returnHome
        
    def add_node(self):

        while True:
            label, ok = QInputDialog.getText(
                self, "Input", "Enter node label:")
            if not ok:
                return

            if label in self.node_labels.values():
                QMessageBox.warning(
                    self, "Error", "This label already exists.")
                continue

            break

        x, ok = QInputDialog.getDouble(
            self, "Input", "Enter entry constraint:")
        if not ok:
            return

        y, ok = QInputDialog.getDouble(self, "Input", "Enter exit constraint:")
        if not ok:
            return

        node_id = str(uuid.uuid4())

        self.graph['nodes'][node_id] = (x, y)
        self.node_labels[node_id] = label

        self.start_node_combo.addItem(label)
        self.end_node_combo.addItem(label)

        row_position = self.node_input_table.rowCount()
        self.node_input_table.insertRow(row_position)

        # Set the values for the new row
        self.node_input_table.setItem(
            row_position, 0, QTableWidgetItem(node_id))
        self.node_input_table.item(
            row_position, 0).setTextAlignment(QtCore.Qt.AlignCenter)
        self.node_input_table.setItem(
            row_position, 1, QTableWidgetItem(label))
        self.node_input_table.item(
            row_position, 1).setTextAlignment(QtCore.Qt.AlignCenter)
        self.node_input_table.setItem(
            row_position, 2, QTableWidgetItem(str(x)))
        self.node_input_table.item(
            row_position, 2).setTextAlignment(QtCore.Qt.AlignCenter)
        self.node_input_table.setItem(
            row_position, 3, QTableWidgetItem(str(y)))
        self.node_input_table.item(
            row_position, 3).setTextAlignment(QtCore.Qt.AlignCenter)

        remove_node_button = QtWidgets.QPushButton("Remove Node")
        remove_node_button.clicked.connect(
            lambda: self.remove_node(row_position))

        self.node_input_table.setCellWidget(
            row_position, 4, remove_node_button)
        # print(self.graph)
        # print(self.node_labels)

    def add_edge(self):

        if len(self.graph['nodes']) < 2:
            QMessageBox.warning(
                self, "Error", "You need to add at least two nodes before adding edges.")
            return

        nodes = list(self.node_labels.values())

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

                # Map labels back to IDs
                start_node_id = [
                    id for id, label in self.node_labels.items() if label == start_node][0]
                end_node_id = [
                    id for id, label in self.node_labels.items() if label == end_node][0]

                # Check if the edge already exists in the graph
                if (start_node_id, end_node_id) in self.graph['edges']:
                    QMessageBox.warning(
                        self, "Error", "This edge already exists.")
                    break

                # If the edge doesn't exist, exit the loop
                break

            # If the edge exists, start over from the beginning
            if (start_node_id, end_node_id) in self.graph['edges']:
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
        self.graph['edges'][(start_node_id, end_node_id)] = {
            'weight': weight, 'duration': duration}

        if (end_node_id, start_node_id) not in self.graph['edges']:
            self.graph['edges'][(end_node_id, start_node_id)] = {
                'weight': weight, 'duration': duration}

        row_position = self.edge_input_table.rowCount()
        self.edge_input_table.insertRow(row_position)

        # Set the values for the new row
        self.edge_input_table.setItem(
            row_position, 0, QTableWidgetItem(edge_id))
        self.edge_input_table.item(
            row_position, 0).setTextAlignment(QtCore.Qt.AlignCenter)
        self.edge_input_table.setItem(
            row_position, 1, QTableWidgetItem(start_node))
        self.edge_input_table.item(
            row_position, 1).setTextAlignment(QtCore.Qt.AlignCenter)
        self.edge_input_table.setItem(
            row_position, 2, QTableWidgetItem(end_node))
        self.edge_input_table.item(
            row_position, 2).setTextAlignment(QtCore.Qt.AlignCenter)
        self.edge_input_table.setItem(
            row_position, 3, QTableWidgetItem(str(weight)))
        self.edge_input_table.item(
            row_position, 3).setTextAlignment(QtCore.Qt.AlignCenter)
        self.edge_input_table.setItem(
            row_position, 4, QTableWidgetItem(str(duration)))
        self.edge_input_table.item(
            row_position, 4).setTextAlignment(QtCore.Qt.AlignCenter)

        remove_edge_button = QtWidgets.QPushButton("Remove Edge")
        remove_edge_button.clicked.connect(
            lambda: self.remove_edge(row_position))

        self.edge_input_table.setCellWidget(
            row_position, 5, remove_edge_button)
        # print(self.graph)

    def remove_node(self, row_position):
        node_id = self.node_input_table.item(row_position, 0).text()
        label = self.node_input_table.item(row_position, 1).text()


        # Collect edges to remove
        edges_to_remove = [
            edge for edge in self.graph['edges'] if node_id in edge]

        # Remove edges
        for edge in edges_to_remove:
            # Find the row position of the edge in the edge_input_table
            for row_position in range(self.edge_input_table.rowCount()):
                start_node = self.edge_input_table.item(row_position, 1).text()
                end_node = self.edge_input_table.item(row_position, 2).text()
                start_node_id = [
                    id for id, label in self.node_labels.items() if label == start_node][0]
                end_node_id = [
                    id for id, label in self.node_labels.items() if label == end_node][0]

                if edge == (start_node_id, end_node_id) or edge == (end_node_id, start_node_id):
                    self.remove_edge(row_position)
                    break

        del self.graph['nodes'][node_id]
        del self.node_labels[node_id]

        self.start_node_combo.removeItem(self.start_node_combo.findText(label))
        self.end_node_combo.removeItem(self.end_node_combo.findText(label))

        self.node_input_table.removeRow(row_position)
        # print(self.node_labels)
        # print(self.graph)

    def remove_edge(self, row_position):
        # Get the start and end nodes of the edge from the table
        start_node = self.edge_input_table.item(row_position, 1).text()
        end_node = self.edge_input_table.item(row_position, 2).text()

        # Map labels back to IDs
        start_node_id = [
            id for id, label in self.node_labels.items() if label == start_node][0]
        end_node_id = [
            id for id, label in self.node_labels.items() if label == end_node][0]

        # Remove the edge from the graph
        del self.graph['edges'][(start_node_id, end_node_id)]
        del self.graph['edges'][(end_node_id, start_node_id)]

        # Remove the row from the table
        self.edge_input_table.removeRow(row_position)

        # print(self.graph)

    def clear(self):
        self.error_label.setStyleSheet("color: #262626;")
        self.result_info_label.setStyleSheet("color: #262626;")
        self.graph = {
            'nodes': {},
            'edges': {},
        }
        self.node_labels = {}

        self.node_input_table.setRowCount(0)
        self.edge_input_table.setRowCount(0)

        self.start_node_combo.clear()
        self.end_node_combo.clear()

        self.graphicsView.setScene(None)

        self.result_info_display.hide()
        self.error_display.hide()

        # print(self.graph)
        # print(self.node_labels)

    def calculate_shortest_path(self):
        self.error_label.setStyleSheet("color: #262626;")
        self.result_info_label.setStyleSheet("color: #262626;")
        self.graphicsView.setScene(None)
        # Check if the tables are empty
        if self.node_input_table.rowCount() == 0 or self.edge_input_table.rowCount() == 0:
            QMessageBox.warning(
                self, "Error", "Please ensure all tables are filled.")
            return

        start_node_label = self.start_node_combo.currentText()
        end_node_label = self.end_node_combo.currentText()

        # id of the start and end nodes
        start_node = [
            id for id, label in self.node_labels.items() if label == start_node_label][0]
        end_node = [
            id for id, label in self.node_labels.items() if label == end_node_label][0]

        # Check if the node selection is empty or invalid
        if not start_node_label or not end_node_label or start_node_label not in self.node_labels.values() or end_node_label not in self.node_labels.values():
            QMessageBox.warning(
                self, "Error", "Please select valid start and end nodes.")
            return

        if start_node_label == end_node_label:
            QMessageBox.warning(
                self, "Error", "The start node and end node cannot be the same.")
            return

        print(self.graph)
        try:
            is_valid, error_message = validate_graph(
                self.graph, self.node_labels)
            if not is_valid:
                error_message = "Le graphe n'est pas valide. Veuillez corriger les erreurs de saisie. \n" + error_message
                self.error_label.setStyleSheet("color: #77a2ba;")
                self.error_display.setText(error_message)
                self.error_display.show()
                self.result_info_display.hide()
            else:
                # Create a new scene
                scene = QGraphicsScene()

                # Add nodes to the scene
                node_positions = {}
                node_items = []
                radius = 15  # Radius of the circles
                for node_id, node_data in self.graph['nodes'].items():
                    while True:
                        # Generate random coordinates
                        x, y = random.randint(
                            radius, 400 - radius), random.randint(radius, 400 - radius)
                        # Adjust the position based on the radius
                        item = QGraphicsEllipseItem(
                            x - radius, y - radius, 2 * radius, 2 * radius)
                        # Check if the item collides with any existing items and if the distance to all existing nodes is above a minimum
                        if not any(item.collidesWithItem(existing_item) for existing_item in node_items) and all(math.sqrt((x - ex)**2 + (y - ey)**2) > 100 for ex, ey in node_positions.values()):
                            break
                    node_positions[node_id] = (x, y)
                    node_items.append(item)
                    scene.addItem(item)

                    # Add label
                    label = QGraphicsTextItem(self.node_labels[node_id])
                    label.setFont(QFont("Arial", 7))  # Set font size
                    label.setPos(x - label.boundingRect().width() / 2, y -
                                 label.boundingRect().height() / 2)  # Center the label
                    scene.addItem(label)

                # Add edges to the scene
                for (start_node_id, end_node_id), edge_data in self.graph['edges'].items():
                    start_x, start_y = node_positions[start_node_id]
                    end_x, end_y = node_positions[end_node_id]
                    # Calculate the direction of the edge
                    direction = math.atan2(
                        end_y - start_y, end_x - start_x)
                    # Move the start and end points along the direction by the radius of the circle
                    start_x += radius * math.cos(direction)
                    start_y += radius * math.sin(direction)
                    end_x -= radius * math.cos(direction)
                    end_y -= radius * math.sin(direction)
                    item = QGraphicsLineItem(
                        QLineF(QPointF(start_x, start_y), QPointF(end_x, end_y)))
                    scene.addItem(item)

                    # Add weight and duration
                    weight = edge_data['weight']
                    duration = edge_data['duration']
                    label = QGraphicsTextItem(
                        f"(W: {weight}, D: {duration})")
                    label.setFont(QFont("Arial", 7))  # Increase font size
                    # Set position at the middle of the edge
                    mid_x = (start_x + end_x) / 2
                    mid_y = (start_y + end_y) / 2
                    label.setPos(mid_x - label.boundingRect().width() / 2, mid_y -
                                 label.boundingRect().height() / 2)  # Center the label

                    scene.addItem(label)

                self.graphicsView.setScene(scene)

                result = solve_shortest_path(
                    self.graph, start_node, end_node)

                if result:
                    shortest_path, total_cost = result
                    # Assuming you have a dictionary node_labels that maps IDs to labels
                    shortest_path_labels = [(self.node_labels[start], self.node_labels[end])
                                            for start, end in shortest_path]
                    result_text = f"Chemin le plus court: {shortest_path_labels}\nCoût total: {total_cost}"

                    # Highlight the shortest path
                    for start_node_id, end_node_id in shortest_path:
                        start_x, start_y = node_positions[start_node_id]
                        end_x, end_y = node_positions[end_node_id]
                        # Calculate the direction of the edge
                        direction = math.atan2(
                            end_y - start_y, end_x - start_x)
                        # Move the start and end points along the direction by the radius of the circle
                        start_x += radius * math.cos(direction)
                        start_y += radius * math.sin(direction)
                        end_x -= radius * math.cos(direction)
                        end_y -= radius * math.sin(direction)
                        item = QGraphicsLineItem(
                            QLineF(QPointF(start_x, start_y), QPointF(end_x, end_y)))
                        # Increase the width of the edges
                        item.setPen(QPen(QColor('light blue'), 4))
                        scene.addItem(item)

                        # Add weight and duration
                        edge_data = self.graph['edges'][(
                            start_node_id, end_node_id)]
                        weight = edge_data['weight']
                        duration = edge_data['duration']
                        label = QGraphicsTextItem(
                            f"(W: {weight}, D: {duration})")
                        label.setFont(QFont("Arial", 7))  # Increase font size
                        # Set position at the middle of the edge
                        mid_x = (start_x + end_x) / 2
                        mid_y = (start_y + end_y) / 2
                        label.setPos(mid_x - label.boundingRect().width() / 2, mid_y -
                                     label.boundingRect().height() / 2)  # Center the label
                        # Set the color of the label
                        label.setDefaultTextColor(QColor('light blue'))
                        scene.addItem(label)

                    # Set the scene on the QGraphicsView
                    self.graphicsView.setScene(scene)

                else:
                    result_text = "Pas de solution optimale trouvée."
                self.result_info_label.setStyleSheet("color: #77a2ba;")
                self.result_info_display.setText(result_text)
                self.result_info_display.show()
                
                self.error_display.hide()

        except Exception as e:
            self.error_label.setStyleSheet("color: #77a2ba;")
            self.error_display.setText(str(e))
            self.error_display.show()
            self.result_info_display.hide()

    def export_graph(self, file_path):
        try:
            with open(file_path, 'w') as file:
                # Write nodes to the file
                nodes_data = [{'id': node_id, 'label': label, 'entry': entry, 'exit': exit}
                              for node_id, (entry, exit) in self.graph['nodes'].items() for label in self.node_labels.values()]
                json.dump(nodes_data, file, indent=4)

                # Write edges to the file
                edges_data = [{'start': start_node, 'end': end_node, 'weight': edge_data['weight'], 'duration': edge_data['duration']}
                              for (start_node, end_node), edge_data in self.graph['edges'].items()]
                file.write('\n')
                json.dump(edges_data, file, indent=4)

            QMessageBox.information(
                self, "Export Successful", "Graph data exported successfully.")
        except Exception as e:
            QMessageBox.warning(
                self, "Export Error", f"An error occurred while exporting the graph data: {str(e)}")

    def export_graph_to_json(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Export Graph Data", "", "JSON Files (.json);;All Files ()")
        if file_path:
            self.export_graph(file_path)

    def export_graph_to_csv(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Export Graph Data", "", "CSV Files (.csv);;All Files ()")
        if file_path:
            try:
                with open(file_path, 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(['Node ID', 'Label', 'Entry', 'Exit'])
                    for node_id, (entry, exit) in self.graph['nodes'].items():
                        writer.writerow(
                            [node_id, self.node_labels[node_id], entry, exit])
                    writer.writerow([])  # Add an empty row
                    writer.writerow(['Start', 'End', 'Weight', 'Duration'])
                    for (start_node, end_node), edge_data in self.graph['edges'].items():
                        writer.writerow(
                            [self.node_labels[start_node], self.node_labels[end_node], edge_data['weight'], edge_data['duration']])
                QMessageBox.information(
                    self, "Export Successful", "Graph data exported successfully.")
            except Exception as e:
                QMessageBox.warning(
                    self, "Export Error", f"An error occurred while exporting the graph data: {str(e)}")

    def setup_menu(self):
        export_menu = self.menuBar().addMenu("&Export")
        export_json_action = QAction("&Export to JSON", self)
        export_json_action.triggered.connect(self.export_graph_to_json)
        export_menu.addAction(export_json_action)

        export_csv_action = QAction("&Export to CSV", self)
        export_csv_action.triggered.connect(self.export_graph_to_csv)
        export_menu.addAction(export_csv_action)