from simplextable import SimplexTable

def Inequalities(f_o:dict,constraints:list):
    """
    <summary>
    </summary>
    """
    for k in f_o:
        if (k != 'z'):
            f_o[k] = f_o[k] * -1
    for i in range ( len(constraints) ):
        restriccion = constraints[i]
        i+=1
        if (restriccion['symbol'] == '>=') or (restriccion['symbol'] == '>') or (restriccion['symbol'] == '=>'):
            restriccion['symbol'] = '='
            restriccion[f'e{i}'] = -1
        else:
            restriccion['symbol'] = '='
            restriccion[f's{i}'] = 1

def Setcolumnsandrows(f_o:dict,constraints:list) -> list:
    columns = []
    rows = []
    #f_0 + cantidad de restricciones
    for i in range(len(constraints)+1):
        rows.append(i) 
    
    for k in f_o.keys():
        columns.append(k)

    for r in constraints:
        for k in r.keys():
            if (k in columns) or (k == 'symbol') or (k == 'c'):
                pass
            else:
                columns.append(k)
    return columns,rows

# def Table(columns,rows,constraints):
#     table={}


Max = True

def main():
    f_o = {'z':1, 'symbol': '=', 'A':1,'B':2}
    constraints = [
        {'A':  1,   'B': 4  , 'symbol': '<=', 'c': 21},
        {'A':  2,   'B': 1  , 'symbol': '>=', 'c': 7},
        {'A':  3,   'B': 1.5, 'symbol': '<=', 'c': 21},
        {'A':  -2,  'B': 6  , 'symbol': '>=', 'c': 0},
        # A + B >= 4    | (-1)A - (1)B + (1)S0 + (0)S1 + (0)S2 + (0)S3 = -4
        # 3A + 4B <= 24 | (03)A + (4)B + (0)S0 + (1)S1 + (0)S2 + (0)S3 = 24
        # A >= 2        | (-1)A + (0)B + (0)S0 + (0)S1 + (1)S2 + (0)S3 = -2
        # A - B <= 0    | (01)A - (0)B + (0)S0 + (0)S1 + (0)S2 + 4(1)S3 =  0
    ]
    Inequalities(f_o,constraints)
    print(f_o)
    print(constraints)
    columnhead,rowhead = Setcolumnsandrows(f_o,constraints)
    print ("COLUMNAS"+str(columnhead))     
    print ("ROWS"+str(rowhead))  
    table = SimplexTable(columnhead,rowhead)
    table.PrintTable()
      
    

if __name__ == '__main__':
    main()
