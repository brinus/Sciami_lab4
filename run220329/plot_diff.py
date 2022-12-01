from matplotlib.pyplot import axis
import numpy as np
import sys
sys.path.append('..')
from read import make_out
from ROOT import TH1F

if __name__ == '__main__':
    ch, time, date, _, _ = make_out('events220329_test.dat')
    
    mask = (ch==1) | (ch==2) | (ch==3) | (ch==4)
    ch = ch[mask]
    time = time[mask]
    date = date[mask]

    channels = [1,2,3,4]
    out = np.array([time[ch==m] for m in channels], dtype='object')
    out = np.array([np.ediff1d(arr) for arr in out], dtype='object')

    h1 = TH1F('h1', 'h1', 100, 0, 1)
    h2 = TH1F('h2', 'h2', 100, 0, 1)
    h3 = TH1F('h3', 'h3', 100, 0, 1)
    h4 = TH1F('h4', 'h4', 100, 0, 1)

    for val in out[0]:
        h1.Fill(val)
    for val in out[1]:
        h2.Fill(val)
    for val in out[2]:
        h3.Fill(val)
    for val in out[3]:
        h4.Fill(val)


    print(h1.GetMaximum())
    print(h2.GetMaximum())
    print(h3.GetMaximum())
    print(h4.GetMaximum())
    h1.SetLineColor(3)
    h2.SetLineColor(4)
    h3.SetLineColor(5)
    h4.SetLineColor(6)
    h1.Draw('E SAMES')
    h2.Draw('E SAMES')
    h3.Draw('E SAMES')
    h4.Draw('E SAMES')