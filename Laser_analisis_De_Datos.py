# -*- coding: utf-8 -*-
"""
Created on Fri Nov  3 08:33:29 2023

@author: Familia
"""

import matplotlib.pyplot as plt
import numpy as np
import scipy.signal
from scipy.optimize import curve_fit
import pandas as pd
import os
from scipy.stats import poisson

path = 'C:/Users/Familia/OneDrive/Escritorio/UBA/6to Cuatri/Labo 5/Laser/Clase 2/'
#%%
data = pd.read_csv(path + 'laser.csv', delimiter=';')
data
I_1, W_prom1, W_std1, I_2, W_prom2 ,W_std2, I_B, W_promB, W_stdB = data.T.to_numpy()
#%%
I = np.append(I_1, np.append(I_2, I_B))
I = np.sort(np.unique(I[~np.isnan(I)]))
#%%
plt.plot(I_1, W_prom1,'o--')

plt.plot(I_2, W_prom2,'o--')