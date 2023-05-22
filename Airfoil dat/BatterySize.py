''' This code is made to compute the battery size in the wings'''

import numpy as np
import matplotlib.pyplot as plt
import math
'''Inputs'''

S=32.79364849 #Total Surface
A = 6 #Aspect ratio
b = np.sqrt(S*A) # outer wing wingspan [m]
V_bat  = 400 # Battery Volume [m^3]
V_body = 100 # Battery Volume [m^3]
V_tot = V_bat + V_body #Total Volume [m^3]



taper_outer=0.267354977
sweep_inner=np.rad2deg(38)
sweep_outer=np.rad2deg(38)
b_inner=4
b_outer=b-b_inner

''' Arifoil Properties '''
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

Area_outer= (negative_surface+postive_surface)
Area_inner = Area_outer
print('Expected volume available for bateries : {} m^2 per chord of 1m'.format(S))

def f(x): #In here x is the inner taper ratio
    Cri = 2 * S / ((taper_outer*x+x)*b_outer+(x+1)*b_inner)
    y=-V_tot + 2*Area_inner * (x**2*b_inner/2+0.5*(1-x)*x*b_inner+1/6*(1-x)**2*b_inner)*Cri**2+ \
      2*Area_outer * (taper_outer**2*b_outer/2+0.5*(1-taper_outer)*taper_outer*b_outer+1/6*(1-taper_outer)**2*b_outer)*x**2*Cri**2
    return y
print(f(0.1))


def gradient(f, x, step):
    return (f(x + step) - f(x - step)) / (step * 2)


def newtonRaphson(f, x0, e, N, h, relax):
    print('\n\n*** NEWTON RAPHSON METHOD IMPLEMENTATION ***')
    i = 0
    step = 1
    flag = 1
    condition = True
    while condition:
        # if g(f,x0,h) == 0.0:
        #     print('Divide by zero error!')
        #     break
        print('x0---', x0)
        print('value---', f(x0))
        print('grad---', gradient(f, x0, h))
        x1 = x0 * relax + (x0 - f(x0) / (gradient(f, x0, h))) * (1 - relax)
        # print('Iteration-%d, x1 = %0.6f and f(x1) = %0.6f' % (step, x1, f(x1)))
        x0 = x1
        step = step + 1
        newvalue = f(x1)
        print(newvalue)
        # if g(f,buildingno,x0,h)<0:
        #     x1=x1/relax

        if abs(newvalue) < e:
            condition = False
        if step > N:
            print('\nNot Convergent.')
            flag = 2
            condition = False
        i += 1
        print('x1---', x1)

    if flag == 1:
        print('\nRequired root is: %0.8f' % x1)
        return x0, i
    else:
        print('\nNot Convergent.')
        return 1000, i





