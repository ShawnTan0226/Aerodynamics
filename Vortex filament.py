import numpy as np
import pandas as pd
import os
import scipy as sp
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d




AR=5
TR=0.5
sweep=np.deg2rad(33)


class Wingmodelling:
    def __init__(self,AR, TR, sweep,airfoil,b,aoa=0,step=1000):
        self.AR=AR
        self.TR=TR
        self.sweep=np.deg2rad(sweep)
        self.S=b**2/AR
        self.b=b
        self.y=np.linspace(-b/2,b/2,step)
        self.rho=1.225
        self.V=110

        self.get_c()
        self.get_aoa(aoa)

        directory_path = "./LLT/Oppoints"
        file_list = []
        data={}

        for filename in os.listdir(directory_path):
            file_list.append(filename)

        for file in file_list:
            filename=directory_path+'/'+file
            df = pd.read_csv(filename,header=None)
            df=np.array(df)
            data[file[:4]]=df

        self.data=data[airfoil]

    def integrator(self,f,init,end,step):
        x=np.arange(init,end,step)
        integ=0
        for i in x:
            sec=(f(i)+f(i+step))*step
            integ+=sec
        return integ
    
    def differentiation(self,y,x):
        diff=[(y[1]-y[0])/(x[1]-x[0])]
        for i in range(len(y)-2):
            diff.append((y[i+2]-y[i])/(x[i+2]-x[i]))
        diff.append((y[-1]-y[-2])/(x[-1]-x[-2]))
        return np.array(diff)

    
    def get_aoa(self,aoa):
        self.geomaoa=np.full(len(self.y), np.deg2rad(aoa))
    
    def get_aoa_fromcl(self,cl):
        f = interp1d(self.data[:,1],self.data[:,0],bounds_error=False,fill_value=0)
        aoa=f(cl)
        return np.deg2rad(aoa)

    def get_cl(self,aoa):
        # f = interp1d(self.data[:,0], self.data[:,1],bounds_error=False,fill_value=0)
        # cl=f(np.rad2deg(aoa))
        start=np.where(self.data[:,0]==-5)[0][0]
        end=np.where(self.data[:,0]==5)[0][0]
        coeff=np.polyfit(self.data[start:end,0],self.data[start:end,1],1)
        cl=coeff[0]*np.rad2deg(aoa)+coeff[1]
        return cl
    
    def get_true_aoa(self,aoa,ai):
        aoa=aoa+ai
        return aoa

    def get_c(self):
        self.c=self.b/self.AR

    def wing_CL(self):
        CL=np.trapz(self.cl*self.c,self.y)/self.S
        return CL

    def calc_induced(self,y):
        tempdGdy=np.copy(self.dGdy)
        tempy=np.copy(self.y)
        offset=0.0001
        for i in range(len(tempy)):
            if tempy[i]==y:
                tempy=np.delete(tempy,i)
                tempy=np.insert(tempy,i,np.array([self.y[i]-offset,self.y[i]+offset]))
                if i==0:
                    tempy=np.delete(tempy,0)
                elif i==len(self.y)-1:
                    tempy=np.delete(tempy,-1)
                else:
                    tempdGdy=np.insert(tempdGdy,i,tempdGdy[i])
                singularity=i
        f=tempdGdy/(y-tempy)
        ai=1/(4*np.pi*self.V)*np.trapz(f,tempy)
        return np.arctan(ai)


    def iterate_CL(self):
        self.cl=self.get_cl(self.geomaoa)*np.sqrt((1-(self.y/(self.b/2))**2))
        self.Gamma=self.cl*self.c*0.5*self.V
        ai=np.zeros(len(self.y))
        aiold=0
        # plt.plot(self.y,self.Gamma)
        error=10
        count=0
        while np.abs(error)>=0.001:
            self.dGdy=self.differentiation(self.Gamma,self.y)
            print('Iteration: ',count+1)
            for i in range(len(self.y)):
                y0=self.y[i]
                induced_aoa_y0=self.calc_induced(y0)
                ai[i]=induced_aoa_y0

            self.aoa=self.geomaoa+ai
            self.cl=self.get_cl(self.aoa)

            error=np.mean(np.abs(aiold-ai))
            aiold=np.copy(ai)

            self.Gammanew=self.cl*self.c*0.5*self.V
            self.Gammanew[0],self.Gammanew[-1]=0,0
            self.Gamma+=0.05*(self.Gammanew-self.Gamma)

            plt.plot(self.y,self.Gamma)
            plt.plot(self.y,self.Gammanew)
            plt.show()
            # print(ai-aiold)
            
            count+=1
        self.ai=ai
        self.CL=self.wing_CL()
        return self.CL

    def calc_CD(self):
        self.CDi=np.trapz(self.cl[1:-1]*self.c*self.ai[1:-1],self.y[1:-1])/self.S
        return self.CDi
    
    def plot_cl(self):
        plt.plot(self.y,self.cl)
        plt.show()
    
    def plot_ai(self):
        plt.plot(self.y,self.ai)
        plt.show()
        

Wingtest=Wingmodelling(4,0.5,33,'MH91',5,5)
CL=Wingtest.iterate_CL()
CDi=Wingtest.calc_CD()
print(CL,CDi)
Wingtest.plot_cl()
