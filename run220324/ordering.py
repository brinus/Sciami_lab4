import numpy as np
from ROOT import TCanvas, TH1F, TLegend, TPaveText

def orderXY(time, ch, channels):
    mask = (ch==channels[0]) | (ch==channels[1])
    ch = ch[mask]
    ch[ch==channels[0]] = 1
    ch[ch==channels[1]] = 2
    time = time[mask]
    diff = (ch - np.roll(ch, -1)) * (time - np.roll(time, -1))
    return diff

def ordering(time, ch, channels, triple):
    out = np.zeros((3,3))
    out_ld = np.array([])
    delta = 3 * 20e-9
    mask = (ch==channels[0]) | (ch==channels[1]) | (ch==channels[2])
    for val in triple[:1000]:
        mmm = (time >= val - delta) & (time <= val + delta) & mask
        ch_window = ch[mmm]
        time_window = time[mmm]
        if len(ch_window) == 3 and np.ediff1d(time_window).sum() > 0. :
            print(time_window)
            print(np.ediff1d(time_window))
            out_ld = np.append(out_ld, np.ediff1d(time[mmm])[-1])
            ch_window[ch_window==channels[0]] = 0
            ch_window[ch_window==channels[1]] = 1
            ch_window[ch_window==channels[2]] = 2
            for idx, val in enumerate(ch_window):
                out[idx][val] += 1
    return out, out_ld

if __name__ == '__main__':

    ch, time = np.loadtxt('data/out_.out', unpack=True)
    ch = ch.astype(int)
    time = np.around(time, 8)

    # Differenze doppie
    T1D34 = orderXY(time, ch, [3,4])
    T1D35 = orderXY(time, ch, [3,5])
    T1D45 = orderXY(time, ch, [4,5])
    T2D67 = orderXY(time, ch, [6,7])
    T2D68 = orderXY(time, ch, [6,8])
    T2D78 = orderXY(time, ch, [7,8])    

    # Ordine di arrivo
    # print('ord1')
    # orders1, last_dT1 = ordering(time, ch, [3,4,5], time[ch==1])
    # print('ord2')
    # orders2, last_dT2 = ordering(time, ch, [6,7,8], time[ch==2])
    # print(orders1)
    # print(orders2)
    
    # ROOT
    NBINS = 10
    MIN = -100e-9
    MAX = 100e-9

    c1 = TCanvas('c1', 'c1', 800, 600)
    c1.SetTitle('ciao')
    c1.Divide(2,1)
    
    c1.cd(1)
    h34 = TH1F('D34', 'D34', NBINS, MIN, MAX)
    h35 = TH1F('D35', 'Differenze tra doppie di T1', NBINS, MIN, MAX)
    h45 = TH1F('D45', 'D45', NBINS, MIN, MAX)
    for val in T1D34:
        h34.Fill(val)
    for val in T1D35:
        h35.Fill(val)
    for val in T1D45:
        h45.Fill(val)
    hsum1 = h34+h35+h45
    hsum1.Draw()
    # h35.Draw('E')
    # h34.Draw('E SAMES')
    # h45.Draw('E SAMES')
    # h34.SetLineColor(2)
    # h35.SetLineColor(3)
    # h45.SetLineColor(4)
    # h34.GetXaxis().SetTitle('Tempo [s]')
    # h34.GetYaxis().SetTitle('Eventi / 20e-9s')

    # leg1 = TLegend(.2,.6,.3,.7)
    # leg1.SetBorderSize(1)
    # leg1.SetFillColor(0)
    # leg1.SetFillStyle(1001)
    # leg1.SetTextFont(42)
    # leg1.SetTextSize(0.035)
    # leg1.SetTextAlign(22)
    # leg1.AddEntry(h34,'D34','LE')
    # leg1.AddEntry(h35,'D35','LE')
    # leg1.AddEntry(h45,'D45','LE')
    # leg1.Draw()
    # infos = TPaveText(0.3,0.75,0.5,0.87, 'nbNDC')
    # infos.AddText('RUN 24/03/22')
    # infos.AddText('PLOT 08/04/22')
    # infos.SetTextAlign(12)
    # infos.SetTextFont(42)
    # infos.SetTextSize(0.04)
    # infos.SetFillColor(0)
    # infos.Draw()
    c1.Update()

    c1.cd(2)
    h67 = TH1F('D67', 'Differenze tra doppie di T2', NBINS, MIN, MAX)
    h68 = TH1F('D68', 'D68', NBINS, MIN, MAX)
    h78 = TH1F('D78', 'D78', NBINS, MIN, MAX)
    for val in T2D67:
        h67.Fill(val)
    for val in T2D68:
        h68.Fill(val)
    for val in T2D78:
        h78.Fill(val)
    hsum2 = h67+h68+h78
    hsum2.Draw()
    # h67.Draw('E')
    # h68.Draw('E SAMES')
    # h78.Draw('E SAMES')
    # h67.SetLineColor(2)
    # h68.SetLineColor(3)
    # h78.SetLineColor(4)  
    # h67.GetXaxis().SetTitle('Tempo [s]')
    # # h67.GetYaxis().SetTitle('Eventi / 20e-9s')  
    
    # leg2 = TLegend(.2,.6,.3,.7)
    # leg2.SetBorderSize(1)
    # leg2.SetFillColor(0)
    # leg2.SetFillStyle(1001)
    # leg2.SetTextFont(42)
    # leg2.SetTextSize(0.035)
    # leg2.SetTextAlign(22)
    # leg2.AddEntry(h67,'D67','LE')
    # leg2.AddEntry(h68,'D68','LE')
    # leg2.AddEntry(h78,'D78','LE')
    # leg2.Draw()
    # c1.Update()
    
    # c2 = TCanvas('c2', 'c2', 1)
    # hLD1 = TH1F('LD1', 'LD1', NBINS, MIN, MAX)
    # hLD2 = TH1F('LD2', 'LD2', NBINS, MIN, MAX)
    # for val in last_dT1:
    #     hLD1.Fill(val)
    # for val in last_dT2:
    #     hLD2.Fill(val)
    # hLD1.SetLineColor(2)
    # hLD2.SetLineColor(3)
    # hLD1.Draw('E')
    # hLD2.Draw('E SAMES')

    # leg3 = TLegend(.2,.6,.3,.7)
    # leg3.SetBorderSize(1)
    # leg3.SetFillColor(0)
    # leg3.SetFillStyle(1001)
    # leg3.SetTextFont(42)
    # leg3.SetTextSize(0.035)
    # leg3.SetTextAlign(22)
    # leg3.AddEntry(hLD1,'hLD1','LE')
    # leg3.AddEntry(hLD2,'hLD2','LE')
    # leg3.Draw()
    # c2.Update()