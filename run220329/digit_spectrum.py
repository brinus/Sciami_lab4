import numpy as np
from ROOT import TH1F, gStyle, TCanvas, TLegend, TPaveText, TGaxis
from ROOT import kRed, kBlue, gPad

def double_cosmic(mask, time, cosmic):
    out = np.array([])
    ch_out = np.array([])
    for val in cosmic:
        idx = np.where(time == val)
        if len(idx[0]) == 1:
            idx = idx[0][0]
            window = time[idx-5:idx+6]
            channels = mask[idx-5:idx+6]
            out = np.append(out, window[channels])    
    return out

if __name__ == '__main__':
    
    # READING
    ch, time = np.loadtxt('data/out_.out', unpack=True)
    ch = ch.astype(int)
    time = np.around(time, 8)
    
    # SPLITTING
    mask1 = (ch==3) | (ch==4) | (ch==5)
    mask2 = (ch==6) | (ch==7) | (ch==8)
    mask12 = (ch==1) | (ch==2)

    time12 = time[mask12]
    ch12 = ch[mask12]
    
    diff_d1 = np.ediff1d(time[mask1])
    diff_d2 = np.ediff1d(time[mask2])

    diff_d1 = diff_d1[diff_d1 < 200e-9]
    diff_d2 = diff_d2[diff_d2 < 200e-9]

    diff = (ch12 - np.roll(ch12, -1)) * (time12 - np.roll(time12, -1))
    cosmic1 = time12[(diff > -20e-9) & (diff < 200e-9) & (diff != 0) & (ch12==1)]
    cosmic2 = time12[(diff > -20e-9) & (diff < 200e-9) & (diff != 0) & (ch12==2)]
    diff = diff[(diff > -20e-9) & (diff < 200e-9) & (diff != 0)]


    out1, ch_out1 = double_cosmic(mask1, time, ch, cosmic1)
    out2, ch_out2 = double_cosmic(mask2, time, ch, cosmic2)
    out1 = np.ediff1d(out1)
    out2 = np.ediff1d(out2)
    out1 = out1[out1 < 100e-9]
    out2 = out2[out2 < 100e-9]

    print(len(out1))
    print(len(out2))

    # PLOT

    MIN = 0
    MAX = 200e-9
    NBINS = 10
    c1 = TCanvas('c1', 'c1', 1)
    c1.SetLogy()
    h1 = TH1F('Doppie T1', 'h1', NBINS, MIN, MAX)
    h2 = TH1F('Doppie T2', 'Differenze tra doppie successive dello stesso T', NBINS, MIN, MAX)
    for val in diff_d1:
        h1.Fill(val)
    for val in diff_d2:
        h2.Fill(val)
    h2.Draw('E')
    h1.Draw('E SAMES')
    h2.GetXaxis().SetTitle('Tempo [s]')
    h2.GetYaxis().SetTitle('occorrenze / 20e-9 ns')
    h1.SetLineColor(kBlue)
    h2.SetLineColor(kRed)
    
    leg1 = TLegend(.2,.6,.3,.7)
    leg1.SetBorderSize(1)
    leg1.SetFillColor(0)
    leg1.SetFillStyle(1001)
    leg1.SetTextFont(42)
    leg1.SetTextSize(0.035)
    leg1.SetTextAlign(22)
    leg1.AddEntry(h1,'T1','LE')
    leg1.AddEntry(h2,'T2','LE')
    leg1.Draw()

    infos1 = TPaveText(0.05,0.1,0.95,0.8, 'br')
    infos1.AddText('Presa dati 24/03/22')
    infos1.SetTextAlign(22)
    infos1.SetTextFont(42)
    infos1.SetTextSize(0.035)
    infos1.Draw()
    c1.Update()


    c2 = TCanvas('c2', 'c2', 1)
    c2.SetLogy()
    h12 = TH1F('T2-T1', 'Differenze tra eventi successivi di T1 e T2', 11, -20e-9, 200e-9)
    d1 = TH1F('D1', 'D1', 5, 0, 100e-9)
    
    for val in diff:
        h12.Fill(val)
    for val in out1:
        d1.Fill(val)
    
    h12.SetLineColor(kBlue)
    d1.SetLineColor(kRed)
    h12.GetXaxis().SetTitle('Tempo [s]')
    h12.GetYaxis().SetTitle('occorrenze / 20e-9 ns')
    h12.Draw('E')
    d1.Draw('E SAMES')
    infos2 = TPaveText(0.05,0.1,0.95,0.8, 'br')
    infos2.AddText('Presa dati 24/03/22')
    infos2.SetTextAlign(22)
    infos2.SetTextFont(42)
    infos2.SetTextSize(0.035)
    infos2.Draw()
    c2.Update()

    entr1 = h1.Integral(0, 5)
    entr2 = h2.Integral(0, 5)
    c2.Update()
    # print(entr1, entr2)