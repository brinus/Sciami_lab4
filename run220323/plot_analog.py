import numpy as np
from ROOT import TH1F, THStack, TCanvas, TGraph
from ROOT import TDatime, gStyle, TLatex

# ch1 = np.loadtxt('data/analog1_220323.out')
ch2 = np.loadtxt('data/analog2_220323.out')

MIN = ch2.min()
MAX = ch2.max()
NBINS = 100

h1 = TH1F('h1', 'h1', NBINS, MIN, MAX)
h2 = TH1F('h2', 'h2', NBINS, MIN, MAX)

for val in ch2:
    h2.Fill(val)

# FWHM CH2
bin1 = h2.FindFirstBinAbove(h2.GetMaximum()/2)
bin2 = h2.FindLastBinAbove(h2.GetMaximum()/2);
fwhm2 = h2.GetBinCenter(bin2) - h2.GetBinCenter(bin1);

print(f'FWHM2 = {fwhm2}\n')

h2.Draw()