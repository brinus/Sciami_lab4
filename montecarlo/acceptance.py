import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from itertools import product, combinations
from random import randint, choice

Lx = 20 # cm
Ly = 40 # cm
S = 3 # cm
D = 7 # cm
Lz = 2 * D + S # cm
DIAG = np.sqrt(Lx**2 + Ly**2 + Lz**2) # cm
STEPS = int(1e3) #s
REP = int(500) # Number of repetitions

def rand_z():
    z = np.random.uniform(0, Lz)
    return z

def rand_pos(z):
    if z <= S: 
        x = np.random.uniform(0, Lx)
        y = np.random.uniform(0, Ly)
        face = 4
    else:
        face = np.random.choice([0,1,2,3])
        if face == 0:
            x = np.random.uniform(0,Lx)
            y = 0
        elif face == 1:
            x = Lx
            y = np.random.uniform(0, Ly) 
        elif face == 2:
            x = np.random.uniform(0, Lx)
            y = Ly
        elif face == 3:
            x = 0
            y = np.random.uniform(0, Ly)
    return x, y, face 

def rand_vel(idx):
    phi = np.random.uniform(0, 2 * np.pi)
    face = [lambda x: np.sin(x), lambda x: -np.cos(x), lambda x: -np.sin(x), lambda x: np.cos(x), lambda x: 1]
    while face[idx](phi) < 0:
        phi = np.random.uniform(0, 2 * np.pi)
    theta = np.abs(np.random.normal(0, np.pi / 4))
    while theta > np.pi / 2:
        theta = np.abs(np.random.normal(0, np.pi / 4))
    return phi, theta

def check():
    z = rand_z()
    x, y, face = rand_pos(z)
    phi, theta = rand_vel(face)
    time = np.linspace(0, DIAG, STEPS)
    x_t = x + (np.sin(theta) * np.cos(phi)) * time
    y_t = y + (np.sin(theta) * np.sin(phi)) * time
    z_t = z + (np.cos(theta)) * time
    check_z = (z_t > Lz - S) & (z_t < Lz)
    check_x = (x_t > 0) & (x_t < Lx)
    check_y = (y_t > 0) & (y_t < Ly)
    check_x = np.intersect1d(x_t[check_x], x_t[check_z]).size
    check_y = np.intersect1d(y_t[check_y], y_t[check_z]).size
    if (check_x != 0) and (check_y != 0) and (z <= S):
        return x_t, y_t, z_t, [theta, phi], 1
    else:
        return x_t, y_t, z_t, [theta, phi], 0 


def simulation():
    x_fin = np.zeros((REP,STEPS))
    y_fin = np.zeros((REP,STEPS))
    z_fin = np.zeros((REP,STEPS))
    angles = np.zeros((REP, 2))
    accep = np.zeros(REP)
    for i in range(REP):
        x_fin[i], y_fin[i], z_fin[i], angles[i], accep[i] = check()
    return x_fin, y_fin, z_fin, angles, accep

if __name__ == "__main__":

    x_fin, y_fin, z_fin, angles, accep = simulation()
    print(f"Acceptance = {accep.sum()}/{REP}")

    # fig, ax = plt.subplots(1,1)
    # ax.hist(angles[:,1], 20)
    # plt.show()

    # Scintillatori 
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    cmap_r = plt.get_cmap("Reds")
    cmap_b = plt.get_cmap("Blues")
    xx = [0, Lx]
    yy = [0, Ly]
    zzz = [[0, S], [D, D+S], [2*D,2*D+S]]

    ax.set_box_aspect((np.ptp([0,Lx]),np.ptp([0,Ly]),np.ptp([0,Lz])))
    for zz in zzz:
        for s, e in combinations(np.array(list(product(xx, yy, zz))), 2):
            if np.sum(np.abs(s-e)) == xx[1]-xx[0] or np.sum(np.abs(s-e)) == yy[1]-yy[0] or np.sum(np.abs(s-e)) == zz[1]-zz[0]:
                ax.plot3D(*zip(s, e), color="b", linewidth=2)
            
    for i in range(REP):
        if accep[i] == 1:
            ax.plot(x_fin[i], y_fin[i], z_fin[i],'-',linewidth=0.8, color="red", alpha=1)
        else:
            ax.plot(x_fin[i], y_fin[i], z_fin[i],'-',linewidth=0.8, color="blue", alpha=1)

    # ax.set_xlabel("X")
    # ax.set_ylabel("Y")
    # ax.set_zlabel("Z")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])
    ax.set_xlim(0, Lx)
    ax.set_ylim(0, Ly)
    ax.set_zlim(0, Lz)
    # ax.set_title(f"Lx=40 cm, Ly=45 cm, S=2 cm, D=4 cm\nREP=100, acceptance = {accep.sum()}/{REP}")
    elevation_angle = choice([randint(-180,-160),randint(160,180)])
    azimutal_angle = randint(0, 360)
    ax.view_init(elev = elevation_angle, azim = azimutal_angle)
    PATH = f"/Users/matteobrini/Documents/NFT/Acceptance/acceptance_{int(accep.sum())}:{REP}.png"
    fig.savefig(PATH, format = "png", dpi = 1200)
