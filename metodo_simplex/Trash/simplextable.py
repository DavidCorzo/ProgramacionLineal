class SimplexTable:
    def __init__(self, f_o, constraints, columnhead, rowhead, equals = [],vb = []):
        self.f_o = f_o
        self.constraints = constraints
        self.columnhead = columnhead
        self.rowhead = rowhead
        self.equals = equals
        self.vb = vb
    
    def PrintTable(self) -> str:
        print ("<<<< TABLE >>>>"+"\n")
        print ("   "+str(self.columnhead))
        for i in range(len(self.rowhead)):
            print (self.rowhead[i])
    
    def FirstRound(self):
        pass
        
    
