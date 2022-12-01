import numpy as np
from ROOT import TCanvas, TRatioPlot, TDatime, TMath
from ROOT import TH1F, TF1, THStack, kRed, kBlue
from ROOT import gStyle, gPad, TLegend, TPaveText
import sys
sys.path.append('../')
from read import make_out
if __name__ == '__main__':

    MIN = -100e-9
    MAX = 200e-9

    # Obtaining data
    ch, time, date, _, _ = make_out('events220316_6d.dat')

    mask = (ch==1) | (ch==2)

    time = time[mask]
    date = date[mask]
    ch = ch[mask]

    # time[ch==1] = time[ch==1] + 46e-9
    diff = (ch - np.roll(ch, -1)) * (time - np.roll(time, -1))

    time_zoom1 = time[(diff > 0) & (diff < MAX)]
    time_zoom2 = time[(diff > MIN) & (diff < 0)]
    print(len(time_zoom1))
    print(len(time_zoom2))
    diff = diff[(diff > MIN) & (diff < MAX) & (diff!=0)]

    # ROOT
    c1 = TCanvas('c1', 'c1', 1)
    c1.SetLogy()
    gStyle.SetOptStat('emr')
    gStyle.SetOptFit(1111), gStyle.SetStatBorderSize(0)
    gStyle.SetStatX(.89), gStyle.SetStatY(.89)
    gStyle.SetTextSize(0.040)
    h1 = TH1F('T2-T1', 'Consecutive T1-T2 events difference', 15, MIN, MAX)
    for val in diff:
        h1.Fill(val)
    h1.Sumw2()
    h1.GetXaxis().SetTitle('Tempo [s]')
    h1.GetYaxis().SetTitle('occorrenze / 20e-9s')
    # func1 = TF1('func1', '[0]*exp(-TMath::Abs(x)/[1])+[2]', MIN, MAX)
    # func1.SetParameters(1e5, 1, 0)
    # func1.SetParNames('A', '#tau', 'q_{0}')
    # h1.Fit('func1', 'LIRMS')
    h1.Draw('E')
    # c1.Clear()

    # rp = TRatioPlot(h1)
    # rp.Draw()
    # rp.GetLowerRefGraph().SetMinimum(-2)
    # rp.GetLowerRefGraph().SetMaximum(2)
    # rp.GetLowerRefYaxis().SetTitle('Dati - best-fit [#sigma]')
    # rp.SetSeparationMargin(0.01)
    # c1.Update()
    # rp.GetUpperPad().cd()

    # leg1 = TLegend(0.12, 0.05, 0.26,0.23, 'NDC')
    # leg1.Clear()
    # leg1.SetBorderSize(1)
    # leg1.SetFillColor(0)
    # leg1.SetFillStyle(1001)
    # leg1.SetTextFont(42)
    # leg1.SetTextSize(0.04)
    # leg1.SetTextAlign(22)
    # leg1.AddEntry(h1,'T1-T2','LE')
    # leg1.AddEntry(func1,'best-fit','L')
    # leg1.AddEntry(rp.GetConfidenceInterval1(), 'CL 68%', 'FL')
    # leg1.AddEntry(rp.GetConfidenceInterval2(), 'CL 95%', 'FL')
    # leg1.Draw()

    infos = TPaveText(0.3,0.75,0.5,0.87, 'nbNDC')
    infos.AddText('RUN 16/03/22')
    infos.AddText('PLOT 08/04/22')
    # infos.AddText('Funzione di fit: y = A e^{-|x|/#tau}+q_{0}')
    infos.SetTextAlign(12)
    infos.SetTextFont(42)
    infos.SetTextSize(0.040)
    infos.SetFillColor(0)
    infos.Draw()

    c1.Update()

    # da = TDatime(2022,3,16,12,33,25)
    # gStyle.SetTimeOffset(da.Convert())
    # c2 = TCanvas('c2', 'c2', 1)
    # c2.cd()
    # c2.SetGrid()
    # h2T1 = TH1F('h2t1', 'h2t1', 100, time.min(), time.max())
    # for val in time_zoom1:
    #     h2T1.Fill(val)
    # h2T1.Sumw2()
    # h2T1.SetLineColor(kBlue)
    # h2T1.Draw('E')
    # h2T2 = TH1F('h2t2', 'h2t2', 100, time.min(), time.max())
    # for val in time_zoom2:
    #     h2T2.Fill(val)
    # h2T2.Sumw2()
    # h2T2.SetLineColor(kRed)
    # h2T2.Draw('E SAMES')
    # h2T1.GetXaxis().SetTimeDisplay(1)
    # c2.Update()
