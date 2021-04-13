# Ian Jenatz y Fabricio Juarez

import numpy as np # manejo de matrices
import sys
import pandas as pd # estructura las matrices para print()

'''
Code Description:
'''

# def inputData():
#     varAmount = 2

#     coefmatrix = [0.0] * varAmount
#     i = 0
#     while i < len(coefmatrix):
#         coef = float(input(" Coeficiente de FO " + str(i + 1) + " : "))
#         coefmatrix[i] = coef * -1
#         print(coefmatrix)
#         i+=1

#     choiceP = input('max o min: ') # used to manipulate the coefficients and final result.
#     print(choiceP)

#     cant_rest = int(input('\nCantidad de Restricciones: '))
#     print(cant_rest, 'restricciones \n')

## if choiceP == "max": # in maximization problems, the coefficients become negative in the simplex table.
##     i = 0
##     while i < len(coefmatrix):
##         coefmatrix[i] *= -1
##         i += 1

#     return varAmount, coefmatrix, choiceP, cant_rest

# varAmount, coefmatrix, choiceP, cant_rest = inputData()

# def createTable():
#     tab_matrix = np.zeros([int(cant_rest)+1, varAmount + 3], dtype = float)
#     ineq_primal = [] # add a 1 to rows for row 0 (z). Also add both 3 extra columns (row, z, and total amount) and the amount of restrictions for the slack variables.

#     tab_matrix[0][1] = 1 # for z variable
#     i = 2
#     while i < varAmount + 2: # inputs coefmatrix values into first row.
#         tab_matrix[0][i] = coefmatrix[i-2]
#         i+=1

#     print(tab_matrix)

#     row = 1 # ignores row 0 (z)
#     col = 2 # ignores 'row' and 'z' columns.
#     while row < cant_rest+1:
#         tab_matrix[row][0] = row # generates row # in 'row' column.
#         col = 2
#         while col < varAmount+2: # asks for data for variable columns.
#             r = input("enter data ")
#             tab_matrix[row,col] = r
#             print(tab_matrix)
#             col+=1
#         ineq_primal.append(str(input("inequality symbol : ")))
#         print(ineq_primal[-1])
#         tab_matrix[row][col] = input("total amount : ")
#         print(tab_matrix)
#         print(ineq_primal)
#         row+=1

#     return tab_matrix, ineq_primal

# primal_matrix, ineq_primal = createTable()







# Ejemplo Min (clase)
primal_matrix = np.array(
[[ 0.0,  1.0, -3.0, -5.0,  0.0],
[ 1.0,  0.0,  25.0,  50.0,  80000.0],
[ 2.0,  0.0,  0.5,  0.25,  700.0],
[ 3.0,  0.0,  1.0,  0.0,  1000.0]])
choiceP = 'max'
ineq_primal = ['<=', '<=', '<=']
ursP = [0, 0]

# # Ejemplo Min (del libro)
# primal_matrix = np.array(
# [[ 0.0,  1.0, -2.0, -3.0,  0.0],
# [ 1.0,  0.0,  0.5,  0.25,  4.0],
# [ 2.0,  0.0,  1.0,  3.0,  20.0],
# [ 3.0,  0.0,  1.0,  1.0,  10.0]])
# choiceP = 'min'
# ineq_primal = ['<=', '>=', '=']
# ursP = [0, 0]

# # Ejemplo Max (en linea) http://www.universalteacherpublications.com/univ/ebooks/or/Ch3/mmethod.htm
# primal_matrix = np.array(
# [[ 0.0,  1.0, -1.0, -5.0,  0.0],
# [ 1.0,  0.0,  3.0,  4.0,  6.0],
# [ 2.0,  0.0,  1.0,  3.0,  2.0]])
# choiceP = 'max'
# ineq_primal = ['<=', '>=']
# ursP = [0, 0]

# # Ejemplo Min 2 (libro)
# primal_matrix = np.array(
# [[ 0.0,  1.0, -4.0, -4.0,  -1,  0.0],
# [ 1.0,  0.0,  1.0,  1.0,  1.0,  2.0],
# [ 2.0,  0.0,  2.0,  1.0,  0.0,  3.0],
# [ 3.0,  0.0,  2.0,  1.0,  3.0,  3.0]])
# choiceP = 'min'
# ineq_primal = ['<=', '<=', '>=']
# ursP = [0, 0, 0]

# # Ejemplo Min 3 (libro)
# primal_matrix = np.array(
# [[ 0.0,  1.0, -2.0, -3.0,  0.0],
# [ 1.0,  0.0,  2.0,  1.0,  4.0],
# [ 2.0,  0.0,  1.0,  -1.0,  -1.0]])
# choiceP = 'min'
# ineq_primal = ['>=', '>=']
# ursP = [0, 0]

# # Ejemplo Max 1 (libro)
# primal_matrix = np.array(
# [[ 0.0,  1.0, -3.0, -1.0,  0.0],
# [ 1.0,  0.0,  1.0,  1.0,  3.0],
# [ 2.0,  0.0,  2.0,  1.0,  4.0],
# [ 3.0,  0.0,  1.0,  1.0,  3.0]])
# choiceP = 'max'
# ineq_primal = ['>=', '<=', '=']
# ursP = [0, 0]

varAmountP = len(primal_matrix[0]) - 3
print(varAmountP)
cant_restP = len(primal_matrix) - 1
slackAmountP = 0

for i in ineq_primal:
    if i != '=':
        slackAmountP += 1

# Dual for normal Primal
dual_matrix = primal_matrix.copy()
dual_matrix = np.delete(dual_matrix, [0, 1], 1)

choiceD = 'min'
if choiceP == 'min':
    choiceD = 'max'

normal = 1
if choiceP == 'max':
    for i in ineq_primal:
        if i != '<=':
            normal = 0
if choiceP == 'min':
    for i in ineq_primal:
        if i != '>=':
            normal = 0

ursD = [0] * cant_restP
ineq_dual = []
if normal == 1:
    if choiceD == 'max':
        for i in range(varAmountP):
            ineq_dual.append('<=')
    elif choiceD == 'min':
        for i in range(varAmountP):
            ineq_dual.append('>=')
elif normal == 0:
    if choiceP == 'max':
        i = 0
        while i < len(ineq_primal):
            if ineq_primal[i] == '>=':
                dual_matrix[i+1] *= -1
            elif ineq_primal[i] == '=':
                ursD[i] = 1
            ineq_dual.append('>=')
            if i < len(ursP):
                if ursP[i] == 1:
                    ineq_dual.append('=')
            i += 1
    elif choiceP == 'min':
        i = 0
        while i < len(ineq_primal):
            if ineq_primal[i] == '<=':
                dual_matrix[i+1] *= -1
            elif ineq_primal[i] == '=':
                ursD[i] = 1
            ineq_dual.append('<=')
            if i < len(ursP):
                if ursP[i] == 1:
                    ineq_dual.append('=')
            i += 1

j = i
while i < len(ursP):
    if ursP[i] == 1:
        ineq_dual.append('=')
    i += 1

while len(ineq_dual) > varAmountP:
    ineq_dual.pop()

while len(ineq_dual) < varAmountP:
    if choiceP == 'max':
        ineq_dual.append('>=')
    elif choiceP == 'min':
        ineq_dual.append('<=')

dual_matrix = np.roll(dual_matrix,-1,0)
dual_matrix = dual_matrix.T
dual_matrix = np.roll(dual_matrix,1,0)

dual_matrix = np.insert(dual_matrix, 0, 0, 1)
dual_matrix = np.insert(dual_matrix, 0, 0, 1)
dual_matrix[0][1] = 1
i = 0
while i < len(dual_matrix):
    dual_matrix[i][0] = i
    i += 1

i = 1
while i < len(dual_matrix):
    dual_matrix[i][-1] *= -1
    i += 1

i = 2
while i < len(dual_matrix[0]) - 1:
    dual_matrix[0][i] *= -1
    i += 1

print("Primal Matrix")
print(primal_matrix[:,2:])
print(ineq_primal)
print(ursP)
print("Dual Matrix")
print(dual_matrix[:,2:])
print(ineq_dual)
print(ursD)

varAmountD = cant_restP
cant_restD = varAmountP
slackAmountD = 0
for i in ineq_dual:
    if i != '=':
        slackAmountD += 1

def initialTable(tab_matrix, slackAmount, varAmount, cant_rest, choice, inequalities, urs):
    # Primal Big M
    i = 1
    j = 2
    while i < len(tab_matrix):
        if tab_matrix[i][-1] < 0:
            while j < len(tab_matrix[0] + 1):
                tab_matrix[i][j] *= -1
                if inequalities[i-1] == '<=':
                    inequalities[i-1] = '>='
                elif inequalities[i-1] == '>=':
                    inequalities[i-1] = '<='
                j += 1
        i += 1
    print(inequalities)

    for i in range(slackAmount):
        tab_matrix = np.insert(tab_matrix, 2 + varAmount, 0, 1)

    print(tab_matrix)

    print(choice)
    row = 1
    col = 2 + varAmount
    artifAmount = 0
    if choice == 'max':
        mVal = 1000000000
    elif choice == 'min':
        mVal = -1000000000
    artifCols = []
    print(mVal)

    while row < len(tab_matrix):
        if inequalities[row - 1] == '<=':
            tab_matrix[row][col + row-1] = 1
        elif inequalities[row - 1] == '>=':
            tab_matrix[row][col + row-1] = -1
            tab_matrix = np.insert(tab_matrix, len(tab_matrix[0]) - 1, 0, 1)
            tab_matrix[row][len(tab_matrix[0]) - 2] = 1
            tab_matrix[0][len(tab_matrix[0]) - 2] = mVal
            artifCols.append(row)
            artifAmount += 1
        elif inequalities[row - 1] == '=':
            tab_matrix = np.insert(tab_matrix, len(tab_matrix[0]) - 1, 0, 1)
            tab_matrix[row][len(tab_matrix[0]) - 2] = 1
            tab_matrix[0][len(tab_matrix[0]) - 2] = mVal
            artifCols.append(row)
            artifAmount += 1
        row += 1
    print(tab_matrix)

    print(urs)
    i = 0
    while i < len(urs):
        if urs[i] == 1:
            tab_matrix = np.insert(tab_matrix, len(tab_matrix[0]) - 1, 0, 1)
            row = 0
            while row < len(tab_matrix):
                tab_matrix[row][-2] = tab_matrix[row][i + 2] * -1
                row += 1
        i += 1

    col = 2
    while col < len(tab_matrix[0]):
        row = 1
        while row < len(tab_matrix):
            if row in artifCols:
                tab_matrix[0][col] += (tab_matrix[row][col] * mVal * -1)
            row += 1
        col += 1

    print("\nInitial Tableau: \n")
    cols = ["Row", "z"]
    i = 0
    while i < varAmount:
        cols.append(f"x{i+1}")
        i+=1
    j = 0
    while j < cant_rest:
        if inequalities[j] == "<=":
            cols.append(f"s{j+1}")
        elif inequalities[j] == ">=":
            cols.append(f"e{j+1}")
        j+=1
    k = 0
    while k < cant_rest:
        if inequalities[k] == ">=":
            cols.append(f"a{k+1}")
        elif inequalities[k] == "=":
            cols.append(f"a{k+1}")
        k+=1
    l = 0
    while l < len(urs):
        if urs[l] == 1:
            cols.append(f"x{l+1}''")
        l += 1

    cols.append("Total")
    print(cols)
    tableau = pd.DataFrame(tab_matrix, columns=cols)
    print(tableau.round(3).to_string(index=False), '\n')

    return tab_matrix, cols, choice, varAmount


# Simplex (Big M)
def findValues():
    print(tab_matrix)
    if choice == 'min':
        min_val_arr = np.where(tab_matrix[0] == np.amax(tab_matrix[0][2:len(tab_matrix[0]) - 1]))
    elif choice == 'max':
        min_val_arr = np.where(tab_matrix[0] == np.amin(tab_matrix[0][2:len(tab_matrix[0]) - 1]))
    i = 0
    while i < len(min_val_arr[0]):
        if min_val_arr[0][i] == 0 or min_val_arr[0][i] == 1:
            min_val_arr = np.delete(min_val_arr, i, 1)
        i += 1
    print(min_val_arr)
    try:
        min_val = int(min_val_arr[0])
    except:
        min_val = int(min_val_arr[0][0])
    pivot = tab_matrix[0][min_val]
    print("Column: ", min_val)
    print("Pivot: ", pivot)

    min_total = float('inf')
    row = 1
    while row < len(tab_matrix):
        if tab_matrix[row][min_val] > 0 and tab_matrix[row][-1]/tab_matrix[row][min_val] < min_total and tab_matrix[row][-1]/tab_matrix[row][min_val] >= 0:
            min_total = tab_matrix[row][-1]/tab_matrix[row][min_val]
            divVal = tab_matrix[row][min_val]
            min_index = row 
        row+=1

    print("Minimum total: ", min_total)
    if min_total == float('inf'):
        sys.exit("No solution")
    print("Value to divide by: ", divVal)
    print("row: ", min_index, "\n")

    return divVal, min_index, min_val


def changeTable():
    matrix_copy = tab_matrix.copy()
    col = 2
    while col < len(tab_matrix[min_index]):
        tab_matrix[min_index][col] = matrix_copy[min_index][col] / divVal
        col += 1

    row = 0
    col = 1
    while row < len(tab_matrix):
        col = 1
        if row != min_index:
            while col < len(tab_matrix[0]):
                tab_matrix[row][col] = matrix_copy[row][col] - (matrix_copy[row][min_val] * tab_matrix[min_index][col])
                col += 1
        row += 1

    tableau = pd.DataFrame(tab_matrix, columns=cols)
    print(tableau.round(3).to_string(index=False), "\n")


def checkIteration():
    iteration = False
    if choice == 'min':
        for i in tab_matrix[0][2:len(tab_matrix[0]) - 1]:
            if i > 0:
                iteration = True
    if choice == 'max':
        for i in tab_matrix[0][2:len(tab_matrix[0]) - 1]:
            if i < 0:
                iteration = True
    return iteration

tab_matrix, cols, choice, varAmount = initialTable(primal_matrix, slackAmountP, varAmountP, cant_restP, choiceP, ineq_primal, ursP)
iteration = checkIteration()
while iteration == True:
    divVal, min_index, min_val = findValues()
    changeTable()
    iteration = checkIteration()

print("\nOptimal Solution Primal: ", tab_matrix[0][-1], "\n\n\n\n\n\n")

tab_matrix, cols, choice, varAmount = initialTable(dual_matrix, slackAmountD, varAmountD, cant_restD, choiceD, ineq_dual, ursD)
iteration = checkIteration()
while iteration == True:
    divVal, min_index, min_val = findValues()
    changeTable()
    iteration = checkIteration()

print("\nOptimal Solution Dual: ", tab_matrix[0][-1])
