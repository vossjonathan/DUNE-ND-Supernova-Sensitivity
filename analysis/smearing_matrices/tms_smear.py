import uproot
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm, TwoSlopeNorm, SymLogNorm
from analysis.config import DETECTOR_SMEARING_CONFIG, ALL_DETECTOR

TMS = Path.home()/"software"/"geant4"/"geant4-work"/"TMS"
ANALYSIS = REPO_ROOT = Path(__file__).resolve().parents[2]
SNOWGLOBES = Path.home()/"software"/"snowglobes"

REPO_ROOT = Path(__file__).resolve().parents[2]

PLOT_DIR = REPO_ROOT /"analysis"/"debug_plots"


def get_smearing_column(file):

    file = uproot.open(file)

    tree = file["TMS"]
    Escint= tree["Escint"].array(library = "np")
    n_generated = len(Escint)


    bin_edges = np.linspace(0.5, 100, 201)


    counts, edges = np.histogram(Escint, bins = bin_edges)

    column = counts / n_generated


    return column

def build_smearing_matrix(detector, channel):

    bin_edges = np.linspace(0.5, 100, 201)
    bin_centers = 0.5 * (bin_edges[:-1] + bin_edges[1:])

    channel_config = DETECTOR_SMEARING_CONFIG[detector]["channels"][channel]
    threshold = channel_config["threshold"]

    smearing_matrix = np.zeros((200, 200))

    for i, E in enumerate(bin_centers):

        if E < threshold:
            continue

        filename = channel_config["filename"].format(E=E)
        file = (ANALYSIS/"data"/ "smearing_matrix_data"/channel_config["folder"]/filename)

        if not file.exists():
            raise FileNotFoundError(f"{channel}: missing file at E = {E:.5f} MeV:\n{file}")

        smearing_matrix[:, i] = get_smearing_column(file)

    if channel_config["ES"]:
        flavor = channel.split("_")[0]
        smearing_matrix = create_ES_smearing_matrix(smearing_matrix, flavor)

    if np.isnan(smearing_matrix).any():
        raise ValueError(f"{channel}: matrix contains NaNs")

    if np.any(smearing_matrix < 0):
        raise ValueError(f"{channel}: matrix contains negative values")

    return smearing_matrix



def write_snowglobes_matrix(smearing_matrix, detector,  channel):
    n_reco, n_true = smearing_matrix.shape
    config = DETECTOR_SMEARING_CONFIG[detector]

    filename = Path.home()/"software"/"snowglobes"/"smear"/f"{detector}"/f"smear_{channel}_{detector}.dat"
    with open(filename, "w") as f:

        f.write(f"energy(#{channel}_smear)<\n")

        for i in range(n_reco):

            values = ",".join("0.0" if x == 0.0 else f"{x:.8e}" for x in smearing_matrix[i])
            line = f"{{0,{n_true - 1},{values}}}"

            if i == 0:
                f.write("@energy = " + line + ":\n")

            elif i == n_reco - 1:
                f.write(line + ";\n")

            else:
                f.write(line + ":\n")

        f.write(">\n")


def create_ES_smearing_matrix(matrix, flavor):
    #print(type(response_matrix))
    SNOWGLOBES = Path.home()/"software"/"snowglobes"

    INTERACTION = SNOWGLOBES / "smearing_code" /"interaction"

    nue_e_file = INTERACTION/ f"interaction_{flavor}_e.ssv"

    matrix_nue_e = np.loadtxt(nue_e_file)
    smearing_matrix = matrix @ matrix_nue_e

    return smearing_matrix


def plot_smearing_matrix(matrix, detector, channel):
    
    print(matrix.sum(axis = 0))

    plt.imshow(matrix, origin = "lower", aspect = "auto", extent=[0.5, 100.0, 0.5, 100.0], norm=LogNorm(vmin=1e-5, vmax=matrix.max()))
    plt.xlabel(r"True neutrino energy E$_\nu$ [MeV]")#(r"true neutrino energy $E_\nu$ [MeV]")
    plt.ylabel(r"Scintillator energy $E_{Sc}$ [MeV]")
    plt.colorbar(label = "Probability")
    #plt.title(f"Smearing matrix for {detector}, {channel}")
    plt.savefig(PLOT_DIR/f"{detector}_{channel}_smearing_matrix.svg", bbox_inches="tight", dpi = 900)
    plt.close()



def plot_effiency(matrix, detector, channel):
    efficiency = matrix.sum(axis=0)

    bin_edges = np.linspace(0.5, 100, 201)
    bin_centers = 0.5 * (bin_edges[:-1] + bin_edges[1:])

    plt.plot(bin_centers, efficiency)
    plt.xlabel(r"$E_\nu$ [MeV]")
    plt.ylabel("Detection efficiency")
    plt.title(f"Effiency plot for {detector}, channel: {channel}")
    plt.ylim(0, 1)
    plt.savefig(PLOT_DIR/f"{detector}_{channel}_efficiency.png")
    plt.close()


def plot_difference_matrix():
    columns = []
    bin_edges = np.linspace(0.5, 100, 201)
    bin_centers = 0.5 * (bin_edges[:-1] + bin_edges[1:])
    bin_centers = bin_centers[bin_centers >= 6.7]

    for i in bin_centers:
        column = get_smearing_column(ANALYSIS/"data"/f"smearing_matrix_data/MARLEY_CC_nue100k_ALLOWED/MARLEY_TMS_{i:.5f}_CC_ALLOWED_Fe56_MeV.root")
        columns.append(column)
    matrix = np.column_stack(columns) #191 columns
    smearing_matrix1 = np.zeros((200, 200))
    a, b = matrix.shape
    smearing_matrix1[:, (200 - b):] = matrix


    columns = []
    bin_edges = np.linspace(0.5, 100, 201)
    bin_centers = 0.5 * (bin_edges[:-1] + bin_edges[1:])
    bin_centers = bin_centers[bin_centers >= 4.6]

    for i in bin_centers:
        column = get_smearing_column(TMS/"build"/f"data_without_marley/CC_nue_56Fe_correct_grid_100k/TMS_{i:.5f}_nue_Fe56_MeV.root")
        columns.append(column)
    matrix = np.column_stack(columns) #191 columns
    smearing_matrix2 = np.zeros((200, 200))
    a, b = matrix.shape
    smearing_matrix2[:, (200 - b):] = matrix

    diff = smearing_matrix1 - smearing_matrix2

    max_abs = np.max(np.abs(diff))

    norm = SymLogNorm(
        linthresh=1e-5,
        linscale=1,
        vmin=-max_abs,
        vmax=max_abs,
        base=10
    )

    plt.figure()

    plt.imshow(diff,origin="lower",aspect="auto",extent=[0.5, 100.0, 0.5, 100.0],norm=norm,cmap="RdBu_r")

    plt.xlabel(r"True neutrino energy $E_\nu$ [MeV]")
    plt.ylabel(r"Scintillator energy $E_{\rm Sc}$ [MeV]")

    plt.colorbar(label="Difference")

    plt.title(r"M$_{marley}$ - M$_{g4}$, marley allowed CC $\nu_e$ on $^{56}$Fe")
    plt.savefig(PLOT_DIR/"diff_matrix_MARLEY_ALLOWED_G4_CC_nue.png",dpi=200,bbox_inches="tight")
    plt.close()








if __name__ == "__main__":
    matrix = build_smearing_matrix("TMS_iron", "nue_Fe56") 

    #write_snowglobes_matrix(matrix, "../../software/snowglobes/smear/TMS_scint/GEANT4_smear_nc_nue_scint_TMS_scint.dat")   
    #matrix = create_ES_smearing_matrix()
    plot_smearing_matrix(
    matrix = matrix,
    detector = "TMS_iron",
    channel = "nue_Fe56")
    #plot_E_L()
    #plot_effiency()
    #plot_difference_matrix()


