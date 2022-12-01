import numpy as np


def check_dif_np(t1, t2, d1, d2):
    ''' Check consistency between difference in consecutive times and consecutive dates.
    Consistency is checked by creating a time interval with the two dates and an addition of 1 
    second at the extremities to account for low precision and retards on the FPGA writing speed.
    Returns an array made of 1 where there are unconsistencies, 0 otherwise.
    '''
    DELTAp = d2 - d1 + np.timedelta64(1, 's')
    DELTAm = d2 - d1 - np.timedelta64(1, 's')
    arr = np.array((abs(t1-t2)*1e9).astype(int), dtype='timedelta64[ns]')
    MASK = (DELTAm < arr) & (DELTAp > arr)
    return np.where(MASK, 0, 1)


def make_out(fname):
    '''Creates the output file in out and the differences between consecutive 
    elements of out in out_exp, it also gives the time, date and ch arrays corrected for time difference
    consistency. Takes as input the name of the .dat file.
    '''
    # Data reading, necessary arrays creation
    ch, time, date = np.genfromtxt(
        fname, unpack=True, dtype=(int, float, 'datetime64[ms]'))

    channels = np.unique(ch)
    mask = np.array([ch == idx for idx in channels])
    time_roll = np.roll(time, -1)
    date_roll = np.roll(date, -1)
    is_dif = check_dif_np(time, time_roll, date, date_roll)
    corr = is_dif * (time + (date_roll-date) /
                     np.timedelta64(1, 's') - time_roll)
    corr = np.roll(corr.cumsum(), 1)
    time = time + corr

    out = np.array([time[m] for m in mask], dtype='object')
    out_exp = np.array([np.ediff1d(arr) for arr in out], dtype='object')

    return ch, time, date, out, out_exp


if __name__ == '__main__':

    folder = 'run220329/'
    datafile = 'events220329_3d.dat'
    _, _, _, out, out_exp = make_out(folder + datafile)

    # Saving results
    for idx, arr in enumerate(out):
        if arr.size != 0:
            fname = 'out' + str(idx + 1) + '_' + datafile[6:12] + '.out'
            np.savetxt(folder + 'data/' + fname, arr)

    for idx, arr in enumerate(out_exp):
        if arr.size != 0:
            fname = 'outexp' + str(idx + 1) + '_' + datafile[6:12] + '.out'
            np.savetxt(folder + 'data/' + fname, arr)
