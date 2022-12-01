import numpy as np
from ROOT import TH1F, TF1, TCanvas, TPad
from ROOT import gStyle

if __name__ == '__main__':

    out_exp2 = np.loadtxt('data/outexp2_220309.out')

    NBINS = 100
    MIN = out_exp2.min()
    MAX = out_exp2.max()

    c1 = TCanvas('c1','c1',800,800)
    pad1 = TPad('pad1','pad1',0,0.40,1,1)
    pad2 = TPad('pad2','pad2',0,0.17,1,0.40)
    pad1.SetBottomMargin(0.00001)
    pad1.SetBorderMode(0)
    pad1.SetLogy()
    pad2.SetTopMargin(0.00001)
    pad2.SetBottomMargin(0.1)
    pad2.SetBorderMode(0)
    pad1.Draw()
    pad2.Draw()
    pad1.cd()
    exp1 = TF1('exp1', '[0]*exp(-x/[1])+[2]', MIN, MAX)
    exp1.SetParameters(20000,1,0)
    h1 = TH1F('TEL2','Flusso di raggi cosmici TEL2',NBINS,MIN,MAX)
    h1.GetYaxis().SetLabelFont(63)
    h1.GetYaxis().SetLabelSize(16)
    h1.GetYaxis().SetTitle('occorrenze / bin')
    for t in out_exp2:
        h1.Fill(t)
    h1.Fit('exp1', 'LIRMS')
    gStyle.SetOptFit(1111)
    h1.Draw('E')
    pad2.cd()
    h2 = TH1F('TEL2 residuals','residuals',NBINS,MIN,MAX)
    h2.GetXaxis().SetLabelFont(63)
    h2.GetXaxis().SetLabelSize(16)
    h2.GetXaxis().SetTitle('time (s)')
    h2.GetYaxis().SetLabelFont(63)
    h2.GetYaxis().SetLabelSize(16)
    for i in range(len(out_exp2)):
        diff = h1.GetBinContent(i)-exp1.Eval(h1.GetBinCenter(i))
        h2.SetBinContent(i,diff)
    h2.Draw('E')