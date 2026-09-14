import uproot
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm, TwoSlopeNorm, SymLogNorm

TMS = Path.home()/"software"/"geant4"/"geant4-work"/"TMS"

def get_smearing_column(file):

    file = uproot.open(file)

    tree = file["TMS"]
    Escint= tree["Escint"].array(library = "np")
    n_generated = len(Escint)


    bin_edges = np.linspace(0.5, 100, 201)


    counts, edges = np.histogram(Escint, bins = bin_edges)

    column = counts / n_generated


    return column



def build_smearing_matrix():
    columns = []
    bin_edges = np.linspace(0.5, 100, 201)
    bin_centers = 0.5 * (bin_edges[:-1] + bin_edges[1:])
    bin_centers = bin_centers[(bin_centers >= 4.8)]# & (bin_centers <= 69)]

    for E in bin_centers:
        #file = Path(TMS/"build"/f"data_marley/MARLEY_CC_nuebar_100k_ALLOWED/MARLEY_TMS_{E:.5f}_CC_nuebar_ALLOWED_Fe56_MeV.root")
        file = Path(TMS/"build"/f"data_without_marley/CC_nue_56Fe_correct_grid_100k/TMS_{E:.5f}_nue_Fe56_MeV.root")
        column = get_smearing_column(file)
        columns.append(column)

    matrix = np.column_stack(columns) #191 columns
    smearing_matrix = np.zeros((200, 200))
    a, b = matrix.shape
    smearing_matrix[:, (200 - b):] = matrix
    
    return smearing_matrix

#build_smearing_matrix()
#atrix = build_smearing_matrix()
#print(matrix.sum(axis = 0))

def write_snowglobes_matrix(smearing_matrix, filename):
    print(type(smearing_matrix))
    n_reco, n_true = smearing_matrix.shape
    with open(filename, "w") as f:

        f.write("energy(#nuebar_Fe56_smear)<\n")

        for i in range(n_reco):

            values = ",".join(
    "0.0" if x == 0.0 else f"{x:.8e}"
    for x in smearing_matrix[i]
)
            line = f"{{0,{n_true - 1},{values}}}"

            if i == 0:
                f.write("@energy = " + line + ":\n")

            elif i == n_reco - 1:
                f.write(line + ";\n")

            else:
                f.write(line + ":\n")

        f.write(">\n")


def create_ES_smearing_matrix(flavor):
    response_matrix = build_smearing_matrix()
    #print(type(response_matrix))
    SNOWGLOBES = Path.home()/"software"/"snowglobes"

    INTERACTION = SNOWGLOBES / "smearing_code" /"interaction"

    nue_e_file = INTERACTION/ f"interaction_{flavor}_e.ssv"

    matrix_nue_e = np.loadtxt(nue_e_file)
    smearing_matrix = response_matrix @ matrix_nue_e

    return smearing_matrix

#create_ES_smearing_matrix()

def plot_smearing_matrix(matrix):
    #matrix = build_smearing_matrix()
    #matrix = create_ES_smearing_matrix()
    
    print(matrix.sum(axis = 0))

    plt.imshow(matrix, origin = "lower", aspect = "auto", extent=[0.5, 100.0, 0.5, 100.0], norm=LogNorm(vmin=1e-5, vmax=matrix.max()))
    plt.xlabel(r"True neutrino energy E$_\nu$ [MeV]")#(r"true neutrino energy $E_\nu$ [MeV]")
    plt.ylabel(r"Scintillator energy $E_{Sc}$ [MeV]")
    plt.colorbar(label = "Probability")
    plt.title(r"MARLEY Smearing Matrix $\bar\nu_e$ CC ALLOWED, 100,000 runs / bin")#(r"ES smearing matrix $\bar\nu_e$, TMS (only scintillator)")
    plt.savefig("TMS_smearing_calc/MARLEY_CC_nuebar_ALLOWED_100k.png")


#plot_smearing_matrix()


def plot_E_L():
    filename = "TMS_50.25_CC_nue_bar_MeV.root"
    file = uproot.open(TMS/"build"/"CC_nue_bar_56Fe_data"/filename)
    tree = file["TMS"]

    Escint = tree["Escint"].array(library="np")
    Lscint = tree["Lscint"].array(library = "np")

    plt.hist2d(Lscint, Escint, bins=100, norm = LogNorm())

    plt.xlabel("Track length in scintillator")
    plt.ylabel(r"$E_{\rm scint}$ [MeV]")
    plt.colorbar(label="Events")
    plt.savefig("E_L.png")

#plot_E_L()
#bin_edges = np.linspace(0.5, 100, 201)
#bin_centers = 0.5 * (bin_edges[:-1] + bin_edges[1:])


#print(bin_centers)
#bin_edges = np.linspace(0.5, 100.0, 201)
#bin_centers = 0.5 * (bin_edges[:-1] + bin_edges[1:])

#matrix = build_smearing_matrix()
#plot_smearing_matrix(matrix)
#write_snowglobes_matrix(matrix, "../../software/snowglobes/smear/TMS_iron/ONLYG4REAL_smear_nuebar_Fe56_TMS_iron.dat")

def plot_effiency():
    matrix = build_smearing_matrix()
    efficiency = matrix.sum(axis=0)

    bin_edges = np.linspace(0.5, 100, 201)
    bin_centers = 0.5 * (bin_edges[:-1] + bin_edges[1:])

    plt.plot(bin_centers, efficiency)
    plt.xlabel(r"$E_\nu$ [MeV]")
    plt.ylabel("Detection efficiency")
    plt.title("MARLEY smearing matrix effiency 100k")
    plt.ylim(0, 1)
    plt.savefig("TMS_smearing_calc/NC_smear_efficiency.png")

#plot_effiency()

def plot_difference_matrix():
    columns = []
    bin_edges = np.linspace(0.5, 100, 201)
    bin_centers = 0.5 * (bin_edges[:-1] + bin_edges[1:])
    bin_centers = bin_centers[bin_centers >= 4.8]

    for i in bin_centers:
        column = get_smearing_column(TMS/"build"/f"data_marley/MARLEY_CC_nuebar_100k_ALLOWED/MARLEY_TMS_{i:.5f}_CC_nuebar_ALLOWED_Fe56_MeV.root")
        columns.append(column)
    matrix = np.column_stack(columns) #191 columns
    smearing_matrix1 = np.zeros((200, 200))
    a, b = matrix.shape
    smearing_matrix1[:, (200 - b):] = matrix


    columns = []
    bin_edges = np.linspace(0.5, 100, 201)
    bin_centers = 0.5 * (bin_edges[:-1] + bin_edges[1:])
    bin_centers = bin_centers[bin_centers >= 4.8]

    for i in bin_centers:
        column = get_smearing_column(TMS/"build"/f"data_without_marley/CC_nuebar_56Fe_correct_grid_100k/TMS_{i:.5f}_nuebar_Fe56_MeV.root")
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

    plt.title(r"M$_{marley}$ - M$_{g4}$, CC $\bar\nu_e$ on $^{56}$Fe")
    plt.savefig("TMS_smearing_calc/diff_matrix_MARLEY_G4_CC_nuebar.png",dpi=200,bbox_inches="tight")
    plt.close()



plot_difference_matrix()

    