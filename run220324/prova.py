import numpy as np
from ROOT import TH1F

a = np.array([0,0,0,1,1,2,3])

h1 = TH1F('h10', 'h1', 5, 0, 5)
for val in a:
    h1.Fill(val)
h1.Draw('E')