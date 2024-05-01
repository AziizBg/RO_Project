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
    def __init__(self):
        super().__init__()
        ui_file_path = os.path.join(os.path.dirname(__file__), 'layout2.ui')
        loadUi(ui_file_path, self)  # Chargez le fichier UI directement

        # set the splitter evenly in two halfs 
        self.splitter.setSizes([350, 650])

        self.tableAdultAnimal.setColumnWidth(0, 160)
        self.tableAdultAnimal.setColumnWidth(2, 150)
        self.tableAdultAnimal.setColumnWidth(3, 150)
        self.tableAdultAnimal.setColumnWidth(4, 160)

        inputs.set_table_initial_values(self,self.tableAdultAnimal)
        inputs.set_table_initial_values(self,self.tableAnimalNeeds)
        inputs.set_table_initial_values(self,self.tableCapacity)
        inputs.set_table_initial_values(self,self.tableSeeds)
        self.tableLands.setItem(0, 0, QTableWidgetItem("0"))
        self.tableLands.setItem(0, 1, QTableWidgetItem("0"))
        

        
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

        self.clear_button_4.clicked.connect(lambda: inputs.clear_inputs(self, self))

        
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

    def clear_inputs(self, main_window):
        self.set_table_initial_values(main_window.tableAdultAnimal)
        self.set_table_initial_values(main_window.tableAnimalNeeds)
        self.set_table_initial_values(main_window.tableCapacity)
        self.set_table_initial_values(main_window.tableSeeds)
        self.set_table_initial_values(main_window.tableLands)
        main_window.number_years.setText("0")
        main_window.additional_payment.setText("0")
        main_window.annual_cost_regular.setText("0")
        main_window.overtime_cost.setText("0")


    def set_table_initial_values(self, table):
        for i in range(table.rowCount()):
            for j in range(table.columnCount()):
                table.setItem(i, j, QTableWidgetItem("0"))

    @staticmethod
    def test_positive_input( dictionary):
        keys = []
        test = False
        for key, value in dictionary.items():
            if isinstance(value, dict):
                inputs.test_positive_input(value)
            elif value < 0:
                keys.append(key)
                test = True
        return test, keys
    
    def get_user_input(main_window, farming2):
        # Retrieve input from table
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
        seed1_intake = float(main_window.tableSeeds.item(0, 0).text())
        seed1_labor = float(main_window.tableSeeds.item(0, 1).text())
        seed1_price = float(main_window.tableSeeds.item(0, 2).text())
        seed1_cost = float(main_window.tableSeeds.item(0, 3).text())
        seed1_land_cost = float(main_window.tableSeeds.item(0, 4).text())

        # seed2 inputs
        seed2_intake = float(main_window.tableSeeds.item(1, 0).text())
        seed2_labor = float(main_window.tableSeeds.item(1, 1).text())
        seed2_price = float(main_window.tableSeeds.item(1, 2).text())
        seed2_cost = float(main_window.tableSeeds.item(1, 3).text())
        seed2_land_cost = float(main_window.tableSeeds.item(1, 4).text())

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
    

        # # Update farming2 dictionary with user input values
        # farming2['animals']['first_production_age'] = animal_first_production_age
        # farming2['animals']['last_sell_age'] = animal_last_sell_age
        # farming2['animals']['min_final_animals'] = min_final_animals
        # farming2['animals']['max_final_animals'] = max_final_animals
        # farming2['animals']['animal_yearly_income'] = animal_yearly_income
        # farming2['animals']['birthrate'] = birthrate

        # farming2['animals_needs']['adult']['land'] = animal_land
        # farming2['animals_needs']['adult']['labor'] = animal_labor
        # farming2['animals_needs']['adult']['decay'] = animal_decay
        # farming2['animals_needs']['adult']['initial_number'] = initial_animals_number
        # farming2['animals_needs']['adult']['price'] = animal_price
        # farming2['animals_needs']['adult']['cost'] = animal_cost

        # farming2['animals_needs']['baby']['land'] = baby_animal_land
        # farming2['animals_needs']['baby']['labor'] = baby_animal_labor
        # farming2['animals_needs']['baby']['decay'] = baby_animal_decay
        # farming2['animals_needs']['baby']['initial_number'] = initial_baby_animal_number
        # farming2['animals_needs']['baby']['price'] = baby_animal_price
        # farming2['animals_needs']['baby']['cost'] = baby_animal_cost

        # farming2['capacity']['housing'] = housing_cap
        # farming2['capacity']['land'] = land_cap
        # farming2['capacity']['labor'] = labor_cap

        # farming2['seeds']['seed1']['intake'] = seed1_intake
        # farming2['seeds']['seed1']['labor'] = seed1_labor
        # farming2['seeds']['seed1']['price'] = seed1_price
        # farming2['seeds']['seed1']['cost'] = seed1_cost
        # farming2['seeds']['seed1']['land_cost'] = seed1_land_cost

        # farming2['seeds']['seed2']['intake'] = seed2_intake
        # farming2['seeds']['seed2']['labor'] = seed2_labor
        # farming2['seeds']['seed2']['price'] = seed2_price
        # farming2['seeds']['seed2']['cost'] = seed2_cost
        # farming2['seeds']['seed2']['land_cost'] = seed2_land_cost

        # farming2['lands']['area'] = seed1_areas
        # farming2['lands']['yield'] = seed1_yields

        # farming2['years_number'] = number_of_years
        # farming2['overtime_cost'] = overtime_cost
        # farming2['regular_time_cost'] = annual_cost_regular
        # farming2['installment'] = additional_payment

        farming2 = {
            # Parameters related to animals
            'animals': {
                'first_production_age': 2,  # Age when animals start production # not 0
                'last_sell_age': 10,  # Age when animals are sold # not 0
                'min_final_animals': 0,  # Minimum number of animals at the end of planning
                'max_final_animals': 175,  # Maximum number of animals at the end of planning # not 0
                'animal_yearly_income': 370.0,  # Income from animals per year # not 0
                'birthrate': 0,  # Expected number of births per year
            },
            # Parameters related to animal needs
            'animals_needs': {
                'adult': {
                    'land': 1.0,  # Land required per adult animal
                    'labor': 0.42,  # Labor required per adult animal
                    'decay': 0.02,  # Proportion of adult animals that die per year
                    'initial_number': 9.8,  # Initial number of adult animals
                    'price': 120.0,  # Price for selling an adult animal
                    'cost': 100.0,  # Cost for supporting an adult animal per year
                },
                'baby': {
                    'land': 0.666,  # Land required per baby animal
                    'labor': 0.1,  # Labor required per baby animal
                    'decay': 0.05,  # Proportion of baby animals that die per year
                    'initial_number': 9.5,  # Initial number of baby animals
                    'price': 40.0,  # Price for selling a baby animal
                    'cost': 50.0,  # Cost for supporting a baby animal per year
                }
            },
            # Parameters related to capacity
            'capacity': {
                'housing': 0,  # Capacity for housing animals
                'land': 200,  # Available land capacity # not 0
                'labor': 0,  # Available labor capacity
            },
            # Parameters related to seeds
            'seeds':{
                'seed1': {
                    'intake': 0,  # Grain intake per animal
                    'labor': 0,  # Labor required per ton of grain
                    'price': 0,  # Price for buying a ton of grain
                    'cost': 0,  # Cost for supporting a ton of grain per year
                    'land_cost': 0,  # Cost for supporting an acre of land for grain per year
                },
                'seed2': {
                    'yield': 1.5,  # Yield of sugar beet per acre #not 0 (divisor)
                    'intake': 0,  # Sugar beet intake per animal
                    'labor': 0,  # Labor required per ton of sugar beet
                    'price': 58.0,  # Price for buying a ton of sugar beet #not 0
                    'cost': 70.0,  # Cost for supporting a ton of sugar beet per year #not 0
                    'land_cost': 0,  # Cost for supporting an acre of land for sugar beet per year
                }
            },
            # Parameters related to land
            'lands':{
                'area': {1: 0},  # Area of land in different groups
                'yield': {1: 8},  # Yield of grain per acre in different groups #not 0
            },
            'years_number': 8,  # Number of years for planning # not 0
            'overtime_cost': 5,  # Cost for overtime labor
            'regular_time_cost': 5,  # Cost for regular labor
            'installment': 0,  # Annual payment for each loan
        }

        # Check if the user input is valid
        [test, keys] = inputs.test_positive_input(farming2)
        if test :
            QMessageBox.warning(main_window, 'Warning', 'The following params must be positive: ' + ', '.join(keys))
        else :
            [objective, finance_plan, seed1_plan, seed2_plan, livestock_plan] = solve_farming_problem(farming2)
            
            

            # Update the QVBoxLayout with the results
            layout = main_window.plan_display
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
