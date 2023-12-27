import numpy as np
import ROOT, array
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

wpfile = ROOT.TFile('WP_3d.root', 'RECREATE')
h_3D = ROOT.TH3F('h_3D', '', len(XBins) - 1, XBins, len(YBins) - 1, YBins, len(ZBins) - 1, ZBins)
for i in range(h_3D.GetNbinsX()):
    for j in range(h_3D.GetNbinsY()):
        for k in range(h_3D.GetNbinsZ()):
            h_3D.SetBinContent(i+1, j+1, k+1, 0)

comsol = open('nexo_x0_y0.txt' , 'r')
for line in comsol:
    if '%' in line or 'NaN' in line:
        continue
    else:
        items = line.split()
        wp = float(items[3])
        if wp < 1.0e-5:
            continue
        else:
            x = float(items[0])*1000 + 0.05
            y = float(items[1])*1000 + 0.05
            z = -1*float(items[2])*1000 + 0.05
            binx = 0
            biny = 0
            binz = 0
            binx = h_3D.GetXaxis().FindBin(x)
            biny = h_3D.GetYaxis().FindBin(y)
            binz = h_3D.GetZaxis().FindBin(z)
            #print(float(items[0])*1000, x, binx, y, biny, z, binz, wp)
            if binz == 0 and wp <= 0.51:
                wp = 0
            h_3D.SetBinContent(binx , biny , binz , wp)
h_3D.Write()
wpfile.Close()
