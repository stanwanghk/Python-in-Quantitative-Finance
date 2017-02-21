from scipy.misc import derivative
pr=100
c=0.0675
dt=0.5
T=4
B=106+(21+1/8)/32
y0=0.049
dy=0.001
def bond_price(y):
    oneyrt=1+y*dt
    n=T/dt
    return pr*(1-(1-c/y)*(1-1/oneyrt**n))

duration_mod=-derivative(bond_price,y0,dy,1)/B
DV01=B*duration_mod/10000
convexity=derivative(bond_price,y0,dy,2)/B

changeOfy=0.0025
changeOfPrice1=B*(-duration_mod*changeOfy+0.5*convexity*(changeOfy**2))
changeOfPrice2=B*(duration_mod*changeOfy+0.5*convexity*(changeOfy**2))

estimatedPrice=B-changeOfPrice1

actualPrice1=bond_price(y0-changeOfy)
actualPrice2=bond_price(y0+changeOfy)
adiff1=actualPrice1-B
adiff2=actualPrice2-B

diff=estimatedPrice-actualPrice1
