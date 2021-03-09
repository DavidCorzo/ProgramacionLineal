from simple_table import SimplexTable
from const import SLACK_KEY, C_J_KEY, SYMBOL
from typing import Container
from inequality import inequality
from equation import equation

PRINT_ALL = True

def standard_form(f_o:equation, constraints:list):
    i = 0
    for _ in constraints:
        constraints[i] = equation().turn_inequality_to_equality( constraints[i], len(constraints), i )
        i += 1

    f_o.everything_to_lhs()



def main() -> None:
    f_o = equation().left_hand_side( {'z': 1} ).right_hand_side( {'A':1, 'B':2} )
    constraints = [
        inequality().left_hand_side( {'A': 1, 'B': 4} ).inequality_symbol( "<=" ).right_hand_side( {'const':  21} ),
        inequality().left_hand_side( {'A': 2, 'B': 1} ).inequality_symbol( ">=" ).right_hand_side( {'const': 7} ),
        inequality().left_hand_side( {'A': 3, 'B': 1.5} ).inequality_symbol( "<=" ).right_hand_side( {'const':  21} ),
        inequality().left_hand_side( {'A': -2, 'B': 6} ).inequality_symbol( ">=" ).right_hand_side( {'const':  0} ),
    ]
    # usual constraints: y, x >= 0
    standard_form(f_o, constraints)
    simplex_table = SimplexTable(constraints, f_o)
    simplex_table.build_matrix()
    while (True):
        break
        # if (simplex_matrix.has_been_optimized()):
        #     break
        # else:
        #     pass

if __name__ == '__main__':
    main()

