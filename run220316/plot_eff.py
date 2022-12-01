import numpy as np
from ROOT import TCanvas, TPad, TH1F, TDatime, TLegend, TPaveText, gStyle

S = 1074/101

if __name__ == '__main__':

    out1 = np.loadtxt('data/out1_220316.out')
    out2 = np.loadtxt('data/out2_220316.out')
    out3 = np.loadtxt('data/out3_220316.out')
    out4 = np.loadtxt('data/out4_220316.out')
    out5 = np.loadtxt('data/out5_220316.out')
    out6 = np.loadtxt('data/out6_220316.out')
    out7 = np.loadtxt('data/out7_220316.out')
    out8 = np.loadtxt('data/out8_220316.out')

    MIN = np.double(out1.min())
    MAX = np.double(out1.max())
    minutes = 60
    NBINS = int((MAX - MIN) / (minutes * 60))

    # ROOT 
    da = TDatime(2022,3,16,12,33,25)
    gStyle.SetTimeOffset(da.Convert())
    gStyle.SetOptStat(0)

    h1 = TH1F('T1', 'T1', NBINS, MIN, MAX)
    h2 = TH1F('T2', 'T2', NBINS, MIN, MAX)
    h3 = TH1F('D12', 'D12', NBINS, MIN, MAX)
    h4 = TH1F('D13', 'D13', NBINS, MIN, MAX)
    h5 = TH1F('D23', 'D23', NBINS, MIN, MAX)
    h6 = TH1F('D65', 'D65', NBINS, MIN, MAX)
    h7 = TH1F('D64', 'D64', NBINS, MIN, MAX)
    h8 = TH1F('D54', 'D54', NBINS, MIN, MAX)
    
    for val in out1:
        h1.Fill(val)
    for val in out2:
        h2.Fill(val)
    for val in out3:
        h3.Fill(val)
    for val in out4:
        h4.Fill(val)
    for val in out5:
        h5.Fill(val)
    for val in out6:
        h6.Fill(val)
    for val in out7:
        h7.Fill(val)
    for val in out8:
        h8.Fill(val)


    h3 = h1 / (h3 * S)
    h4 = h1 / (h4 * S)
    h5 = h1 / (h5 * S)

    h6 = h2 / (h6 * S)
    h7 = h2 / (h7 * S)
    h8 = h2 / (h8 * S)

    c1 = TCanvas('c1', 'c1', 1)
    c1.Divide(1,2)
    
    c1.cd(1)
    h3.Draw('E')
    h4.Draw('E SAME')
    h5.Draw('E SAME')

    h3.SetLineColor(2)
    h4.SetLineColor(3)
    h5.SetLineColor(4)
    h3.GetXaxis().SetTimeDisplay(1)
    h3.GetXaxis().SetTitle('Data [gg/mm]')
    h3.GetYaxis().SetTitle('Efficienza #epsilon')
    h3.GetYaxis().SetRangeUser(0.2, 0.83)

    leg1 = TLegend(0.12, 0.15, 0.20,0.3, 'NDC')
    leg1.Clear()
    leg1.SetBorderSize(1)
    leg1.SetFillColor(0)
    leg1.SetFillStyle(1001)
    leg1.SetTextFont(42)
    leg1.SetTextSize(0.035)
    leg1.SetTextAlign(22)
    leg1.AddEntry(h3,'#epsilon(3)','LE')
    leg1.AddEntry(h4,'#epsilon(2)','LE')
    leg1.AddEntry(h5,'#epsilon(1)','LE')
    leg1.Draw()

    infos2 = TPaveText(0.15,0.75,0.35,0.87, 'nbNDC')
    infos2.AddText('RUN 16/03/22')
    infos2.AddText('PLOT 11/04/22')
    infos2.SetTextAlign(12)
    infos2.SetTextFont(42)
    infos2.SetTextSize(0.035)
    infos2.SetFillColor(0)
    infos2.Draw()
    
    c1.cd(2)
    h6.Draw('E')
    h7.Draw('E SAME')
    h8.Draw('E SAME')

    h6.SetLineColor(2)
    h7.SetLineColor(3)
    h8.SetLineColor(4)
    h6.GetXaxis().SetTimeDisplay(1)
    h6.GetXaxis().SetTitle('Data [gg/mm]')
    h6.GetYaxis().SetTitle('Efficienza #epsilon')
    h6.GetYaxis().SetRangeUser(0.40, 1)

    leg2 = TLegend(0.12, 0.15, 0.20,0.3, 'NDC')
    leg2.Clear()
    leg2.SetBorderSize(1)
    leg2.SetFillColor(0)
    leg2.SetFillStyle(1001)
    leg2.SetTextFont(42)
    leg2.SetTextSize(0.035)
    leg2.SetTextAlign(22)
    leg2.AddEntry(h6,'#epsilon(6)','LE')
    leg2.AddEntry(h7,'#epsilon(5)','LE')
    leg2.AddEntry(h8,'#epsilon(4)','LE')
    leg2.Draw()
    
    c1.Update()