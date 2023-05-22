''' This code is made to compute the battery size in the wings'''

import numpy as np
import matplotlib.pyplot as plt
'''Inputs'''

S=32.79364849
A = 6 #Aspect ratio
taper0 = 0.4 #Ratio tip over chord
b = np.sqrt(S*A) # outer wing wingspan [m]
V  = 40000 # Battery Volume [m^3]


taper_inner=0.4
taper_outer=0.267354977
sweep_inner=np.rad2deg(38)
sweep_outer=np.rad2deg(38)
b_inner=2
b_outer=b-b_inner
''' Arifoil Properties '''

file_path = "MH 91  14.98%.dat"  # Replace with the path to your .dat file

# Initialize empty arrays
column1 = []
column2 = []

# Read the .dat file
file_path = "MH 91  14.98%.dat"  # Replace with the path to your .dat file

# Initialize empty arrays for positive and negative values
positive_column1 = []
positive_column2 = []
negative_column1 = []
negative_column2 = []

# Read the .dat file
with open(file_path, 'r') as file:
    for line in file:
        # Remove leading/trailing whitespaces and split the line by spaces
        data = line.strip().split()
        if len(data) >= 2:  # Ensure the line has at least two columns
            value1 = float(data[0])
            value2 = float(data[1])
            if 0.15 <= value1 <= 0.55:
                if value2 >= 0:
                    positive_column1.append(value1)
                    positive_column2.append(value2)
                else:
                    negative_column1.append(value1)
                    negative_column2.append(value2)

# Print the positive and negative arrays
print("Positive Column 1:", positive_column1)
print("Positive Column 2:", positive_column2)
print("Negative Column 1:", negative_column1)
print("Negative Column 2:", negative_column2)


# Compute the surface using numpy
postive_surface = -np.trapz(positive_column2, positive_column1)
negative_surface = -np.trapz(negative_column2, negative_column1)

# Plot the surface
plt.plot(positive_column1, positive_column2, label='Positive')
plt.plot(negative_column1, negative_column2, label='Negative')
plt.xlabel('Column 1 (X-axis)')
plt.ylabel('Column 2 (Y-axis)')
plt.title('Surface Plot')
plt.grid(True)
ax = plt.gca()
ax.set_aspect('equal', adjustable='box')
plt.draw()
plt.show()

print(negative_surface)
print(postive_surface)

S= (negative_surface+postive_surface)
print('Expected volume available for bateries : {} m^2 per chord of 1m'.format(S))



'''Calculations'''


