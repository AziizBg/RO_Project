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
from PyQt5.QtWidgets import QPushButton


class LayoutApp2(QMainWindow):
    def __init__(self):
        super().__init__()
        ui_file_path = os.path.join(os.path.dirname(__file__), 'layout2.ui')
        loadUi(ui_file_path, self)  # Chargez le fichier UI directement


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

        # Connect signal from button to slot
        self.pushButton_submit.clicked.connect( lambda: inputs.get_user_input(self) )
         # Connectez le signal clicked du bouton add_lands_button à la fonction addLandRow
        self.add_lands_button.clicked.connect(self.addLandRow)
        
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


class inputs(QMainWindow):
    def __init__(self):
        super().__init__()

    def set_table_initial_values(self, table):
        for i in range(table.rowCount()):
            for j in range(table.columnCount()):
                table.setItem(i, j, QTableWidgetItem("0"))
        

    def get_user_input(self):
        # Retrieve input from table
        animal_first_production_age = int(self.tableAdultAnimal.item(0, 0).text())
        animal_last_sell_age = int(self.tableAdultAnimal.item(0, 1).text())
        min_final_animals = int(self.tableAdultAnimal.item(0, 2).text())
        max_final_animals = int(self.tableAdultAnimal.item(0, 3).text())
        animal_yearly_income = float(self.tableAdultAnimal.item(0, 4).text())
        birthrate = float(self.tableAdultAnimal.item(0, 5).text())

        # Do something with the input
        print("First Production Age:", animal_first_production_age)
        print("Last Sell Age:", animal_last_sell_age)
        print("Min Final Animals:", min_final_animals)
        print("Max Final Animals:", max_final_animals)
        print("Animal Yearly Income:", animal_yearly_income)
        print("Birthrate:", birthrate)

        # Cow inputs
        animal_land = float(self.tableAnimalNeeds.item(0, 0).text())
        animal_labor = float(self.tableAnimalNeeds.item(0, 1).text())
        animal_decay = float(self.tableAnimalNeeds.item(0, 2).text())
        initial_animals_number = float(self.tableAnimalNeeds.item(0, 3).text())
        animal_price = float(self.tableAnimalNeeds.item(0, 4).text())
        animal_cost = float(self.tableAnimalNeeds.item(0, 5).text())
        
        # Heifer inputs
        baby_animal_land = float(self.tableAnimalNeeds.item(1, 0).text())
        baby_animal_labor = float(self.tableAnimalNeeds.item(1, 1).text())
        baby_animal_decay = float(self.tableAnimalNeeds.item(1, 2).text())
        initial_baby_animal_number = float(self.tableAnimalNeeds.item(1, 3).text())
        baby_animal_price = float(self.tableAnimalNeeds.item(1, 4).text())
        baby_animal_cost = float(self.tableAnimalNeeds.item(1, 5).text())
        
        # Do something with the input
        print("Animal Land:", animal_land)
        print("Animal Labor:", animal_labor)
        print("Animal Decay:", animal_decay)
        print("Initial Number of Animals:", initial_animals_number)
        print("Animal Price:", animal_price)
        print("Animal Cost:", animal_cost)
        
        print("Baby Animal Land:", baby_animal_land)
        print("Baby Animal Labor:", baby_animal_labor)
        print("Baby Animal Decay:", baby_animal_decay)
        print("Initial Number of Baby Animals:", initial_baby_animal_number)
        print("Baby Animal Price:", baby_animal_price)
        print("Baby Animal Cost:", baby_animal_cost)

        #capacity
        housing_cap = float(self.tableCapacity.item(0, 0).text())
        land_cap = float(self.tableCapacity.item(0, 1).text())
        labor_cap = float(self.tableCapacity.item(0, 2).text())

        print("Housing Capacity:", housing_cap)
        print("Labor Capacity:", labor_cap)
        print("Land Capacity:", land_cap)

        #☺ seed1 inputs
        seed1_intake = float(self.tableSeeds.item(0, 0).text())
        seed1_labor = float(self.tableSeeds.item(0, 1).text())
        seed1_price = float(self.tableSeeds.item(0, 2).text())
        seed1_cost = float(self.tableSeeds.item(0, 3).text())
        seed1_land_cost = float(self.tableSeeds.item(0, 4).text())

        # seed2 inputs
        seed2_intake = float(self.tableSeeds.item(1, 0).text())
        seed2_labor = float(self.tableSeeds.item(1, 1).text())
        seed2_price = float(self.tableSeeds.item(1, 2).text())
        seed2_cost = float(self.tableSeeds.item(1, 3).text())
        seed2_land_cost = float(self.tableSeeds.item(1, 4).text())

        # Do something with the input
        print("Seed1 Intake:", seed1_intake)
        print("Seed1 Labor:", seed1_labor)
        print("Seed1 Price:", seed1_price)
        print("Seed1 Cost:", seed1_cost)
        print("Seed1 Land Cost:", seed1_land_cost)

        print("Seed2 Intake:", seed2_intake)
        print("Seed2 Labor:", seed2_labor)
        print("Seed2 Price:", seed2_price)
        print("Seed2 Cost:", seed2_cost)
        print("Seed2 Land Cost:", seed2_land_cost)

        # Lands inputs
        for i in range(self.tableLands.rowCount()):
            seed1_area = self.tableLands.item(i, 0).text()
            print("Seed1 Area:", seed1_area)
        for i in range(self.tableLands.rowCount()):
            seed2_area = self.tableLands.item(i, 1).text()
            print("Seed2 Area:", seed2_area)