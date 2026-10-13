import numpy as np
import matplotlib.pyplot as plt
from pathlib  import Path
import uproot
from analysis.config import DETECTOR_SMEARING_CONFIG, ENERGY_GRID, ALL_DETECTOR, iron_channels, argon_channels, lead_channels, scint_channels
from analysis.helper import load_events_weighted


SNOWGLOBES = Path.home()/"software"/"snowglobes"

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

        plt.stairs(
        counts16,
        edges16,
        label=fr"$E_e={E_nu:.0f}$ MeV, d = 16 mm",
        baseline=None,)
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
    plt.ylabel("Events per 0.5 MeV bin")
    plt.xlim(1, 15)
    plt.ylim(0,5000)
    plt.grid(True, alpha = 0.3)
    plt.legend()
    #plt.title("100,000 events per electron energy generated, uniformly and isotropically in Fe layers")
    plt.savefig("debug_plots/compare_peak_structure_16_32.png")

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
    plt.savefig("debug_plots/MARLEY100k_NOMARLEY_COMPARISON.png")

def compare_settings_effects(tree_name="TMS",pdg_branch="PDG",kinetic_energy_branch="Ekin",bins=np.linspace(0, 40, 81)):

    plt.figure(figsize=(8, 5))

    folder = Path.home()/"software"/"geant4"/"geant4-work"/"TMS"/"build"/"data_marley"/"MARLEY_compare_settings"
    files = {
        "discrete": 
            "MARLEY_TMS_40.00000_only_discrete.root",

        "discrete + continuum":
            "MARLEY_TMS_40.00000_discrete_continuum.root",

        "discrete + allowed":
            "MARLEY_TMS_40.00000_only_discrete_allowed.root",

        "discrete + continuum + allowed":
            "MARLEY_TMS_40.00000_discrete_continuum_allowed.root",
    }

    for label, filename in files.items():

        path = Path(folder) / filename

        with uproot.open(path) as f:
            tree = f[tree_name]

            pdg = tree[pdg_branch].array(library="np")
            Ekin = tree[kinetic_energy_branch].array(library="np")

        # select electrons
        electron_Ekin = Ekin[pdg == 11]

        print(
            f"{label:35s}: "
            f"N_e = {len(electron_Ekin):7d}, "
            f"mean = {np.mean(electron_Ekin):6.3f} MeV, "
            f"median = {np.median(electron_Ekin):6.3f} MeV"
        )

        plt.hist(
            electron_Ekin,
            bins=bins,
            histtype="step",
            density=True,
            linewidth=1.8,
            label=label
        )

    plt.xlabel(r"Electron kinetic energy $T_e$ [MeV]")
    plt.ylabel("Probability density [1/MeV]")
    plt.title(r"$\nu_e + {}^{56}\mathrm{Fe}$ at $E_\nu = 40$ MeV")
    plt.legend()
    plt.grid(alpha=0.25)

    plt.tight_layout()
    plt.savefig("debug_plots/compare_settings_effects.png")

if __name__ ==  "__main__":
    #findPeakFe()
    #compare_MARLEY_NOMARLEY()
    #compare_settings_effects

    pass