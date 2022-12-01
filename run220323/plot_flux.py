import numpy as np
from ROOT import TH1F, THStack, TCanvas, TGraph

S = 1074/101

if __name__ == '__main__':

    out = np.array([np.loadtxt(f'data/out{idx}_220323.out') for idx in range(1,9)], dtype='object')

    MIN = out[0].min()
    MAX = out[0].max()
    minutes = 60 # minutes per bin
    NBINS = int((MAX - MIN) / (minutes * 60))

    print(f'NBINS = {NBINS}\nMIN = {MIN}\nMAX = {MAX}')
    for idx, val in enumerate(out):
        print(f'len(CH{idx + 1}) = {len(val)}')

    # ROOT
    c1 = TCanvas('c1', 'c1', 1)
    c2 = TCanvas('c2', 'c2', 1)
    c1.cd()
    hs = THStack('hs', 'Flusso di raggi cosmici nei due telescopi')
    h1 = TH1F('h1', 'h1', NBINS, MIN, MAX)
    h2 = TH1F('h2', 'h2', NBINS, MIN, MAX)
    h3 = TH1F('h3', 'h3', NBINS, MIN, MAX)
    h4 = TH1F('h4', 'h4', NBINS, MIN, MAX)
    h5 = TH1F('h5', 'h5', NBINS, MIN, MAX)
    h6 = TH1F('h6', 'h6', NBINS, MIN, MAX)
    h7 = TH1F('h7', 'h7', NBINS, MIN, MAX)
    h8 = TH1F('h8', 'h8', NBINS, MIN, MAX)
    hT1 = TH1F('ht1', 'ht1', NBINS, MIN, MAX)
    hT2 = TH1F('ht2', 'ht2', NBINS, MIN, MAX)

    for val in out[0]:
        h1.Fill(val)
    for val in out[1]:
        h2.Fill(val)
    for val in out[2]:
        h3.Fill(val)
    for val in out[3]:
        h4.Fill(val)
    for val in out[4]:
        h5.Fill(val)
    for val in out[5]:
        h6.Fill(val)
    for val in out[6]:
        h7.Fill(val)
    for val in out[7]:
        h8.Fill(val)

    hT1 = h3 * h4 * h5 / (h1 * h1)
    hT2 = h6 * h7 * h8 / (h2 * h2)

    hT1.Scale(S*S*S)
    hT2.Scale(S*S*S) 

    for idx in range(NBINS):
        if (h1.GetBinContent(idx)!=0 and 
            h3.GetBinContent(idx)!=0 and 
            h4.GetBinContent(idx)!=0 and 
            h5.GetBinContent(idx)!=0):
            hT1.SetBinError(idx, (h3.GetBinError(idx)/h3.GetBinContent(idx) + 
                                h4.GetBinError(idx)/h4.GetBinContent(idx) + 
                                h5.GetBinError(idx)/h5.GetBinContent(idx) + 
                                2 * (h1.GetBinError(idx)/h1.GetBinContent(idx))) * 
                                hT1.GetBinContent(idx))

    for idx in range(NBINS):
        if (h2.GetBinContent(idx)!=0 and 
            h6.GetBinContent(idx)!=0 and 
            h7.GetBinContent(idx)!=0 and 
            h8.GetBinContent(idx)!=0):
            hT2.SetBinError(idx, (h6.GetBinError(idx)/h6.GetBinContent(idx) + 
                                h7.GetBinError(idx)/h7.GetBinContent(idx) + 
                                h8.GetBinError(idx)/h8.GetBinContent(idx) + 
                                2 * (h2.GetBinError(idx)/h2.GetBinContent(idx))) * 
                                hT2.GetBinContent(idx))


    hs.Add(hT1)
    hs.Add(hT2)
    hs.Draw()
    hs.GetXaxis().SetTimeDisplay(1)
    hs.GetXaxis().SetTitle('Data [giorno/mese]')
    hs.GetYaxis().SetTitle('Eventi [h^{-1}]')
    c1.SetGrid()
    c1.Update()

    c2.cd()

    T1_entries = np.array([hT1.GetBinContent(bin) for bin in range(NBINS)])
    T2_entries = np.array([hT2.GetBinContent(bin) for bin in range(NBINS)])

    h_corr = TGraph(NBINS, T1_entries, T2_entries)
    h_corr.SetMarkerStyle(20)
    h_corr.Draw('ap')