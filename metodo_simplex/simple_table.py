from const import SLACK_KEY, C_J_KEY, SYMBOL

class SimplexTable:
    def __init__(self, constraints:list, f_o:dict):
        self.constraints = constraints
        self.f_o = f_o
        self.simplex_matrix = [ [None]*(len(f_o[C_J_KEY].keys())+len(f_o[SLACK_KEY].keys())+1) ] * (len(f_o[SLACK_KEY].keys())+2)
        self.simplex_matrix = [ x for x in self.simplex_matrix ]
        self.f_o_coheficients = list(f_o[C_J_KEY].keys()) + list(f_o[SLACK_KEY].keys())
        print(self.f_o_coheficients)

        

