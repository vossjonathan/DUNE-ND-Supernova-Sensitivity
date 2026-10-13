import numpy as np
import matplotlib.pyplot as plt
from pathlib  import Path
import uproot


SNOWGLOBES = Path.home()/"software"/"snowglobes"

REPO_ROOT = Path(__file__).resolve().parents[2]

PLOT_DIR = REPO_ROOT /"analysis"/"debug_plots"

#mainly debug plot functions
def findPeakFe():
    TMS = Path.home() / "software/geant4/geant4-work/TMS"
    DATA16 = TMS / "build" / "explain_peak_data"
    DATA32 = TMS / "build" / "explain_peak_data32scint"


    energies = np.array([30,70])

    for E_nu in energies:

        file16 = DATA16 / f"TMS_{E_nu:.5f}_nuebar_Fe56_MeV.root"

        with uproot.open(file16) as f:
            hist = f["Escint"]

            counts16, edges16 = hist.to_numpy()

    # relative Häufigkeit pro erzeugtem Eveng
    #counts = counts / 100000

        plt.stairs(counts16,edges16,label=fr"$E_e={E_nu:.0f}$ MeV, d = 16 mm",baseline=None,)
        file32 = DATA32 / f"TMS_{E_nu:.5f}_nuebar_Fe56_MeV.root"

        with uproot.open(file32) as f:
            hist = f["Escint"]

            counts32, edges32 = hist.to_numpy()

    # relative Häufigkeit pro erzeugtem Eveng
    #counts = counts / 100000

        plt.stairs(
        counts32,
        edges32,
        label=fr"$E_e={E_nu:.0f}$ MeV, d = 32 mm",
        baseline=None,
        linestyle = "--")

    plt.xlabel(r"Deposited scintillator energy $E_{\mathrm{scint}}$ [MeV]")
    plt.ylabel("Events per 1 MeV bin")
    plt.xlim(1, 15)
    plt.ylim(0,5000)
    plt.grid(True, alpha = 0.3)
    plt.legend()
    #plt.title("100,000 events per electron energy generated, uniformly and isotropically in Fe layers")
    plt.savefig(PLOT_DIR/"compare_peak_structure_16_32.svg", bbox_inches = "tight")
    plt.close()


def compare_MARLEY_NOMARLEY():

    file_MARLEY = SNOWGLOBES/"out"/"MARLEY100k_garching_nue_Fe56_TMS_iron_events_smeared_unweighted.dat"
    file_NOMARLEY = SNOWGLOBES/"out"/"NOMARLEY_garching_nue_Fe56_TMS_iron_events_smeared_unweighted.dat"

    data_MARLEY = np.loadtxt(file_MARLEY, max_rows=200)
    data_NOMARLEY = np.loadtxt(file_NOMARLEY, max_rows=200)

    energy = np.linspace(0.5, 100, 201)
    events_MARLEY = data_MARLEY[:, 1]
    events_NOMARLEY = data_NOMARLEY[:, 1]

    plt.stairs(events_MARLEY, energy, baseline = None, label="MARLEY + G4", color="blue")
    plt.stairs(events_NOMARLEY, energy, baseline = None, label=r"Only G4: T$_e$ = E$_\nu$ - Q ", color="red")
    plt.text(0.595, 0.75,f"MARLEY + G4 events: {events_MARLEY.sum():.2f}\nOnly G4 events: {events_NOMARLEY.sum():.2f}",transform=plt.gca().transAxes)#,ha="right",va="top")
    #plt.text(0.84, 0.77,f"Total events unsmeared: {events_unsmeared.sum():.2f}",transform=plt.gca().transAxes,ha="right",va="top")
    plt.xlabel(r" Deposited E in scint [MeV]")
    plt.xlim(0,20)
    plt.ylabel("Number of Events per bin")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.title(r"CC $\nu_e$ on $^{56}$Fe in TMS, MARLEY + G4 vs only G4 smearing matrx")#0% efficiency $\leq$ 5 MeV")
    plt.savefig(PLOT_DIR/"MARLEY100k_NOMARLEY_COMPARISON.svg", bbox_inches = "tight")
    plt.close()


if __name__ ==  "__main__":
    findPeakFe()
    compare_MARLEY_NOMARLEY()
    pass