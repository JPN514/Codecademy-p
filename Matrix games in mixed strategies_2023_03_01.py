import numpy as np
import matplotlib.pyplot as plt
import operator 


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
    
    def get_a(self):
        a = self.values[1][1]-self.values[0][1]
        return a
    def get_b(self):
        b = self.values[1][1]-self.values[1][0]
        return b
    def get_alpha(self):
        alpha = self.get_a() / self.diagonal() 
        return alpha
    def get_beta(self):
        beta = self.get_b() / self.diagonal()
        return beta
    
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

class test_matrix_A(two_by_two_matrix):

    def __init__(self):
        super().__init__()
        self.get_values()

    def get_values(self):

        values = "5,0"
        row = list(map(int,values.split(",")))
        self.values = np.array(row)

        for i in range(1,self.rows):
            row = []
            values = "0,1"
            row = list(map(int,values.split(",")))
            self.values = np.vstack([self.values,row])   
        
        self.print_matrix()
        return 
class test_matrix_B(two_by_two_matrix):
        def __init__(self):
            super().__init__()
            self.get_values()

        def get_values(self):

            values = "1,2"
            row = list(map(int,values.split(",")))
            self.values = np.array(row)

            for i in range(1,self.rows):
                row = []
                values = "3,4"
                row = list(map(int,values.split(",")))
                self.values = np.vstack([self.values,row])   
            
            self.print_matrix()
            return 
        
class null_matrix(two_by_two_matrix):
        #class for a null matrix, ie full of 0s.
        #will be 2x2 for now 
        def __init__(self):
                super().__init__()
                self.get_values()

        def get_values(self):

            values = "0,0"
            row = list(map(int,values.split(",")))
            self.values = np.array(row)

            for i in range(1,self.rows):
                row = []
                values = "0,0"
                row = list(map(int,values.split(",")))
                self.values = np.vstack([self.values,row])   
            
            self.print_matrix()
            return 


#Below class will be used to solve the two player bi-matrix game with matrices A and B
#This differs from above as we do not necessarily need A=-B, which is a zero sum matrix game, resulting in one payoff matrix like the above
#We can instead have A<>-B which is a generalisation of the above matrix games, ie each player has their own payoff matrix.
#This will contain methods to solve a 2x2 bi-matrix game graphically using the so-called "Swastika method".
#The aim is to produce the solution of the game in terms of strategies and the value of the game for each player I and II.
#Note we will initialise the two matrices A and B using the classes above and work from there.
class Graphical_Solution_Bi_matrix():
    def __init__(self):
       
        self.A = test_matrix_A() #using test matrices for now
        self.B = test_matrix_B()

        #print("Matrix A: ")
        #self.A.get_values()
        #print("Matrix B: ")
        #self.B.get_values()
        self.A.d = self.A.diagonal()
        self.B.d = self.B.diagonal()
        self.A.a = self.A.get_a()
        self.B.b = self.B.get_b()
        self.A.alpha = self.A.get_alpha()
        self.B.beta = self.B.get_beta()

        print("Matrix A = ")
        self.A.print_matrix()
        print("Matrix B = ")
        self.B.print_matrix()

        return
    
    def print_info(self):
        #to print all relevant conditions and variables, plus what we have calculated
        print("Values for matrix A:")
        print("d(A)={}, a={}, alpha={}".format(self.A.d,self.A.a,self.A.alpha))
        print("Values for matrix B:")
        print("d(B)={}, b={}, beta={}".format(self.B.d,self.B.b,self.B.beta))



    def graph(self):
        #method to set up the graphical solution  
        plt.axis([-0.005,1.005,-0.005,1.005])
        plt.title("Graphical solution(s) for bi-matrix game A,B.")
        plt.xlabel("x")
        plt.ylabel("y",rotation = 0)
        plt.xticks([0,1])
        plt.yticks([0,1])
        self.get_cases_A()
        self.get_cases_B()
        plt.show()

        return

    def get_cases_A(self):
        
        if self.A.d == 0 and self.A.a > 0:
            x = np.linspace(0,1,100)
            plt.vlines(0,0,1,colors='red')
        if self.A.d == 0 and self.A.a < 0:
            x = np.linspace(0,1,100)
            plt.vlines(1,0,1,colors='red')

        if self.A.d > 0:
            if self.A.alpha > 1:
                x = np.linspace(0,1,100)
                plt.vlines(0,0,1,colors='red')
            elif self.A.alpha < 0:
                x = np.linspace(0,1,100)
                plt.vlines(1,0,1,colors='red')
            elif self.A.alpha >= 0 and self.A.alpha <= 1:
                x = np.linspace(0,1,100)
                plt.vlines(1,self.A.alpha,1,colors='red')
                plt.vlines(0,0,self.A.alpha,colors='red')
                plt.hlines(self.A.alpha,0,1,colors='red')   

        if self.A.d < 0:
            if self.A.alpha > 1:
                x = np.linspace(0,1,100)
                plt.vlines(1,0,1,colors='red')
            elif self.A.alpha < 0:
                x = np.linspace(0,1,100)
                plt.vlines(0,0,1,colors='red')
            elif self.A.alpha >= 0 and self.A.alpha <= 1:
                x = np.linspace(0,1,100)
                plt.vlines(0,self.A.alpha,1,colors='red',linewidth=2.5)
                plt.vlines(1,0,self.A.alpha,colors='red',linewidth=2.5)
                plt.hlines(self.A.alpha,0,1,colors='red',linewidth=2.5)     

            return
        
    def get_cases_B(self):
            
            if self.B.d == 0 and self.B.b > 0:
                x = np.linspace(0,1,100)
                plt.hlines(0,0,1,colors='green')
            if self.B.d == 0 and self.B.b < 0:
                x = np.linspace(0,1,100)
                plt.hlines(1,0,1,colors='green')

            if self.B.b > 0:
                if self.B.beta > 1:
                    x = np.linspace(0,1,100)
                    plt.hlines(0,0,1,colors='green')
                elif self.B.beta < 0:
                    x = np.linspace(0,1,100)
                    plt.hlines(1,0,1,colors='green')
                elif self.B.beta >= 0 and self.B.beta <= 1:
                    x = np.linspace(0,1,100)
                    plt.hlines(1,self.B.beta,1,colors='green',linewidth=2.5)
                    plt.hlines(0,0,self.B.beta,colors='green',linewidth=2.5)
                    plt.vlines(self.B.beta,0,1,colors='green',linewidth=2.5)   

            if self.B.d < 0:
                if self.B.beta > 1:
                    x = np.linspace(0,1,100)
                    plt.hlines(1,0,1,colors='green')
                elif self.B.beta < 0:
                    x = np.linspace(0,1,100)
                    plt.hlines(0,0,1,colors='green')
                elif self.B.beta >= 0 and self.B.beta <= 1:
                    x = np.linspace(0,1,100)
                    plt.hlines(0,self.B.beta,1,colors='green')
                    plt.hlines(1,0,self.B.beta,colors='green')
                    plt.vlines(self.B.beta,0,1,colors='green')     

                return
            
    def get_strategies(self):
        #displays the optimal strategies for both players which comes from the values of alpha and beta, or from other intersections on the graphs
        #here ^T is the transpose of the vector
        x_star = []
        y_star = []
        x_star = [self.B.beta,1-self.B.beta]
        y_star = [self.A.alpha,1-self.A.alpha]

        print("Player I: x*=({},{})^T".format(x_star[0],x_star[1]))
        print("Player II: y*=({},{})^T".format(y_star[0],y_star[1]))

        return        
    
    def get_game_value(self):
        #used to return the values of A(x*,y*) and B(x*,y*)
        #these are the values of the matrix games provided there is no solution in pure strategies
        #ie not necessary to have A(x*,y*)=v(A), nor B(x*,y*)=v(B).

        val_A = self.A.determinant() / self.A.d
        val_B = self.B.determinant() / self.B.d

        print("Value of A in mixed strategies A(x*,y*)={}".format(val_A))
        print("Value of B in mixed stratgies B(x*,y*)={}".format(val_B))

        return

class bi_matrix_pure_strategies(matrix):
    #this will look for a solution to the bi-matrix game in pure strategies.
    # That is, a method which looks for a position which is both a column max in A and a row max in matrix B.
    # We will utilise the transpose of B and simplify by looking for a column max in B tranposed, which is equivalent to a row max in B.
    def __init__(self):
        self.A = test_matrix_A()
        self.B = test_matrix_B()
        self.transpose(self.B)
        self.B_T.print_matrix()
        self.find_equilibrium_point() #could be many points 

        return


    def transpose(self,B):
        #to transpose the matrix B
        self.B_T = null_matrix()
        for i in range(len(B.values)):
            for j in range(len(B.values[0])):
                self.B_T.values[j][i] = self.B.values[i][j]

        return
    
    def find_equilibrium_point(self):
        #this will find the column maxes for both A and B transpose

        A_list = self.A.col_max()
        B_list = self.B_T.col_max()
        self.find_saddle_point(A_list,B_list)

        return 
    
    #function to find equilibrium points of the matrix by repurposing the above saddle point function
    def find_saddle_point(self,row_mins_list,col_max_list): 
        #a saddle point is a row min which is also a column max
        #we aim to compare the two lists and find if a saddle point exists
        #a saddle point is a solution to the matrix game
        saddle_point_list = []

        for row_min in row_mins_list:
            if row_min in col_max_list:
                saddle_point_list.append(row_min)

        if len(saddle_point_list) > 0:
          print("Equilibrium points at: "+ ",".join(str(tuple(map(operator.add,item,(1,1)))) for item in saddle_point_list))  
          self.find_value(saddle_point_list[0])
        else:
            print("The matrix game has no saddle points and therefore has no solution in pure strategies.")  
            return

    #function to find the value of the matrix game ie the value in the position of a saddle point
    def find_value(self,saddle_point):
        r = saddle_point[0]
        s = saddle_point[1]
        value = self.A.values[r][s]
        print("The value of A is: " + str(value))
        value = self.B.values[r][s]
        print("The value of B is: " + str(value))
                


    
#game2 = two_by_two_matrix()
#game2.get_values()
#game2.print_matrix()
#game2.find_value(game2.determinant(),game2.diagonal())
#game2.strategies()
#print(game2.get_a(),game2.get_b())
#test_A = test_matrix_A()
#test_B = test_matrix_B()
bimatrix_game1 = Graphical_Solution_Bi_matrix()
bimatrix_game1.print_info()
bimatrix_game1.graph()
bimatrix_game1.get_strategies()
bimatrix_game1.get_game_value()

bi_matrix_pure_strategies()

