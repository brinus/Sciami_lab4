import numpy as np
from ROOT import TCanvas, gStyle, gPad
from ROOT import TF1, TH1F, TRatioPlot, TLegend, TPaveText

if __name__ == '__main__':
    time = np.loadtxt('data/outexp1_220316.out')

    NBINS = 50
    MIN = 0
    MAX = 100e-6

    print(len(time[(time > MIN) & (time < MAX)]))

    # ROOT
    c1 = TCanvas('c1', 'c1', 1)
    c1.SetLogy()
    gStyle.SetOptStat(0)
    gStyle.SetOptFit(1111), gStyle.SetStatBorderSize(0)
    gStyle.SetStatX(.89), gStyle.SetStatY(.89)
    h1 = TH1F('T2', 'Differenze eventi successivi T1', NBINS, MIN, MAX)
    for val in time:
        h1.Fill(val)
    h1.Sumw2()
    # exp = TF1('f1', '[0]*exp(-x/[1])+[2]', MIN, MAX)
    # exp.SetParameters(1e2, 1, 0)
    # exp.SetParNames('A', '#tau', 'q_{0}')
    # h1.Fit('f1', 'LIRMS')
    h1.GetXaxis().SetTitle('Tempo [s]')
    h1.GetYaxis().SetTitle('Eventi / 2e-6s')
    # gStyle.SetOptFit(1111)
    # c1.Clear()
    # rp = TRatioPlot(h1)
    h1.Draw('E')
    # rp.GetLowerRefGraph().SetMinimum(-2)
    # rp.GetLowerRefGraph().SetMaximum(2)
    # rp.GetLowerRefYaxis().SetTitle('Dati - best-fit [#sigma]')
    # rp.SetSeparationMargin(0.01)

    # rp.GetUpperPad().cd()
    # leg1 = TLegend(0.12, 0.05, 0.26,0.23, 'NDC')
    # leg1.Clear()
    # leg1.SetBorderSize(1)
    # leg1.SetFillColor(0)
    # leg1.SetFillStyle(1001)
    # leg1.SetTextFont(42)
    # leg1.SetTextSize(0.04)
    # leg1.SetTextAlign(22)
    # leg1.AddEntry(h1,'T1','LE')
    # leg1.AddEntry(exp,'best-fit','L')
    # leg1.AddEntry(rp.GetConfidenceInterval1(), 'CL 68%', 'FL')
    # leg1.AddEntry(rp.GetConfidenceInterval2(), 'CL 95%', 'FL')
    # leg1.Draw()

    infos = TPaveText(0.3,0.75,0.5,0.87, 'nbNDC')
    infos.AddText('RUN 16/03/22')
    infos.AddText('PLOT 11/04/22')
    # infos.AddText('Funzione di fit: y = A e^{-x/#tau}+q_{0}')
    infos.SetTextAlign(12)
    infos.SetTextFont(42)
    infos.SetTextSize(0.040)
    infos.SetFillColor(0)
    infos.Draw()

    c1.Update()