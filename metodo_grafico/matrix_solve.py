class Matrix:
    def __init__(self, matrix ):
        self.n = len(matrix) - 1
        self.matrix = [x[:-1] for x in matrix]
        self.results = [x[-1] for x in matrix]  

    def rows(self) -> int:
        return len(self.matrix)

    def cols(self) -> int:
        return len(self.matrix[0])
    
    def num_zeros(self) -> int:
        num_0 = 0
        for i in self.matrix:
            for ii in self.matrix:
                if (ii == 0): num_0 += 1
        return num_0
        
    def gaussian_elimination(self):
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
        # print(self.matrix)
        
        return self

    def print(self):
        s = str()
        for i in range(len(self.matrix)):
            s += f"{' '.join([str(x) for x in self.matrix[i]])} | {self.results[i]}\n"
        print(s)
        return s

if __name__ == "__main__":
    m = Matrix([[1,1,50], [3,1,90]])
    print(m.solve_intersection())

