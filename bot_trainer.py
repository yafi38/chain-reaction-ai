import subprocess
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time

total_start = time.time()
# Read weights of all population
Big_Theta = np.array(pd.read_csv('thetas.csv'))

population_size = 64
child_size = population_size - 7
parent_size = 8

sz = 64 * 65
big_sz = 2 * 64 * 65

total_gens = 20
total_rounds = 6

mutation_chance = 0.2
mut_genes = int(big_sz / 5)
eps = 0.00390625

def create_child(p1, p2):
    beta = np.random.uniform(low=0, high=1, size=(big_sz,))  
    child = beta * p1 + (1 - beta) * p2
    return child

def mutate_child(child):
    ind_mut = np.random.choice(big_sz, mut_genes, replace=False)
    mut_val = np.random.uniform(low=-eps, high=eps, size=(mut_genes,))
    child[ind_mut] = child[ind_mut] + mut_val
    return child

gs = np.arange(0, total_gens, 1)

std_err = np.zeros((total_gens,))
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
            Red_Theta = Big_Theta[:, red_ind]
            Red_Theta = Red_Theta.reshape((sz, 2))
            data_set = pd.DataFrame(Red_Theta, columns=['Theta1', 'Theta2'])
            data_set.to_csv('red_thetas.csv', index=False)
            
            i = i + 1
            # Take weights of second player
            green_ind = ind[i]
            Green_Theta = Big_Theta[:, green_ind]
            Green_Theta = Green_Theta.reshape((sz, 2))
            data_set = pd.DataFrame(Green_Theta, columns=['Theta1', 'Theta2'])
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
                elif(win_num == 1):
                    score[green_ind] = score[green_ind] + 1
                    # print('Green Won')
                else:
                    print("wait what?")
        
        # Sort the index by their position
        ind = np.argsort(score)
        print('')
    
    # Breeding
    parents = Big_Theta[:, ind[population_size - parent_size:population_size]]
    
    children = np.zeros((big_sz, child_size))
    
    for c in range(child_size):
        ind1 = np.random.randint(0, parent_size)
        ind2 = np.random.randint(0, parent_size)
        while (ind2 == ind1):
            ind2 = np.random.randint(0, parent_size)
        
        p1 = parents[:, ind1]
        p2 = parents[:, ind2]
        
        # ind_p1 = np.random.choice(big_sz, int(big_sz/2), replace=False)
        # ind_p1 = np.sort(ind_p1)
        
        # children[:, c] = p2
        # children[ind_p1, c] = p1[ind_p1]
        
        child = create_child(p1, p2)
        
        # Mutation
        rn = np.random.random()
        if (rn <= mutation_chance):
            child = mutate_child(child)
            
        children[:, c] = child
        
        # if (rn >= mutation_chance):
        #     m_val = np.random.uniform(low=-eps, high=eps, size=(big_sz,))
        #     children[:, c] = children[:, c] + m_val
    
    
    
    Big_Theta[:, ind[:child_size]] = children 
    
    std_err[g] = sum(np.std(parents, axis=1))
    print(std_err[g])
    
    end_time = time.time()
    print("Training time %s seconds" % (end_time - start_time))
    print("===================================================================")
    
    # Saving Data of this generation
    df = pd.DataFrame(Big_Theta)
    df.to_csv('history/new_thetas(6).csv', index=False)
        
    Fit_Theta = Big_Theta[:, ind[population_size-1]]   
    Fit_Theta = Fit_Theta.reshape((sz, 2))
    data_set = pd.DataFrame(Fit_Theta, columns=['Theta1', 'Theta2'])
    data_set.to_csv('history/fit_thetas(6).csv', index=False)   
    
    print('')
    
    # Letting CPU rest for a while
    time.sleep(10)
    
total_end = time.time()

print("Total time %s seconds" % (total_end - total_start))   


plt.plot(gs, std_err)
plt.show()


    
    
    
    
    