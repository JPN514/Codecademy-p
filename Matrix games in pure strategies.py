import numpy as np
import operator
#tuple(map(operator.add, a, b))

#Python program to find solution to 2 player matrix games in pure strategies.
#The aim is to find the positions (i,j) row minimums and column maximums in the matrix and see if any 
# position is both a row min and column max, which is called a saddle point, this is a solution to the matrix game.
#Note that the matrix game has a solution in pure strategies if and only if there exists a saddle point.
#Once the saddle point (r,s) is found this means that row r is player 1's optimal strategy and column s
# is player 2's optimal strategy.
#The value of the matrix game is then the number found at the position of the saddle point.
#We note that matrices can have more than one saddle point, although the value found at each saddle point will be the same
# and hence the value of the game is unchanged by the presence of multiple saddle points. Essentially, this means a player/players
# could have more than one optimal strategy.

#class for the matrix game
class matrix():
    
    def __init__(self,rows,columns): #to initialize the number of rows and cols and values list
        self.rows = rows
        self.columns = columns

        #self.values = np.array()

    # we are storing the values as a list of rows where each row is also a list
    def get_values(self):

        values = input("Enter the {0} values of row {1}, separated by commas: ".format(self.columns,1))
        row = (values.split(","))
        self.values = np.array(row)

        for i in range(1,self.rows):
            row = []
            values = input("Enter the {0} values of row {1}, separated by commas: ".format(self.columns,i+1))
            row = (values.split(","))
            self.values = np.vstack([self.values,row]) 

        self.convert_to_int()    

     #converts the input string values to integers
    def convert_to_int(self):
        for lst in self.values:
            for item in lst:
                item = int(item)

     #prints the rows of the matrix
    def print_matrix(self):
        #self.convert_to_int()

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


#loop to run the program allowing user to enter multiple matrix games.
answer = ""

while answer != "N":

    rows = int(input("Enter the number of rows in the matrix: "))
    columns = int(input("Enter the number of columns in the matrix: "))

    game1 = matrix(rows,columns)
    game1.get_values()
    game1.print_matrix()

    list_row_mins = game1.row_min() 
    list_col_maxes = game1.col_max()

    game1.find_saddle_point(list_row_mins,list_col_maxes)

    del game1
    answer = input("\n Do you want to enter another matrix game? (Y/N): ")
print("Program ended.")