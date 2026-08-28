import uproot
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

TMS = Path.home()/"software"/"geant4"/"geant4-work"/"TMS"


'''nu_energy = 0
for i in range(1, 11):

    nu_energy = i * 10
    file = uproot.open(TMS/"build"/f"TMS_Enu_{nu_energy}.0MeV.root")
    tree = file["TMS"]

    Escint = tree["Escint"].array(library="np")


print(Escint)
print(len(Escint))
'''



#printMacro()


def get_smearing_column(filename):

    file = uproot.open(TMS/"build"/"CC_nuebar_56Fe_correct_grid_100k"/filename)

    tree = file["TMS"]
    Escint= tree["Escint"].array(library = "np")
    n_generated = len(Escint)


    bin_edges = np.linspace(0.5, 100, 201)
    bin_centers = 0.5 * (bin_edges[:-1] + bin_edges[1:])


    counts, edges = np.histogram(Escint, bins = bin_edges)

    column = counts / n_generated
    Escint = file["TMS"]["Escint"].array(library="np")


    return column



def build_smearing_matrix():
    columns = []
    bin_edges = np.linspace(0.5, 100, 201)
    bin_centers = 0.5 * (bin_edges[:-1] + bin_edges[1:])
    bin_centers = bin_centers[bin_centers >= 4.71]

    for i in bin_centers:
        column = get_smearing_column(f"TMS_{i:.5f}_nuebar_Fe56_MeV.root")
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
matrix = build_smearing_matrix()
write_snowglobes_matrix(matrix, "../../software/snowglobes/smear/TMS_iron/calc100k_smear_nuebar_Fe56_TMS_iron.dat")

def create_ES_smearing_matrix():
    response_matrix = build_smearing_matrix()
    #print(type(response_matrix))
    SNOWGLOBES = Path.home()/"software"/"snowglobes"

    INTERACTION = SNOWGLOBES / "smearing_code" /"interaction"

    nue_e_file = INTERACTION/ "interaction_nutaubar_e.ssv"

    matrix_nue_e = np.loadtxt(nue_e_file)
    smearing_matrix = response_matrix @ matrix_nue_e

    return smearing_matrix

#create_ES_smearing_matrix()

def plot_smearing_matrix():
    matrix = build_smearing_matrix()
    #matrix = create_ES_smearing_matrix()
    
    print(matrix.sum(axis = 0))

    plt.imshow(matrix, origin = "lower", aspect = "auto", extent=[0.5, 100.0, 0.5, 100.0], norm=LogNorm(vmin=1e-5, vmax=matrix.max()))
    plt.xlabel(r"$T_e$ [MeV]")#(r"true neutrino energy $E_\nu$ [MeV]")
    plt.ylabel(r"Scintillator energy $E_{Sc}$ [MeV]")
    plt.colorbar(label = "Probability")
    plt.title(r"Smearing Matrix CC $\bar\nu_e$, 100,000 runs / bin")#(r"ES smearing matrix $\bar\nu_e$, TMS (only scintillator)")
    plt.savefig("TMS_smearing_calc/TMS_nuebar_Fe56_response_matrix100k.png")


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

'''matrix = build_smearing_matrix()


acceptance = matrix.sum(axis=0)

bin_edges = np.linspace(0.5, 100.0, 201)
bin_centers = 0.5 * (bin_edges[:-1] + bin_edges[1:])

for E, A in zip(bin_centers, acceptance):
    if 5 <= E <= 30:
        print(E, A)'''


