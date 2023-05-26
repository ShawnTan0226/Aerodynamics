import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from scipy.interpolate import interp1d

class Plane:
    def __init__(self,Cri,taper,sweep,b,h=5000,V=110,airfoil=".\Airfoil_dat\MH 91  14.98%.dat"):
        self.c=np.array([Cri])
        self.taper = np.array(taper)
        self.sweep = np.array(np.deg2rad(sweep))
        self.b = np.concatenate(([0],b))
        self.coords=np.array([])
        self.S_list=np.array([])
        self.V=V
        self.h=h

        self.draw()
        self.MAC_aircraft()
        self.define_airfoil(airfoil)
        self.aerodynamic_properties()

    def draw(self):
        self.offset=np.array([0])
        count=0
        for i in self.taper:
            self.c=np.concatenate((self.c, [i*self.c[-1]]))
            nextoffset=self.offset[-1]+np.tan(self.sweep[count])*(self.b[count+1]-self.b[count])/2+0.25*self.c[-2]-0.25*self.c[-1]
            self.offset=np.concatenate((self.offset, [nextoffset]))
            self.S_list=np.concatenate((self.S_list,[(self.c[-1]+self.c[-2])/2*(self.b[count+1]-self.b[count])]))
            count+=1
        
        self.S=np.sum(self.S_list)
        self.coords_bot=self.offset+self.c
        self.coords=np.concatenate((self.coords,self.offset,self.coords_bot[::-1]))
        self.coords=np.concatenate((self.coords,self.coords[::-1]))
        negative=np.concatenate((-self.b,-self.b[::-1]))[::-1]


        self.bfull=np.concatenate((self.b,self.b[::-1],negative))

    def plot_plane(self):
        plt.plot(self.bfull,self.coords)
        plt.gca().invert_yaxis()
        plt.show()

    def xflrvelues(self):
        xflr={}
        xflr['c']=self.c
        xflr['b']=self.b
        xflr['offset']=self.offset
        print('c: ',self.c)
        print('b: ',self.b)
        print('offset: ',self.offset)
        return xflr
    def drawbox(self,opacity):
        frontbox=self.offset+0.15*self.c
        backbox=self.offset+0.65*self.c
        x_store=np.concatenate((frontbox,backbox[::-1]))
        x_store=np.concatenate((x_store,x_store[::-1]))
        y=np.concatenate((self.b,self.b[::-1]))
        y=np.concatenate((y,-y[::-1]))

        x_red=np.concatenate((self.offset,frontbox[::-1]))
        x_red=np.concatenate((x_red,x_red[::-1]))

        x_red2=np.concatenate((self.offset+self.c,backbox[::-1]))
        x_red2=np.concatenate((x_red2,x_red2[::-1]))

        plt.plot(self.bfull,self.coords, color='black')
        plt.gca().invert_yaxis()
        plt.fill(y,x_store, color='blue', alpha=opacity, label='Battery')
        plt.fill(y,x_red, color='orange', alpha=opacity)
        plt.fill(y,x_red2, color='orange', alpha=opacity)
        plt.show()

    def drawtail(self,opacity):
        x_front=self.offset[-2:]
        x_back=self.coords_bot[-2:]
        x=np.concatenate((x_front,x_back[::-1]))
        y=np.concatenate((self.b[-2:],self.b[-2:][::-1]))
        negy=-y

        plt.plot(self.bfull,self.coords, color='black')
        plt.plot([self.b[-2],self.b[-2]],[self.offset[-2],self.coords_bot[-2]],  color='black')
        plt.plot([-self.b[-2],-self.b[-2]],[self.offset[-2],self.coords_bot[-2]],  color='black')

        plt.gca().invert_yaxis()
        plt.fill(self.bfull,self.coords, color='blue', alpha=opacity)
        plt.fill(y,x, color='orange', alpha=1)
        plt.fill(negy,x, color='orange', alpha=1)
        plt.show()
        
    def MAC_part(self,cr, ct, sweep, b):
        #MAC
        y = 2/3 * (cr + ct - (cr*ct)/(cr+ct))
        #offset from that parts root on quarter chord
        off_x = -(b/2/(ct-cr))*(y-ct)
        off_y = cr*0.25-ct*0.25 + np.tan(sweep)*off_x
        return y, off_x, off_y

    def listgenerator(self):
        self.MAC_list=np.array([])
        self.x_list=np.array([])
        for i in range(len(self.taper)):
            part= self.MAC_part(self.c[i],self.c[i+1],self.sweep[i],self.b[i+1])
            self.MAC_list=np.concatenate((self.MAC_list,[part[0]]))
            self.x_list=np.concatenate((self.x_list,[part[1]]))

    def MAC_aircraft(self):#Make sure to use numpy array
        self.listgenerator()
        self.MAC = np.sum((self.MAC_list*self.S_list))/np.sum(self.S_list)
        self.x_quarter = np.sum(self.x_list)/np.sum(self.S_list)
        return self.MAC, self.x_quarter
    def define_airfoil(self,file_path):
        # Initialize empty arrays for positive and negative values
        positive_column1 = []
        positive_column2 = []
        negative_column1 = []
        negative_column2 = []

        positive_column11 = []
        positive_column21 = []
        negative_column11 = []
        negative_column21 = []

        # Read the .dat file
        with open(file_path, 'r') as file:
            for line in file:
                # Remove leading/trailing whitespaces and split the line by spaces
                data = line.strip().split()
                if len(data) >= 2:  # Ensure the line has at least two columns
                    try:
                        value1 = float(data[0])
                        value2 = float(data[1])
                        if 0.15 <= value1 <= 0.55:
                            if value2 >= 0:
                                positive_column1.append(value1)
                                positive_column2.append(value2)
                            else:
                                negative_column1.append(value1)
                                negative_column2.append(value2)
                            
                    except ValueError:
                        continue
                    try:
                        value1 = float(data[0])
                        value2 = float(data[1])
                        if value2 >= 0:
                            positive_column11.append(value1)
                            positive_column21.append(value2)
                        else:
                            negative_column11.append(value1)
                            negative_column21.append(value2)
                            
                    except ValueError:
                        continue
        # Compute the surface using numpy
        postive_surface = -np.trapz(positive_column2, positive_column1)
        negative_surface = -np.trapz(negative_column2, negative_column1)
        Area = (negative_surface+postive_surface)

        self.eq_positive=interp1d(positive_column11[::-1],positive_column21[::-1],bounds_error=False,fill_value='extrapolate')
        self.eq_negative=interp1d(negative_column11,negative_column21,bounds_error=False,fill_value='extrapolate')
        thickness=self.eq_positive(np.arange(0,1,0.001))-self.eq_negative(np.arange(0,1,0.001))
        self.max_thickness = np.max(thickness)
        self.max_thickness_location = np.argmax(thickness)*0.001
        return Area
    
    def atmos(self):
        self.T=288.15-0.0065*self.h
        self.rho=1.225*(self.T/288.15)**(-1+9.81/(287.058*0.0065))
        self.nu=0.0000169

    def aerodynamic_properties(self):
        self.atmos()
        self.Re=self.rho*self.V*self.MAC/self.nu
        self.Re_list=self.rho*self.V*self.MAC_list/self.nu
        self.a=np.sqrt(1.4*287.058*self.T)
        self.M=self.V/self.a
    
    def define_C_f(self,laminar_frac,part):
        C_f_laminar=1.328/np.sqrt(self.Re_list[part])
        C_f_turbulent=0.455/((np.log10(self.Re_list[part]))**2.58*(1+0.144*self.M**2))
        C_f_total=laminar_frac*C_f_laminar+(1-laminar_frac)*C_f_turbulent
        print('C_f_total',C_f_total)
        return C_f_total
    
    def define_C_D_part_wing(self,laminar_frac,part):
        #modern blended winglet IF= 1-1.01, so IF can be neglected
        C_f=self.define_C_f(laminar_frac,part)
        FF=(1+0.6/self.max_thickness_location*self.max_thickness+100*(self.max_thickness)**(4))*(1.34*self.M**0.18*(np.cos(self.sweep[part]))**0.28)
        print('FF',FF)
        S_wet=2*self.S_list[part]*1.07
        C_D_part=FF*C_f*S_wet/self.S
        return C_D_part
    
    def define_C_D_0(self,laminar_frac):
        self.C_D_0=0
        for i in range(len(self.taper)):
            self.C_D_0+=self.define_C_D_part_wing(laminar_frac,i)
        self.C_D_0+=0.1*self.C_D_0

    

