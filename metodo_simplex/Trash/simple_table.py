from equation import equation
from const import CONST, F_O_VAR, SLACK_KEY, C_J_KEY, SYMBOL

class SimplexTable:
    def __init__(self, constraints:list, f_o:equation):
        self.f_o = f_o # equation.
        self.constraints = constraints # a list of now equations, previously inequalities.
        self.matrix = []
        self.header = None
        self.numpy_matrix = None
        
    def build_matrix(self) -> None:
        header = [F_O_VAR] + [x for x in self.constraints[0].get_var_names()]
        header = dict([x for x in zip(header, range(len(header)))])


        row = [0] * len(header)
        for k,v in self.f_o.get_everything().items():
            row[header[k]] = v
        self.matrix.append(row)

        row = [0] * len(header)
        for i in self.constraints:
            row = [0] * len(header)
            for k,v in i.get_everything().items(): # i is an equation, i get everything.
                row[header[k]] = v
            self.matrix.append(row)
        print(list(header.keys()))
        for i in self.matrix:
            print(i)
            
    def has_been_optimized(self) -> bool:
        if ( min(self.f_o.values()) > 0 ):
            return True
        return False
        
    def __str__(self) -> str:
        CENTER_CHAR = 10
        # First Line. Header:
        vars = [F_O_VAR] + self.constraints[0].get_var_names()
        COLS = len(vars)
        s = '|' + 'R'.center(CENTER_CHAR, ' ') + '|'
        for i in vars:
            s += i.center(CENTER_CHAR, ' ') + '|'
        s += '\n'
        
        return s

