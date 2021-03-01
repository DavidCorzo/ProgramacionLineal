

class inequality:
    def __init__(self):
        self.lhs:dict = None
        self.rhs:dict = None
        self.symbol:str = None

    def left_hand_side(self, lhs:dict):
        self.lhs = lhs
        return self
    def right_hand_side(self, rhs:dict):
        self.rhs = rhs 
        return self
    def inequality_symbol(self, symbol:str):
        self.symbol = symbol
        return self



