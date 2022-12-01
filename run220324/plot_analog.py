import numpy as np
from ROOT import TH1F, THStack, TCanvas, TGraph
from ROOT import TDatime, gStyle, TLatex

ch1 = np.loadtxt('data/analog1_220324.out')
ch2 = np.loadtxt('data/analog2_220324.out')
ch3 = np.loadtxt('../run220323/data/analog2_220323.out')

MIN = min([ch1.min(), ch2.min(), ch3.min()]) 
MAX = max([ch1.max(), ch2.max(), ch3.max()])
NBINS = 50

h1 = TH1F('h1', 'h1', 20, MIN, MAX)
h2 = TH1F('h2', 'h2', 20, MIN, MAX)
h3 = TH1F('h3', 'h3', 200, MIN, MAX)

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

c1 = TCanvas('c1', 'c1', 1)
h3.Draw()
c2 = TCanvas('c2', 'c2', 1)
h1.Draw()
h2.Draw('SAMES')
h1.SetLineColor(4)
h2.SetLineColor(2)
