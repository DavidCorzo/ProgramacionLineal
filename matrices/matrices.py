class Matrix:
    def __init__(self, filename, file = False):
        self.n = 0
        self.file = file
        if not file:
            self.n = int(input("Ingrese el número de ecuaciones: "))
        else: 
            with open("data.txt", mode="r") as file:
                self.n = len(file.readlines())
                file.close()
        self.matrix = [None]*self.n
        self.matrix = [([0])*(self.n+1) for x in range(self.n)]
        self.results = [0]*self.n
        self.filename = filename
            
    def populate(self):
        if (file):
            self.populate_from_file()
        else: 
            self.populate_from_console()


    def populate_from_console(self):
        for i in range(self.n):
            for ii in range(self.n + 1):
                self.matrix[i][ii] = float(input(f"[{i}][{ii}]: "))

    def populate_from_file(self):
        """
        <summary>
            The following loads a matrix stored in a file.
            The file is always called "data.txt" this is a constant in the program.
        </summary>
        """
        with open("data.txt", mode="r") as file:
            lines = file.readlines()
            lines = [line.replace('\n','').replace(' ','').split(',') for line in lines]
            i = 0
            while (i < len(self.matrix)):
                ii = 0
                while (ii < len(self.matrix[i])):
                    self.matrix[i][ii] = float(lines[i][ii])
                    ii += 1
                i += 1
            file.close()
        
    def solve(self):
        """
        <summary> 
            The following first sorts the rows in deceding order, 
            then performs gaussian elimination on a list of lists. 
        </summary>
        """
        # print(self.matrix)
        i = 0
        while (i < self.n):
            j = i + 1
            while (j < self.n):
                if ( abs(self.matrix[i][i]) < abs(self.matrix[j][i]) ):
                    k = 0
                    while (k < (self.n + 1)):
                        # swap, decending order: 
                        # Before: [[1.0, 2.0, 3.0, 4.0], [5.0, 6.0, 7.0, 19.0], [3.0, 4.0, 5.0, 2.0]]
                        # After:  [[5.0, 6.0, 7.0, 19.0], [3.0, 4.0, 5.0, 2.0], [1.0, 2.0, 3.0, 4.0]]
                        self.matrix[i][k], self.matrix[j][k] = self.matrix[j][k], self.matrix[i][k]
                        k += 1
                j += 1
            i += 1
        # print(self.matrix)

        # Now for the actual gaussian elimination.
        i = 0
        while (i < (self.n - 1)): # Because we dont want the constants, we want the left vals.
            j = i + 1
            while (j < self.n):
                factor = float(self.matrix[j][i] / self.matrix[i][i])
                k = 0
                while (k < self.n): # multiply the entire row by f.
                    self.matrix[j][k] = self.matrix[j][k] - (factor * self.matrix[i][k])
                    k += 1
                j += 1
            i += 1
        
        i = self.n-1
        while (0 <= i):
            self.results[i] = self.matrix[i][self.n-1]
            j = i + 1
            while (j < self.n):
                if (i != j): # afectando todos menos la diagonal principal.
                    self.results[i] = self.results[i] - (self.matrix[i][j] * self.results[j])
                j += 1
            i -= 1
        
        print(self.results)
        

    def __str__(self):
        s = str()
        for i in range(len(self.matrix)):
            s += f"{i} " + str(self.matrix[i]) + "\n"
        return s

if __name__ == '__main__':
    file = True
    m = Matrix("data.txt", file)
    m.populate()
    m.solve()
    print(m)

