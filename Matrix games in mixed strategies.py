import numpy as np


#Program made to solve matrix games in mixed strategies.
#When a matrix has no solution in pure strategies (a saddle point) we can look for a solution in 
# mixed strategies. 
# This instead gives a mixed strategy for each player p which is a probability distribution
# on the set of pure strategies of player p. 
# That is, for player p with m strategies, the player gets a vector x of
# size m where the sum of the components of the vector is equal to 1 eg x = (0.5,0.5) for m=2.
# So if the matrix game was to be repeated many times this player would chose strategy 1 50% of the time 
# and strategy 2 50% of the time.
#This program will hopefully cover 2x2 matrix formulae, graphical methods for 2 x n and m x 2 sized matrices 
# and column/row domination methods. 
#There will also be pure strategies functionality in this program.

#class for the matrix game
class matrix():
    
    def __init__(self,rows,columns): #to initialize the number of rows and cols and values list
        self.rows = rows
        self.columns = columns

        #self.values = np.array()

    # we are storing the values as a list of rows where each row is also a list
    def get_values(self):

        values = input("Enter the {0} values of row {1}, separated by commas: ".format(self.columns,1))
        row = list(map(int,values.split(",")))
        self.values = np.array(row)

        for i in range(1,self.rows):
            row = []
            values = input("Enter the {0} values of row {1}, separated by commas: ".format(self.columns,i+1))
            row = list(map(int,values.split(",")))
            self.values = np.vstack([self.values,row])        

     #prints the rows of the matrix
    def print_matrix(self):
         for i in range(self.rows):
            print(self.values[i])           
                
      #function to find positions of the row minimums         
    def row_min(self):
        row_mins_list = [] #list to store the position tuples of the row minimums
        final_list = []

        for i in range(self.rows):
            min = self.values[i][0]
            row_mins_list = []
            row_mins_list.append((i,0))
            for j in range(1,self.columns):
                if self.values[i][j] < min:
                    row_mins_list = []
                    min = self.values[i][j]
                    row_mins_list.append((i,j))
                elif self.values[i][j] == min:
                    row_mins_list.append((i,j))    
            for item in row_mins_list:
                final_list.append(item) 

        print("Row minimums at: "+ ",".join(str(tuple(map(operator.add,item,(1,1)))) for item in final_list))
        return final_list               
    
     #function to find positions of the column maximums
    def col_max(self):
       col_max_list = [] #list to store the column maxes
       final_list = []

       for j in range(self.columns):
            max = self.values[0][j]
            col_max_list = []
            col_max_list.append((0,j))
            for i in range(1,self.rows):
                if self.values[i][j] > max:
                    col_max_list = []
                    max = self.values[i][j]
                    col_max_list.append((i,j))
                elif self.values[i][j] == max:
                    col_max_list.append((i,j))  
            for item in col_max_list:
                final_list.append(item)         

       print("Column maximums at: "+ ",".join(str(tuple(map(operator.add,item,(1,1)))) for item in final_list)) 
       return final_list

       #function to find saddle points of the matrix
    def find_saddle_point(self,row_mins_list,col_max_list): 
        #a saddle point is a row min which is also a column max
        #we aim to compare the two lists and find if a saddle point exists
        #a saddle point is a solution to the matrix game
        saddle_point_list = []

        for row_min in row_mins_list:
            if row_min in col_max_list:
                saddle_point_list.append(row_min)

        if len(saddle_point_list) > 0:
          print("Saddle points at: "+ ",".join(str(tuple(map(operator.add,item,(1,1)))) for item in saddle_point_list))  
          self.find_value(saddle_point_list[0])
        else:
            print("The matrix game has no saddle points and therefore has no solution in pure strategies.")  
            return

    #function to find the value of the matrix game ie the value in the position of a saddle point
    def find_value(self,saddle_point):
        r = saddle_point[0]
        s = saddle_point[1]
        value = self.values[r][s]
        print("The value of the game is: " + str(value))

        

#class for the 2x2 matrices
class two_by_two_matrix(matrix):
    def __init__(self):
        self.rows = 2
        self.columns = 2
     
     #input the values of the 2x2 matrix, the parent method still works fine.
    def get_values(self):
        super().get_values()
        self.values.astype(int)
        for i in range(2):
            for j in range(2):
                self.values[i][j] = int(self.values[i][j])
            
     
     #finds the determinant of the matrix
    def determinant(self):
        determinant = (self.values[0][0]*self.values[1][1]) - (self.values[1][0]*self.values[0][1])
        return determinant

     #finds the other relevant value for the matrix, we call it the diagonal.
     #if a matrix game has no solution in pure strategies then the diagonal is non-zero.
    def diagonal(self):
        diagonal = self.values[0][0] + self.values[1][1] - self.values[1][0] - self.values[0][1]
        return diagonal
    
     #this function uses a formula which gives the value of the game. This is strictly for matrices with no saddle points.
    def find_value(self,determinant,diagonal):
        game_value = determinant / diagonal
        print("The value of the game is " + str(game_value))

     #this function uses formula to produce a tuple for the mixed strategies for each player.
     #We will print this out as the transpose of the actual vector for simplicity and readability.
    def strategies(self):
        d = self.diagonal()

        x1 = (self.values[1][1]-self.values[1][0])/d
        x2 = (self.values[0][0]-self.values[0][1])/d

        y1 = (self.values[1][1]-self.values[0][1])/d
        y2 = (self.values[0][0]-self.values[1][0])/d

        x = (x1,x2)
        y = (y1,y2)
        print("The mixed strategy for player 1 is: " + str(x))
        print("The mixed strategy for player 2 is: " + str(y))


game2 = two_by_two_matrix()
game2.get_values()
game2.print_matrix()
game2.find_value(game2.determinant(),game2.diagonal())
game2.strategies()

