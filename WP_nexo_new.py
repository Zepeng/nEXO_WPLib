import numpy as np
import ROOT, array
import pandas as pd
from EField import EField
import time
import argparse

class WPLib:
    def __init__(self, fcomsol):
        comsol = pd.read_csv(fcomsol, skiprows=9, names = ['x', 'y', 'z', 'E'])
        points = []
        for i in range(len(comsol['x'])):
            x = float(comsol['x'][i])*1000
            y = float(comsol['y'][i])*1000
            z = float(comsol['z'][i])*1000
            E = float(comsol['E'][i])
            points.append([x, y, z])
        from scipy.interpolate import NearestNDInterpolator
        self.fWP = NearestNDInterpolator(points, comsol['E'])
        print("Weight potential library built!")
    def calc_wp(self, point):
        return self.fWP(point)

def wp_bins():
    XBins = array.array('f')
    YBins = array.array('f')
    ZBins = array.array('f')
    for i in range(150):
        if i < 100:
            XBins.append(i*0.2)
        else:
            XBins.append((i-100)*2 + 20)
    for i in range(345):
        if i < 300:
            YBins.append(i*0.2)
        else:
            YBins.append((i-300)*2 + 60)
    for i in range(980):
        if i < 500:
            ZBins.append(i*0.1)
        elif i < 600:
            ZBins.append( (i-500)*0.5+ 50)
        elif i < 700:
            ZBins.append((i-600) + 100)
        elif i < 800:
            ZBins.append((i-700)*2 + 200)
        else:
            ZBins.append((i-800)*5 + 400)
    return XBins, YBins, ZBins

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-x', '--xindex', help='x index', type=int)
    args = parser.parse_args()

    print('EField Sim')
    simfield = EField('/scratch/zpli/EField3d.csv')
    endpoints = []
    XBins, YBins, ZBins = wp_bins()
    wpfile = ROOT.TFile('WP_3d_y{}.root'.format(args.xindex), 'RECREATE')
    h_3D = ROOT.TH3F('h_3D', '', len(XBins) - 1, XBins, len(YBins) - 1, YBins, len(ZBins) - 1, ZBins)
    for i in range(h_3D.GetNbinsX()):
        for j in range(h_3D.GetNbinsY()):
            for k in range(h_3D.GetNbinsZ()):
                h_3D.SetBinContent(i+1, j+1, k+1, 0)

    simwp = WPLib('/scratch/zpli/nexo_x0_y0.csv')
    start = time.time()
    for x in XBins:
        for y in YBins[args.xindex:args.xindex+1]:
            print(x, y, time.time() - start)
            init_x = x
            init_y = y
            init_z = -1*ZBins[-1]
            for z in ZBins[::-1]:
                endpoints = []
                wp = 0
                endpoints = simfield.calc_drift([init_x, init_y, init_z],-z )
                init_x = endpoints[0]
                init_y = endpoints[1]
                init_z = endpoints[2]+0.1
                wp = simwp.calc_wp([init_x, init_y, init_z])
                binx = 0
                biny = 0
                binz = 0
                binx = h_3D.GetXaxis().FindBin(x + 0.05)
                biny = h_3D.GetYaxis().FindBin(y + 0.05)
                binz = h_3D.GetZaxis().FindBin(init_z + 0.05)
                if wp > 1.0:
                    wp = 1.0
                if binz == 0:
                    if wp <= 0.51:
                        wp = 0
                    else:
                        wp = 1
                h_3D.SetBinContent(binx , biny , binz , wp)
    h_3D.Write()
    wpfile.Close()
