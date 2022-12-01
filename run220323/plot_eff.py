import numpy as np
from ROOT import TCanvas, TPad, TH1F, TGraphErrors

S = 1074/101 # scaling factor on double coincidences

if __name__ == '__main__':

    out1 = np.loadtxt('data/out1_220310.out') # R123
    out3 = np.loadtxt('data/out3_220310.out') # R13, eff(2)
    out4 = np.loadtxt('data/out4_220310.out') # R12, eff(3)

    MIN = np.double(out1.min())
    MAX = np.double(out1.max())
    minutes = 60 * 24 # minutes per bin
    NBINS = int((MAX - MIN) / (minutes * 60))

    hist1, edges1 = np.histogram(out1, NBINS, range=(MIN, MAX))
    bin_centers = edges1[:-1] + np.diff(edges1) / 2
    hist3, _ = np.histogram(out3, NBINS, range=(MIN, MAX))
    hist4, _ = np.histogram(out4, NBINS, range=(MIN, MAX))

    hist3, hist4 = hist3 * S, hist4 * S # rescaling

    eff2 = hist1 / hist3
    eff3 = hist1 / hist4

    eff2e = np.sqrt(hist1 * (1 - eff2)) / hist3
    eff3e = np.sqrt(hist1 * (1 - eff3)) / hist4
    bin_width = np.ones(len(hist1)) * (MAX - MIN) / NBINS / 2

    c1 = TCanvas('c1','c1',800,800)
    pad1 = TPad('pad1','pad1',0,0.40,1,1)
    pad2 = TPad('pad2','pad2',0,0.10,1,0.40)
    pad1.SetBottomMargin(0.00001)
    pad1.SetBorderMode(0)
    pad2.SetTopMargin(0.00001)
    pad2.SetBottomMargin(0.1)
    pad2.SetBorderMode(0)
    pad1.Draw()
    pad2.Draw()
    pad1.cd()
    h1 = TH1F('TEL1','Flusso di raggi cosmici TEL1', NBINS, MIN, MAX)
    h1.GetYaxis().SetLabelFont(63)
    h1.GetYaxis().SetLabelSize(16)
    h1.GetYaxis().SetTitle('occorrenze / bin')
    for val in out1:
        h1.Fill(val)
    for i in range(NBINS):
        rescale = h1.GetBinContent(i) / (eff2[i] * eff3[i])
        h1.SetBinContent(i,rescale)
    h1.Draw('E')
    pad2.cd()
    gr2 = TGraphErrors(NBINS, bin_centers, eff2, bin_width, eff2e)
    gr3 = TGraphErrors(NBINS, bin_centers, eff3, bin_width, eff3e)
    gr2.SetTitle('efficienza PMT2 PMT3')
    gr2.SetMarkerStyle(20)
    gr2.GetXaxis().SetTitle( 'time (s)' )
    gr2.GetYaxis().SetTitle( 'efficienza / bin' )
    gr2.SetMarkerColor(4)
    gr2.Draw('AP')
    gr3.SetMarkerStyle(20)
    gr3.SetMarkerColor(3)
    gr3.Draw('same P')