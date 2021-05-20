NUMERO_DE_PRUEBA = int(input("0 to enter problems, 1-11 to do a problem already entered: "))
        if (NUMERO_DE_PRUEBA == 0):
            f_o, constraints = user_enter_f_o_and_constraints(dict(), list())
        elif (NUMERO_DE_PRUEBA == 1):
            # ejercicio max clase 
            # passa ambos con 8400
            f_o = {'z': 1, 'symbol': '=', 'X1': 3, 'X2': 5}
            constraints = [
                {'X1':  25, 'X2':   50, 'symbol': '<=', 'c': 80_000}, 
                {'X1': 0.5, 'X2': 0.25, 'symbol': '<=', 'c': 700},
                {'X1':   1, 'X2':    0, 'symbol': '<=', 'c': 1_000}
            ]
            m1:bool = True
        elif (NUMERO_DE_PRUEBA == 2):
            # ejemplo min libro
            # pasa ambos con 25
            f_o = {'z': 1, 'symbol': '=', 'X1': 2, 'X2': 3}
            constraints = [
                {'X1': 0.5, 'X2': 0.25, 'symbol': '<=', 'c':  4},
                {'X1':   1, 'X2':    3, 'symbol': '>=', 'c': 20},
                {'X1':   1, 'X2':    1, 'symbol': '=', 'c': 10}
            ]
            m1:bool = False
        elif (NUMERO_DE_PRUEBA == 3):
            # ejemplo max en línea
            # pasa ambos con ~7.50
            f_o = {'z': 1, 'symbol': '=', 'X1': 1, 'X2': 5}
            constraints = [
                {'X1': 3, 'X2': 4, 'symbol': '<=', 'c': 6},
                {'X1': 1, 'X2': 3, 'symbol': '>=', 'c': 2}
            ]
            m1:bool = True
        elif (NUMERO_DE_PRUEBA == 4):
            # ejemplo min 2 libro
            # pasa ambos con 1.0
            f_o = {'z': 1, 'symbol': '=', 'X1': 4, 'X2': 4, 'X3': 1}
            constraints = [
                {'X1': 1, 'X2': 1, 'X3': 1, 'symbol': '<=', 'c': 2},
                {'X1': 2, 'X2': 1, 'X3': 0, 'symbol': '<=', 'c': 3},
                {'X1': 2, 'X2': 1, 'X3': 3, 'symbol': '>=', 'c': 3}
            ]
            m1:bool = False
        elif (NUMERO_DE_PRUEBA == 5):
            # ejemplo min 3 libro
            # pasa ambos con 4.0
            f_o = {'z': 1, 'symbol': '=', 'X1': 2, 'X2': 3}
            constraints = [
                {'X1': 2, 'X2':  1, 'symbol': '>=', 'c':  4},
                {'X1': 1, 'X2': -1, 'symbol': '>=', 'c': -1}
            ]
            m1:bool = False
        elif (NUMERO_DE_PRUEBA == 6):
            # ejemplo max 1 libro 
            # pasa ambos con 5
            f_o = {'z': 1, 'symbol': '=', 'X1': 3, 'X2': 1}
            constraints = [
                {'X1': 1, 'X2': 1, 'symbol': '>=', 'c': 3},
                {'X1': 2, 'X2': 1, 'symbol': '<=', 'c': 4},
                {'X1': 1, 'X2': 1, 'symbol': '=' , 'c': 3}
            ]
            m1:bool = True
        elif (NUMERO_DE_PRUEBA == 7):
            # ejercicio 1 prueba
            # pasa ambos con ~3.33
            f_o = {'z': 1, 'symbol': '=', 'X1': 2, 'X2': 3, 'X3': 0}
            constraints = [
                {'X1': 2, 'X2': -1, 'X3': -1, 'symbol': '>=', 'c': 3},
                {'X1': 1, 'X2': -1, 'X3':  1, 'symbol': '>=', 'c': 2}
            ]
            urs=[0, 0, 0]
            m1:bool = False
        elif (NUMERO_DE_PRUEBA == 8):
            # ejercicio 2 prueba
            # pasa ambos con 160.
            f_o = {'z': 1, 'symbol': '=', 'X1': 5, 'X2': 10, 'X3': 8}
            constraints = [
                {'X1': 3, 'X2': 5, 'X3': 2, 'symbol': '<=', 'c':  60},
                {'X1': 4, 'X2': 4, 'X3': 4, 'symbol': '<=', 'c':  72},
                {'X1': 2, 'X2': 4, 'X3': 5, 'symbol': '<=', 'c': 100}
            ]
            m1:bool = True
        elif (NUMERO_DE_PRUEBA == 9):
            # ejercicio 3 prueba
            # pasa ambas con ~-2.4
            f_o = {'z': 1, 'symbol': '=', 'X1': -2, 'X2': -1}
            constraints = [
                {'X1': -3, 'X2': -1, 'symbol': '<=', 'c': -3},
                {'X1': -4, 'X2': -3, 'symbol': '<=', 'c': -6},
                {'X1': -1, 'X2': -2, 'symbol': '<=', 'c': -3}
            ]
            m1:bool = True
        elif (NUMERO_DE_PRUEBA == 10):
            # ejercicio 4 prueba
            # pasa ambas con 23.
            f_o = {'z': 1, 'symbol': '=', 'X1': 5, 'X2': 3}
            constraints = [
                {'X1': 2, 'X2': 4, 'symbol': '<=', 'c': 12},
                {'X1': 2, 'X2': 2, 'symbol': '=' , 'c': 10},
                {'X1': 5, 'X2': 2, 'symbol': '>=', 'c': 10}
            ]
            m1:bool = False
        elif (NUMERO_DE_PRUEBA == 11):
            # ejercicio 5
            # pasa ambos con 15.
            f_o = {'z': 1, 'symbol': '=', 'X1': 1, 'X2': 2, 'X3': 3, 'X4': -1}
            constraints = [
                {'X1': 1  , 'X2': 2, 'X3': 3, 'X4': 0  , 'symbol': '='    , 'c': 15 },
                {'X1': 2  , 'X2': 1, 'X3': 5, 'X4': 0  , 'symbol': '='    , 'c': 20 },
                {'X1': 1  , 'X2': 2, 'X3': 1, 'X4': 1  , 'symbol': '='    , 'c': 10 }
            ]
            m1:bool = True
