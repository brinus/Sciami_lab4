from unittest import result
from acceptance import *
import numpy as np
import matplotlib.pyplot as plt

ITER = int(1e2)
results = np.zeros((ITER))
for i in range(ITER):
    _, _, _, _, accep = simulation()
    results[i] = accep.sum()

# np.savetxt("results01.out", results)

string = f"""
$\mu$ = {np.mean(results)/REP:.3f}
$\sigma$ = {np.std(results)/REP:.3f}
"""

fig, ax = plt.subplots(1,1)
ax.hist(results, histtype="step", color="blue")
ax.set_xlabel("Particelle passate da 3 scintillatori ogni 1000 particelle")
ax.set_ylabel("Occorrenze")
ax.set_title("#Particelle/simulazione = 1000, #Ripetizioni simulazione = 1000")
ax.text(0.1,0.8,string, transform=ax.transAxes, 
    bbox=dict(boxstyle='round', facecolor='white', alpha=0.75))
plt.show()