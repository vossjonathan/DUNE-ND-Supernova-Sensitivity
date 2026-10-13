import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt

#local SNOwGLoBES installation
FLUXES = Path.home()/"software"/"snowglobes"/"fluxes"

REPO_ROOT = Path(__file__).resolve().parents[2]
PLOT_DIR = REPO_ROOT /"analysis"/"debug_plots"

#creates garching.dat 
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



#fluence comparison of livermore and garching model
#right column must be chosen for corresponding channel
def plot_livermore_garching(channel):

    print("Plotting Graching vs Livermore flux comparison for: ", channel)
    channels = {"nue": 1, "numu": 2, "nutau": 3, "nuebar": 4, "numubar": 5, "nutaubar": 6}
    
    file_livermore = FLUXES/"livermore.dat"
    file_garching = FLUXES/"garching.dat"

    livermore = np.loadtxt(file_livermore)
    garching = np.loadtxt(file_garching)

    energies_livermore = livermore[:, 0] * 1000
    energies_garching = garching[:, 0] * 1000

    column = channels[channel]
    fluence_livermore = livermore[:, column]
    fluence_garching = garching[:, column]


    plt.plot(energies_livermore, fluence_livermore, label = "livermore")
    plt.plot(energies_garching, fluence_garching, label = "garching")
    plt.legend()
    plt.xlabel("E [MeV]")
    plt.ylabel(r"Fluence [cm$^{-2}$] per 0.2 MeV bin")
    plt.title(f"livermore/garching {channel} fluence comparison")
    plt.grid(alpha = 0.3)
    plt.savefig(PLOT_DIR/f"livermore_garching_comparison_{channel}.png")
    plt.close()

if __name__ == "__main__":
    channels = ["nue", "nuebar", "numu", "numubar", "nutau", "nutaubar"]
    for channel in channels:
        plot_livermore_garching(channel)
