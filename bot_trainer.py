import subprocess
import pandas as pd
import numpy as np

# Read weights of all population
Big_Theta = pd.read_csv('thetas.csv')

population_size = 20
sz = 64 * 65

ind = range(64)
score = np.zeros((64,))
i = 0
while i < population_size:
    print('round: ' + str(i/2))
    # Take weights of first player
    red_ind = ind[i]
    Theta = np.array(Big_Theta.iloc[:, red_ind])
    Theta = Theta.reshape((sz, 3))
    data_set = pd.DataFrame(Theta, columns=['Theta1', 'Theta2', 'Theta3'])
    data_set.to_csv('red_thetas.csv', index=False)
    
    i = i + 1
    # Take weights of second player
    blue_ind = ind[i]
    Theta = np.array(Big_Theta.iloc[:, blue_ind])
    Theta = Theta.reshape((sz, 3))
    data_set = pd.DataFrame(Theta, columns=['Theta1', 'Theta2', 'Theta3'])
    data_set.to_csv('blue_thetas.csv', index=False)
    
    i = i + 1;
    # Run the game
    subprocess.run(['python', 'aicontest.py', '1'], stdout=subprocess.DEVNULL)
    
    # Check winner
    with open('winner.txt', 'r') as winner:
        win_num = int(winner.readline())
        
        if (win_num == 0):
            score[red_ind] = score[red_ind] + 1
            # print('Red Won')
        else:
            score[blue_ind] = score[blue_ind] + 1
            # print('Green Won')

print(score)