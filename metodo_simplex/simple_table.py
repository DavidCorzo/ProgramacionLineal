from equation import equation
from const import CONST, F_O_VAR, SLACK_KEY, C_J_KEY, SYMBOL

class SimplexTable:
    def __init__(self, constraints:list, f_o:equation):
        self.f_o = f_o # equation.
        self.constraints = constraints # a list of now equations, previously inequalities.
        self.matrix = [ [None] * (len(self.constraints[0]) + 1) ] * (len(self.constraints) + 1)
        for i in self.matrix:
            print(i)
    
    def has_been_optimized(self) -> bool:
        if ( min(self.f_o.values()) > 0 ):
            return True
        return False

    def choose_column(self) -> int:
        """
        <summary>
            Choose the coheficient of the f_o which is more negative.
        </summary>
        """
        
    def __str__(self) -> str:
        CENTER_CHAR = 10
        # First Line. Header:
        vars = [F_O_VAR] + self.constraints[0].get_var_names()
        print(vars)
        COLS = len(vars)
        s = '|' + 'R'.center(CENTER_CHAR, ' ') + '|'
        for i in vars:
            s += i.center(CENTER_CHAR, ' ') + '|'
        s += '\n'
        # Coefficients of the Objective function.
        s += '|' + '0'.center(CENTER_CHAR, ' ') + '|'
        lhs_coef = self.f_o.get_coehficients_lhs()
        for i in self.f_o.get_coehficients_lhs():
            s += str(i).center(CENTER_CHAR, ' ') + '|'
        rhs_coef = self.f_o.get_coehficients_rhs()
        for i in self.f_o.get_coehficients_rhs():
            s += str(i).center(CENTER_CHAR, ' ') + '|'
        for i in range(COLS-len(lhs_coef)-len(rhs_coef)):
            s += str(i).center(CENTER_CHAR, ' ') + '|'
        # Coefficients of all of the constraints.
        # for i in self.constraints:
        #     print(i)
        s += '\n'
        n = 1
        for j in self.constraints:
            s += '|' + f'{n}'.center(CENTER_CHAR, ' ') 
            s += '|' + '0'.center(CENTER_CHAR, ' ') + '|'
            for i in j.get_coehficients_lhs():
                s += str(i).center(CENTER_CHAR, ' ') + '|'
            for i in j.get_coehficients_rhs():
                s += str(i).center(CENTER_CHAR, ' ') + '|'
            s += '\n'
            n += 1
        return s

