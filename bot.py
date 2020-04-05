import numpy as np
import pandas as pd
import sys


class Bot:
    def __init__(self, color):
        # self.cost = 0
        # self.moves = 0
        
        # Theta = pd.read_csv('fit_thetas.csv')
        if (color == 'R'):    
            Theta = pd.read_csv('red_thetas.csv')
            self.log_file = open('red_log.txt', 'w')
        else:
            Theta = pd.read_csv('green_thetas.csv')
            self.log_file = open('green_log.txt', 'w')
   
        self.Theta1 = np.array(Theta[['Theta1']]).reshape((64, 65))
        self.Theta2 = np.array(Theta[['Theta2']]).reshape((64, 65))
        # self.Theta3 = np.array(Theta[['Theta3']]).reshape((64, 65))
        
        if(color == 'R'):
            self.dict = {
                'R3': 3,
                'R2': 2,
                'R1': 1,
                'No': 0,
                'G1': -1,
                'G2': -2,
                'G3': -3
            }
        else:
            self.dict = {
                'R3': -3,
                'R2': -2,
                'R1': -1,
                'No': 0,
                'G1': 1,
                'G2': 2,
                'G3': 3
            }

    def get_move(self, board):
        X = np.zeros((65, 1))
        X[-1] = 1
        X[:-1] = np.array(list(map(self.dict.get, board))).reshape(-1, 1)
        # print(self.X)
        a1 = np.zeros((65, 1))
        a1[-1] = 1
        
        a1[:-1] = np.matmul(self.Theta1, X)
        a1 = a1 * (a1 > 0)
        
        # a2 = np.zeros((65, 1))
        # a2[-1] = 1
        
        # a2[:-1] = np.matmul(self.Theta2, a1)
        # a2 = a2 * (a2 > 0)
        
        y = np.matmul(self.Theta2, a1)
        my_move = np.argmax(y)
        
        cost = self.move_cost(X, y)
        # self.moves = self.moves + 1
        
        self.log_file.write(str(cost))
        self.log_file.write('\n')
        self.log_file.flush()
        
        return my_move
    
    def move_cost(self, X, y):
        y = np.exp(y)
        sm = np.sum(y)
        y /= sm
        
        ind_zero = X[:-1] >= 0
        y[ind_zero] = 0
        
        y = np.log(1 - y)
        sm = -np.sum(y)
        return sm
   

my_color = sys.argv[1]
# my_color = 'B'
my_bot = Bot(my_color)
grid_size = 8

# log_file = open('my_log.txt', 'w')

is_start = ""
while is_start != "start":
    is_start = input()

while (True):
    board = []
    try:
        for i in range(grid_size):
            line = input().strip().split(' ')
            board.extend(line)
            # log_file.writelines(line)
      
        move = my_bot.get_move(board)
        x = int(move / 8)
        y = int(move % 8) 
        move = str(x) + ' ' + str(y)
        print(move)
    except EOFError:
        sys.exit(0)
        