from const import CONST
from inequality import inequality


class equation:
    def __init__(self):
        self.lhs:dict = None
        self.rhs:dict = None
        self.lhs_slack_vars:dict = None
        self.symbol:str = '='

    def left_hand_side(self, lhs:dict):
        self.lhs = lhs
        return self
    def right_hand_side(self, rhs:dict):
        self.rhs = rhs 
        return self
    
    def is_in_standard_form(self):
        items = list(self.lhs.items())
        if ( ( len(items) == 1) and ( items[0] == CONST ) ):
            return True
        return False

    def get_lhs(self) -> dict:
        d = {}
        d.update(self.lhs)
        if (self.lhs_slack_vars != None):
            d.update(self.lhs_slack_vars)
        return d
    
    def get_rhs(self) -> dict:
        return self.rhs
        
    def get_var_names(self) -> list:
        vars = [x for x in self.lhs.keys()]
        if (self.lhs_slack_vars != None):
            vars += [x for x in self.lhs_slack_vars.keys()]
        vars += [x for x in self.rhs.keys()]
        return vars
        
    def turn_inequality_to_equality(self, inequality_wo_s:inequality, num_of_constraints:int, n:int):
        """
        <summary>
            This method turns an inequality object into an equality object using slack
            variables. It adds 's' if the constraint is of type '<' or '<=' and 'e' if the 
            constraint is of type '>' and '>='.
        </summary>
        """
        self.lhs = inequality_wo_s.lhs # left hand side is equal.
        self.lhs_slack_vars = {}
        for i in range(num_of_constraints):
            if ( i == n ):
                if ( (inequality_wo_s.symbol == '>=') or (inequality_wo_s.symbol == '>') or (inequality_wo_s.symbol == '=>') ):
                    self.lhs_slack_vars[f"e{i}"] = -1
                else:
                    self.lhs_slack_vars[f"s{i}"] = 1
            else: self.lhs_slack_vars[f"s{i}"] = 0
        self.symbol = '='
        self.rhs = inequality_wo_s.rhs
        return self

    def everything_to_lhs(self) -> None:
        self.lhs = {k:v for (k,v) in self.lhs.items() if ((k != CONST) and (v != 0))}
        self.rhs = {k:v for (k,v) in self.rhs.items() if ((k != CONST) and (v != 0))}
        for k,v in self.rhs.items():
            self.lhs.update({k:-v})
        self.rhs = {CONST:0}

    def everything_to_rhs(self) -> None:
        self.lhs = {k:v for (k,v) in self.lhs.items() if ((k != CONST) and (v != 0))}
        self.rhs = {k:v for (k,v) in self.rhs.items() if ((k != CONST) and (v != 0))}
        for k,v in self.lhs.items():
            self.rhs.update({k:-v})
        self.lhs = {CONST:0}
    
    def __str__(self) -> str:
        left = ""
        l = 0
        CHARS = 6
        for i in self.lhs.items():
            if (l != len(self.lhs.items()) - 1):
                if (i[0] != CONST):
                    left += ("(" + str(i[1]) + ")").center(CHARS,' ') + str(i[0]) + " + "
                else: left += str(i[1])
            else: 
                if (i[0] != CONST):
                    left += ("(" + str(i[1]) + ")").center(CHARS,' ') + str(i[0])
                else: left += str(i[1])
            l += 1
        l = 0
        if (self.lhs_slack_vars != None):
            left += " + "
            for i in self.lhs_slack_vars.items():
                if (l != len(self.lhs_slack_vars) - 1): 
                    left += ("(" + str(i[1]) + ")").center(CHARS,' ') + str(i[0]) + " + "
                else:
                    left += ("(" + str(i[1]) + ")").center(CHARS,' ') + str(i[0])
                l += 1
        right = ""
        l = 0
        for i in self.rhs.items():
            if (l != len(self.rhs.items()) - 1):
                if (i[0] != CONST):
                    right += ("(" + str(i[1]) + ")").center(CHARS,' ') + str(i[0]) + " + "
                else: right += str(i[1])
            else: 
                if (i[0] != CONST):
                    right += ("(" + str(i[1]) + ")").center(CHARS) + str(i[0])
                else: right += str(i[1])
            l += 1
        return f"{left} {self.symbol} {right}"

    def __len__(self) -> int:
        return len(self.lhs) + len(self.lhs_slack_vars) + len(self.rhs)
