import numpy as np
import sys
sys.path.append('..')
from read import make_out

ch, time, _, _, _ = make_out('events220316_6d.dat')
np.savetxt('data/out_.out', np.c_[ch, time])