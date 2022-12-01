import numpy as np
from ROOT import TCanvas, gStyle
from ROOT import TF1, TH1F, TRatioPlot

if __name__ == '__main__':
    time = np.loadtxt('data/outexp1_220310.out')

    NBINS = 100
    MIN = 1e-3
    MAX = 9e-2

    print(len(time[(time > MIN) & (time < MAX)]))

    c1 = TCanvas('c1', 'c1', 1)
    c1.SetLogy()
    h1 = TH1F('h1', 'h1', NBINS, MIN, MAX)
    for val in time:
        h1.Fill(val)
    h1.Sumw2()
    exp = TF1('f1', '[0]*exp(-x/[1])+[2]', time.min(), time.max())
    exp.SetParameters(1e3, 1, 0)
    h1.Fit('f1', 'LIRMS')
    gStyle.SetOptFit(1111)
    c1.Clear()
    rp = TRatioPlot(h1)
    rp.Draw()
    rp.GetLowerRefGraph().SetMinimum(-2);
    rp.GetLowerRefGraph().SetMaximum(2);
    c1.Update()