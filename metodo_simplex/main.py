import pruebas
from typing import Counter, OrderedDict
from tabulate import tabulate
import numpy


# cast into matrix.
primal_matrix = numpy.zeros([
    (1 + len(primal_restrictions)), len(primal_objective_function) + 1
], dtype=float)
symbols = [v for k,v in primal_objective_function.items() if (k == 'symbol')] + [v['symbol'] for v in [x for x in primal_restrictions]]
primal_restriction_symbols:list = symbols[1:]

for i in range(len(primal_matrix)): primal_matrix[i][0] = i # adding indexes

number_of_variables:int = len([x for x in primal_restrictions[0].keys() if (x[0].lower() == 'x')])

# populate the matrix with the values.
variables = [k for k,v in primal_restrictions[0].items() if (k[0].lower() == 'x')]
variables.sort(key=lambda x: x[1:])

temp = [OrderedDict({k:-v for k,v in primal_objective_function.items() if (k != 'symbol' and k != 'c')})] + primal_restrictions
index = 0
for row in range(len(primal_matrix)):
    col = 1
    # Adding the z 
    if (temp[row].get('z') == None): primal_matrix[row, col] = 0
    else: primal_matrix[row, col] = 1
    col += 1
    # Adding variables.
    for i in variables:
        primal_matrix[row, col] = temp[row][i]
        col += 1
    # adding the constants
    if (temp[row].get('c') == None): primal_matrix[row, col] = 0
    else: primal_matrix[row, col] = temp[row]['c']

# Figuring out the variable quantity and the restriction quantity 
primal_variable_quantity:int = len(variables)
primal_restriction_quantity:int = len(primal_restrictions)
print(f"primal_variable_quantity: {primal_variable_quantity}", f"primal_restriction_quantity: {primal_restriction_quantity}")

# Calculate quantity of slack variables. 
# The quantity of slack variables are going to be the 
# total number of constraints minus the number of constraints with an '='
primal_slack_variable_quantity:int = len(primal_restriction_symbols) - symbols[1:].count('=')
print(f"primal_slack_variable_quantity: {primal_slack_variable_quantity}")

# Make the dual matrix 
dual_matrix = numpy.array([x[2:] for x in primal_matrix]) # no z, no index

# determining choices for dual.
dual_choice = choices['min']
if (primal_choice == choices['min']): dual_choice = choices['max']

# determining normality.
normal = True
if (primal_choice == choices['max']): 
    for i in primal_restriction_symbols: 
        if (i != '<=' or i != '=<'): 
            normal = not normal
            break
elif (primal_choice == choices['min']): 
    for i in primal_restriction_symbols: 
        if (i != '>=' or i != '=>'): 
            normal = not normal
            break

# dual making the urs and the inequality symbols.
dual_unrestricted_variables = [0 for x in primal_restriction_quantity]
dual_restriction_symbols = []
