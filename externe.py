from problem2 import solve_farming_problem 

farming = {
    'animals': {
        'first_production_age': 2,
        'last_sell_age': 10,
        'min_final_animals': 50,
        'max_final_animals': 175,
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
    'years_number': 8,
    'overtime_cost': 1.20,
    'regular_time_cost': 4000.0,
    'installment': 39.71,
}

solve_farming_problem(farming)

