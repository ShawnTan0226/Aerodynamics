import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

class Plane:
    def __init__(self,Cri,taper,sweep,b):
        self.c=np.array([Cri])
        self.taper = np.array(taper)
        self.sweep = np.array(np.deg2rad(sweep))
        self.b = np.concatenate(([0],b))
        self.coords=np.array([])

        self.draw()

    def draw(self):
        self.offset=np.array([0])
        count=0
        for i in self.taper:
            self.c=np.concatenate((self.c, [i*self.c[-1]]))
            nextoffset=self.offset[-1]+np.tan(self.sweep[count])*(self.b[count+1]-self.b[count])/2+0.25*self.c[-2]-0.25*self.c[-1]
            self.offset=np.concatenate((self.offset, [nextoffset]))
            count+=1
        
        coords_bot=self.offset+self.c
        self.coords=np.concatenate((self.coords,self.offset,coords_bot[::-1]))
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
    def drawbox(self):
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


        plt.plot(self.bfull,self.coords)
        plt.gca().invert_yaxis()
        # plt.fill(y,x_store, color='blue', alpha=0.5)
        plt.fill(y,x_red, color='red', alpha=0.5)
        plt.fill(y,x_red2, color='red', alpha=0.5)
        plt.show()
    def MAC_part(self,cr, ct, sweep, b):
        #MAC
        y = 2/3 * (cr + ct - (cr*ct)/(cr+ct))
        #offset from that parts root on quarter chord
        off_x = (b/2/(ct-cr))*(y-ct)
        off_y = cr*0.25-ct*0.25 + np.tan(sweep)*off_x
        return y, off_x, off_y

    def listgenerator(self):
        self.MAC_list=np.array([])
        self.S_list=np.array([])
        self.x_list=np.array([])
        for i in range(len(self.taper)):
            part= self.MAC_part(self.c[i],self.c[i+1],self.sweep[i],self.b[i+1])
            self.MAC_list=np.concatenate((self.MAC_list,[part[0]]))
            self.S_list=np.concatenate((self.S_list,[(self.c[i]+self.c[i+1])/2*self.b[i+1]]))
            self.x_list=np.concatenate((self.x_list,[part[1]]))

    def MAC_aircraft(self):#Make sure to use numpy array
        self.listgenerator()
        self.MAC = np.sum((self.MAC_list*self.S_list))/np.sum(self.S_list)
        self.x_quarter = np.sum(self.x_list)/np.sum(self.S_list)
        return self.MAC, self.x_quarter

test=Plane(9.72,[0.3,0.267],[38,38],[8.82,22])
# test.plot_plane()
test.xflrvelues()
test.drawbox()
print(test.MAC_aircraft())
