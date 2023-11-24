# -*- coding: utf-8 -*-
"""
Created on Tue Oct 31 14:40:45 2023

@author: shar_sp
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Jun 1 20:19:36 2023

@author: shar_sp
"""

# from __future__ import division


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os
import time
from concurrent.futures import ThreadPoolExecutor  # Import ThreadPoolExecutor

start_time = time.time()

#%%

def B(omega, c_inf, r):
    """
    This function will return the first part of the formula
    """
    B = omega**2. / (16. * np.sqrt(np.pi) * c_inf**4. * r**2.)
    return B

def C(rho, k, l_s, c_a, tau):
    """
    This function will return the integral part of the formula

    Parameters
    ----------
    rho : mean density
    k : turbulent kinetic energy from the fine scales [ARRAY]
    l : length scale [ARRAY]
    c_a : ?
    tau : time scale [ARRAY]
    omega : angular frequency [ARRAY]
    u : mean velocity [ARRAY]
    c : speed of sound

    Returns
    -------
    C

    """
    C = (rho**2. / c_a**2) * (k**2 * l_s**3 / tau)
    return C

def D(omega, l_s, u):
    """
    Parameters
    ----------
    omega : angular frequency [ARRAY]
    l_s : length scale [ARRAY]
    u : mean velocity [ARRAY]

    Returns
    -------
    D.
    """
    D = np.exp((-omega**2. * l_s**2) / (u**2. * 4 * np.log(2)))
    return D

def E(u, c_inf, omega, tau, theta):
    """
    Parameters
    ----------
    u : mean velocity [ARRAY]
    c_inf : speed of sound in ambient condition
    omega : angular frequency [ARRAY]
    tau : time scale [ARRAY]

    Returns
    -------
    E.
    """
    E = (1 + ((1 - ((u / c_inf) * (np.cos(np.deg2rad(theta)))**2)) * omega**2. * tau))
    return E
#%%
# Ask the user for the values of 'r' and 'theta'
D_j = 0.005 # jet exit diameter in m
multiple_of_D_j = float(input("Enter the multiple of jet exit diameter for 'r': "))
r = multiple_of_D_j * D_j  # Calculate 'r' based on the multiple
# r = float(input("Enter the value of 'r' (observer's location in meters): "))
theta = float(input("Enter the value of 'theta' (observer's orientation in degrees from the downstream of the jet axis): "))


# Ask the user for the number of .dat files to read
num_files_to_read = int(input("How many .dat files do you want to process? "))

# Create a list of .dat files in the directory
file_list = sorted([file for file in os.listdir('.') if file.endswith('.dat')], key=lambda x: int(x.split('.')[0]))

# Ensure that num_files_to_read is not greater than the number of available .dat files
num_files_to_read = min(num_files_to_read, len(file_list))

sp_values = []  # Empty list to store sp values
# Initialize an iteration counter
iteration_count = 0

for file in file_list[:num_files_to_read]:
    iteration_count += 1  # Increment the iteration count
    f = open(file, 'r')
    for _ in range(1):
        next(f)  # skip the first row
    df = pd.DataFrame(l.rstrip().split() for l in f)
    df = df.apply(pd.to_numeric, errors='coerce')
    df = df.head(20700)
                

    p_ref = 0.00002 # reference pressure in Pa
    c_inf = 318.14 # speed of sound in ambient air in m/s
    D_j = 0.005 # jet exit diameter in m
    Ma = 0.9
    u = Ma * c_inf
    freq = np.linspace(10,40000,2000) # frequency
    omega = 2.*np.pi*freq # angular frequency
    # r = 30*D_j # observer's location
    # theta = 60 # (degrees) observer's orientation from the downstream of the jet axis
    rho = 1.225 # density of air in kg/m^3
    k = df[7]
    l_s = df[1]
    c_a = 0.9 # source coefficient
    tau = df[5]
    # u = np.linspace(Ma * c_inf,Ma * c_inf/2.5,10700)
    u = 25
    # omega1 = 62.83

    # Outside the integral
    a = (1./(4.*np.log(2.)))**(3./2.)
    # b = B(omega1,c_inf,r)
    

    appended_data = []
    for i in omega:
        appended_data.append(B(i,c_inf,r))
    bh = pd.DataFrame({'0':appended_data})
    
    
        
    # Inside the integral
    c = C(rho,k,l_s,c_a,tau).sum(axis = 0, skipna = True)
    
    appended_data1 = []
    for i in omega:
        appended_data1.append(D(i,l_s,u).sum(axis = 0, skipna = True))
    dh = pd.DataFrame({'0':appended_data1})
    
    
    # d = D(omega1,l_s,u).sum(axis = 0, skipna = True)
    # e = E(u,c_inf,omega1,tau,theta).sum(axis = 0, skipna = True)
    
    appended_data2 = []
    for i in omega:
        appended_data2.append(E(u,c_inf,i,tau,theta).sum(axis = 0, skipna = True))
    eh = pd.DataFrame({'0':appended_data2})
    
    
    # S = a*b*(c*d/e)
    sh = a*bh*(c*dh/(eh*4*np.pi))
    
    sp = 10.*np.log((4*np.pi*sh)/(p_ref**2.*D_j/(Ma * c_inf)))
    st = freq*D_j/(Ma * c_inf)
    
    sp_values.append(sp)  # Append sp value to the list
    print(f"Iteration {iteration_count} is complete.")

print("--- %s seconds ---" % (time.time() - start_time))

#%%
# plt.figure()
# Ask the user for the number of points to skip between data points
skip_interval = int(input("Enter the number of points to skip between data points: "))

plt.figure()
# for sp in sp_values:
#     plt.plot(st,sp,c='grey')
for sp in sp_values:
    plt.plot(st[::skip_interval], sp[::skip_interval], 'ro', markersize=3, alpha=0.02, markeredgecolor='red')
plt.plot(st,np.mean(sp_values, axis=0), 'k--', label='Average')
plt.semilogx()  # Set logarithmic scale on x-axis       
plt.xlabel('Strouhal number $[St]$')
plt.ylabel('Sound Pressure Level $[L_p]$')
# plt.xlim([0.01, .21])
plt.legend()
# plt.ylim([0, 250])
# plt.xlim([0.1, 2])
# plt.title('sp_values Plot')
# plt.legend(range(len(sp_values)))  # Add legend for each sp_values
plt.savefig('SPL_St.pdf', dpi=80)
# plt.show()

plt.rcParams['font.family'] = 'serif'
# plt.rcParams['font.serif'] = ['Computer Modern Roman']
# plt.rcParams['font.serif'] = ['Times New Roman']
plt.rcParams['font.size'] = 11
plt.figure()
csv_file_path = 'C:\\Users\shar_sp\Downloads\Default Dataset.csv'
df = pd.read_csv(csv_file_path)

# Plot the first and second columns
plt.plot(df.iloc[:, 0],df.iloc[:, 1],'b-', label='Experiment')  # Assuming 0-indexed columns
# plt.plot(, label='Column 2')  # Assuming 0-indexed columns
# for sp in sp_values:
#     plt.plot(st,sp,c='grey')
for sp in sp_values:
    plt.plot(freq[::skip_interval], sp[::skip_interval], 'ro', markersize=3, alpha=0.02, markeredgecolor='red')
plt.legend(['All Plots'])    
plt.plot(freq,np.mean(sp_values, axis=0), 'k-', label='Numerical')
plt.semilogx()  # Set logarithmic scale on x-axis       
plt.xlabel('Frequency $[f]$')
plt.ylabel('Sound Pressure Level $[L_p]$')
# plt.xlim([0.01, .21])
plt.legend()
plt.ylim([-10, 60])
plt.xlim([500,20000])
# plt.title('sp_values Plot')
# plt.legend(range(len(sp_values)))  # Add legend for each sp_values
plt.savefig('SPL_freq.pdf', dpi=80)
# plt.show()


