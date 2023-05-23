#Libraries
import numpy as np
import matplotlib.pyplot as plt
import math



#Mean aerodynamic chord
def MAC(cr, ct, sweep, b):
    #MAC
    y = 2/3 * (cr + ct - (cr*ct)/(cr+ct))
    #offset from that parts root
    off_x = cr * 0.25 - ct * 0.25 + np.tan(sweep) * b / 2
    off_y =
    return y, off


