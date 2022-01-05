from typing import OrderedDict
from tabulate import tabulate
import numpy

primal_objective_function:dict = {
    'z': 1, 'symbol': '=', 'X1': 3, 'X2': 5
}
primal_restrictions:list = [
    OrderedDict({'X1': 25 , 'X2': 50  , 'symbol': '<=', 'c': 80000}),
    OrderedDict({'X1': 0.5, 'X2': 0.25, 'symbol': '<=', 'c': 700  }),
    OrderedDict({'X1': 0.1, 'X2': 0   , 'symbol': '<=', 'c': 1000 })
]
primal_unrestricted_variables:list = [0 for k,v in primal_restrictions[0].items() if (k[0].lower() == 'x')]

# cast into matrix.
primal_matrix = numpy.zeros([
    (1 + len(primal_restrictions)), len(primal_objective_function) + 1
], dtype=float)
symbols = [v for k,v in primal_objective_function.items() if (k == 'symbol')] + [v['symbol'] for v in [x for x in primal_restrictions]]

for i in range(len(primal_matrix)): primal_matrix[i][0] = i # adding indexes

number_of_variables:int = len([x for x in primal_restrictions[0].keys() if (x[0].lower() == 'x')])

# populate the matrix with the values.
temp = [primal_objective_function] + primal_restrictions
index = 0
variables = [k for k,v in primal_restrictions[0].items() if (k[0].lower() == 'x')].sort()
variable_quantity = len(variables)
for row in range(len(primal_matrix)):
    col = 1
    # Adding variables.
    for i in variables:
        primal_matrix[row, col] = temp[row][i]
        col += 1
    
        


# print(primal_matrix)
