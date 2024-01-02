#-- coding:UTF-8 --
import ROOT
import math
import sys
import os
import string
from array import array

def read_axes(tfile):
    h3dfile = ROOT.TFile(tfile, 'READ')
    h_3d = h3dfile.Get('h_3D')
    xaxis_new = h_3d.GetXaxis()
    yaxis_new = h_3d.GetYaxis()
    zaxis_new = h_3d.GetZaxis()
    return xaxis_new.Clone(), yaxis_new.Clone(), zaxis_new.Clone()

def read_wp(tfile, x, y):
    return 0

if __name__ == '__main__':
    ROOT.gROOT.SetBatch(True)
    ROOT.RooMsgService.instance().setGlobalKillBelow(ROOT.RooFit.WARNING)
    ROOT.RooMsgService.instance().setSilentMode(True)
    ROOT.gStyle.SetOptStat(0)
    ROOT.gStyle.SetOptFit(0)

    #read the axis from a subfile and save for the merged library file.
    wpfile = ROOT.TFile('nEXO_6mm_COMSOL.root', 'RECREATE')
    xaxis_new, yaxis_new, zaxis_new = read_axes('./outputs/WP_3d_x0.root')
    wpfile.cd()
    xaxis_new.SetTitle('X (mm)')
    xaxis_new.Write()
    yaxis_new.SetTitle('Y (mm)')
    yaxis_new.Write()
    zaxis_new.Write()
    print('finished writting of  axes')
    ZBins = array('d')
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
    wpf = ROOT.TF1('wpf', '[0] + [1]*x + [2]*x*x + [3]*x*x*x + [4]*x*x*x*x + [5]*x*x*x*x*x + [6]*x*x*x*x*x*x + [7]*x*x*x*x*x*x*x', 0, 150)
    for xbin in range(1, xaxis_new.GetNbins() + 1):
        h_3d = read_wp('./outputs/WP_3d_x{}.root'.format(xbin-1))
        for ybin in range(1, yaxis_new.GetNbins() + 1):
            name = 'wp_x'+str(xbin)+'_y'+str(ybin)
            wpHist = ROOT.TH1F(name, '', zaxis_new.GetNbins() , ZBins)
            for k in range(1, zaxis_new.GetNbins() + 1):
                wpHist.SetBinContent(k, 0)
            """
            for k in range(1, h_3d.GetNbinsZ() + 1):
                wpHist.SetBinContent(k, h_3d.GetBinContent(xbin, ybin, k)*1e5)
            #if wpHist.GetMaximum()> 0.9*1e5:
            #    print(xbin, ybin)
            if wpHist.GetMaximum() > 90000:
                #wpHist.Fit('wpf')
                p0 = wpf.GetParameter(0)
                p1 = wpf.GetParameter(1)
                p2 = wpf.GetParameter(2)
                p3 = wpf.GetParameter(3)
                p4 = wpf.GetParameter(4)
                p5 = wpf.GetParameter(5)
                p6 = wpf.GetParameter(6)
                p7 = wpf.GetParameter(7)
                print(p0, p1, p2, p3, p4, p5, p6, p7)
            else:
                p0 = 0
                p1 = 0
                p2 = 0
                p3 = 0
                p4 = 0
                p5 = 0
                p6 = 0
                p7 = 0
                wpf.SetParameter(0, 0)
                wpf.SetParameter(1, 0)
                wpf.SetParameter(2, 0)
                wpf.SetParameter(3, 0)
                wpf.SetParameter(4, 0)
                wpf.SetParameter(5, 0)
                wpf.SetParameter(6, 0)
                wpf.SetParameter(7, 0)
            #tg = ROOT.TGraph(wpHist)
            #ts = ROOT.TSpline3('ts_x' + str(xbin)+ '_y' + str(ybin) , tg)
            wpHist.Write()
            #ts.Write()
            if wpHist.GetMaximum()>90000:
                for zbin in range(wpHist.GetNbinsX()):
                    print(wpHist.GetBinCenter(zbin + 1), wpf.Eval(wpHist.GetBinCenter(zbin+1)), wpHist.GetBinContent(zbin+1))
#            print xbin,'|',ybin
    wpfile.Close()
    """