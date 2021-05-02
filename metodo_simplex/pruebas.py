from typing import Counter, OrderedDict

num = 1

choices = {'max': True, 'min': False}

primal_objective_function:dict = None
primal_restrictions:list = None
primal_unrestricted_variables:list = None
primal_choice:bool = None
if (num == 1):
    primal_objective_function:dict = {
        'z': 1, 'symbol': '=', 'X1': 3, 'X2': 5
    }
    primal_restrictions:list = [
        OrderedDict({'X1': 25 , 'X2': 50  , 'symbol': '<=', 'c': 80000}),
        OrderedDict({'X1': 0.5, 'X2': 0.25, 'symbol': '<=', 'c': 700  }),
        OrderedDict({'X1': 1, 'X2': 0   , 'symbol': '<=', 'c': 1000 })
    ]
    primal_unrestricted_variables:list = [0 for k,v in primal_restrictions[0].items() if (k[0].lower() == 'x')]
    primal_choice:bool = choices['max'] # Max is true, false is min
elif (num == 2):
    primal_objective_function:dict = {
        'z': 1, 'symbol': '=', 'X1': 2, 'X2': 3
    }
    primal_restrictions:list = [
        OrderedDict({'X1': 0.5, 'X2': 0.25, 'symbol': '<=', 'c': 4.0 }),
        OrderedDict({'X1': 1.0, 'X2': 3.00, 'symbol': '>=', 'c': 20.0}),
        OrderedDict({'X1': 1.0, 'X2': 1.00, 'symbol': '=' , 'c': 10.0})
    ]
    primal_unrestricted_variables:list = [0 for k,v in primal_restrictions[0].items() if (k[0].lower() == 'x')]
    primal_choice:bool = choices['min'] # Max is true, false is min
elif (num == 3):
    primal_objective_function:dict = {
        'z': 1, 'symbol': '=', 'X1': 1, 'X2': 5
    }
    primal_restrictions:list = [
        OrderedDict({'X1': 3.0, 'X2': 4.0, 'symbol': '<=', 'c': 6.0 }),
        OrderedDict({'X1': 1.0, 'X2': 3.0, 'symbol': '>=', 'c': 2.0})
    ]
    primal_unrestricted_variables:list = [0 for k,v in primal_restrictions[0].items() if (k[0].lower() == 'x')]
    primal_choice:bool = choices['max'] # Max is true, false is min
elif (num == 4):
    primal_objective_function:dict = {
        'z': 1, 'symbol': '=', 'X1': 4, 'X2': 4, 'X3': 1
    }
    primal_restrictions:list = [
        OrderedDict({'X1': 1, 'X2': 1, 'X3': 1, 'symbol': '<=', 'c': 2}),
        OrderedDict({'X1': 2, 'X2': 1, 'X3': 0, 'symbol': '<=', 'c': 3}),
        OrderedDict({'X1': 2, 'X2': 1, 'X3': 3, 'symbol': '>=', 'c': 3})
    ]
    primal_unrestricted_variables:list = [0 for k,v in primal_restrictions[0].items() if (k[0].lower() == 'x')]
    primal_choice:bool = choices['min'] # Max is true, false is min
elif (num == 5):
    primal_objective_function:dict = {
        'z': 1, 'symbol': '=', 'X1': 2, 'X2': 3
    }
    primal_restrictions:list = [
        OrderedDict({'X1': 2, 'X2':  1, 'symbol': '>=', 'c':  4}),
        OrderedDict({'X1': 1, 'X2': -1, 'symbol': '>=', 'c': -1}),
    ]
    primal_unrestricted_variables:list = [0 for k,v in primal_restrictions[0].items() if (k[0].lower() == 'x')]
    primal_choice:bool = choices['min'] # Max is true, false is min
elif (num == 6):
    primal_objective_function:dict = {
        'z': 1, 'symbol': '=', 'X1': 2, 'X2': 3, 'X3': 0
    }
    primal_restrictions:list = [
        OrderedDict({'X1': 2, 'X2': -1, 'X3': -1, 'symbol': '>=', 'c': 3}),
        OrderedDict({'X1': 1, 'X2': -1, 'X3':  1, 'symbol': '>=', 'c': 2})
    ]
    primal_unrestricted_variables:list = [0 for k,v in primal_restrictions[0].items() if (k[0].lower() == 'x')]
    primal_choice:bool = choices['min'] # Max is true, false is min
elif (num == 7):
    

