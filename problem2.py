import numpy as np
import pandas as pd

import gurobipy as gp
from gurobipy import GRB

# Parameters

#1. years = [1,2,3,4,5, 6, 7, 8]
years_number = int(input("Enter the number of years: ")) # number of years given by the user
years = [i for i in range(1, years_number+1)] # plan years given by the user
print("years: ", years)

#2. lands = [1,2,3,4] 
lands_number = int(input("Enter the number of land types: ")) # number of land types given by the user
lands = [i for i in range(1, lands_number+1)] # land types given by the user
print("lands: ", lands)

#3. animals 
#animal_ages = [2,3,4,5,6,7,8,9,10,11] # animal ages (before having to sell them) given by the user: from ... to ...
#3.1 animals
#tableau1 : {
#              first_production_age    last_sell_age       min_final_animals       max_final_animals      animal_yearly_income       birthrate
#animal
animal_first_production_age = int(input("Enter the first production age of the animal: ")) # 
animal_last_sell_age = int(input("Enter the last sell age of the animal: ")) #
animal_ages = [i for i in range(animal_first_production_age, animal_last_sell_age+1)] # animal ages (before having to sell them) given by the user: from ... to ...
# ages = [1,2,3,4,5,6,7,8,9,10,11,12] # ages = animal_ages + [1] + ... + [min(animal_ages)-1] + [max(animal_ages)+1] 
ages = [i for i in range(1, max(animal_ages)+1)] 
# min_final_animals = 50
# max_final_animals = 175
min_final_animals = int(input("Enter the minimum number of final animals: ")) # minimum number of final animals
max_final_animals = int(input("Enter the maximum number of final animals: ")) # maximum number of final animals
#animal_yearly_income = 370 #milk, eggs, etc.
animal_yearly_income = float(input("Enter the yearly income: ")) # yearly income
# birthrate = 1.1
birthrate = float(input("Enter the birthrate: ")) # birthrate
#} fin de tableau 1



#tableau2 : {
#             land      labor    decay    initial_number     price    cost   
#animal    
#heifer

#animal land = 1
animal_land = float(input("Enter the land needed for an animal: ")) # land needed for an animal
# animal_labor = 42/100.0 # labor needed for an animal
animal_labor = float(input("Enter the labor needed for an animal: ") ) # labor needed for an animal
#animal_decay = 0.02
animal_decay = float(input("Enter the animal decay: ")) # animal decay
# initial_animals_number = 9.8
initial_animals_number = float(input("Enter the initial number of animals: ")) # initial number of animals
#animal_price = 120
animal_price = float(input("Enter the animals price: ")) # animals price
#animal_cost = 100 #Yearly cost for supporting an animal.
animal_cost = float(input("Enter the yearly cost for supporting an animal: ")) #Yearly cost for supporting an animal.
print("animal_ages: ", animal_ages)
print("possible ages: ", ages)
print("animal_labor: ", animal_labor)
print("animal_decay: ", animal_decay)
print("initial_animals_number: ", initial_animals_number)
print("min_final_animals: ", min_final_animals)
print("max_final_animals: ", max_final_animals)
print("animal_price: ", animal_price)
print("animal_yearly_income: ", animal_yearly_income)
print("birthrate: ", birthrate)
print("animal_cost: ", animal_cost)



#3.2 baby_animals
# baby_animal_land = 2/3.0 # land needed for a baby_animal
baby_animal_land = float(input("Enter the land needed for a baby_animal: ")) 
# baby_animal_labor = 10/100.0 # labor needed for a baby_animal
baby_animal_labor = float(input("Enter the labor needed for a baby_animal: ")) 
#baby_animal_decay = 0.05
baby_animal_decay = float(input("Enter the baby_animal decay: ")) 
# initial_baby_animal_number = 9.5
initial_baby_animal_number = float(input("Enter the initial number of baby_animals: "))
#baby_animal_price = 40 
baby_animal_price = float(input("Enter the baby_animals price: ")) 
#baby_animal_cost = 50 #Yearly cost for supporting a baby_animal
baby_animal_cost = float(input("Enter the yearly cost for supporting a heifer: ")) #Yearly cost for supporting a heifer.
print("baby_animal_land:", baby_animal_land)
print("baby_animal_labor:", baby_animal_labor)
print("baby_animal_decay:", baby_animal_decay)
print("initial_baby_animal_number:", initial_baby_animal_number)
print("baby_animal_price:", baby_animal_price)
print("baby_animal_cost:", baby_animal_cost) 
#} fin de tableau 2


#4. housing_cap && land_cap && labor_cap
# tableau 3: capacity
#              housing         land            labor
#capacity
#housing_cap = 130
housing_cap = int(input("Enter the housing capacity: ")) # housing capacity given by the user
# land_cap = 200 # land capacity which is the maximum land that can be used for farming (in acres)
land_cap = int(input("Enter the land capacity: ")) # land capacity which is the maximum land that can be used for farming (in acres)
# labor_cap = 5500/100.0
labor_cap = int(input("Enter the labor capacity: ")) # labor capacity which is the maximum labor that can be used for farming (in hours)
print("housing_cap: ", housing_cap)
print("land_cap: ", land_cap)
print("labor_cap: ", labor_cap)
#} fin de tableau 3


#5. seeds
#tableau4: {
#              seed1_area             seed1_yield
#land1
#...
#landn

#5.1. seed1 : seed1
# lands_area = {1: 20.0, 2: 30.0, 3: 20.0, 4: 10.0} # area of land type i (in acres) given by the user
seed1_area = {} # area of land type i (in acres) given by the user
for i in range(1, lands_number+1):
    seed1_area[i] = float(input("Enter the area of land type " + str(i) + ": ")) 

# seed1_yield_lands = {1:1.1, 2:0.9, 3:0.8, 4:0.65} 
seed1_yield = {}
for i in range(1, lands_number+1):
    seed1_yield[i] = float(input("Enter the yield of seed1ain in land type " + str(i) + ": "))
#} fin de tableau 4

#tableau 5:{
#             intake     labor    price    cost    land_cost
#seed1
#seed2

# seed1_intake = 0.6 # seed1 intake (intake means the amount of food that the animal eats)
seed1_intake = float(input("Enter the seed1 intake: ")) # seed1 intake (intake means the amount of food that the animal eats)
# seed1_labor = 4/100.0
seed1_labor = float(input("Enter the labor needed for a seed1ain: ")) # labor needed for a seed1ain
#seed1_price = 75 # Price for selling a ton of seed1ain
seed1_price = float(input("Enter the price for selling a ton of seed1ain: ")) # Price for selling a ton of seed1ain
# seed1_cost = 90 # Cost for buying a ton of seed1ain
seed1_cost = float(input("Enter the cost for buying a ton of seed1ain: ")) # Cost for buying a ton of seed1ain
# seed1_land_cost = 15 #Yearly cost for supporting an acre of land devoted to seed1ain.
seed1_land_cost = float(input("Enter the yearly cost for supporting an acre of land devoted to seed1ain: ")) #Yearly cost for supporting an acre of land devoted to seed1ain.
print("seed1_area: ", seed1_area)
print("seed1_yield: ", seed1_yield)
print("seed1_intake: ", seed1_intake)
print("seed1_labor: ", seed1_labor)
print("seed1_price: ", seed1_price)
print("seed1_cost: ", seed1_cost)
print("seed1_land_cost: ", seed1_land_cost)


#5.2. seed2 : 
# seed2_yield = 1.5 
seed2_yield = float(input("Enter the yield of seed2: ")) 
# seed2_intake = 0.7
seed2_intake = float(input("Enter the seed2 intake: ")) #intake (intake means the amount of food that the animal eats)
# seed2_labor = 14/100.0
seed2_labor = float(input("Enter the labor needed for a seed2: ")) # labor needed
# seed2_price = 58 # Price for selling a ton of seed2
seed2_price = float(input("Enter the price for selling a ton of seed2: ")) # Price for selling a ton
# seed2_cost = 70 # Cost for buying a ton of seed2
seed2_cost = float(input("Enter the cost for buying a ton of seed2: ")) # Cost for buying a ton
# seed2_land_cost = 10 #Yearly cost for supporting an acre of land devoted 
seed2_land_cost = float(input("Enter the yearly cost for supporting an acre of land devoted to seed2: ")) #Yearly cost for supporting an acre of land devoted
print("seed2_yield: ", seed2_yield)
print("seed2_intake: ", seed2_intake)
print("seed2_labor: ", seed2_labor)
print("seed2_price: ", seed2_price)
print("seed2_cost: ", seed2_cost)
print("seed2_land_cost: ", seed2_land_cost)
#} fin de tableau 5


#6. labor cost
#6.1. overtime_cost = 1,20 # Cost for getting an hour of overtime.
overtime_cost = float(input("Enter the cost for getting an hour of overtime: ")) # Cost for getting an hour of overtime.

#6.2. regular_time_cost = 4000 #Cost for having 5,500 hours of labor in regular time.
regular_time_cost = float(input("Enter the cost for having"  + "hours of labor in regular time: ")) #Cost for having labor_cap hours of labor in regular time.

#installment = 39.71 #Annual payment for each  $200  loan
installment = float(input("Enter the annual payment for each $200 loan: ")) #Annual payment for each  $200  loan


model = gp.Model('Farming')
seed2 = model.addVars(years, vtype=GRB.CONTINUOUS, name="seed2")
seed1_buy = model.addVars(years, vtype=GRB.CONTINUOUS, name="seed1_buy")
seed1_sell = model.addVars(years, vtype=GRB.CONTINUOUS, name="seed1_sell")
seed2_buy = model.addVars(years, vtype=GRB.CONTINUOUS, name="seed2_buy")
seed2_sell = model.addVars(years, vtype=GRB.CONTINUOUS, name="seed2_sell")
overtime = model.addVars(years, vtype=GRB.CONTINUOUS, name="Overtime")
outlay = model.addVars(years, vtype=GRB.CONTINUOUS, name="Outlay")
baby_animals_sell = model.addVars(years, vtype=GRB.CONTINUOUS, name="baby_animals_sell")
newborn = model.addVars(years, vtype=GRB.CONTINUOUS, name="Newborn")
profit = model.addVars(years, vtype=GRB.CONTINUOUS, name="Profit")
seed1 = model.addVars(years, lands, vtype=GRB.CONTINUOUS, name="seed1")
animals = model.addVars(years, ages, vtype=GRB.CONTINUOUS, name="animals")


# 1. Housing capacity

HousingCap = model.addConstrs((newborn[year] +
                    animals[year,1] +
                    gp.quicksum(animals[year,age] for age in animal_ages) -
                    gp.quicksum(outlay[d] for d in years if d <= year)
                    <= housing_cap for year in years), name="Housing_cap")

# 2.1 Food consumption (seed1ain)

seed1ainConsumption = model.addConstrs((gp.quicksum(seed1_intake*animals[year, age] for age in animal_ages)
                  <= seed1_buy[year] - seed1_sell[year] + seed1.sum(year, '*')
                  for year in years), name="Seed1_consumption")

# 2.1 Food consumption (Sugar beet)
SugarbeetConsumption = model.addConstrs((gp.quicksum(seed2_intake*animals[year, age] for age in animal_ages)
                  <= seed2_buy[year] - seed2_sell[year] + seed2[year]
                  for year in years), name="Seed2_consumption")

# 3. seed1ain seed1owing

seed1eed1owing = model.addConstrs((seed1[year, land] <= seed1_yield[land]*seed1_area[land]
                  for year in years for land in lands), name="Seed1_seed1owing")

# 4. Land capacity

LandCap = model.addConstrs((seed2[year]/seed2_yield + baby_animal_land*(newborn[year] + animals[year,1])
                  + gp.quicksum((1/seed1_yield[land])*seed1[year, land] for land in lands)
                  + gp.quicksum(animal_land*animals[year, age] for age in animal_ages)
                  <= land_cap for year in years), name="Land_capacity")


# 5. Labor

Labor = model.addConstrs((baby_animal_labor*(newborn[year] + animals[year,1])
                  + gp.quicksum(animal_labor*animals[year, age] for age in animal_ages)
                  + gp.quicksum(seed1_labor/seed1_yield[land]*seed1[year,land] for land in lands)
                  + seed2_labor/seed2_yield*seed2[year] 
                  <= labor_cap + overtime[year] for year in years), name="Labor")

# 6.1 Continuity

Continuity1 = model.addConstrs((animals[year,1] == (1-baby_animal_decay)*newborn[year-1] 
                  for year in years if year > min(years)),
                 name="Continuity_a")

# 6.2 Continuity

Continuity2 = model.addConstrs((animals[year,2] == (1-baby_animal_decay)*animals[year-1,1] 
                  for year in years if year > min(years)),
                 name="Continuity_b")

# 6.3 Continuity

Continuity3 = model.addConstrs((animals[year,age+1] == (1-animal_decay)*animals[year-1,age]
                  for year in years for age in animal_ages if year > min(years) and age < max(animal_ages)),
                 name="Continuity_c")

# 7. Heifers birth

Heiferseed2irth = model.addConstrs((newborn[year] + baby_animals_sell[year] 
                  == gp.quicksum(birthrate/2*animals[year,age] for age in animal_ages) for year in years)
                 , name="Heifers_birth")

# 8. Final animals
FinalDairyanimals = model.addRange(gp.quicksum(animals[max(years), age] for age in animal_ages), min_final_animals, max_final_animals, name="Final_dairy_animals" )

# 9.1-9.2 Initial conditions

InitialHeifers = model.addConstrs((initial_baby_animal_number == animals[1, age] for age in ages if age < 3),
                 name="Initial_conditions")

# 9.3 Initial conditions

Initialanimals = model.addConstrs((initial_animals_number == animals[1, age] for age in ages if age >= 3),
                 name="Initial_condition_animals")

# 10. Yearly profit

YearlyProfit = model.addConstrs((profit[year]
                  == baby_animal_price*birthrate/2*gp.quicksum(animals[year, age] for age in animal_ages)
                  + baby_animal_price*baby_animals_sell[year] + animal_price*animals[year, animal_last_sell_age]
                  + animal_yearly_income*gp.quicksum(animals[year, age] for age in animal_ages)
                  + seed1_price*seed1_sell[year] + seed2_price*seed2_sell[year]
                  - seed1_cost*seed1_buy[year] - seed2_cost*seed2_buy[year]
                  - overtime_cost*overtime[year] - regular_time_cost
                  - baby_animal_cost*(newborn[year] + animals[year,1])
                  - animal_cost*gp.quicksum(animals[year, age] for age in animal_ages)
                  - seed1_land_cost*gp.quicksum(seed1[year, land]/seed1_yield[land] for land in lands)
                  - seed2_land_cost*seed2[year]/seed2_yield
                  - installment*gp.quicksum(outlay[d] for d in years if d <= year)
                  for year in years), name="Yearly_profit")

# 0. Total profit

model.setObjective(gp.quicksum(profit[year] - installment*(year+4)*outlay[year] for year in years), GRB.MAXIMIZE)

model.optimize()

rows = ["Profit", "Outlay"]
columns = years.copy()
finance_plan = pd.DataFrame(columns=columns, index=rows, data=0.0)

for year in years:
    if (abs(profit[year].x) > 1e-6):
        finance_plan.loc["Profit", year] = np.round(profit[year].x, 1)
    if (abs(outlay[year].x) > 1e-6):
        finance_plan.loc["Outlay", year] = np.round(outlay[year].x, 1)

finance_plan

rows = lands.copy() + ["Buy", "Sell"]
columns = years.copy()
seed1_plan = pd.DataFrame(columns=columns, index=rows, data=0.0)

for year, land in seed1.keys():
    if (abs(seed1[year, land].x) > 1e-6):
        seed1_plan.loc[land, year] = np.round(seed1[year, land].x, 1)
for year in years:
    if (abs(seed1_buy[year].x) > 1e-6):
        seed1_plan.loc["Buy", year] = np.round(seed1_buy[year].x, 1)
    if (abs(seed1_sell[year].x) > 1e-6):
        seed1_plan.loc["Sell", year] = np.round(seed1_sell[year].x, 1)
seed1_plan


rows = ["seed1ow", "Buy", "Sell"]
columns = years.copy()
seed2_plan = pd.DataFrame(columns=columns, index=rows, data=0.0)

for year in years:
    if (abs(seed2[year].x) > 1e-6):
        seed2_plan.loc["seed1", year] = np.round(seed2[year].x, 1)
    if (abs(seed2_buy[year].x) > 1e-6):
        seed2_plan.loc["Buy", year] = np.round(seed2_buy[year].x, 1)
    if (abs(seed2_sell[year].x) > 1e-6):
        seed2_plan.loc["Sell", year] = np.round(seed2_sell[year].x, 1)
seed2_plan


rows = ["Sell", "Raise"]
columns = years.copy()
livestock_plan = pd.DataFrame(columns=columns, index=rows, data=0.0)

for year in years:
    if (abs(baby_animals_sell[year].x) > 1e-6):
        livestock_plan.loc["Sell", year] = np.round(baby_animals_sell[year].x, 1)
    if (abs(newborn[year].x) > 1e-6):
        livestock_plan.loc["Raise", year] = np.round(newborn[year].x, 1)
livestock_plan


