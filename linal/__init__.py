import math

class Matrix:
    _matrix = None
    _rows = None
    _columns = None

    #constructor
    def __init__(self, array):
        """Takes a 2d array and stores it as the matrix"""
        if type(array[0]) is list:
            self._matrix = array
        elif len(array) == 1:
            self._matrix = [array]
        else:
            raise ValueError("Constructor takes 2d array as argument.")
        
        self._rows = len(self._matrix)
        self._columns = len(self._matrix[0])
    #end constructor

    def from_row(array):
        """Creates a row vector from a 1d array"""
        return Matrix([array])
    #end from_row

    def from_column(array):
        """Creates a column vector from a 1d array"""
        new_matrix = []

        for item in array:
            new_matrix.append([item])

        return Matrix(new_matrix)
    #end from_column

    def augment(self, other):
        """Attaches other to the right side of self and returns a new matrix"""
        if self.rows() != other.rows(): 
            raise ValueError("Other must have the same number of rows.")
        
        new_matrix = self._matrix
        
        for i in range(len(new_matrix)):
            for j in range(other.columns()):
                new_matrix[i].append(other.elem(i,j))
        
        return Matrix(new_matrix)
    #end augment

    def elem(self, i, j):
        """Retrieves the element at i x j from the matrix"""
        return self._matrix[i][j]
    #end elem
    
    def rows(self):
        """Returns the number of rows in the matrix"""
        return self._rows
    #end rows
    
    def columns(self):
        """Returns the number of columns in the matrix"""
        return self._columns
    #end columns

    def swap_row(self, i, j):
        """swaps row i with row j"""
        temp_row = self._matrix[i]
        self._matrix[i] = self._matrix[j]
        self._matrix[j] = temp_row
        return self
    #end swap_row

    def scale_row(self, row, k):
        """scales the row by k"""
        self._matrix[row] = list(map(lambda x: x*k, self._matrix[row]))
        return self
    #end scale_row

    def add_rows(self, source_row, dest_row, k=1):
        """Multiplies source row by k then adds to destination row"""
        self._matrix[dest_row] = list(map(lambda s, d: d+s*k, self._matrix[source_row], self._matrix[dest_row]))
        return self
    #end add_rows
    
    def make_int(self,row):
        """Makes the specified row into integers."""
        for i in range(self.columns()):
            self._matrix[row][i] = int(self._matrix[row][i])
        return self
    #end make_int
    
    def make_int(self):
        """Makes the entire matrix into integers"""
        for i in range(self.rows()):
            for j in range(self.columns()):
                self._matrix[i][j] = int(self._matrix[i][j])
        
        return self
    #end make_int
    
    def get_column(self,col):
        """Returns all numbers in the specified column as a list."""
        column = []
        for row in self._matrix:
            column.append(row[col])
        return column
    #end get_column

    def get_row(self, row):
        """Returns the row as a list"""
        return self._matrix[row]
    #end get_row

    def get_rows(self,start,end):
        return self._matrix[start:end]
    #end get_rows

    def get_columns(self,start,end):
        output = []
        for i in range(start,end):
            output.append(self.get_column(i))
        return output
    #end get_columns

    def gaussian_reduction(self):
        new_matrix = Matrix(self._matrix.copy())
        current_row = 0
        current_column = 0

        while current_column < new_matrix.columns() and current_row < new_matrix.rows():
            working_column = new_matrix.get_column(current_column)[current_row:]

            #skip column if it is already zeroed
            if working_column == [0] * (new_matrix.rows() - current_row):
                current_column += 1
                continue
            
            #swap the top row with one that has a non-zero value in the current column
            for i in range(len(working_column)):
                if working_column[i] != 0:
                    new_matrix.swap_row(current_row + i, current_row)
                    break

            #apply subtractions to lower rows to get zeroes below the new leading 1
            for i in range(current_row + 1, new_matrix.rows()):
                new_matrix.add_rows(current_row, i, -new_matrix.elem(i,current_column)/new_matrix.elem(current_row,current_column))
            
            current_column += 1
            current_row += 1
        #end while

        #scale rows to get leading 1's
        for row in range(new_matrix.rows()):
            for item in new_matrix.get_row(row):
                if item == 0: continue
                elif item != 1: new_matrix.scale_row(row, 1/item)
                break
        #end scale rows
        
        return new_matrix
    #end gaussian reducion

    def gauss_jordan(self):
        new_matrix = self.gaussian_reduction()
        leads  = []
        
        #list locations of leading 1's
        for row in range(new_matrix.rows()):
            for i in range(len(new_matrix.get_row(row))):
                item = new_matrix.elem(row,i)
                if item == 0: continue
                elif item == 1: 
                    leads.append((row,i))
                    break
        #end finding leading 1's

        #reverse order of leading 1's
        leads.reverse()

        #reduce the matrix backwards
        for lead in leads:
            for row in range(lead[0]):
                new_matrix.add_rows(lead[0], row, -new_matrix.elem(row,lead[1])/new_matrix.elem(lead[0],lead[1]))
        
        return new_matrix

    def transpose(self):
        new_matrix = []

        for i in range(self.columns()):
            new_matrix.append(self.get_column(i))
        
        return Matrix(new_matrix)
    #end transpose

    def trace(self):
        if self.rows() != self.columns():
            raise ValueError("Matrix must be square.")
        
        output = 0
        for i in range(self.rows()):
            output += self.elem(i,i)
        
        return output
    #end trace

    def is_invertible(self):
        return (self.rows() == self.columns()) and self.determinant() != 0
    #end is_invertible

    def inverse(self):
        """Returns the inverted matrix"""
        if not self.is_invertible():
            raise ValueError("Matrix is not invertible.")
        
        return self.adjoint() * (1 / self.determinant())
    #end inverse

    def minor(self, row, column):
        """Returns the matrix after removing row and column"""
        new_matrix = []

        for i in range(self.rows()):
            if i == row: continue
            new_matrix.append([])
            for j in range(self.columns()):
                if j == column: continue
                new_matrix[len(new_matrix) - 1].append(self.elem(i, j))
        
        return Matrix(new_matrix)
    #end minor

    def cofactor(self, i, j):
        """Returns the cofactor of row i and column j."""
        return math.pow(-1, i + j) * self.minor(i, j).determinant()
    #end cofactor

    def adjoint(self):
        new_matrix = []

        for i in range(self.rows()):
            new_matrix.append([])
            for j in range(self.columns()):
                new_matrix[i].append(self.cofactor(j, i))
        
        return Matrix(new_matrix)
    #end adjoint

    def determinant(self):
        """Returns the determinant of the matrix by cofactor expansion"""
        if self.rows() != self.columns():
            raise ValueError("Matrix must be square")

        if self.rows() == 1: return self.elem(0, 0)
        
        det = 0

        for i in range(len(self.get_row(0))):
            det += self.elem(0,i) * self.cofactor(0, i)

        return det
    #end determinant

    def zero(val_rows, val_coulmns=None):
        if val_coulmns is None: val_coulmns = val_rows
        if val_rows < 1 or val_coulmns < 1:
            raise ValueError("Dimensions must be 1 or more")
        
        new_matrix = []

        for i in range(val_rows):
            new_matrix.append([])
            for _ in range(val_coulmns):
                new_matrix[i].append(0)
        
        return Matrix(new_matrix)
    #end zero

    def identity(size):
        if size < 1:
            raise ValueError("Size must be 1 or more")
        
        new_matrix = []

        for i in range(size):
            new_matrix.append([])
            for j in range(size):
                new_matrix[i].append(int(i == j))
        
        return Matrix(new_matrix)
    #end identity

    def __add__(self, other):
        """Returns a new matrix that is the sum of the provided matrices"""
        if self.rows() != other.rows() or self.columns() != other.columns():
            raise ValueError("Matrix A and B must have identical dimensions")

        new_matrix = []

        for i in range(self.rows()):
            new_matrix.append([])
            for j in range(self.columns()):
                new_matrix[i].append(self.elem(i,j) + other.elem(i,j))
        
        return Matrix(new_matrix)
    #end __add__

    def __sub__(self, other):
        """Returns a new matrix that is the difference of the provided matrices"""
        if self.rows() != other.rows() or self.columns() != other.columns():
            raise ValueError("Matrix A and B must have identical dimensions")

        new_matrix = []

        for i in range(self.rows()):
            new_matrix.append([])
            for j in range(self.columns()):
                new_matrix[i].append(self.elem(i,j) - other.elem(i,j))
        
        return Matrix(new_matrix)
    #end __sub__

    def __mul__(self, other):
        new_matrix = []

        if type(other) == int or type(other) == float:
            #scalar multiplication
            for i in range(self.rows()):
                new_matrix.append([])
                for j in range(self.columns()):
                    new_matrix[i].append(self.elem(i,j) * other)

            return Matrix(new_matrix)
        elif self.columns() != other.rows(): 
            raise ValueError("Matrix A must have as many columns as Matrix B has rows.")

        #matrix multiplication
        for i in range(self.rows()):
            new_matrix.append([])
            for j in range(other.columns()):
                terms = []
                for k in range(self.columns()):
                    terms.append(self.get_row(i)[k] * other.get_column(j)[k])
                new_matrix[i].append(sum(terms))
        
        return Matrix(new_matrix)
    #end __mul__

    def __eq__(self, other):
        if self.rows() != other.rows() or self.columns() != other.columns():
            return False

        for i in range(self.rows()):
            for j in range(self.columns()):
                if self.elem(i,j) != other.elem(i,j):
                    return False

        return True
    #end __eq__

    def __ne__(self, other):
        return not self == other
    #end __ne__

    def __str__(self):
        output = ""

        for row in self._matrix:
            output += str(row) + "\n"

        return output[:-1]
    #end __str__

    def __repr__(self):
        return str(self._matrix)
    #end __repr__
#end class Matrix

class Vector(Matrix):
    def __init__(self, *vargs):
        super().__init__([list(vargs)])
    # end __init__

    def norm(self):
        result = 0

        for v in self._matrix[0]:
            result += v**2
        
        return math.sqrt(result)
    # end norm

    def unit(self):
        return self * (1/self.norm())
    # end unit

    def __mul__(self, other):
        return super().__mul__(other.transpose())._matrix[0][0]
    #end __mul__

    def angle(self, other):
        return math.acos((self*other)/(self.norm()*other.norm()))
    # end angle
# end class Vector