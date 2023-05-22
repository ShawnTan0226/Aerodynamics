''' This code is made to compute the battery size in the wings'''

import numpy as np
'''Inputs'''

A = 6 #Aspect ratio
taper = 0.4 #Ratio tip over chord
b = 40 #winspang [m]
rho = 4 #Battery density [Wh/kg]
epsilon = 4 #Batter density [Wh/m^3]
E  = 40000 # Battery size [Wh]

''' Arifoil Properties '''
S = 40

file_path = "MH 91  14.98%.dat"  # Replace with the path to your .dat file

# Initialize empty arrays
column1 = []
column2 = []

# Read the .dat file
file_path = "MH 91  14.98%.dat"  # Replace with the path to your .dat file

# Initialize empty arrays
column1 = []
column2 = []

# Read the .dat file
with open(file_path, 'r') as file:
    for line in file:
        # Remove leading/trailing whitespaces and split the line by spaces
        data = line.strip().split()
        if len(data) >= 2:  # Ensure the line has at least two columns
            value1 = float(data[0])
            value2 = float(data[1])
            if 0.15 <= value1 <= 0.55:
                column1.append(value1)
                column2.append(value2)

# Print the filtered arrays
print("Filtered Column 1:", column1)
print("Filtered Column 2:", column2)

'''Calculations'''
