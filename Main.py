from Plane import Plane
from BatterySize import Planform_calculation

MakePlane = Planform_calculation(".\Airfoil_dat\MH 91  14.98%.dat",".\Airfoil_dat\MH 91  14.98%.dat",19902,2409,20.5,0.25,0.4)
MakePlane.makeplane()
MakePlane.plane.xflrvelues()
MakePlane.plane.define_C_D_0(0.2)
print(MakePlane.plane.C_D_0)

test=Plane(9.72,[0.3,0.267,0.5],[38,38,5],[8.82,22,28])
# test.plot_plane()
test.xflrvelues()
# test.drawbox(0.5)
test.drawtail(0.2)
print(test.MAC_aircraft())