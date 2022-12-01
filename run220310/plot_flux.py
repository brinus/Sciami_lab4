import numpy as np
from ROOT import Math
from ROOT import TCanvas, TH1F, TF1
from ROOT import gStyle
from ROOT import TPaveText, TDatime

def func1(x):
    return 1.72e4
def func2(x):
    return 3.44e4

if __name__ == '__main__':

    out1 = np.loadtxt('data/out1_220310.out')
    out2 = np.loadtxt('data/out2_220310.out')

    MIN = np.double(np.min(out1))
    MAX = np.double(np.max(out1))
    minutes = 60 # minutes per bin
    NBINS = int((MAX - MIN) / (minutes * 60))

    print(NBINS)

    da = TDatime(2022,3,10,18,15,29)
    gStyle.SetTimeOffset(da.Convert())
    c1 = TCanvas('c1','c1',600,800)
    c1.Divide(1,2)
    c1.cd(1)

    h1 = TH1F('TEL1','Flusso di raggi cosmici TEL1',NBINS,MIN,MAX)
    h1.GetYaxis().SetTitle('occorrenze / bin')
    h1.GetXaxis().SetTimeDisplay(1)

    for val in out1:
        h1.Fill(val)
    k1 = TF1('k1', '[0]', MIN, MAX)
    k1.SetParameters(0,1)
    h1.Fit('k1', 'LIRMS')

    testfunc = Math.Functor1D(func1)
    GoF = Math.GoFTest(len(out1), out1, testfunc, Math.GoFTest.kPDF, MIN, MAX)
    dn_1 = GoF.KolmogorovSmirnovTest('t')
    pvalue_1 = GoF.KolmogorovSmirnovTest()

    print(f'p-value: {pvalue_1}\nD statistic: {dn_1}')

    gStyle.SetOptStat('ne')
    gStyle.SetOptFit(1111)
    h1.Draw('E')
    
    infos = TPaveText(0.3,0.75,0.5,0.87, 'nbNDC')
    infos.AddText('RUN 10/03/22')
    infos.AddText('PLOT 10/04/22')
    infos.SetTextAlign(12)
    infos.SetTextFont(42)
    infos.SetTextSize(0.04)
    infos.SetFillColor(0)
    infos.Draw()

    c1.cd(2)
    h2 = TH1F('TEL2','Flusso di raggi cosmici TEL2',NBINS,MIN,MAX)
    h2.GetXaxis().SetTitle('time (s)')
    for val in out2:
        h2.Fill(val)
    k2 = TF1('k2', '[0]', MIN, MAX)
    k2.SetParameters(0,1)
    h2.Fit('k2', 'LIRMS')
    h2.GetXaxis().SetTimeDisplay(1)


    testfunc = Math.Functor1D(func2)
    GoF = Math.GoFTest(len(out2), out2, testfunc, Math.GoFTest.kPDF, MIN, MAX)
    dn_2 = GoF.KolmogorovSmirnovTest('t')
    pvalue_2 = GoF.KolmogorovSmirnovTest()

    print(f'p-value: {pvalue_2}\nD statistic: {dn_2}')

    gStyle.SetOptStat('ne')
    gStyle.SetOptFit(1111)
    h2.Draw('E')

    c1.Update()