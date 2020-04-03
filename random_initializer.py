import numpy as np
import pandas as pd

sz = 64 * 65

Theta1 = np.random.uniform(low=-0.5, high=0.5, size=(sz, 1))
Theta2 = np.random.uniform(low=-0.5, high=0.5, size=(sz, 1))
Theta3 = np.random.uniform(low=-0.5, high=0.5, size=(sz, 1))

Theta = np.concatenate((Theta1, Theta2, Theta3), axis=1)

data_set = pd.DataFrame(Theta, columns=['Theta1', 'Theta2', 'Theta3'])
data_set.to_csv('thetas.csv', index=False)
