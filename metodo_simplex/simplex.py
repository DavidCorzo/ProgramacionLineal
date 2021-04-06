

def pass_everything_in_f_o_to_left(f_o:dict) -> None:
    for k,v in f_o.items():
        if ((k != 'symbol') and (k != 'z')):
            f_o[k] = -v

def make_inequalities_equalities(constraints:list) -> None:
    n = 1
    index = 0
    for i in constraints:
        if ( i['symbol'] == '=' ):
            continue
        elif ((i['symbol'] == '<=') or (i['symbol'] == '<') or (i['symbol'] == '=<')):
            constraints[index].update( {f's{str(n)}': 1} )
        elif ( (i['symbol'] == '>=') or (i['symbol'] == '>') or (i['symbol'] == '=>') ):
            constraints[index].update( {f'e{str(n)}': -1} )
        constraints[index]['symbol'] = '='
        index += 1
        n += 1

def make_initial_simplex_table(f_o:dict, constraints:list) -> list:
    f_o['VB'] = 0
    n = 1
    index = 0
    for i in constraints:
        if (i.get(f"s{n}") != None):
            constraints[index]['VB'] = constraints[index][f"s{n}"]*constraints[index]['c']
        elif ( i.get(f"e{n}") != None ):
            constraints[index]['VB'] = constraints[index][f"e{n}"]*constraints[index]['c']
        index += 1
        n += 1    
        
    simplex_table = [f_o] + constraints
    s = set()
    for i in simplex_table:
        for ii in i.keys():
            s.add(ii)
    for i in simplex_table:
        for ii in s:
            if i.get(ii) == None:
                i[ii] = 0
    for i in simplex_table:
        i['pivot'] = 0
    for i in range(len(simplex_table)):
        simplex_table[i]['index'] = i
    return simplex_table

def is_part_of_equation(k:str):
    return ((k != 'symbol') and (k != 'z') and (k != 'VB') and (k != 'c') and (k != 'pivot') and (k != 'index'))

def find_minimum_coeficient_of_f_o(f_o:dict) -> int:
    m = {}
    for k,v in f_o.items():
        if ( is_part_of_equation(k) ):
            m.update( {k:v} )
    return min(m, key=lambda k: m[k])

def optimum_reached(f_o:dict) -> bool:
    opt = list()
    for k,v in f_o.items():
        if ( (k != 'pivot') and (k != 'index') and (k != 'symbol') ):
            opt.append(v)

    if ( 0 <= min(opt) ):
        return True
    return False

def mult_row(row, coef) -> dict:
    for k,v in row.items():
        if ( (k != 'symbol') and (k != 'index') and (k != 'pivot') ):
            row[k] *= coef
    return row

def div_row(row, coef) -> dict:
    for k,v in row.items():
        if ( (k != 'symbol') and (k != 'index') and (k != 'pivot') ):
            row[k] /= coef
    return row

def make_zero_except_selected(selected, affected, smallest_coef_column_name):
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

def iteration(simplex_table):
    smallest_coef_column_name = find_minimum_coeficient_of_f_o(simplex_table[0])

    for i in simplex_table:
        try: val = i['c'] / i[smallest_coef_column_name]
        except: val = 0
        # print(i['c'],'/', i[smallest_coef_column_name])
        i['pivot'] = val

    selected_index = min([i for i in simplex_table[1:] if i['pivot'] > 0 and i['c'] > 0], key=lambda k: k['pivot'])
    selected_index = selected_index['index']

    print(f"({smallest_coef_column_name}, {selected_index})")
    
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

    pretty_print(simplex_table)
    return simplex_table

# def iteration_one(simplex_table:list):
#     pass
#     smallest_coef_column_name = find_minimum_coeficient_of_f_o(simplex_table[0])

#     for i in simplex_table[1:]:
#         val = i['c'] / i[smallest_coef_column_name]
#         # if val > 0:
#         #     i['pivot'] = val
#         i['pivot'] = val

#     index = min([i for i in simplex_table[1:] if i['pivot'] > 0], key=lambda k: k['pivot'])
#     index = index['index']
#     # print(index)

#     # Divide the selected column by the pivot. f1 = f1/smallest_coef_column_number
#     smallest_coef_column_number = simplex_table[index][smallest_coef_column_name]
#     for k,v in simplex_table[index].items():
#         if ( (k != 'symbol') and (k != 'VB') and (k != 'index') and (k != 'pivot') ):
#             simplex_table[index][k] = simplex_table[index][k] / smallest_coef_column_number
        
    
#     selected_row = {k:v for k,v in simplex_table[index].items()} # B
    # j = 0
    # for i in simplex_table:
    #     if ( j != index ):
    #         simplex_table[j] = make_zero_except_selected(selected_row.copy(), simplex_table[j], smallest_coef_column_name)
    #     j += 1
#     # for i in simplex_table:
#     #     print(i)
#     pretty_print(simplex_table)
#     return simplex_table


# def iteration(simplex_table:list):
#     for i in range(len(simplex_table)):
#         simplex_table[i]['index'] = i
    
#     smallest_coef_column_name = find_minimum_coeficient_of_f_o(simplex_table[0])

#     for i in simplex_table:
#         val = i['c'] / i[smallest_coef_column_name]
#         i['pivot'] = val

#     index = min([i for i in simplex_table[1:] if i['pivot'] > 0], key=lambda k: k['pivot'])
#     index = index['index']
#     # print(index)

#     # Divide the selected column by the pivot. f1 = f1/smallest_coef_column_number
#     smallest_coef_column_number = simplex_table[index][smallest_coef_column_name]
#     for k,v in simplex_table[index].items():
#         if ( (k != 'symbol') and (k != 'VB') and (k != 'index') and (k != 'pivot') ):
#             simplex_table[index][k] = simplex_table[index][k] / smallest_coef_column_number
        
    
#     selected_row = {k:v for k,v in simplex_table[index].items()} # B
#     j = 0
#     for i in simplex_table:
#         if ( j != index ):
#             simplex_table[j] = make_zero_except_selected(selected_row.copy(), simplex_table[j], smallest_coef_column_name)
#         j += 1
#     # for i in simplex_table:
#     #     print(i)
#     pretty_print(simplex_table)

def pretty_print(simplex_table) -> None:
    header = [x for x in simplex_table[0].keys()]
    print("-"*100)
    for i in header:
        print(f"|{str(i).center(10, ' ')}", end="")
    print("|")
    for i in range(len(simplex_table)):
        for ii in header:
            if (isinstance(simplex_table[i][ii], float)):
                print(f"|{str(simplex_table[i][ii])[:8].center(10, ' ')}", end="")
            else:
                print(f"|{str(simplex_table[i][ii]).center(10, ' ')}", end="")
        print("|")
    print("-"*100)


def main() -> None:
    f_o = {'z':1, 'symbol': '=', 'X1':30, 'X2':35, 'X3':20, 'X4':30, 'X5': 40, 'c': 0}
    constraints = [
        {'X1': 1, 'X2': 1, 'X3': 0, 'X4': 0, 'X5': 0, 'symbol': '=', 'c': 100},
        {'X1': 0, 'X2': 0, 'X3': 1, 'X4': 1, 'X5': 1, 'symbol': '=', 'c': 120},
        {'X1': 1, 'X2': 0, 'X3': 1, 'X4': 0, 'X5': 0, 'symbol': '<', 'c': 130},
        {'X1': 0, 'X2': 1, 'X3': 0, 'X4': 1, 'X5': 0, 'symbol': '<', 'c':  60},
        {'X1': 0, 'X2': 0, 'X3': 0, 'X4': 0, 'X5': 1, 'symbol': '<', 'c': 50},
    ]

    pass_everything_in_f_o_to_left(f_o)
    make_inequalities_equalities(constraints)
    simplex_table = make_initial_simplex_table(f_o, constraints)
    while not optimum_reached(simplex_table[0]):
        simplex_table = iteration(simplex_table)

    
    
if __name__ == '__main__':
    main()
