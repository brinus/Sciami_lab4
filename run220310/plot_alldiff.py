import numpy as np
from ROOT import TH1F, TF1, TRatioPlot, TCanvas, gStyle
if __name__ == '__main__':

    time = np.loadtxt('data/out2_220310.out')

    NBINS = 20
    MIN = 0
    MAX = 0.01

    # mesh = np.array(np.meshgrid(time[:10000], time[10000]))
    # combinations = mesh.T.reshape(-1, 2)
    # out = np.diff(combinations)

    out = []
    print(f'len(time) = {len(time)}')
    for idx in range(len(time[:1000000])-1):
        next = 1
        while time[idx+next] - time[idx] < 2 and idx+next < len(time)-1:
            out.append(time[idx+next] - time[idx])
            next += 1

    print('ROOT')
    c1 = TCanvas('c1', 'c1', 1)
    c1.SetLogy()
    h1 = TH1F('T1', 'T1-T1 events difference within 1 second', 50, 0.0, 2)
    for val in out:
        h1.Fill(val)
    h1.GetXaxis().SetTitle('Tempo [s]')
    h1.GetYaxis().SetTitle('occorrenze / bin [u.a.]')
    h1.Sumw2()
    h1.Draw()
    func1 = TF1('func1', '[0]', 0, 2)
    func1.SetParameters(0,1)
    h1.Fit('func1', 'LIRMS')
    gStyle.SetOptFit(1111)
    c1.Clear()

    rp = TRatioPlot(h1)
    rp.Draw()
    rp.GetLowerRefGraph().SetMinimum(-2);
    rp.GetLowerRefGraph().SetMaximum(2);
    c1.Update()

