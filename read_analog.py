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
    return np.where( MASK, 0, 1)

def make_out(fname):
    '''Creates the output file in out and the differences between consecutive 
    elements of out in out_exp, it also gives the time, date and ch arrays corrected for time difference
    consistency. Takes as input the name of the .dat file.
    '''
    # Data reading, necessary arrays creation
    time, ch1, ch2, date = np.genfromtxt(fname, unpack=True, dtype=(float, float, float, 'datetime64[ms]'))

    time_roll = np.roll(time, -1)
    date_roll = np.roll(date, -1)
    is_dif = check_dif_np(time, time_roll, date, date_roll)
    corr = is_dif * (time + (date_roll-date)/np.timedelta64(1,'s') - time_roll)
    corr = np.roll(corr.cumsum(), 1)
    time = time + corr
    
    return time, ch1, ch2, date

if __name__ == '__main__':

    folder = 'run220401/'
    datafile = 'events220401a_5d.dat'
    _, ch1, ch2, _ = make_out(folder + datafile)

    # Saving results
    fname = 'analog1_' + datafile[6:12] + '.out'
    np.savetxt(folder + 'data/' + fname, ch1)
    fname = 'analog2_' + datafile[6:12] + '.out'
    np.savetxt(folder + 'data/' + fname, ch2)
