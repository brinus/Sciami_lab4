import numpy as np
from ROOT import TH1F, TF1, TCanvas, TRatioPlot
from ROOT import gStyle

if __name__ == '__main__':

    time = np.loadtxt('data/outexp2_220310.out')

    NBINS = 20
    MIN = 0
    MAX = 0.01

    c1 = TCanvas('c1','c1',1)
    c1.SetLogy()
    exp1 = TF1('exp1', '[0]*exp(-x/[1])+[2]', MIN, MAX)
    exp1.SetParameters(20000,1,0)
    h1 = TH1F('TEL2','Differenze tempi successivi TEL2',NBINS,MIN,MAX)
    h1.GetXaxis().SetTitle('Tempo [s]')
    h1.GetYaxis().SetTitle('occorrenze / bin [u.a.]')
    for t in time:
        h1.Fill(t)
    h1.Fit('exp1', 'LIRMS')
    gStyle.SetOptFit(1111)
    h1.Sumw2()

    rp = TRatioPlot(h1)
    rp.Draw()
    rp.GetLowerRefGraph().SetMinimum(-2);
    rp.GetLowerRefGraph().SetMaximum(2);
    c1.Update()

