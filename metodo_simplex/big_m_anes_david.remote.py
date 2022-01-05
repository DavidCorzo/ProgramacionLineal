#!/usr/bin/env python
# coding: utf-8

# 2]:


from typing import OrderedDict

# ANES MAATENS Y DAVID CORZO

def make_inequalities_equalities(constraints:list, f_o: dict, m1:bool, big_m:int) -> None:
    """
    <summary>
        <args>
            constraints: type list of dictionaries, the dictionaries are the keys and values of the information of the constraints.
            f_o: type dict, keys and values of the information of the objective function.
            m1: type bool, true if max, false if min.
            big_m: type int, a very big number that represents big_m.
        </args>
        This function turns inequalities to equalities using slack variables, excess variables and artificial variables.
        Makes the step 1-4 in the big m.
        If there are no artificial variables the keys will be added with values 0.
        Returns Nothing.
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

    print("before")
    for i in constraints: print(i)

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
            if m1: f_o.update( {f'a{str(n)}': -1 * big_m} ) # Agrego las variables artificiales a la función objetivo.
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
    for i in constraints: print(i)


#  3]:


def pass_everything_in_f_o_to_left(f_o:dict) -> None:
    """
    <summary>
        <args>
            f_o: type dict, keys and values of the information of the objective function.
        </args>
        Pasa todo lo que esta al lado derecho de la funcion objetivo a la izquierda para dejar la constante de la derecha sola. Asume entrada de tipo: z = x1 + x2 + ... + xn -> z - x1 - x2 - ... - xn = 0.
    </summary>
    """
    for k,v in f_o.items():
        if ((k != 'symbol') and (k != 'z')):
            f_o[k] = -v


# 4]:


def is_part_of_equation(k:str):
    """
    <summary>
        <args>
            k: type string, sirve para ver si es parte de la ecuación para así poder ver si se opera o no.
        </args>
        Revisa si k es parte de interés para no dividir tipos incompatibles por numeros, cosas como char/num...
    </summary>
    """
    return (k not in ('symbol', 'z', 'VB', 'c', 'pivot', 'index'))


# 5]:


def find_minimum_coeficient_of_f_o(f_o:dict) -> int:
    """
    <summary>
        <args>
            f_o: type dict, las llaves y valores de la función objetivo.
        </args>
        Encuentra el mínimo coheficiente de la función objetivo, esto se vuelve en la columna seleccionada.
        Returna el máximo del diccionario m compuesto de los valores de f_o.
    </summary>
    """
    m = {}
    for k,v in f_o.items():
        if ( is_part_of_equation(k) ):
            m.update( {k:v} )
    return min(m, key=lambda k: m[k])

def find_maximum_coeficient_of_f_o(f_o:dict) -> int:
    """
    <summary>
        <args>
            f_o: type dict, las llaves y valores de la función objetivo.
        </args>
        Encuentra el máximo coheficiente de la función objetivo, esto se vuelve en la columna seleccionada.
        Returna el máximo del diccionario m compuesto de los valores de f_o.
    """
    m = {}
    for k,v in f_o.items():
        if ( is_part_of_equation(k) ):
            m.update( {k:v} )
    return max(m, key=lambda k: m[k])


# 6]:


def optimum_reached(f_o:dict, m:bool) -> bool:
    """
    <summary>
        <args>
            f_o: type dict, las llaves y valores de la función objetivo.
            m: type boolean, true si es maximizar, false si es minimizar.
        </args>
        Chequea si hemos llegado a una solución o si es necesaria otra iteración de simplex.
        Retorna False si si se necesita otra iteración simplex y True si ya no.
    </summary>
    """
    opt = list()
    for k,v in f_o.items():
        if ( k not in ('pivot', 'index', 'symbol', 'c', 'VB', 'z') ):
            opt.append(v)
    if (m): # Maximización.
        if ( 0 <= min(opt) ):
            print("Optimum reached: ", min(opt), ", c = ", f_o['c'])
            return True
        # print("Optimum not reached yet.", min(opt))
        return False
    else: # Minimización.
        if ( max(opt) <= 0 ):
            print("Optimum reached: ", max(opt), ", c = ", f_o['c'])
            return True
        # print("Optimum not reached yet.", max(opt))
        return False


# 7]:


def mult_row(row:dict, coef:float) -> dict:
    """
    <summary>
        <args>
            row: type dict, una fila de una matriz que se utilizará para multiplicar cada elemento por el coef dado.
            coef: type float, el número por el cual multiplicaremos todos los elementos de row.
        </args>
        Multiplica una fila por el coeficiente dado. Se excluyen llaves puesto a que estas denotan información extra y no son parte de la ecuación.
        Retorna row que es la fila ya multiplicada por el coeficiente.
    </summary>
    """
    for k,v in row.items():
        if ( (k != 'symbol') and (k != 'index') and (k != 'pivot') ):
            row[k] *= coef
    return row


# 8]:


def div_row(row, coef) -> dict:
    """
    <summary>
        <args>
            row: type dict, una fila de una matriz que se utilizará para dividir cada elemento por el coef dado.
            coef: type float, el número por el cual dividiremos todos los elementos de row.
        </args>
        Divide una fila por el coeficiente dado. Se excluyen llaves puesto a que estas denotan información extra y no son parte de la ecuación.
        Retorna row que es la fila ya multiplicada por el coeficiente.
    </summary>
    """
    for k,v in row.items():
        if ( (k != 'symbol') and (k != 'index') and (k != 'pivot') ):
            row[k] /= coef
    return row


# 9]:


def make_zero_except_selected(selected:dict, affected:dict, smallest_coef_column_name:str):
    """
    <summary>
        <args>
            selected: type dict, provee los valores para que se pueda determinar cuánto se necesita para hacer 0 los elementos de la fila 'affected.
            affected: type dict, es la fila en la que se intenta hacer 0.
            smallest_coef_column_name: type str, en esta columna que tiene el coeficiente más pequeño o más grande segun sea el caso (max/min).
        </args>
        Se encarga de hacer 0 una fila con otra, pero deja en uno la que se indique ser el smallest_coef, la columna de smallest_coef quedará en uno. Se excluyen llaves que no son operables de nuevo.
        Retorna la fila afectada.
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


# 10]:


def is_actual_variable(string):
    """
    <summary>
        <args>
            string: type str, ve si la llave es proveida corresponde a ser una variable original (no artificial, ni slack, ni excess).
        </args>
        Ve si la llave proporcionada corresponde a una variable original.
        Retorna true si lo es, false si no lo es.
    </summary>
    """
    return (string[0] == 'X')

def is_slack_excess_variable(string):
    """
    <summary>
        <args>
            string: type str, ve si la llave es proveida corresponde a ser una variable de exceso (no original, no artificial, ni slack).
        </args>
        Ve si la llave proporcionada corresponde a una variable de exceso.
        Retorna true si lo es, false si no lo es.
    </summary>
    """
    return (string[0] in ('s', 'e')) and (string != 'symbol')

def is_artifitial_variable(string):
    """
    <summary>
        <args>
            string: type str, ve si la llave es proveida corresponde a ser una variable de artificial (no original, no exceso, ni slack).
        </args>
        Ve si la llave proporcionada corresponde a una variable de artificial.
        Retorna true si lo es, false si no lo es.
    </summary>
    """
    return (string[0] == 'a')


# 11]:


def make_initial_simplex_table(simplex_table:OrderedDict, constraints: list, f_o:dict, big_m, m1, urs):
    """ 
    <summary>
        <args>
            simplex_table: type OrderedDict, se le ingresa vacío para utilizarlo para hacer la matriz de f_o y constraints.
            constraints: type lista de diccionarios, trae la información de los constraints.
            f_o: type dict, trae la información de la función objetivo.
        </args>
        Crea la simplex table inicial preparando para tener big m.
        Retorna la tabla inicial preparada.
    </summary>
    """
    if (m1): 
        big_m = -big_m

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

    # Add URS vars.
    urs_variables = zip(a_vars, urs)
    print(urs_variables)
    exit()

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

    # {'X1': [-2, 0.5, 1, 1], 'X2': [-3, 0.25, 3, 1], 's1': [0, 1, 0, 0], 'e2': [0, 0, -1, 0], 'a2': [-10000, 0, 1, 0], 'a3': [-10000, 0, 0, 1], 'z': [1, 0, 0, 0], 'c': [0, 4, 20, 10], 'pivot': [0, 0, 0, 0], 'VB': [0, 0, 0, 0], 'index': [0, 1, 2, 3]}

    # Transpose.
    simplex_table_T = [ {} for x in range(len(simplex_table['z'])) ]
    for k,v in simplex_table.items():
        for i in range(len(simplex_table_T)):
            simplex_table_T[i].update( { k:v[i] } )
    
    # new_row:
    print("simplex_table_T: ", simplex_table_T)
    new_row_0 = []
    for i in simplex_table_T:
        contributes_to_new_row = False
        for k,v in i.items():
            if ( (k[0] == 'a') and (v != 0) ):
                contributes_to_new_row = True
        if contributes_to_new_row:
            new_row_0.append(i.copy())
    if (len(new_row_0) == 0):
        new_row_0 = [simplex_table_T[0].copy()]
    
    print("new_row_0", new_row_0)
    new_row = []
    for i in new_row_0:
        is_first_row = False
        for k,v in i.items():
            if ( (k == 'z') and (v == 1) ):
                is_first_row = True
                break

        if is_first_row:
            new_row.append(i)
        else:
            new_row.append(mult_row(i, big_m))

    # Sum all the interesting rows.
    print(new_row)
    new_row_0 = {k:0 for k,v in new_row[0].items()}
    for i in new_row:
        for k,v in i.items():
            new_row_0[k] += v

    # Make artificial letters 0.
    for k,v in new_row_0.items():
        if (k[0] == 'a'):
            new_row_0[k] = 0
    
    # Making the new_row_0 the new zeroth row.
    simplex_table_T[0] = new_row_0

    # Adding pivot column and VB column. Adding an index.
    index = 0
    for i in range(len(simplex_table_T)):
        simplex_table_T[i].update( {'pivot':0} )
        # simplex_table_T[i].update( {'VB':0} )
        simplex_table_T[i].update( {'index': index} )
        index += 1

    # Setting up VB.
    n = 1
    index = 0
    for i in simplex_table_T[1:]:
        if (i.get(f"s{n}") != None):
            simplex_table_T[index]['VB'] = simplex_table_T[index][f"s{n}"]*simplex_table_T[index]['c']
        elif ( i.get(f"e{n}") != None ):
            simplex_table_T[index]['VB'] = simplex_table_T[index][f"e{n}"]*simplex_table_T[index]['c']
        index += 1
        n += 1

    
    return simplex_table_T


# 12]:


def iteration(simplex_table, m1):
    """
    <summary>
        <args>
            simplex_table: OrderedDict type, la tabla simplex ya inicializada.
            m1: true si es maximizar, false si es minimización.
        </args>
        Esta hace la iteración de simplex.
    </summary>
    """    
    if (m1): # False = Min 
        coef_column_name = find_minimum_coeficient_of_f_o(simplex_table[0])
    else:
        coef_column_name = find_maximum_coeficient_of_f_o(simplex_table[0])

    print(coef_column_name)

    for i in simplex_table:
        try: val = i['c'] / i[coef_column_name]
        except ZeroDivisionError: val = float("inf")
        i['pivot'] = val
    
    for i in simplex_table: print(i)
    ## -- !!! pivot es -1 aveces
    print(simplex_table)
    selected_index = min([i for i in simplex_table[1:] if i['pivot'] >= 0 and i[coef_column_name] > 0 ], key=lambda k: k['pivot'])
    selected_index = selected_index['index']
    # print(selected_index)
    # exit()
    
    # make the rows selected column name 1
    num = simplex_table[selected_index][coef_column_name]
    print("Value to divide by: ",num)
    simplex_table[selected_index] =  div_row(simplex_table[selected_index], num)
    selected_row = {k:v for k,v in simplex_table[selected_index].items()}
    
    j = 0
    for i in simplex_table:
        if ( j != selected_index ):
            simplex_table[j] = make_zero_except_selected(selected_row.copy(), simplex_table[j], coef_column_name)
        j += 1
    
    for i in simplex_table:
        i['VB'] = abs(i['c'])

    
    # with open("result.txt", mode="a+") as file:
    #     file.write(f"({coef_column_name}, {selected_index})" + pretty_print(simplex_table))
    #     file.close()
    
    # for i in simplex_table: print(i)
        
    return simplex_table


# 13]:


def pretty_print(simplex_table, chars = 20) -> None:
    """
    <summary>
        <args>
            simplex_table: OrderedDict type, la tabla simplex ya inicializada.
            chars: type int, provee el padding para imprimir la tabla.
        </args>
        Permite imprimir la tabla.
        Retorna la string a imprimir.
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


# 14]:


## Funciones usadas para trabajar con non normal lp
def CheckNormalorNonNormal(constraints:list, urs:list, m1:bool) -> bool:
    '''
    <summmary>
        <args>
            constraints: list. Lista de constraints del primal
            urs: list. Lista de urs del primal
            m1: bool. Si la funcion primal es maximizacion o minimizacion para identificar si sus signos son                normales
        </args>
        Reconoce si el problema es normal o no normal. Se usa en Dual()
        Returns -> Bool: True if Normal, False if not normal
    </summary>
    '''
    normal = True
    for i in range(len(constraints)):
            if (constraints[i]['symbol'] == '=') or (1 in urs) or ((m1 == True) and (constraints[i]['symbol'] == ">=")) or ((m1 == False) and (constraints[i]['symbol'] == "<=")):
                normal = False
    return normal

def BuildNewConstraintsFromEquality(constraint:dict) -> list:
    '''
    <summmary>
        <args>
            constraint: dict. Restriccion con signo "="
        </args>
        Crea constraints >= y <= a base de constraint =
        Returns -> list con restriccion "<=", ">="
    </summary>
    '''
    new_constraint1={}
    new_constraint2={}
    new_constraint1.update(constraint)
    new_constraint2.update(constraint)

    new_constraint1.update({"symbol":"<="})
    new_constraint2.update({"symbol":">="})

    return new_constraint1,new_constraint2


#  ]:


def dual(f_o:dict, constraints:list,urs:list,m1:bool):
    '''
    <summmary>
        <arg>
        f_o: dict -> funcion objetiva primal
        constraints: list -> restricciones primal
        urs: list -> lista de urs de primal
        m1: bool -> si el primal es maximizacion o minimizacion
        </arg>
        Crear un dual basado en el primal.
        Returns -> f_o, constraints y urs del dual; m2 que indica si la dual es minimizacion (False = Min)
    </summary>
    '''
    ## si la primal fuese minimizacion en vez de maximizacion, la dual sera maximizacion 
    if m1 == False:
        m2 = True 
    else:
        m2 = False
        
    new_f_o = {'z':1,'symbol': '='} ## Nueva funcion Objetivo. 
    new_constraints = [] ## Nuevas constraints

    normal = CheckNormalorNonNormal(constraints,urs,m1)

    # convierte constraints en f_o
    biggerthan_constraint = 1
    for i in range(len(constraints)):
        new_key = f'X{i+1}' ##cada constraint es una variable distinta
        new_coeficiente = 0  
        for k,v in constraints[i].items():
            if ( k == 'c'):
                new_coeficiente = v
            if normal == False:
                if ( k == 'symbol'):
                    ## en casos de no normalidad, tambien se multiplica *-1 los coeficientes del nuevo f_o
                    if (v == "<=") and (m1 == False):
                        biggerthan_constraint= -1
                    elif (v == ">=") and (m1 == True):
                        biggerthan_constraint= -1
                    else:
                        biggerthan_constraint = 1
        new_f_o.update({new_key: (new_coeficiente * biggerthan_constraint)})
    
       ## cantidad de constraints
    quantity_of_new_constraints = 0
    for k,v in f_o.items():
        if (k != 'z') and (k != 'symbol'):
            quantity_of_new_constraints+=1
    
    ## CREACION DE RESTRICCIONES DE DUAL
    # convierte f_o en constraints
    if normal == True:
        print("NORMAL")
        new_urs = [0]*len(constraints)
        for i in range(quantity_of_new_constraints):
            key_in_constraints = f'X{i+1}' 
            constraint = {}
            for i in range(len(constraints)):
                new_key = f'X{i+1}'
                new_coeficiente = 0 
                new_symbol = '='
                for k,v in constraints[i].items():
                    if ( k == key_in_constraints):
                        new_coeficiente = v
                if m2 == True:
                    new_symbol = "<="
                elif m2 == False:
                    new_symbol = ">="
                constraint.update({new_key:new_coeficiente}) ## transversar la matriz de constraints original
            constraint.update({'symbol' : new_symbol})
            constraint.update({'c':f_o[key_in_constraints]}) ## coeficientes de xi de f_o se vuelven 'c'
            new_constraints.append(constraint)

    ## SI NO ES NORMAL
    else:
        print("NON NORMAL")
        ##Uso de urs
        new_urs = [0]*len(constraints)
        original_constraints = len(constraints)##mantiene constante el numero de variables de las constraints nuevas
        for i in range(len(constraints)):
            ## identificar cuando existe "=" e identificar nuevos urs
            if constraints[i]['symbol'] == "=":
                new_urs[i] = 1
                # new_constraint1, new_constraint2 = BuildNewConstraintsFromEquality(constraints[i])
                # constraints.remove(constraints[i])
                # constraints.insert(i,new_constraint1)
                # constraints.insert(i,new_constraint2)
        
        for i in range(quantity_of_new_constraints):
            key_in_constraints = f'X{i+1}' 
            constraint = {}
            for i in range(original_constraints):
                print(i)
                new_key = f'X{i+1}'
                new_coeficiente = 0 
                new_symbol = '='
                ##
                print(str(constraints[0].items()))
                for k,v in constraints[i].items():
                    print("k",key_in_constraints)
                    biggerthan_constraint = 1
                    if ( k == key_in_constraints):
                        new_coeficiente = v
                        print(k,v)
                    elif ( k == 'symbol'):
                        if m2 == False:
                            if ( v == '>=' ):
                                new_symbol = '>='
                                ## si es un ">=" constraint, multiplicar por -1 el constraint entero
                                biggerthan_constraint = -1
                            elif ( v == '<=' ):
                                    new_symbol = '>='
                        elif m2 == True:
                            if ( v == '<=' ):
                                new_symbol = '<='
                                ## si es un ">=" constraint, multiplicar por -1 el constraint entero
                                biggerthan_constraint = -1
                            elif ( v == '>=' ):
                                    new_symbol = '<='                     
                    # for i in constraint:
                    #     constraint[i] = mult_row(constraint[i], -1)

                    constraint.update({new_key : (new_coeficiente * biggerthan_constraint) }) ## transversar la matriz de constraints original
                    #print({new_key : (new_coeficiente * biggerthan_constraint) })
            constraint.update({'symbol' : new_symbol})
            constraint.update({'c' : ((f_o[key_in_constraints]) * biggerthan_constraint) }) ## coeficientes de xi de f_o se vuelven 'c'
            new_constraints.append(constraint)
        print("NEW CONSTRAINTS: ",new_constraints)

    return(new_f_o,new_constraints,new_urs,m2)


# 20]:


def main() :
    """
    <summary>
        <args> Nada </args>
        Punto de entrada al programa.
        Retorna Nada.
    </summary>
    """
    # f_o = {'z': 1, 'symbol': '=', 'X1': 2, 'X2': 3} ## z se mantiene en 1, para que exista. Representa Utilidades
    # constraints = [
    #     {'X1':1/2, 'X2':1/4, 'symbol': '<=', 'c': 4}, 
    #     {'X1':1, 'X2':3, 'symbol': '<=', 'c': 20}, 
    #     {'X1':1, 'X2':1, 'symbol': '<=', 'c': 10} 
    # ]
    # urs = [0,0,0]
    # ## True -> Maximizacion; False -> Minimizacion
    # m1:bool = True ## m primal    
    # 1
    # f_o = {'z': 1, 'symbol': '=', 'X1': 2, 'X2': 3, 'X3': 0}
    # constraints = [
    #     {'X1': 2  , 'X2': -1  ,'X3': -1 , 'symbol': '>='    , 'c': 3 },
    #     {'X1': 1  , 'X2': -1  ,'X3':  1 , 'symbol': '>='    , 'c': 2 }
    # ]
    # urs=[0, 0]
    # m1:bool = False ## m primal
    # 2
    # f_o = {'z': 1, 'symbol': '=', 'X1': 5, 'X2': 10, 'X3': 8}
    # constraints = [
    #     {'X1': 3  , 'X2': 5 , 'X3': 2 , 'symbol': '<='    , 'c': 60 },
    #     {'X1': 4  , 'X2': 4 , 'X3': 4 , 'symbol': '<='    , 'c': 72 },
    #     {'X1': 2  , 'X2': 4 , 'X3': 5 , 'symbol': '<='    , 'c': 100 }
    # ]
    # urs=[0, 0, 0]
    # m1:bool = True ## m primal
    # 3
    # f_o = {'z': 1, 'symbol': '=', 'X1': -2, 'X2': -1}
    # constraints = [
    #     {'X1': -3  , 'X2': -1  , 'symbol': '<='    , 'c': -3 },
    #     {'X1': -4  , 'X2': -3  , 'symbol': '<='    , 'c': -6 },
    #     {'X1': -1 , 'X2': -2  , 'symbol': '<='    , 'c': -3 }
    # ]
    # urs=[0, 0]
    # m1:bool = True ## m primal
    # 4 it should not work
    f_o = {'z': 1, 'symbol': '=', 'X1': 5, 'X2': 3}
    constraints = [
        {'X1': 2  , 'X2': 4  , 'symbol': '<='    , 'c': 12 },
        {'X1': 2  , 'X2': 2  , 'symbol': '='    , 'c': 10 },
        {'X1': 5  , 'X2': 2  , 'symbol': '>='    , 'c': 10 }
    ]
    urs=[0, 0]
    m1:bool = False ## m primal
    # # 5
    # f_o = {'z': 1, 'symbol': '=', 'X1': 2, 'X2': 3, 'X3': 0}
    # constraints = [
    #     {'X1': 2  , 'X2': -1  ,'X3': -1 , 'symbol': '>='    , 'c': 3 },
    #     {'X1': 1  , 'X2': -1  ,'X3':  1 , 'symbol': '>='    , 'c': 2 }
    # ]
    # urs=[0, 0,0]
    # m1:bool = False ## m primal
            
    
    big_m: int = 10_000
    print("PRIMAL \n MAX: "+ str(m1) + "\n F_O: " + str(f_o) + "\n Constraints: " + str(constraints) + "\n URS: " + str(urs) + "\n\n")

    ## funcion dual
    dual_f_o, dual_constraints, dual_urs, m2 = dual(f_o.copy(), constraints.copy(), urs.copy(),m1)
    print("DUAL \n MAX: "+ str(m2) + "\n F_O: " + str(dual_f_o) + "\n Constraints: " + str(dual_constraints) + "\n URS: " + str(dual_urs) + "\n\n")
    # with open("result.txt", mode="a+") as file:
    #     file.truncate(0)
    #     file.close()

    print("-"*100)
    make_inequalities_equalities(constraints=constraints, f_o=f_o, m1=m1, big_m=big_m)
    make_inequalities_equalities(constraints=dual_constraints, f_o=dual_f_o, m1=m2, big_m=big_m)
    pass_everything_in_f_o_to_left(f_o)
    pass_everything_in_f_o_to_left(dual_f_o)
    simplex_table = make_initial_simplex_table(OrderedDict(), constraints, f_o, big_m, m1)
    simplex_table_dual = make_initial_simplex_table(OrderedDict(), dual_constraints, dual_f_o, big_m, m2)
    while not optimum_reached(simplex_table[0], m1):
        simplex_table = iteration(simplex_table, m1)
    print("+"*150)
    while not optimum_reached(simplex_table_dual[0], m2):
        simplex_table_dual = iteration(simplex_table_dual, m2)

main()
