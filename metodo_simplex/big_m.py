

from typing import Container, OrderedDict


def make_inequalities_equalities(constraints:list, f_o: dict, max:bool, big_m:int) -> None:
    """
    <summary>
        This function turns inequalities to equalities using slack variables.
        Makes the step 1-4 in the big m.
    </summary>
    """
    oposite_symbol = {
        '<' : '>' , 
        '>' : '<' , 
        '<=': '>=', 
        '>=': '<=',
        '=>': '=<',
        '=<': '=>',
        '=': '='
    }
    # El siguiente convierte la constante negativa de los constraints en positivos.
    for index in range(len(constraints)):
        if (constraints[index]['c'] < 0):
            constraints[index] = mult_row(constraints[index], -1)
            constraints[index]['symbol'] = oposite_symbol[constraints[index]['symbol']]
            
    # Add slack variables and excess variables and artificial variables.
    n = 1
    index = 0
    for i in constraints:
        # '=' or '>='
        if ( i['symbol'] in ('=', '>=', '=>') ): # (i['symbol'] == '=') and ((i['symbol'] == '>=') or (i['symbol'] == '=>'))
            constraints[index].update( {f'a{str(n)}': 1} ) # Agrego las artifitial variables.
            if max: f_o.update( {f'a{str(n)}': -1 * big_m} ) # Agrego las variables artificiales a la función objetivo.
            else: f_o.update( {f'a{str(n)}': 1 * big_m} )
        # '<=' or '<'
        if ( i['symbol'] in ('<=', '<', '=<') ):
            constraints[index].update( {f's{str(n)}': 1} ) # Agrego las slack variables.
        # '>=' or '>'
        elif ( i['symbol'] in ('>=', '>', '=>') ):
            constraints[index].update( {f'e{str(n)}': -1} ) # Agrego las excess variables.
        constraints[index]['symbol'] = '=' # Cambio el signo por que la restricción está en standard form.
        index += 1
        n += 1


def pass_everything_in_f_o_to_left(f_o:dict) -> None:
    """
    <summary>
        Pasa todo lo que esta al lado derecho de la funcion objetivo a la izquierda.
    </summary>
    """
    for k,v in f_o.items():
        if ((k != 'symbol') and (k != 'z')):
            f_o[k] = -v




def is_part_of_equation(k:str):
    """
    <summary>
        Revisa si k es parte de interés para no dividir tipos incompatibles por numeros, cosas como char/num...
    </summary>
    """
    return ((k != 'symbol') and (k != 'z') and (k != 'VB') and (k != 'c') and (k != 'pivot') and (k != 'index'))



def find_minimum_coeficient_of_f_o(f_o:dict) -> int:
    """
    <summary>
        Encuentra el mínimo coheficiente de la función objetivo, esto se vuelve en la columna seleccionada.
    </summary>
    """
    m = {}
    for k,v in f_o.items():
        if ( is_part_of_equation(k) ):
            m.update( {k:v} )
    return min(m, key=lambda k: m[k])



def optimum_reached(f_o:dict, m:bool) -> bool:
    """
    <summary>
        Chequea si hemos llegado a maximizar o minimizar.
    </summary>
    """
    opt = list()
    for k,v in f_o.items():
        # if ( (k != 'pivot') and (k != 'index') and (k != 'symbol') ):
        #     opt.append(v)
        if ( (k[0] == 'a') ):
            opt.append(v)
    if (m):
        if ( 0 <= min(opt) ):
            return True
        return False
    else: 
        if ( min(opt) <= 0 ):
            return True
        return False



def mult_row(row, coef) -> dict:
    """
    <summary>
        Multiplica una fila por el coeficiente dado.
    </summary>
    """
    for k,v in row.items():
        if ( (k != 'symbol') and (k != 'index') and (k != 'pivot') ):
            row[k][0] *= coef
    return row



def div_row(row, coef) -> dict:
    """
    <summary>
        Divide una fila por el coeficiente dado.
    </summary>
    """
    for k,v in row.items():
        if ( (k != 'symbol') and (k != 'index') and (k != 'pivot') ):
            row[k] /= coef
    return row



def make_zero_except_selected(selected, affected, smallest_coef_column_name):
    """
    <summary>
        Se encarga de hacer 0 una fila con otra, pero deja en uno la que se indique ser el smallest_coef
    </summary>
    """
    # selected es la fila que está en uno, affected es lo que queremos hacer cero.
    # row = mult_row(selected, -affected[smallest_coef_column_name])
    # print("selected: ", selected)
    # print("affected: ", affected)
    selected = mult_row(selected, -affected[smallest_coef_column_name])
    # print(selected[smallest_coef_column_name], affected[smallest_coef_column_name])
    for k,v in selected.items():
        if ( (k != 'symbol') and (k != 'VB') and (k != 'index') and (k != 'pivot') ):
            affected[k] += selected[k]
    return affected

def is_actual_variable(string):
    return (string[0] == 'X')

def is_slack_excess_variable(string):
    return (string[0] in ('s', 'e')) and (string != 'symbol')

def is_artifitial_variable(string):
    return (string[0] == 'a')

def make_initial_simplex_table(simplex_table:OrderedDict, constraints: list, f_o:dict):
    """ 
    <summary>

    </summary>
    """
    # Agarrar las variables pertinentes.
    variables = set()
    for i in constraints:
        for k in i.keys():
            variables.add(k)
    for k in f_o.keys():
        variables.add(k)
    
    f_o_var =  set(variables) - set([x for x in f_o.keys()])
    for i in f_o_var:
        f_o.update( {i:0} )
    
    index = 0
    for i in constraints:
        constraints_i = variables - set(i.keys())
        for j in constraints_i:
            constraints[index].update( {j:0} )
        index += 1

    temp = {}
    temp.update( {k:0 for k,v in f_o.items()} )
    for i in constraints:
        temp.update( {k:0 for k,v in i.items()} )
    del temp['symbol']
    
    # Add the actual variables.
    actual_vars = []
    for k,v in temp.items():
        if ( is_actual_variable(k) ):
            actual_vars.append(k)
    actual_vars.sort(key=lambda x: x[1:])
    for i in actual_vars: simplex_table.update( {i:[]} )
    # Add the slack/excess variables.
    s_e_vars = []
    for k,v in temp.items():
        if ( is_slack_excess_variable(k) ):
            s_e_vars.append(k)
    s_e_vars.sort(key=lambda x: x[1:])
    for i in s_e_vars: simplex_table.update( {i:[]} )
    # Add the artifitial variables.
    a_vars = []
    for k,v in temp.items():
        if ( is_artifitial_variable(k) ):
            a_vars.append(k)
    a_vars.sort(key=lambda x: x[1:])
    for i in a_vars: simplex_table.update( {i:[]} )

    # Add the z.
    simplex_table.update( {'z': []} )

    # Add the c.
    simplex_table.update( {'c': []} )
    
    # Copying the information in f_p and constraints to the simplex table:
    for k,v in simplex_table.items():
        simplex_table[k].append(f_o[k])
    for k,v in simplex_table.items():
        for i in range(len(constraints)):
            simplex_table[k].append(constraints[i][k])
    print(dict(simplex_table))
    

    
    
    return simplex_table



def iteration(simplex_table):
    """
    <summary>
        Esta hace la iteración de simplex.
    </summary>
    """
    smallest_coef_column_name = find_minimum_coeficient_of_f_o(simplex_table[0])

    for i in simplex_table:
        try: val = i['c'] / i[smallest_coef_column_name]
        except ZeroDivisionError: val = 0
        # print(i['c'],'/', i[smallest_coef_column_name])
        i['pivot'] = val

    selected_index = min([i for i in simplex_table[1:] if i['pivot'] > 0 and i['c'] > 0], key=lambda k: k['pivot'])
    selected_index = selected_index['index']
    
    # make the rows selected column name 1
    num = simplex_table[selected_index][smallest_coef_column_name]
    simplex_table[selected_index] =  div_row(simplex_table[selected_index], num)
    selected_row = {k:v for k,v in simplex_table[selected_index].items()}
    
    j = 0
    for i in simplex_table:
        if ( j != selected_index ):
            simplex_table[j] = make_zero_except_selected(selected_row.copy(), simplex_table[j], smallest_coef_column_name)
        j += 1
    
    for i in simplex_table:
        i['VB'] = abs(i['c'])

    
    with open("result.txt", mode="a+") as file:
        file.write(f"({smallest_coef_column_name}, {selected_index})" + pretty_print(simplex_table))
        file.close()
        
    return simplex_table



def pretty_print(simplex_table, chars = 20) -> None:
    """
    <summary>
        Permite imprimir la tabla.
    </summary>
    """
    header = [i for i in [x for x in list(simplex_table[0].keys())] if ((i != 'pivot') or (i != 'symbol') or (i != 'index'))]
    s = str()
    s += '\n'
    s += "-"*100
    s += '\n'
    for i in header:
        s += f"|{str(i).center(chars, ' ')}"
    s += "|\n"
    for i in range(len(simplex_table)):
        for ii in header:
            if (isinstance(simplex_table[i][ii], float)):
                s += f"|{str(simplex_table[i][ii])[:chars-2].center(chars, ' ')}"
            else:
                s += f"|{str(simplex_table[i][ii]).center(chars, ' ')}"
        s += "|\n"
    s += "-"*100
    s += '\n'
    return s



def dual(f_o:dict, constraints:list,m1:bool):
    '''
    <summmary>
        Crear un dual basado en el primal.
        Returns -> f_o y constraints del dual. m2 que indica si la dual es minimizacion (False = Min)
    </summary>
    '''
    ## si la primal fuese minimizacion en vez de maximizacion, la dual sera maximizacion 
    if m1 == False:
        m2 = True 
    else:
        m2 = False
        
    new_f_o = {'z':1,'symbol': '='} ## Nueva funcion Objetivo. 
    new_constraints = [] ## Nuevas constraints
    

    # convierte constraints en f_o
    for i in range(len(constraints)):
        new_key = f'x{i+1}' ##cada constraint es una variable distinta
        new_coeficiente = 0  
        for k,v in constraints[i].items():
            if ( k == 'c'):
                new_coeficiente = v
        new_f_o.update({new_key:new_coeficiente})
    
       ## cantidad de constraints
    quantity_of_new_constraints = 0
    for k,v in f_o.items():
        if k != 'z' and k != 'symbol':
            quantity_of_new_constraints+=1
    
    
    # convierte f_o en constraints
    for i in range(quantity_of_new_constraints):
        key_in_constraints = f'x{i+1}' 
        constraint = {}
        for i in range(len(constraints)):
            new_key = f'x{i+1}'
            new_coeficiente = 0 
            new_symbol = '='
            for k,v in constraints[i].items():
                if ( k == key_in_constraints):
                    new_coeficiente = v
                elif ( k == 'symbol'):
                    if ( v == '<=' ):
                        new_symbol = '>='
                    elif ( v == '>=' ):
                        new_symbol = '<='
                    elif ( v == '<' ):
                        new_symbol = '>'
                    elif ( v == '>' ):
                        new_symbol = '<' 
            constraint.update({new_key:new_coeficiente}) ## transversar la matriz de constraints original
        constraint.update({'symbol' : new_symbol})
        constraint.update({'c':f_o[key_in_constraints]}) ## coeficientes de xi de f_o se vuelven 'c'
        new_constraints.append(constraint)
    print(new_f_o,new_constraints,m2)



def main() :
    """
    <summary>
        Punto de entrada al programa.
    </summary>
    """
#     f_o = {'z':1, 'symbol': '=', 'x1': -3,'x2': 1, 'x3': -2}
#     constraints = [
#         {'x1': 1, 'x2':  3, 'x3':  1, 'symbol': '<=', 'c': 5},
#         {'x1': 2, 'x2': -1, 'x3':  1, 'symbol': '>=', 'c': 2},
#         {'x1': 4, 'x2':  3, 'x3': -2, 'symbol': '=', 'c': 5},
#     ]

    f_o = {'z': 1, 'symbol': '=', 'X1': 2, 'X2': 3} ## z se mantiene en 1, para que exista. Representa Utilidades
    constraints = [
        {'X1': 1/2  , 'X2': 1/4, 'symbol': '<=', 'c': 4},
        {'X1': 1    , 'X2': 3  , 'symbol': '>=', 'c': 20},
        {'X1': 1    , 'X2': 1  , 'symbol': '=' , 'c': 10}
    ]
    
    ## True -> Maximizacion; False -> Minimizacion
    m1:bool = False
    big_m: int = 10_000
    # dual(f_o, constraints, m1)
    simplex_table = OrderedDict({})
    
    with open("result.txt", mode="a+") as file:
        file.truncate(0)
        file.close()

    make_inequalities_equalities(constraints=constraints, f_o=f_o, max=m1, big_m=big_m)
    pass_everything_in_f_o_to_left(f_o)
    simplex_table = make_initial_simplex_table(simplex_table, constraints, f_o)
    # for i in simplex_table:
    #     print(i)
    exit()
    while not optimum_reached(simplex_table[0], m1):
        simplex_table = iteration(simplex_table)
        for i in simplex_table:
            print(i)

    
if __name__ == '__main__':
    main()




# def make_initial_simplex_table(f_o:dict, constraints:list) -> list:
#     """
#     <summary>
#         This function makes the initial simplex table.
#         Agrega los slack variables que son 0.
#         Junta los coeficientes de la función objetivo y las condiciones a una misma lista de diccionarios.
#         Agrega llave 'pivot' que permite seleccionar la siguiente fila y columna.
#     </summary>
#     """
#     f_o['VB'] = 0
#     n = 1
#     index = 0
#     for i in constraints:
#         if (i.get(f"s{n}") != None):
#             constraints[index]['VB'] = constraints[index][f"s{n}"] * constraints[index]['c']
#         elif ( i.get(f"e{n}") != None ):
#             constraints[index]['VB'] = constraints[index][f"e{n}"] * constraints[index]['c']
#         index += 1
#         n += 1    
        
#     simplex_table = [f_o] + constraints
#     s = set()
#     for i in simplex_table:
#         for ii in i.keys():
#             s.add(ii)
#     for i in simplex_table:
#         for ii in s:
#             if i.get(ii) == None:
#                 i[ii] = 0
#     for i in simplex_table:
#         i['pivot'] = 0
#     for i in range(len(simplex_table)):
#         simplex_table[i]['index'] = i
#     return simplex_table
