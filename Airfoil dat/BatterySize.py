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
S = 40m2
'''Calculations'''
Volume