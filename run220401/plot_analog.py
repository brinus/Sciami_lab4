import numpy as np
from ROOT import TH1F, TCanvas
from ROOT import gStyle, TLegend, TPaveText

ch1 = np.loadtxt('data/analog1_220401.out')
ch2 = np.loadtxt('data/analog2_220401.out')
ch3 = np.loadtxt('../run220323/data/analog2_220323.out')

MIN = min([ch1.min(), ch2.min(), ch3.min()]) 
MAX = max([ch1.max(), ch2.max(), ch3.max()])

NBINS = 60

h1 = TH1F('Energia SUM(PMT(4,5,6))', 'h1', NBINS, MIN, MAX)
h2 = TH1F('Energia PMT4', 'h2', NBINS, MIN, MAX)
h3 = TH1F('Energia PMT1', 'Energia rilasciata nei PMT', NBINS, MIN, MAX)

for val in ch1:
    if val != 0:
        h1.Fill(val)
for val in ch2:
    if val != 0:
        h2.Fill(val)
for val in ch3:
    if val != 0:
        h3.Fill(val)

# FWHM CH1
bin1 = h1.FindFirstBinAbove(h1.GetMaximum()/2)
bin2 = h1.FindLastBinAbove(h1.GetMaximum()/2);
fwhm1 = h1.GetBinCenter(bin2) - h1.GetBinCenter(bin1);

# FWHM CH2
bin1 = h2.FindFirstBinAbove(h2.GetMaximum()/2)
bin2 = h2.FindLastBinAbove(h2.GetMaximum()/2);
fwhm2 = h2.GetBinCenter(bin2) - h2.GetBinCenter(bin1);

print(f'FWHM1 = {fwhm1}\nFWHM2 = {fwhm2}\n')

c2 = TCanvas('c2', 'c2', 1)
h3.Draw()
h1.Draw('SAMES')
h2.Draw('SAMES')

h3.SetLineColor(3)
h1.SetLineColor(4)
h2.SetLineColor(2)

leg1 = TLegend(0.12, 0.15, 0.20,0.3, 'NDC')
leg1.Clear()
leg1.SetBorderSize(1)
leg1.SetFillColor(0)
leg1.SetFillStyle(1001)
leg1.SetTextFont(42)
leg1.SetTextSize(0.035)
leg1.SetTextAlign(22)
leg1.AddEntry(h1,'PMT 4','LE')
leg1.AddEntry(h2,'SUM(PMT(4,5,6))','LE')
leg1.AddEntry(h3, 'PMT 1', 'LE')
leg1.Draw()

infos = TPaveText(0.3,0.65,0.5,0.87, 'nbNDC')
infos.AddText('PMT 1: RUN 23/03/22 TRIG T1')
infos.AddText('PMT 4: RUN 01/04/22 TRIG T1#wedgeT2')
infos.AddText('SUM(PMT(4,5,6)): RUN 01/04/22 TRIG T1#wedgeT2')
infos.AddText('PLOT 11/04/22')
infos.SetTextAlign(12)
infos.SetTextFont(42)
infos.SetTextSize(0.04)
infos.SetFillColor(0)
infos.Draw()