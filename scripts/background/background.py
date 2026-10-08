import uproot
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm, TwoSlopeNorm, SymLogNorm
from scripts.config import DETECTOR_SMEARING_CONFIG, ALL_DETECTOR

TMS = Path.home()/"software"/"geant4"/"geant4-work"/"TMS"
ANALYSIS = Path.home()/"duke"/"analysis"
SNOWGLOBES = Path.home()/"software"/"snowglobes"
CUTS = np.arange(0, 100, 1)
EXPECTED_MUONS = 150 * 9
BG_FILE = TMS/"build"/"data_without_marley"/"Cosmic_data_theta_36"/"TMS_cosmic_mu.root"
#TODOO: create functions:
# 
# seperate plot functions, 
# function which applies Energy cut as wished, 
# function which applies Lscint cut as wished,
# function which applies both cuts and prints the expected events

def load_background_data(file):
    with uproot.open(file) as root_file:
        tree = root_file["TMS"]

        Escint = tree["Escint"].array(library="np")
        Lscint = tree["Lscint"].array(library="np")

    return Escint, Lscint

def print_background_info():
    Escint, Lscint = load_background_data(BG_FILE)

    n_generated = len(Escint)
    n_zero = np.count_nonzero(Escint == 0)

    energy_mask = (Escint >= 0.5) & (Escint < 15)

    E_relevant = Escint[energy_mask]
    L_relevant = Lscint[energy_mask]

    n_generated = len(Escint)
    n_zero = len(Escint[Escint == 0])
    frac_kept = len(E_relevant)/n_generated

    print("Number of events 0.5 Mev < E < 15 MeV: ", len(E_relevant), f"({frac_kept*100}%)")
    print(f"{frac_kept * EXPECTED_MUONS} background muon events during 9s SN")
    print("Number generated: ", n_generated)
    print("Number events E = 0: ", n_zero)
    print("number relevant: ", len(E_relevant))
    print("mean L all: ", np.mean(Lscint), "mm")
    print("mean L relevant: ", np.mean(L_relevant), "mm")
    print("median L: ", np.median(L_relevant), "mm")



def apply_cuts(Emax, Lmax, Emin = 0.5, Lmin = 0):
    
    Escint, Lscint = load_background_data(BG_FILE)
    mask = ((Escint > Emin) & (Escint < Emax) & (Lscint > Lmin) & (Lscint < Lmax))
    E_cut = Escint[mask]
    L_cut= Lscint[mask]

    return E_cut, L_cut



def plot_bg_energy_distr():
    Escint, Lscint = load_background_data(BG_FILE)
    n_generated = len(Escint)
    bins = np.linspace(0.5, 400, 401)
    event_weight = EXPECTED_MUONS/n_generated


    counts, edges = np.histogram(Escint, bins = bins, weights=np.full(len(Escint), event_weight))
    #plt.title("Cosmic muon background deposited energy")
    plt.stairs(counts, edges, linewidth = 1.3, baseline = None)
    plt.xlabel("Deposited energy in scintillator [MeV]")
    plt.ylabel("Expected events per 1 MeV bin")
    plt.grid(True, alpha = 0.3)
    plt.savefig("debug_plots/muon_distribution_theta_36GeV.svg", bbox_inches="tight", dpi=900)
    plt.close()


def get_weighted_unsmeared_rates():
    detectors = ["TMS_iron", "TMS_scint"]

    bin_edges = np.linspace(0.5, 100, 201)
    bin_centers = 0.5 * (bin_edges[:-1] + bin_edges[1:])

    weighted_L_sum = 0
    weighted_event_sum = 0

    weighted_pass = np.zeros(len(CUTS))


    for detector in detectors:
        channel_config = DETECTOR_SMEARING_CONFIG[detector]["channels"]
        print("Calculating for: ", detector)
        for channel in channel_config.keys():
            if channel_config[channel]["ES"]:
               continue
            print("calculating for: ", channel)
            geant4_folder = channel_config[channel]["folder"]

            channel_weight = ALL_DETECTOR[detector]["channels"][channel]
            unsmeared_file = SNOWGLOBES/"out"/f"garching_{channel}_{detector}_events_unweighted.dat"
            data_unsmeared = np.loadtxt(unsmeared_file, max_rows=200)
            events_unsmeared = data_unsmeared[:, 1] * channel_weight
            threshold = channel_config[channel]["threshold"]

            for i, E in enumerate(bin_centers):
                if E < threshold:
                    continue
                geant4_filename = channel_config[channel]["filename"].format(E = E)
                file = ANALYSIS/"data"/"smearing_matrix_data"/geant4_folder/geant4_filename
                file = uproot.open(file)
                tree = file["TMS"]
                Escint= tree["Escint"].array(library = "np")
                Lscint= tree["Lscint"].array(library = "np")

                N_SN = events_unsmeared[i]

                N_total = len(Escint)

                event_weight = N_SN/N_total

                relevant_energies = (Escint >= 0.5) & (Escint < 15)
                for j, cut in enumerate(CUTS):

                    mask_pass = relevant_energies & (Lscint < cut)

                    weighted_pass[j] += (event_weight * np.count_nonzero(mask_pass))

                weighted_L_sum += event_weight * np.sum(Lscint[relevant_energies])

                weighted_event_sum += event_weight * np.sum(relevant_energies)

    frac = []

    for cut, n_pass in zip(CUTS, weighted_pass):

        fraction = n_pass / weighted_event_sum
        frac.append(fraction)

        print(f"L < {cut:3} mm: "f"{fraction:.4f} "f"({n_pass:.3f} expected SN events)")
    mean_Lscint = weighted_L_sum / weighted_event_sum
    print("weighted selected SN events: ", weighted_event_sum)
    print("weighted neutrino events Lscint: ", mean_Lscint, "mm")

    return frac

def events_after_cuts(Emax, Lmax, Emin = 0.5, Lmin = 0):
    E_scint, L_scint = load_background_data(BG_FILE)
    E_cut, L_cut = apply_cuts(Emax, Lmax, Emin = Emin, Lmin = Lmin)
    n_generated = len(E_scint)
    n_kept = len(E_cut)
    frac_kept = n_kept/n_generated
    SN_bg_events = frac_kept * EXPECTED_MUONS
    SN_events = 10.48
    print(f"From {EXPECTED_MUONS} muons:")
    print(f"{SN_bg_events} are within the cuts, so {Emin} < E < {Emax} and {Lmin} < L < {Lmax}")


def plot_frac_cut(cut):
    chosen_cut = cut

    Escint, Lscint = load_background_data(BG_FILE)

    # Background after energy cut only
    energy_mask = (Escint > 0.5) & (Escint < 15)
    L_after_energy_cut = Lscint[energy_mask]

    bg_acceptance = []

    for l_cut in CUTS:
        frac = np.mean(L_after_energy_cut < l_cut)
        bg_acceptance.append(frac)

        print(f"L < {l_cut:3} mm: {frac:.4f}")

    bg_acceptance = np.array(bg_acceptance)
    bg_rejection = 1 - bg_acceptance

    signal_acceptance = np.array(get_weighted_unsmeared_rates())

    cut_index = np.argmin(np.abs(CUTS - chosen_cut))

    print(f"With a cut of {chosen_cut}mm, {(signal_acceptance[cut_index]*100):.2f}% of neutrino events would be kept and {(bg_rejection[cut_index]*100):.2f}% would be cut.")
    plt.plot(CUTS, bg_rejection, label ="Background rejection")
    plt.plot(CUTS, signal_acceptance, label = "Signal acceptance")
    plt.xlabel(r"$L_{scint}^{cut}$ [mm]")
    plt.ylabel(r"Fraction of events")
    plt.axvline(chosen_cut, ls="--", linewidth = 1, color = "black")
    plt.grid(True, alpha = 0.3)
    #plt.title(r"Scintillator path length $L_{scint}$ comparison")
    plt.legend(loc = "upper right", bbox_to_anchor=(1.0, 0.90))
    plt.savefig("debug_plots/fracplot2.svg", bbox_inches="tight", dpi=900)
    plt.close()





if __name__ == "__main__":
    print_background_info()  
    events_after_cuts(15, 30)
    #get_weighted_unsmeared_rates()
    plot_bg_energy_distr()
    plot_frac_cut(30)