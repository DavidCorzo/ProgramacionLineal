from simple_table import SimplexTable
from const import SLACK_KEY, C_J_KEY, SYMBOL
from typing import Container

PRINT_ALL = True



# https://www.youtube.com/watch?v=M8POtpPtQZc

def write_in_standard_form(constraints:list) -> None:
    """
    <summary>
        Esta función pasa cualquier condicion puesta en 
        términos de ">=" o ">" a "<=" y "<". 
        De esa manera se pueden sumar las variables de holgura sin importar 
        qué tipo de desigualdad sea por que todas seran ya sea "<=" o "<".
    </summary>
    """
    for i in range(len(constraints)):
        # <=, =<, <
        if ( (constraints[i][SYMBOL] != '<=') or (constraints[i][SYMBOL] != '=<') or (constraints[i][SYMBOL] != '<') ):
            if ((constraints[i][SYMBOL] == '>=') or (constraints[i][SYMBOL] == '=>') or (constraints[i][SYMBOL] == '>')):
                # si es >=, =>, o >; tenemos que multiplicar todo por -1
                for k in constraints[i].keys():
                    if (k != SYMBOL):
                        constraints[i][k] *= -1
    if PRINT_ALL:
        for i in constraints:
            print(i)
    

def include_slack_vars(f_o:dict, constraints:list) -> None:
    """
    <summary>
        The reason for adding slack variables is in 
        order to make the inquality an equality.
        Its important to execute the "turn_into_less_than_or_equal" function first, 
        this function assumes that all constraints are in "<=" form.
        10x_1 + 20x_2 <= 120
        8 x_1 + 8 x_2 <= 80
        ...
        10x_1 + 20x_2 + 1S_1 + 0S_2 = 120
        8x_1  + 8x_2  + 0S_1 + 1S_2 = 80
    </summary>
    """
    # Example: 
    # [
    #   {'s0': 1, 's1': 0, 's2': 0, ..., 'sn': 0}, 
    #   {'s0': 0, 's1': 1, 's2': 0, ..., 'sn': 0}, 
    #   {'s0': 0, 's1': 0, 's2': 1, ..., 'sn': 1}
    # ]
    n:int = len(constraints)
    id_matrix = [{} for i in range(n)]
    for i in range(n):
        for ii in range(n):
            id_matrix[i][f"s{ii}"] = 0
        id_matrix[i][f"s{i}"] = 1

    # Example:
    # [
    #   {'x1': 2, 'x2':1, 's': '<=', 'c': 18} + {'s0': 1, 's1': 0, 's2': 0}
    #   {'x1': 2, 'x2':3, 's': '<=', 'c': 42} + {'s0': 0, 's1': 1, 's2': 0}
    #   {'x1': 3, 'x2':1, 's': '<=', 'c': 24} + {'s0': 0, 's1': 0, 's2': 1}
    # ]
    for i in range(len(constraints)):
        constraints[i][SLACK_KEY] = id_matrix[i]
        constraints[i][SYMBOL] = '='
    # Now add the slack variables to the objective function.
    f_o.update({SLACK_KEY: {}})
    for i in id_matrix[0].keys():
        f_o[SLACK_KEY].update({i:0})
    
    # if PRINT_ALL:
    #     for i in constraints:
    #         print(i)
    #     print(f_o)


def make_the_initial_simplex_table(simplex_matrix: SimplexTable) -> None:

    pass

def main() -> None:
    f_o = {C_J_KEY: {'A': 1, 'B': 2}}
    constraints = [
        {'A':  1, 'B': 4, SYMBOL: '<=', 'c':  21},
        {'A':  2, 'B': 1, SYMBOL: '>=', 'c': 7},
        {'A':  3, 'B': 1.5, SYMBOL: '<=', 'c':  21},
        {'A':  -2, 'B':6, SYMBOL: '>=', 'c':  0},
        # A + B >= 4    | (-1)A - (1)B + (1)S0 + (0)S1 + (0)S2 + (0)S3 = -4
        # 3A + 4B <= 24 | (03)A + (4)B + (0)S0 + (1)S1 + (0)S2 + (0)S3 = 24
        # A >= 2        | (-1)A + (0)B + (0)S0 + (0)S1 + (1)S2 + (0)S3 = -2
        # A - B <= 0    | (01)A - (0)B + (0)S0 + (0)S1 + (0)S2 + 4(1)S3 =  0
    ]
    # usual constraints: y, x >= 0
    # write_in_standard_form(constraints)
    # include_slack_vars(f_o, constraints)
    # simplex_matrix = SimplexTable(constraints, f_o)
    # make_the_initial_simplex_table(simplex_matrix)

if __name__ == '__main__':
    main()

