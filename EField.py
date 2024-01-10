import numpy as np
import pandas as pd
from scipy.interpolate import NearestNDInterpolator
import matplotlib.pyplot as plt
from math import copysign
sign = lambda x : copysign(1, x)

class EField:
    def __init__(self, fcomsol):
        comsol = pd.read_csv(fcomsol, skiprows=9, names = ['x', 'y', 'z', 'Ex', 'Ey', 'Ez'])
        #comsol = open(fcomsol , 'r')
        Ex = []
        Ey = []
        Ez = []
        points = []
        for i in range(len(comsol['x'])):
                x = 1000*float(comsol['x'][i]) - 6
                y = 1000*float(comsol['y'][i])
                z = 1000*float(comsol['z'][i])
                points.append([x, y, z])
                Ex.append(comsol['Ex'][i])
                Ey.append(comsol['Ey'][i])
                Ez.append(comsol['Ez'][i])

        self.fx = NearestNDInterpolator(points, Ex)
        self.fy = NearestNDInterpolator(points, Ey)
        self.fz = NearestNDInterpolator(points, Ez)
    def calc_drift(self, point, z):
        if z < -90 or z >0.0000:
            return point
        else:
            mod_x = abs(point[0])//6
            mod_y = abs(point[1])//6
            init_x = abs(point[0]) % 6
            init_y = abs(point[1]) % 6
            init_z = point[2]
            while init_z < z:
                step = 1
                if init_z > -15:
                    step = 0.1
                delta_x = -1*self.fx([init_x, init_y, init_z]).item(0)
                delta_y = -1*self.fy([init_x, init_y, init_z]).item(0)
                delta_z = -1*self.fz([init_x, init_y, init_z]).item(0)
                mag = np.sqrt(delta_x*delta_x+delta_y*delta_y + delta_z*delta_z)
                init_x += delta_x/mag*step
                init_y += delta_y/mag*step
                init_z += delta_z/mag*step
            #print(np.array([init_x + 0.006*mod_x, init_y + 0.006*mod_y, z]) - np.array(point) )
            return [sign(point[0])*(init_x + 6*mod_x), sign(point[1])*(init_y + 6*mod_y), z]

if __name__ == '__main__':
    print('EField Sim')
    simfield = EField('/scratch/zpli/EField3d_v2.csv')
    endpoints = []
    rng = np.random.default_rng()
    for i in range(2000):
        init_x = rng.random()*6
        init_y = rng.random()*6
        init_z = -90
        #print(i)
        endpoints.append(simfield.calc_drift([init_x, init_y, -90], -0.1))
    x, y, z = np.array(endpoints).T
    fig1, ax1 = plt.subplots(figsize=(15, 15))
    histbins = np.arange(-3, 9, 0.2)
    ax1.hist2d(x, y, bins=[histbins, histbins], cmap='Blues')
    ax1.tick_params(axis='both', which='major', labelsize=22)
    ax1.set_xlabel('X (mm)', fontsize=24)
    ax1.set_ylabel('Y (mm)', fontsize=24)
    #ax1.set_xticks(np.arange(0, 12, 0.5))
    #ax1.set_yticks(np.arange(0, 12, 0.5))
    ax1.grid()
    fig1.savefig('endpoints_shift.png')
