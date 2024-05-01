import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QPushButton,QVBoxLayout, QLabel, QTableView
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt, QAbstractTableModel
from PyQt5.QtWidgets import QMessageBox
import uuid
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QInputDialog
from problem2 import solve_farming_problem 
import pandas as pd
from PyQt5.QtGui import QFont


class LayoutApp2(QMainWindow):
    def __init__(self,widget):
        super().__init__()
        ui_file_path = os.path.join(os.path.dirname(__file__), 'layout2.ui')
        loadUi(ui_file_path, self)  # Chargez le fichier UI directement

        # set the splitter evenly in two halfs 
        self.splitter.setSizes([350, 650])

        self.returnHome.clicked.connect( lambda: widget.setCurrentIndex(0) )

        self.tableAdultAnimal.setColumnWidth(0, 160)
        self.tableAdultAnimal.setColumnWidth(2, 150)
        self.tableAdultAnimal.setColumnWidth(3, 150)
        self.tableAdultAnimal.setColumnWidth(4, 160)

        
         # Connectez le signal clicked du bouton add_lands_button à la fonction addLandRow
        self.add_lands_button.clicked.connect(self.addLandRow)

        self.farming2 = {
            'animals': {
                'first_production_age': None,
                'last_sell_age': None,
                'min_final_animals': None,
                'max_final_animals': None,
                'animal_yearly_income': None,
                'birthrate': None,
            },
            'animals_needs': {
                'adult': {
                    'land': None,
                    'labor': None,
                    'decay': None,
                    'initial_number': None,
                    'price': None,
                    'cost': None,
                },
                'baby': {
                    'land': None,
                    'labor': None,
                    'decay': None,
                    'initial_number': None,
                    'price': None,
                    'cost': None,
                }
            },
            'capacity': {
                'housing': None,
                'land': None,
                'labor': None,
            },
            'seeds': {
                'seed1': {
                    'intake': None,
                    'labor': None,
                    'price': None,
                    'cost': None,
                    'land_cost': None,
                },
                'seed2': {
                    'yield': 1.15,
                    'intake': None,
                    'labor': None,
                    'price': None,
                    'cost': None,
                    'land_cost': None,
                }
            },
            'lands': {
                'area': {},
                'yield': {},
            },
            'years_number': None,
            'overtime_cost': None,
            'regular_time_cost': None,
            'installment': None,
        }
        
        # Connect signal from button to slot
        self.pushButton_submit.clicked.connect( lambda: self.get_user_input() )

        self.clear_button_4.clicked.connect( lambda: inputs.clear_inputs(self) )

        
    def get_return_home_button(self):
        return self.returnHome

    def addLandRow(self):
        # Récupérez le nombre de lignes actuel dans le tableau
        numRows = self.tableLands.rowCount()

        # Insérez une nouvelle ligne dans le tableau
        self.tableLands.insertRow(numRows)

        # Ajoutez un bouton de suppression dans la nouvelle ligne
        delete_button = QPushButton("Delete")
        delete_button.clicked.connect(lambda _, row=numRows: self.deleteLandRow(row))
        self.tableLands.setCellWidget(numRows, 2, delete_button)

        # Remplissez la nouvelle ligne avec des cellules vides
        self.tableLands.setItem(numRows, 0, QTableWidgetItem("0"))
        self.tableLands.setItem(numRows, 1, QTableWidgetItem("0"))

    def deleteLandRow(self, row):
        self.tableLands.removeRow(row)

    def get_user_input(self):
        inputs.get_user_input(self, self.farming2)

class inputs(QMainWindow):
    def __init__(self):
        super().__init__()

    def clear_inputs(main_window):
        # Clear the tableAdultAnimal
        for i in range(main_window.tableAdultAnimal.columnCount()):
            main_window.tableAdultAnimal.item(0, i).setText(None)

        # Clear the tableAnimalNeeds
        for i in range(main_window.tableAnimalNeeds.rowCount()):
            for j in range(main_window.tableAnimalNeeds.columnCount()):
                main_window.tableAnimalNeeds.item(i, j).setText(None)

        # Clear the tableCapacity
        for i in range(main_window.tableCapacity.rowCount()):
            for j in range(main_window.tableCapacity.columnCount()):
                main_window.tableCapacity.item(i, j).setText(None)

        # Clear the tableSeeds
        for i in range(main_window.tableSeeds.rowCount()):
            for j in range(main_window.tableSeeds.columnCount()):
                main_window.tableSeeds.item(i, j).setText(None)

        # Clear the tableLands
        for i in range(main_window.tableLands.rowCount()):
            for j in range(main_window.tableLands.columnCount()):
                main_window.tableLands.item(i, j).setText(None)

        # Clear the additional inputs
        main_window.number_years.setText(None)
        main_window.additional_payment.setText(None)
        main_window.annual_cost_regular.setText(None)
        main_window.overtime_cost.setText(None)

    @staticmethod
    def test_positive_input(dictionary, test=False, keys=None):
        if keys is None:
            keys = []
        for key, value in dictionary.items():
            if isinstance(value, dict):
                test, keys = inputs.test_positive_input(value, test, keys)
            elif value < 0:
                keys.append(key)
                test = True
        return test, keys

    @staticmethod
    def test_filled_input(dictionary, test=False, keys=None):
        if keys is None:
            keys = []
        for key, value in dictionary.items():
            if isinstance(value, dict):
                test, keys = inputs.test_filled_input(value, test, keys)
            elif value is None:
                keys.append(key)
                test = True
        return test, keys
    
    def get_user_input(main_window, farming2):

        layout = main_window.plan_display
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # Retrieve input from table
        try:
            animal_first_production_age = int(main_window.tableAdultAnimal.item(0, 0).text())
            animal_last_sell_age = int(main_window.tableAdultAnimal.item(0, 1).text())
            min_final_animals = int(main_window.tableAdultAnimal.item(0, 2).text())
            max_final_animals = int(main_window.tableAdultAnimal.item(0, 3).text())
            animal_yearly_income = float(main_window.tableAdultAnimal.item(0, 4).text())
            birthrate = float(main_window.tableAdultAnimal.item(0, 5).text())

            # Cow inputs
            animal_land = float(main_window.tableAnimalNeeds.item(0, 0).text())
            animal_labor = float(main_window.tableAnimalNeeds.item(0, 1).text())
            animal_decay = float(main_window.tableAnimalNeeds.item(0, 2).text())
            initial_animals_number = float(main_window.tableAnimalNeeds.item(0, 3).text())
            animal_price = float(main_window.tableAnimalNeeds.item(0, 4).text())
            animal_cost = float(main_window.tableAnimalNeeds.item(0, 5).text())

            # Heifer inputs
            baby_animal_land = float(main_window.tableAnimalNeeds.item(1, 0).text())
            baby_animal_labor = float(main_window.tableAnimalNeeds.item(1, 1).text())
            baby_animal_decay = float(main_window.tableAnimalNeeds.item(1, 2).text())
            initial_baby_animal_number = float(main_window.tableAnimalNeeds.item(1, 3).text())
            baby_animal_price = float(main_window.tableAnimalNeeds.item(1, 4).text())
            baby_animal_cost = float(main_window.tableAnimalNeeds.item(1, 5).text())

            #capacity
            housing_cap = float(main_window.tableCapacity.item(0, 0).text())
            land_cap = float(main_window.tableCapacity.item(0, 1).text())
            labor_cap = float(main_window.tableCapacity.item(0, 2).text())

            #☺ seed1 inputs
            seed1_intake = float(main_window.tableSeeds.item(0, 1).text())
            seed1_labor = float(main_window.tableSeeds.item(0, 2).text())
            seed1_price = float(main_window.tableSeeds.item(0, 3).text())
            seed1_cost = float(main_window.tableSeeds.item(0, 4).text())
            seed1_land_cost = float(main_window.tableSeeds.item(0, 5).text())

            # seed2 inputs
            seed2_yield = float(main_window.tableSeeds.item(1, 0).text())
            seed2_intake = float(main_window.tableSeeds.item(1, 1).text())
            seed2_labor = float(main_window.tableSeeds.item(1, 2).text())
            seed2_price = float(main_window.tableSeeds.item(1, 3).text())
            seed2_cost = float(main_window.tableSeeds.item(1, 4).text())
            seed2_land_cost = float(main_window.tableSeeds.item(1, 5).text())

            # Lands inputs
            seed1_areas = {}
            seed1_yields = {}
            for i in range(main_window.tableLands.rowCount()):
                seed1_area = float(main_window.tableLands.item(i, 0).text())
                seed1_areas[i + 1] = seed1_area
            for i in range(main_window.tableLands.rowCount()):
                seed1_yield = float(main_window.tableLands.item(i, 1).text())
                seed1_yields[i + 1] = seed1_yield

            # get the additional inputs
            number_of_years = int(main_window.number_years.text())
            additional_payment = float(main_window.additional_payment.text())
            annual_cost_regular = float(main_window.annual_cost_regular.text())
            overtime_cost = float(main_window.overtime_cost.text())

            # Update farming2 dictionary with user input values
            farming2['animals']['first_production_age'] = animal_first_production_age
            farming2['animals']['last_sell_age'] = animal_last_sell_age
            farming2['animals']['min_final_animals'] = min_final_animals
            farming2['animals']['max_final_animals'] = max_final_animals
            farming2['animals']['animal_yearly_income'] = animal_yearly_income
            farming2['animals']['birthrate'] = birthrate

            farming2['animals_needs']['adult']['land'] = animal_land
            farming2['animals_needs']['adult']['labor'] = animal_labor
            farming2['animals_needs']['adult']['decay'] = animal_decay
            farming2['animals_needs']['adult']['initial_number'] = initial_animals_number
            farming2['animals_needs']['adult']['price'] = animal_price
            farming2['animals_needs']['adult']['cost'] = animal_cost

            farming2['animals_needs']['baby']['land'] = baby_animal_land
            farming2['animals_needs']['baby']['labor'] = baby_animal_labor
            farming2['animals_needs']['baby']['decay'] = baby_animal_decay
            farming2['animals_needs']['baby']['initial_number'] = initial_baby_animal_number
            farming2['animals_needs']['baby']['price'] = baby_animal_price
            farming2['animals_needs']['baby']['cost'] = baby_animal_cost

            farming2['capacity']['housing'] = housing_cap
            farming2['capacity']['land'] = land_cap
            farming2['capacity']['labor'] = labor_cap

            farming2['seeds']['seed1']['intake'] = seed1_intake
            farming2['seeds']['seed1']['labor'] = seed1_labor
            farming2['seeds']['seed1']['price'] = seed1_price
            farming2['seeds']['seed1']['cost'] = seed1_cost
            farming2['seeds']['seed1']['land_cost'] = seed1_land_cost

            farming2['seeds']['seed2']['intake'] = seed2_intake
            farming2['seeds']['seed2']['labor'] = seed2_labor
            farming2['seeds']['seed2']['price'] = seed2_price
            farming2['seeds']['seed2']['cost'] = seed2_cost
            farming2['seeds']['seed2']['land_cost'] = seed2_land_cost

            farming2['lands']['area'] = seed1_areas
            farming2['lands']['yield'] = seed1_yields

            farming2['years_number'] = number_of_years
            farming2['overtime_cost'] = overtime_cost
            farming2['regular_time_cost'] = annual_cost_regular
            farming2['installment'] = additional_payment

            # Check if the user input is valid
            [test, keys] = inputs.test_positive_input(farming2)
            if test :
                QMessageBox.warning(main_window, 'Warning', 'The following params must be positive: ' + ', '.join(keys))
            elif min_final_animals > max_final_animals:
                QMessageBox.warning(main_window, 'Warning', 'The minimum number of final animals must be less than the maximum number of final animals')
            elif animal_first_production_age == 0 or animal_last_sell_age == 0 or birthrate == 0 or animal_land ==0 or baby_animal_land ==0 or land_cap ==0 or initial_animals_number ==0 or initial_baby_animal_number ==0 or animal_price ==0 or baby_animal_price ==0 or number_of_years ==0 :
                QMessageBox.warning(main_window, 'Warning', 'Some fields cannot be zero, Read the Input Constraints and check the mentioned fields')
            else :
                [objective, finance_plan, seed1_plan, seed2_plan, livestock_plan] = solve_farming_problem(farming2)
                
                # Update the QVBoxLayout with the results
                
                layout.setAlignment(Qt.AlignTop)

                # Create a QFont object with bold style and fontsize 11
                label_font = QFont()
                label_font.setBold(True)
                label_font.setPointSize(11)

                # Add labels with the specified font properties
                objective_label = QLabel("Objective:")
                objective_label.setFont(label_font)
                layout.addWidget(objective_label)

                # Add the objective text (assuming it's a string)
                objective_text_label = QLabel(str(objective))
                layout.addWidget(objective_text_label)

                # Add other labels in a similar manner
                finance_plan_label = QLabel("Finance Plan:")
                finance_plan_label.setFont(label_font)
                layout.addWidget(finance_plan_label)
                layout.addWidget(QTableView())

                seed1_plan_label = QLabel("Seed1 Plan:")
                seed1_plan_label.setFont(label_font)
                layout.addWidget(seed1_plan_label)
                layout.addWidget(QTableView())

                seed2_plan_label = QLabel("Seed2 Plan:")
                seed2_plan_label.setFont(label_font)
                layout.addWidget(seed2_plan_label)
                layout.addWidget(QTableView())

                livestock_plan_label = QLabel("Livestock Plan:")
                livestock_plan_label.setFont(label_font)
                layout.addWidget(livestock_plan_label)
                layout.addWidget(QTableView())

                # Create PandasModel instances for each DataFrame
                finance_model = PandasModel(finance_plan)
                seed1_model = PandasModel(seed1_plan)
                seed2_model = PandasModel(seed2_plan)
                livestock_model = PandasModel(livestock_plan)

                # Set the models to the corresponding QTableView widgets
                layout.itemAt(3).widget().setModel(finance_model)
                layout.itemAt(5).widget().setModel(seed1_model)
                layout.itemAt(7).widget().setModel(seed2_model)
                layout.itemAt(9).widget().setModel(livestock_model)
        except ValueError:
            QMessageBox.warning(main_window, 'Warning', 'Please enter valid numbers in the input fields')

        

class PandasModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parent=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return str(self._data.columns[section])
        if orientation == Qt.Vertical and role == Qt.DisplayRole:
            return str(self._data.index[section])
        return None
