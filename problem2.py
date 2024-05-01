import numpy as np
import pandas as pd

import gurobipy as gp
from gurobipy import GRB
farming = {
    'animals': {
        'first_production_age': 2,
        'last_sell_age': 10,
        'min_final_animals': 50,
        'max_final_animals': 175,
#       'min_final_animals': 50000,
#       'max_final_animals': 500000,
        'animal_yearly_income': 370.0,
        'birthrate': 1.1,
    },
    'animals_needs': {
        'adult': {
            'land': 1.0,
            'labor': 0.42,
            'decay': 0.02,
            'initial_number': 9.8,
            'price': 120.0,
            'cost': 100.0,
        },
        'baby': {
            'land': 0.666,
            'labor': 0.1,
            'decay': 0.05,
            'initial_number': 9.5,
            'price': 40.0,
            'cost': 50.0,
        }
    },
    'capacity': {
        'housing': 130,
        'land': 200,
        'labor': 55,
    },
    'seeds':{
        'seed1': {
            'intake': 0.6,
            'labor': 0.04,
            'price': 75.0,
            'cost': 90.0,
            'land_cost': 15.0,
        },
        'seed2': {
            'yield': 1.5,
            'intake': 0.7,
            'labor': 0.14,
            'price': 58.0,
            'cost': 70.0,
            'land_cost': 10.0,
        }
    },
    'lands':{
        'area': {1: 20.0, 2: 30.0, 3: 20.0, 4: 10.0},
        'yield': {1: 1.1, 2: 0.9, 3: 0.8, 4: 0.65},
    },
    'years_number': 5,
    'overtime_cost': 1.20,
    'regular_time_cost': 4000.0,
    'installment': 39.71,
}





# function to create a model and solve it and return the results (finance_plan, seed1_plan, seed2_plan, livestock_plan)
def solve_farming_problem(farming):

    # Assigning values from dictionary to variables
    animals = farming['animals']
    animals_needs = farming['animals_needs']
    capacity = farming['capacity']
    seeds = farming['seeds']
    lands = farming['lands']

    years_number = farming['years_number']      # plan duration 
    overtime_cost = farming['overtime_cost']    #  Cost for getting an hour of overtime.
    regular_time_cost = farming['regular_time_cost']
    installment = farming['installment']

    years_number = farming['years_number'] # number of years
    years = [i for i in range(1, years_number+1)] # plan years

    lands_number = len(farming['lands']['area']) # number of land types
    lands = [i for i in range(1, lands_number+1)] # land types

    #tableau 1 {
    animal_first_production_age = farming['animals']['first_production_age'] # first production age of the animal
    animal_last_sell_age = farming['animals']['last_sell_age'] # last sell age of the animal
    animal_ages = [i for i in range(animal_first_production_age, animal_last_sell_age+1)] # animal ages (before having to sell them): from ... to ...
    ages = [i for i in range(1, max(animal_ages)+1)] 
    min_final_animals = farming['animals']['min_final_animals'] # minimum number of final animals
    max_final_animals = farming['animals']['max_final_animals'] # maximum number of final animals
    animal_yearly_income = farming['animals']['animal_yearly_income'] # yearly milk income
    birthrate = farming['animals']['birthrate'] 
    #} fin de tableau 1



    #tableau2 : {
    animal_land = farming['animals_needs']['adult']['land'] # land needed for an animal
    animal_labor = farming['animals_needs']['adult']['labor'] # labor needed for an animal
    animal_decay = farming['animals_needs']['adult']['decay'] # animal decay
    initial_animals_number = farming['animals_needs']['adult']['initial_number'] # initial number of animals
    animal_price = farming['animals_needs']['adult']['price'] # cow price
    animal_cost = farming['animals_needs']['adult']['cost'] #Yearly cost for supporting an animal.
 
    baby_animal_land = farming['animals_needs']['baby']['land'] # land needed for a baby animal
    baby_animal_labor = farming['animals_needs']['baby']['labor'] # labor needed for a baby animal
    baby_animal_decay = farming['animals_needs']['baby']['decay'] # heifer decay
    initial_baby_animal_number = farming['animals_needs']['baby']['initial_number'] # initial number of baby animals
    baby_animal_price = farming['animals_needs']['baby']['price'] # baby animals price
    baby_animal_cost = farming['animals_needs']['baby']['cost'] # Yearly cost for supporting a baby animal.
    #} fin du tableau 2


    # tableau 3: capacity{
    housing_cap = farming['capacity']['housing'] # housing capacity 
    land_cap = farming['capacity']['land'] # land capacity 
    labor_cap = farming['capacity']['labor'] # labor capacity which is the maximum labor that can be used for farming (in hours)
    #} fin de tableau 3

    #tableau4: {
    seed1_area = farming['lands']['area'] # area of land type i that can be used for seed1
    seed1_yield = farming['lands']['yield'] # yield of seed1 in land type i (in tons per acre)
    #} fin de tableau 4


    #tableau 5:{
    #5.1. seed1
    seed1_intake = farming['seeds']['seed1']['intake'] # seed1 intake (intake means the amount of food that the animal eats)
    seed1_labor = farming['seeds']['seed1']['labor'] # labor needed 
    seed1_price = farming['seeds']['seed1']['price'] # Price for selling a ton 
    seed1_cost = farming['seeds']['seed1']['cost'] # Cost for buying a ton 
    seed1_land_cost = farming['seeds']['seed1']['land_cost'] #Yearly cost for supporting an acre of land devoted to seed1.

    #5.2. seed2
    seed2_yield = farming['seeds']['seed2']['yield'] 
    seed2_intake = farming['seeds']['seed2']['intake']
    seed2_labor = farming['seeds']['seed2']['labor'] 
    seed2_price = farming['seeds']['seed2']['price'] 
    seed2_cost = farming['seeds']['seed2']['cost'] 
    seed2_land_cost = farming['seeds']['seed2']['land_cost'] 
    #} fin de tableau 5


    overtime_cost = farming['overtime_cost'] # Cost for getting an hour of overtime.
    regular_time_cost = farming['regular_time_cost'] #Cost for having labor_cap hours of labor in regular time.
    installment = farming['installment'] #Annual payment for each loan

    # model and decision variables
    model = gp.Model('Farming')
    outlay = model.addVars(years, vtype=GRB.CONTINUOUS, name="Outlay") # money spent in year i on extra housing
    overtime = model.addVars(years, vtype=GRB.CONTINUOUS, name="Overtime") # overtime hours in year i
    newborn = model.addVars(years, vtype=GRB.CONTINUOUS, name="Newborn") # number of newborn female animals kept to be raised in year i
    baby_animals_sell = model.addVars(years, vtype=GRB.CONTINUOUS, name="baby_animals_sell") # number of female baby animals sold in year i
    profit = model.addVars(years, vtype=GRB.CONTINUOUS, name="Profit")  # profit in year i
    seed1_buy = model.addVars(years, vtype=GRB.CONTINUOUS, name="seed1_buy") # amount of seed1 bought in year i (in tons)
    seed2_buy = model.addVars(years, vtype=GRB.CONTINUOUS, name="seed2_buy") # amount of seed2 bought in year i (in tons)
    seed1_sell = model.addVars(years, vtype=GRB.CONTINUOUS, name="seed1_sell") # amount of seed1 sold in year i (in tons)
    seed2_sell = model.addVars(years, vtype=GRB.CONTINUOUS, name="seed2_sell") # amount of seed2 sold in year i (in tons)
    seed1 = model.addVars(years, lands, vtype=GRB.CONTINUOUS, name="seed1")  # amount of seed1 grown in year i in land j (in tons)
    seed2 = model.addVars(years, vtype=GRB.CONTINUOUS, name="seed2")     # amount of seed2 grown in year i (in tons)
    animals = model.addVars(years, ages, vtype=GRB.CONTINUOUS, name="animals") # number of adult animals of age j in year i


    # Constraints:
    # 1. Housing capacity : The number of animals in the farm should not exceed the housing capacity.
    # newborn(year) + sum(animals(year,age)) - sum(outlay(d)) <= housing_cap 
    HousingCap = model.addConstrs((newborn[year] +
                        # animals[year,1] 
                        gp.quicksum(animals[year,age] for age in ages) -
                        gp.quicksum(outlay[d] for d in years if d <= year)
                        <= housing_cap for year in years), name="Housing_cap")

    # 2.1 Food consumption(seed1): The amount of seed1 consumed by the animals should not exceed the amount of seed1 bought and grown.
    # sum(seed1_intake*animals(year,age)) <= seed1_buy(year) - seed1_sell(year) + sum(seed1(year,land))
    seed1Consumption = model.addConstrs((
                    gp.quicksum(seed1_intake*animals[year, age] for age in animal_ages)
                    <= seed1_buy[year] - seed1_sell[year] + seed1.sum(year, '*')
                    for year in years), name="Seed1_consumption")

    # 2.2 Food consumption (seed2)
    seed2Consumption = model.addConstrs((
                    gp.quicksum(seed2_intake*animals[year, age] for age in animal_ages)
                    <= seed2_buy[year] - seed2_sell[year] + seed2[year]
                    for year in years), name="Seed2_consumption")

    # 3. seed1 growing: The amount of seed1 grown in a land should not exceed the yield of the land.
    # seed1(year,land) <= seed1_yield[land]*seed1_area[land]
    seed1growing = model.addConstrs((seed1[year, land] <= seed1_yield[land]*seed1_area[land]
                    for year in years for land in lands), name="Seed1_growing")

    # 4. Land capacity: The amount of land used for animals and seeds should not exceed the land capacity.
    # seed2[year]/seed2_yield + baby_animal_land*(newborn[year] + animals[year,[1, min-1]]) + sum(seed1[year,land]/seed1_yield[land]) + sum(animal_land*animals[year,age]) <= land_cap
    LandCap = model.addConstrs((seed2[year]/seed2_yield + baby_animal_land*sum(newborn[year] + animals[year,k] for k in range(1, animal_first_production_age))
                    + gp.quicksum((1/seed1_yield[land])*seed1[year, land] for land in lands)
                    + gp.quicksum(animal_land*animals[year, age] for age in animal_ages)
                    <= land_cap for year in years), name="Land_capacity")


    # 5. Labor: The amount of labor used for animals and seeds should not exceed the labor capacity.
    # seed2_labor*seed2[year]/seed2_yield + baby_animal_labor*(newborn[year] + animals[year,[1, min-1]]) + sum(seed1_labor/seed1_yield[land]*seed1[year,land]) + sum(animal_labor*animals[year,age]) <= labor_cap + overtime[year]
    Labor = model.addConstrs((baby_animal_labor*sum(newborn[year] + animals[year,k] for k in range(1, animal_first_production_age))
                    + gp.quicksum(animal_labor*animals[year, age] for age in animal_ages)
                    + gp.quicksum(seed1_labor/seed1_yield[land]*seed1[year,land] for land in lands)
                    + seed2_labor/seed2_yield*seed2[year] 
                    <= labor_cap + overtime[year] for year in years), name="Labor")

    # 6.1 Continuity1: The number of baby animals in year i should be equal to the number of baby animals in year i-1 multiplied by the baby decay rate.
    Continuity1 = model.addConstrs((animals[year,1] == (1-baby_animal_decay)*newborn[year-1] 
                    for year in years if year > min(years)),
                    name="Continuity_a")

    # 6.2 Continuity2: The number of first production age animals in year i should be equal to the number of first (production age animals-1) babies in year i-1 multiplied by the baby decay rate.
    Continuity2 = model.addConstrs((animals[year,animal_first_production_age] == (1-baby_animal_decay)*animals[year-1,animal_first_production_age-1] 
                    for year in years if year > min(years)),
                    name="Continuity_b")

    # 6.3 Continuity3: The number of animals of age j in year i should be equal to the number of animals of age j+1 in year i-1 multiplied by the animal decay rate.
    Continuity3 = model.addConstrs((animals[year,age+1] == (1-animal_decay)*animals[year-1,age]
                    for year in years for age in animal_ages if year > min(years) and age < max(animal_ages)),
                    name="Continuity_c")

    # 7. baby animals birth: The number of female baby animals born in year i should be equal to the number of female babies sold + kept to be raised in year i.
    baby_birth = model.addConstrs((newborn[year] + baby_animals_sell[year] 
                    == gp.quicksum(birthrate/2*animals[year,age] for age in animal_ages) for year in years)
                    , name="Baby_animals_birth")

    # 8. Final animals: The number of final animals in the last year should be between the minimum and maximum number of final animals.
    FinalDairyanimals = model.addRange(gp.quicksum(animals[max(years), age] for age in animal_ages), 
                                       min_final_animals, max_final_animals, name="Final_dairy_animals" )

    # 9. Initial conditions: the initial number of animals and babies
    InitialBabies = model.addConstrs((initial_baby_animal_number == animals[1, age] for age in range(1, animal_first_production_age)),
                    name="Initial_conditions")
    Initialanimals = model.addConstrs((initial_animals_number == animals[1, age] for age in ages if age >= animal_first_production_age),
                    name="Initial_condition_animals")

    # 10. Yearly profit
    YearlyProfit = model.addConstrs((profit[year]
                == baby_animal_price*birthrate/2*gp.quicksum(animals[year, age] for age in animal_ages)  # income from selling male baby animals
                + baby_animal_price*baby_animals_sell[year] + animal_price*animals[year, animal_last_sell_age] # income from selling female baby animals and adult animals
                + animal_yearly_income*gp.quicksum(animals[year, age] for age in animal_ages) # adult animals yearly income
                + seed1_price*seed1_sell[year] + seed2_price*seed2_sell[year] # income from selling seed1 and seed2
                - seed1_cost*seed1_buy[year] - seed2_cost*seed2_buy[year] # cost of buying seed1 and seed2
                - overtime_cost*overtime[year] - regular_time_cost # labor cost
                - baby_animal_cost*sum(newborn[year] + animals[year,k] for k in range(1, animal_first_production_age)) # baby animals cost
                - animal_cost*gp.quicksum(animals[year, age] for age in animal_ages) # adult animals cost
                - seed1_land_cost*gp.quicksum(seed1[year, land]/seed1_yield[land] for land in lands) # seed1 land cost
                - seed2_land_cost*seed2[year]/seed2_yield # seed2 land cost
                - installment*gp.quicksum(outlay[d] for d in years if d <= year) # loan installment
                for year in years), name="Yearly_profit")

    # Objective function: maximize the total profit over the years:
    model.setObjective(gp.quicksum(profit[year] - installment*(year+years_number-1)*outlay[year] for year in years), GRB.MAXIMIZE)

    # Solve the model
    model.optimize()
    print("========================================================================================================")
    #print IIS if the model is infeasible
    if(model.status != GRB.OPTIMAL):
        model.computeIIS() # IIS: Irreducible Infeasible Set which is a subset of the constraints that are infeasible
        #print the infeasible constraints:
        for constr in model.getConstrs():
            if constr.IISConstr:
                print(constr.ConstrName + " is infeasible")
        return None, None, None, None, None

    objective = model.objVal

    #Analysis: 
    #1. finance_plan:
    rows = ["Profit", "Outlay"]
    columns = years.copy()
    finance_plan = pd.DataFrame(columns=columns, index=rows, data=0.0)

    for year in years:
        if (abs(profit[year].x) > 1e-6):
            finance_plan.loc["Profit", year] = np.round(profit[year].x, 1)
        if (abs(outlay[year].x) > 1e-6):
            finance_plan.loc["Outlay", year] = np.round(outlay[year].x, 1)
    # finance_plan

    #2. seed1_plan:
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
    # seed1_plan


    #3. seed2_plan:
    rows = ["Grow", "Buy", "Sell"]
    columns = years.copy()
    seed2_plan = pd.DataFrame(columns=columns, index=rows, data=0.0)
    for year in years:
        if (abs(seed2[year].x) > 1e-6):
            seed2_plan.loc["Grow", year] = np.round(seed2[year].x, 1)
        if (abs(seed2_buy[year].x) > 1e-6):
            seed2_plan.loc["Buy", year] = np.round(seed2_buy[year].x, 1)
        if (abs(seed2_sell[year].x) > 1e-6):
            seed2_plan.loc["Sell", year] = np.round(seed2_sell[year].x, 1)
    # seed2_plan

    #4. livestock_plan:
    rows = ["Sell", "Raise"]
    columns = years.copy()
    livestock_plan = pd.DataFrame(columns=columns, index=rows, data=0.0)
    for year in years:
        if (abs(baby_animals_sell[year].x) > 1e-6):
            livestock_plan.loc["Sell", year] = np.round(baby_animals_sell[year].x, 1)
        if (abs(newborn[year].x) > 1e-6):
            livestock_plan.loc["Raise", year] = np.round(newborn[year].x, 1)
    # livestock_plan

    # if the model is infeasible, print the infeasible constraints
    if(model.status != GRB.OPTIMAL):
        model.computeIIS() # IIS: Irreducible Infeasible Set which is a subset of the constraints that are infeasible
        #print the infeasible constraints:
        for constr in model.getConstrs():
            if constr.IISConstr:
                print(constr.ConstrName)
        return None, None, None, None, None
    

    #return the results
    return objective, finance_plan, seed1_plan, seed2_plan, livestock_plan


# calling the function to solve the problem

[objective, finance_plan, seed1_plan, seed2_plan, livestock_plan] = solve_farming_problem(farming)
if(objective != None):
    print("Objective: ", objective)
    print("Finance Plan: ")
    print(finance_plan)
    print("Seed1 Plan: amount of seed1 to gorw in each land type in each year + amount to sell and buy ")
    print(seed1_plan)
    print("Seed2 Plan: ")
    print(seed2_plan)
    print("Livestock Plan: ")
    print(livestock_plan)
else:
    print("The model is infeasible")
    print("The constraints that are infeasible are printed above.")




