import numpy as np
from matplotlib import pyplot as plt

if __name__ == '__main__':
    ch, time, date = np.genfromtxt("events220302_1d.dat", unpack=True, 
                                dtype=(int, float, 'datetime64[ms]'))

    mask1 = ch==1
    mask2 = ch==2

    time1 = time[mask1]
    time2 = time[mask2]
    date1 = date[mask1]
    date2 = date[mask2]

    limit = np.datetime64("2022-03-02T13")

    fig, ax = plt.subplots(2,1, sharex=True)
    ax[0].errorbar(date1[date1 < limit], time1[date1 < limit], fmt='.k', markersize=0.6)
    ax[1].errorbar(date2[date2 < limit], time2[date2 < limit], fmt='.k', markersize=0.6)
    ax[0].set_ylabel("FPGA timestamp [s]")
    ax[1].set_ylabel("FPGA timestamp [s]")
    ax[0].set_title("CHANNEL 1")
    ax[1].set_title("CHANNEL 2")
    ax[1].set_xlabel("Local time [dd hh:mm]")

    plt.show()