import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt


FLUXES = Path.home()/"software"/"snowglobes"/"fluxes"

def create_garching_fluence():

    file_pinched_0 = FLUXES/"garching_fluxes"/"pinched_0.dat"

    pinched_0 = np.loadtxt(file_pinched_0)

    energy_template = pinched_0[:, 0]

    bins = len(energy_template)

    nue_fluence = np.zeros(bins)
    numu_fluence = np.zeros(bins)
    nutau_fluence = np.zeros(bins)

    nuebar_fluence = np.zeros(bins)
    numubar_fluence = np.zeros(bins)
    nutaubar_fluence = np.zeros(bins)


    for i in range(300):
        file_pinched = FLUXES/"garching_fluxes"/f"pinched_{i}.dat"
        pinched = np.loadtxt(file_pinched)

        nue_fluence += pinched[:, 1]
        numu_fluence += pinched[:, 2]
        nutau_fluence += pinched[:, 3]

        nuebar_fluence += pinched[:, 4]
        numubar_fluence += pinched[:, 5]
        nutaubar_fluence += pinched[:, 6]

    output = np.column_stack((energy_template, nue_fluence, numu_fluence, nutau_fluence, nuebar_fluence, numubar_fluence, nutaubar_fluence))
    outfile = FLUXES/"garching.dat"


    np.savetxt(outfile, output, fmt = "%.6e")
    print(np.sum(pinched_0[:, 1]))
    print(np.sum(nue_fluence))




def plot_livermore_garching():
    
    file_livermore = FLUXES/"livermore.dat"
    file_garching = FLUXES/"garching.dat"

    livermore = np.loadtxt(file_livermore)
    garching = np.loadtxt(file_garching)

    energies = livermore[:, 0]*1000 #in MeV

    nue_livermore = livermore[:, 4]
    nue_garching = garching[:, 4]

    print(len(energies))
    plt.plot(energies, nue_livermore, label = "livermore")
    plt.plot(energies, nue_garching, label = "garching")
    plt.legend()
    plt.xlabel("E [MeV]")
    plt.ylabel(r"Fluence [cm$^{-2}$] per 0.2 MeV bin")
    plt.title(r"livermore/garching $\nu_e$ fluence comparison")
    plt.grid(alpha = 0.3)
    plt.savefig("debug_plot/livermore_garching_comparison.png")


if __name__ == "__main__":
    plot_livermore_garching()
