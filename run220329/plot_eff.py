import numpy as np
from ROOT import TCanvas, TH1F, TDatime, TLegend, TPaveText, gStyle

S = 115.3/10.4

if __name__ == '__main__':

    out1 = np.loadtxt('data/out1_220324.out')
    out2 = np.loadtxt('data/out2_220324.out')
    out3 = np.loadtxt('data/out3_220324.out')
    out4 = np.loadtxt('data/out4_220324.out')
    out5 = np.loadtxt('data/out5_220324.out')
    out6 = np.loadtxt('data/out6_220324.out')
    out7 = np.loadtxt('data/out7_220324.out')
    out8 = np.loadtxt('data/out8_220324.out')

    MIN = np.double(out1.min())
    MAX = np.double(out1.max())
    minutes = 60
    NBINS = int((MAX - MIN) / (minutes * 60))

    # ROOT 
    da = TDatime(2022,3,24,18,44,30)
    gStyle.SetTimeOffset(da.Convert())

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
    h3.GetYaxis().SetTitle('Eventi [h^{-1}]')
    h3.GetYaxis().SetRangeUser(0.20, 0.82)
    
    c1.cd(2)
    h6.Draw('E')
    h7.Draw('E SAME')
    h8.Draw('E SAME')

    h6.SetLineColor(2)
    h7.SetLineColor(3)
    h8.SetLineColor(4)
    h6.GetXaxis().SetTimeDisplay(1)
    h6.GetXaxis().SetTitle('Data [gg/mm]')
    h6.GetYaxis().SetTitle('Eventi [h^{-1}]')
    h6.GetYaxis().SetRangeUser(0.40, 1)
    
    c1.Update()