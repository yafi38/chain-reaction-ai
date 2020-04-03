import numpy as np
import pandas as pd
import sys

class Bot:
    def __init__(self, color):
        self.X = np.random.uniform(0, 1, (65, 1))
        self.X[-1] = 1
        
        self.a1 = np.zeros((65, 1))
        self.a1[-1] = 1
        
        self.a2 = np.zeros((65, 1))
        self.a2[-1] = 1
        
        self.y = np.zeros((64, 1))
        
        Theta = pd.read_csv('thetas.csv')
        self.Theta1 = np.array(Theta[['Theta1']]).reshape((64, 65))
        self.Theta2 = np.array(Theta[['Theta2']]).reshape((64, 65))
        self.Theta3 = np.array(Theta[['Theta3']]).reshape((64, 65))
        
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
        self.X[:-1] = np.array(list(map(self.dict.get, board))).reshape(-1, 1)
        # print(self.X)
        self.a1[:-1] = np.matmul(self.Theta1, self.X)
        self.a1 = self.a1 * (self.a1 > 0)
        
        self.a2[:-1] = np.matmul(self.Theta2, self.a1)
        self.a2 = self.a2 * (self.a2 > 0)
        
        self.y = np.matmul(self.Theta3, self.a2)
        self.y = (1 / (1 + np.exp(-self.y)))
        return np.argmax(self.y)
   
        

# =============================================================================
# grid_size = 8
# temp_grid = []
# for i in range(grid_size):
#     line = input().split(' ')
#     temp_grid.extend(line)
# 
# print(temp_grid)
# 
# my_list = ['No',
# 'No',
# 'G1',
# 'No',
# 'G1',
# 'R1',
# 'No',
# 'G1',
# 'G1',
# 'G1',
# 'R1',
# 'G1',
# 'No',
# 'G1',
# 'R2',
# 'G2',
# 'No',
# 'R1',
# 'G1',
# 'No',
# 'No',
# 'R1',
# 'No',
# 'No',
# 'No',
# 'G1',
# 'G1',
# 'R1',
# 'No',
# 'R1',
# 'G2',
# 'G1',
# 'R1',
# 'R3',
# 'R1',
# 'R1',
# 'No',
# 'G1',
# 'No',
# 'No',
# 'R1',
# 'No',
# 'G1',
# 'No',
# 'G1',
# 'No',
# 'R1',
# 'G2',
# 'G2',
# 'R2',
# 'No',
# 'G1',
# 'G2',
# 'R2',
# 'R1',
# 'No',
# 'No',
# 'R2',
# 'No',
# 'No',
# 'R1',
# 'R1',
# 'No',
# 'No']
# 
# my_bot = Bot('B')
# my_bot.get_move(my_list)
# =============================================================================

my_color = sys.argv[1]
# my_color = 'B'
my_bot = Bot(my_color)
grid_size = 8

log_file = open('my_log.txt', 'w')

is_start = ""
while is_start != "start":
    is_start = input()

while (True):
    board = []
    for i in range(grid_size):
        line = input().strip().split(' ')
        board.extend(line)
        log_file.writelines(line)
      
    move = my_bot.get_move(board)
    x = int(move / 8)
    y = int(move % 8) 
    move = str(x) + ' ' + str(y)
    print(move)
    

    
    
    