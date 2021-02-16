# David Corzo & Anesveth Maatens 

# coeficientes de la función objectivo FO
# pido si estoy maximizando o minimizando
# Cantidad de restricciones.
# Coheficientes de restricciones. Matriz de r*c
# Determinar cantidad de puntos de interés: r*c-#ceros+Comb(#restriccioes, 2)
# determinar cuales del inciso 5 cumplen todas las restricciones.
# verificar el valor de cada candidato en la funcion objetivo.
# De los valores funcionales, quedarme con el máximo o mínimo según sea el case.

from matrix_solve import Matrix
from math import factorial
import numpy as np

def evaluate_polinomial(c_0:float, c_1:float, i:tuple) -> float:
    """
    <summary>
        Lo siguiente evalúa un polinomio dado los coheficientes, se usa para evaluar las 
        restricciones y la función objetivo. c_0 la constante que acompaña a la x, c_1 la 
        que acompaña a la y, i es una tupla (x,y).
    </summary>
    """
    return c_0 * i[0] + c_1 * i[1]
    

def nCr(n, r) -> int:
    """
    <summary>
        Lo siguiente devuelve una combinación dado un input n,r.
    </summary>
    """
    return factorial(n) / factorial(r) / factorial(n - r)

def find_intersections(a:float, b:float, c:float, d:float) -> float:
    """
    <summary>
        Para encontrar la intersección de dos funciones lineales definidas en términos de x dado un input de ax+b=cx+d.
    </summary>
    """
    # si es paralela return none.
    if (a == c) and (b == d):
        return None
        # print("Infinite sols.")
    elif (a == c):
        return None
        # print("X cancel each other out.")
    else:
        return (d-b)/(a-c)


def calcular_vertices_en_ejes(constraints) -> set():
    """
    <summary>
        Para calcular los vertices en los ejes dado un argumento: lista de diccionarios describiendo las restricciones.
    </summary>
    """
    # 'despejar' para y(0). x=0
    vertices = set()
    for i in range(len(constraints)):
        if (constraints[i]['y'] != 0):
            vertices.add(tuple([0,constraints[i]['c']/constraints[i]['y']]))
    for i in range(len(constraints)):
        if (constraints[i]['x'] != 0):
            vertices.add(tuple([constraints[i]['c']/constraints[i]['x'],0]))
    return vertices

def calcular_vertices(constraints) -> set:
    """
    <summary>
        Para calcular los vertices. Dado una lista de diccionarios describiendo las restricciones.
    </summary>
    """
    vertices = set()
    for i in range(len(constraints)):
        if ((constraints[i]['y'] != 1)):
            a = -constraints[i]['x']
            b = constraints[i]['c']
        else:
            a = (-constraints[i]['x']) / constraints[i]['y']
            b = (constraints[i]['c']) / constraints[i]['y']
        for j in range(len(constraints)):
            if (i != j):
                # print("\t"+str(j))
                try:
                    if (constraints[i]['y'] != 1):
                        c = -constraints[j]['x']
                        d = constraints[j]['c']
                    else:
                        c = (-constraints[j]['x']) / constraints[j]['y']
                        d = (constraints[j]['c']) / constraints[j]['y']
                except:
                    c = -constraints[j]['x']
                    d = constraints[j]['c']
                # print(f"a {a} b {b}")
                res_x = find_intersections(a,b,c,d)
                if (res_x != None) and (res_x >= 0):
                    res_y = a*res_x + b # ax + b
                    vertices.add(tuple([res_x, res_y]))
    # print(vertices)
    return vertices


def main() -> None:
    """
    <summary>
        Los siguiente es el main, el punto de entrada al programa.
        Referencia ejemplo 1 en http://www.phpsimplex.com/en/graphical_method_example.htm
    </summary>
    """
    # coheficientes de función objetivo.
    input_everything:bool = False
    if (input_everything):
        c_0, c_1 = float(input("Enter c_0 of th OF (accompanies the x): ")), float(input("Enter c_1 of th OF (accompanies the y): "))
        maximize:bool = bool(int(input("Maximizing? (0,1) ")))
        n: int = int(input("Enter the number of restrictions: "))
        constraints = [None]*n
        for i in range(n):
            constraints[i] = dict()
            print(f"[{i}]:")
            constraints[i]['x'] = float(input("\tEnter the term that accompanies x: "))
            constraints[i]['y'] = float(input("\tEnter the term that accompanies y: "))
            constraints[i]['s'] = input("\tEnter the condition (<=,>=,<,>,=): ")
            constraints[i]['c'] = float(input("\tEnter the constant term: "))
    else: 
        c_0, c_1 = 1, 1 # f(x,y) = 3x + 2y
        # maximizando o minimizando?
        maximize:bool = True
        # numero de restricciones.
        n: int = 3
        # restricciones.
        constraints = [
            # x: EX-Rider, y: Lady-sport
            {'x':  1, 'y': 0, 's': '>=', 'c':  30},
            {'x':  6, 'y': 10, 's': '>=', 'c': 7.5},
            {'x':  1, 'y': 1, 's': '<=', 'c': 100},
        ]
    
    # num restricciones r*c-#ceros+Comb(#restriccioes, 2)
    num_zeros = 0
    for i in range(len(constraints)):
        if (
            (constraints[i]['x'] == 0) or
            (constraints[i]['y'] == 0) or 
            (constraints[i]['c'] == 0)
            ):
            num_zeros += 1
    num_rest:int = len(constraints)*(len(constraints[0])-1) + num_zeros + nCr(n,2)
    # determinar las intersecciones
    # y_1 = 18 - 2x
    # y_2 = 14 - 2/3x
    # y_3 = 24 - 3x
    vertices:set = calcular_vertices(constraints)
    interest_pts = set()
    for i in vertices:
        is_in_feasable_region = True
        for j in range(len(constraints)):
            candidate = evaluate_polinomial(constraints[j]['x'], constraints[j]['y'], i)
            limit  = constraints[j]['c']
            simbol = constraints[j]['s']
            if ( # check all viable options.
                    ((simbol == "<=") and (candidate <= limit)) or 
                    ((simbol == '>=') and (candidate >= limit)) or 
                    ((simbol == '<') and (candidate < limit)) or 
                    ((simbol == '>') and (candidate > limit)) or 
                    ((simbol == '=') and (candidate == limit))
                ):
                continue
            else: 
                is_in_feasable_region = False
                break
        if (is_in_feasable_region): interest_pts.add(i)


    vertices_in_axis = calcular_vertices_en_ejes(constraints)
    interest_pts_in_axis = set()
    vertices_in_axis.add(tuple([0,0]))
    for i in vertices_in_axis:
        is_in_feasable_region = True
        for j in range(len(constraints)):
            candidate = evaluate_polinomial(constraints[j]['x'], constraints[j]['y'], i)
            limit  = constraints[j]['c']
            simbol = constraints[j]['s']
            if ( # check viable options.
                ((simbol == "<=") and (candidate <= limit)) or 
                ((simbol == '>=') and (candidate >= limit)) or 
                ((simbol == '<') and (candidate < limit))   or 
                ((simbol == '>') and (candidate > limit))   or 
                ((simbol == '=') and (candidate == limit))
                ): continue
            else: is_in_feasable_region = False
        if (is_in_feasable_region): interest_pts_in_axis.add(i)
    
    interest_pts = interest_pts.union(interest_pts_in_axis)

    print(interest_pts)

    candidates = dict()
    for i in interest_pts:
        candidates.update({i:evaluate_polinomial(c_0, c_1, i)})
    print(candidates)
    k = list(candidates.keys())
    v = list(candidates.values())
    if (maximize):
        m = max(v)
        i = list(v).index(m)
    else: 
        m = min(v)
        i = list(v).index(m)
    
    print(f"Optimum: {m} with (x,y)={k[i]}")
        
    
if __name__ == "__main__":
    main()
