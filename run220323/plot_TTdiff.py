import numpy as np
from ROOT import TCanvas, TRatioPlot
from ROOT import TH1F, TF1, THStack
from ROOT import gStyle, gPad
import sys
sys.path.append('../')
from read import make_out
if __name__ == '__main__':

    MIN = -200e-9
    MAX = 200e-9

    # Obtaining data
    ch, time, date, _, _ = make_out('events220310_5d.dat')

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
    gPad.SetFrameFillStyle(0)
    h1 = TH1F('T2-T1', 'Consecutive T1-T2 events difference', 20, MIN, MAX)
    for val in diff:
        h1.Fill(val)
    h1.Sumw2()
    h1.GetXaxis().SetTitle('Tempo [s]')
    h1.GetYaxis().SetTitle('occorrenze / bin [u.a.]')
    h1.Draw()
    # func1 = TF1('func1', '[0]*exp(-x/[1])+[2]', diff.min(), diff.max())
    # func1.SetParameters(1e3, 1, 0)
    # h1.Fit('func1', 'LIRMS')
    # gStyle.SetOptFit(1111)
    # c1.Clear()

    # rp = TRatioPlot(h1)
    # rp.Draw()
    # rp.GetLowerRefGraph().SetMinimum(-2);
    # rp.GetLowerRefGraph().SetMaximum(2);
    # c1.Update()

    c2 = TCanvas('c2', 'c2', 1)
    hs = THStack('hs', 'hs')
    h2T1 = TH1F('h2t1', 'h2t1', 100, time.min(), time.max())
    for val in time_zoom1:
        h2T1.Fill(val)
    h2T1.SetMarkerColor(4)
    hs.Add(h2T1)
    h2T2 = TH1F('h2t2', 'h2t2', 100, time.min(), time.max())
    for val in time_zoom2:
        h2T2.Fill(val)
    h2T2.SetMarkerColor(5)
    hs.Add(h2T2)
    hs.Draw('e1c')