# -*- coding: utf-8 -*-
"""
Created on Mon Aug 28 01:29:44 2023

@author: Familia
"""

# ANALISIS DATOS NUCLEAR

import matplotlib.pyplot as plt
import numpy as np
import scipy.signal
from scipy.optimize import curve_fit
import pandas as pd
import os
from scipy.stats import poisson

# DEFINIO LA FUNCION PARA LOS HISTOGRAMAS LINDOS 

def histograma(y, bins = 10, rango = None, normalizado = False): # en bins se puede pasar una lista con los bins que quiera o un int con la cantidad de bins totales y los separa con el mismo ancho
    Y, bins = np.histogram(y, bins = bins, range = rango, density = False)
    Err = np.sqrt(Y)
    
    # Normalizo
    if normalizado:
        w = np.diff(bins)
        Err = Err / (np.sum(Y * w))
        Y = Y / (np.sum(Y * w))
        
        # Chequeo que el area este normalizada
        area = (sum(Y*w))
        
        #print(f'El area del histograma da {area}')
        
    return Y, bins, Err
#%% ANALIZO LOS DATOS DE LA PRIMERA CLASE

ruta_carpeta = r'C:\Users\C_Gab\Downloads\Labo 5\nuclear'
data1 = pd.read_csv(f'{ruta_carpeta}\\picos_tot_44.csv')
amplit= data1['voltaje'].to_numpy()

#%% SEPARO LOS ARRAYS CADA 10 SEG
n=150
vmin=7

subarrays = np.array_split(amplit, n) #separo los arrays en muchos chicos
lista_final=[]
for i in range(n):# lista parcial la amplitud de foto picos , la lista total tiene el numero de todos los fotopicis de q¿cada sybarray
    lista_parcial=[]
    for j in range(len(subarrays[i])):
        if subarrays[i][j]>vmin:
            lista_parcial.append(subarrays[i][j])
    lista_final.append(len(lista_parcial))
#%%HISTOGRAMA DE PICOS
picos_y=np.array(lista_final)
bines = 40
fonts = 12

frec, bins, err = histograma(picos_y, bins = bines) # la cantidad de bins es para tener un bin por numero
plt.bar(bins[:-1], frec, width = (bins[0]-bins[-1])/(len(bins)-1), align='center',  color='red', edgecolor='black', alpha = 0.6, yerr = err, ecolor = 'black',capsize = 3,  label = f'Cuentas de amplitud')

plt.ylabel(r'Cuentas', fontsize = fonts)
plt.xlabel(r'Numero de picos',fontsize = fonts)
plt.title(r'Distribución de numero de picos ')
plt.grid()
plt.minorticks_on()
plt.grid(which = 'minor',linestyle=':', linewidth='0.1', color='black' )
plt.legend()
            


#%% FILTRO LOS PICOS

xmax, ymax = scipy.signal.find_peaks(data['voltaje'],height = 0.1)
picos_y = ymax['peak_heights']
picos_t = data['tiempo'][xmax]
picos = pd.DataFrame({'t': picos_t , 'y': picos_y})

plt.plot(data['tiempo'], data['voltaje'])

data1['tiempo']+=1

#%% PLOTEO HISTOGRAMA DE AMPLITUDES DE PICOS
bines = 40
fonts = 12

frec, bins, err = histograma(picos_y, bins = bines) # la cantidad de bins es para tener un bin por numero
plt.bar(bins[:-1], frec, width = (bins[0]-bins[-1])/(len(bins)-1), align='center',  color='#0052FF', edgecolor='black', alpha = 0.6, yerr = err, ecolor = 'blue',capsize = 3,  label = f'Cuentas de amplitud')

plt.ylabel(r'Cuentas', fontsize = fonts)
plt.xlabel(r'Amplitud del pico [V]',fontsize = fonts)
plt.title(r'Distribución de amplitudes de los picos ($\propto$ Energia)')
plt.grid()
plt.minorticks_on()
plt.grid(which = 'minor',linestyle=':', linewidth='0.1', color='black' )
plt.legend()


#%% PLOTEO PARA VER LA DISTRIBUCION DE POISSON DE A INTERVALOS DE 0.1 S

i=0
intervalo = 0.1
cuentas = []

while i+ intervalo < max(picos_t):
    cuentas.append(len(picos['t'][(picos['t'] >= i) & (picos['t'] < i+intervalo) ]))
    i+=intervalo

#%% PLOTEO HISTOGRAMA DE POISSON
bines = 10
fonts = 12
x = np.arange(min(cuentas), max(cuentas)+1)

cuentas_prom = np.mean(cuentas)
plt.plot(x, poisson.pmf(x, cuentas_prom), c='red', label = 'Poisson con $\mu=$'+f'{round(cuentas_prom,2)}')

frec, bins, err = histograma(cuentas, bins = bines, normalizado = True) # la cantidad de bins es para tener un bin por numero
plt.bar(bins[:-1], frec, width = (bins[0]-bins[-1])/(len(bins)-1), align='center',  color='#0052FF', edgecolor='black', alpha = 0.6, yerr = err, ecolor = 'blue',capsize = 3,  label = f'Cantidad de eventos')

plt.ylabel(r'Frecuencia', fontsize = fonts)
plt.xlabel(f'Nro de decaimientos en {intervalo}s',fontsize = fonts)
plt.title(f'Distribución de decaimientos en {intervalo}s')
plt.grid()
plt.minorticks_on()
plt.grid(which = 'minor',linestyle=':', linewidth='0.1', color='black' )
plt.legend()


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    