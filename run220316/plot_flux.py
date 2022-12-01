import numpy as np
from ROOT import TH1F, TCanvas, TGraph, TLegend, TF1
from ROOT import TDatime, gStyle, kBlue, kRed, TPaveText

S = 1074/101

if __name__ == '__main__':

    da = TDatime(2022,3,16,12,33,25)
    gStyle.SetTimeOffset(da.Convert())
    out = np.array([np.loadtxt(f'data/out{idx}_220316.out') for idx in range(1,9)], dtype='object')

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
    c3 = TCanvas('c3', 'c3', 1)
    
    # Flusso
    c1.cd()
    gStyle.SetOptStat(0)
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

    hT1.Draw('E')
    hT2.Draw('E SAMES')
    hT1.SetTitle('Flusso di raggi cosmici nei due telescopi')
    hT1.SetLineColor(kBlue)
    hT2.SetLineColor(kRed)
    hT1.GetXaxis().SetTimeDisplay(1)
    hT1.GetXaxis().SetTitle('Data [gg/mm]')
    hT1.GetYaxis().SetTitle('Eventi [h^{-1}]')
    c1.SetGrid()

    print(f'hT1 = {hT1.GetMean(2)/3600} +- {hT1.GetMeanError(2)/3600}')
    print(f'hT2 = {hT2.GetMean(2)/3600} +- {hT2.GetMeanError(2)/3600}')

    leg1 = TLegend(0.12, 0.15, 0.20,0.3, 'NDC')
    leg1.Clear()
    leg1.SetBorderSize(1)
    leg1.SetFillColor(0)
    leg1.SetFillStyle(1001)
    leg1.SetTextFont(42)
    leg1.SetTextSize(0.035)
    leg1.SetTextAlign(22)
    leg1.AddEntry(hT1,'T1','LE')
    leg1.AddEntry(hT2,'T2','LE')
    leg1.Draw()

    infos = TPaveText(0.3,0.75,0.5,0.87, 'nbNDC')
    infos.AddText('RUN 16/03/22')
    infos.AddText('PLOT 07/04/22')
    # infos.AddText('T1 frequency = 81.57#pm0.37 Hz')
    # infos.AddText('T2 frequency = 73.53#pm0.35 Hz')
    infos.SetTextAlign(12)
    infos.SetTextFont(42)
    infos.SetTextSize(0.04)
    infos.SetFillColor(0)
    infos.Draw()
    
    c1.Update()

    # Correlazione
    c2.cd()
    gStyle.SetOptFit(1111), gStyle.SetStatBorderSize(0)
    gStyle.SetStatX(.89), gStyle.SetStatY(.37)
    T1_entries = np.array([hT1.GetBinContent(bin) for bin in range(NBINS)])
    T2_entries = np.array([hT2.GetBinContent(bin) for bin in range(NBINS)])

    T1_entries = T1_entries[T1_entries != 0]
    T2_entries = T2_entries[T2_entries != 0]
    
    g_corr = TGraph(NBINS, T1_entries, T2_entries)
    g_corr.Draw('ap')
    g_corr.SetMarkerStyle(23)
    g_corr.SetMarkerColor(6)
    g_corr.SetTitle('Correlazione fra i due telescopi')
    g_corr.GetXaxis().SetTitle('T1 entries [eventi #upoint h^{-1}]')
    g_corr.GetYaxis().SetTitle('T2 entries [eventi #upoint h^{-1}]')
    func = TF1('f1', '[0] * x +[1]', 35e3, 150e3)
    func.SetParNames('m', 'q')
    g_corr.Fit('f1', 'FMRS')

    leg2 = TLegend(0.12, 0.15, 0.26,0.33, 'NDC')
    leg2.Clear()
    leg2.SetBorderSize(1)
    leg2.SetFillColor(0)
    leg2.SetFillStyle(1001)
    leg2.SetTextFont(42)
    leg2.SetTextSize(0.035)
    leg2.SetTextAlign(22)
    leg2.AddEntry(g_corr,'corr(T1,T2)','P')
    leg2.AddEntry(func, 'best-fit', 'L')
    leg2.Draw()

    infos2 = TPaveText(0.15,0.75,0.35,0.87, 'nbNDC')
    infos2.AddText('RUN 16/03/22')
    infos2.AddText('PLOT 07/04/22')
    infos2.AddText('Funzione di fit: y = mx + q')
    infos2.SetTextAlign(12)
    infos2.SetTextFont(42)
    infos2.SetTextSize(0.035)
    infos2.SetFillColor(0)
    infos2.Draw()

    # Rapporto
    c3.cd()
    gStyle.SetOptStat(0)
    h_ratio = hT1 / hT2
    for idx in range(NBINS):
        if (h1.GetBinContent(idx)!=0 and 
            h2.GetBinContent(idx)!=0):
            h_ratio.SetBinError(idx, (h1.GetBinError(idx)/h1.GetBinContent(idx) +
                                    h2.GetBinError(idx)/h2.GetBinContent(idx)) * 
                                    h_ratio.GetBinContent(idx)) 

    h_ratio.Draw('E')
    h_ratio.SetTitle('Rapporto tra eventi [h^{-1}] dei dei due telescopi')
    h_ratio.GetXaxis().SetTimeDisplay(1)
    h_ratio.GetXaxis().SetTitle('Data [gg/mm]')
    h_ratio.GetYaxis().SetTitle('T1 / T2 [u.a.]')

    infos3 = TPaveText(0.15,0.75,0.35,0.87, 'nbNDC')
    infos3.AddText('RUN 16/03/22')
    infos3.AddText('PLOT 07/04/22')
    infos3.SetTextAlign(12)
    infos3.SetTextFont(42)
    infos3.SetTextSize(0.04)
    infos3.SetFillColor(0)
    infos3.Draw()