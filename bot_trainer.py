import subprocess
import pandas as pd
import numpy as np
import time

total_start = time.time()
# Read weights of all population
Big_Theta = np.array(pd.read_csv('thetas.csv'))

population_size = 64
half_population_size = int(64 / 2)
child_size = population_size - 7

sz = 64 * 65
big_sz = 3 * 64 * 65

total_gens = 10
total_rounds = 6

mutation_chance = 0.2
eps = 0.75

for g in range(total_gens):
    print('Gen %s started' % (g))
    
    # Training
    score = np.zeros((64,))
    ind = range(64)
    start_time = time.time()
    for j in range(total_rounds):
        print('round: ' + str(j))
        i = 0
        while i < population_size:
            print('.', end=' ', flush=True)
            # Take weights of first player
            red_ind = ind[i]
            Theta = Big_Theta[:, red_ind]
            Theta = Theta.reshape((sz, 3))
            data_set = pd.DataFrame(Theta, columns=['Theta1', 'Theta2', 'Theta3'])
            data_set.to_csv('red_thetas.csv', index=False)
            
            i = i + 1
            # Take weights of second player
            blue_ind = ind[i]
            Theta = Big_Theta[:, blue_ind]
            Theta = Theta.reshape((sz, 3))
            data_set = pd.DataFrame(Theta, columns=['Theta1', 'Theta2', 'Theta3'])
            data_set.to_csv('green_thetas.csv', index=False)
            
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
        
        # Sort the index by their position
        ind = np.argsort(score)
        print('')
    
    # Breeding
    
    parents = Big_Theta[:, ind[half_population_size:]]
    
    children = np.zeros((big_sz, child_size))
    
    for c in range(child_size):
        ind1 = np.random.randint(0, half_population_size)
        ind2 = np.random.randint(0, half_population_size)
        
        p1 = parents[:, ind1]
        p2 = parents[:, ind2]
        
        ind_p1 = np.random.choice(big_sz, int(big_sz/2), replace=False)
        ind_p1 = np.sort(ind_p1)
        
        children[:, c] = p2
        children[ind_p1, c] = p1[ind_p1]
        
        rn = np.random.random()
        
        if (rn >= mutation_chance):
            m_val = np.random.uniform(low=-eps, high=eps, size=(big_sz,))
            children[:, c] = children[:, c] + m_val
        
    Big_Theta[:, ind[:child_size]] = children 
    
    end_time = time.time()
    print("Training time %s seconds" % (end_time - start_time))
    print("===================================================================")
    
    # Saving Data of this generation
    df = pd.DataFrame(Big_Theta)
    df.to_csv('new_thetas.csv', index=False)
        
    Fit_Theta = Big_Theta[:, ind[population_size-1]]   
    Fit_Theta = Fit_Theta.reshape((sz, 3))
    data_set = pd.DataFrame(Fit_Theta, columns=['Theta1', 'Theta2', 'Theta3'])
    data_set.to_csv('fit_thetas.csv', index=False)   
    
    print('')
    
    # Letting CPU rest for a while
    time.sleep(10)
    
total_end = time.time()

print("Total time %s seconds" % (total_end - total_start))   
    
    
    
    
    
    
    
    
    
    
    
    
    