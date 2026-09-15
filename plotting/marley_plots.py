import uproot
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import awkward as ak
from matplotlib.colors import LogNorm, SymLogNorm


MARLEY = Path.home()/"software"/"marley"
OUT = MARLEY/"out"

def plot_electron_kinetic_energy():
    energies = [10, 20, 30, 40]
    colors = ["blue", "red", "green", "orange"]
    for j,(i, color) in enumerate(zip(energies, colors)):
        Q = 4.567 #in MeV
        file = uproot.open(MARLEY/"out_SAM"/f"Fe_SAM_{i}MeV_summary.root")

        tree = file["mst"]

        T_e = tree["KEl"].array(library = "np")
        print(T_e)
        bins = np.linspace(0, 40, 81)
        plt.axvline(x = i - Q,  linestyle='--', color= color , label=r"$T_e = E_\nu-Q$" if j == 0 else "_nolegend_")
        plt.hist(T_e, bins=bins, label = r"$E_\nu$ = " + str(i) + " MeV", color = color)
        plt.xlabel("Electron Kinetic Energy [MeV]")
        plt.ylabel("Events")
        plt.legend(loc="upper left", bbox_to_anchor=(1.02, 1))
        plt.title(r"Electron Kinetic Energy Distribution for MARLEY 56Fe, SAM .react file")

    plt.savefig("Marley_helper/electron_energy_comparison_SAM.png",bbox_inches="tight")
    plt.close()

def plot_excited_energy():
    energies = [10, 20, 30, 40]
    colors = ["blue", "red", "green", "orange"]
    data = {}

    for E_nu in energies:
        file = uproot.open(MARLEY/"out_SAM"/f"Fe_SAM_{E_nu}MeV_summary.root")
        Ex = file["mst"]["Ex"].array(library="np")
        Ex = np.round(Ex, 2)

        levels, counts = np.unique(Ex, return_counts=True)
        fractions = counts / len(Ex)
        data[E_nu] = dict(zip(levels, fractions))

    all_levels = np.array(sorted(set().union(*(d.keys() for d in data.values()))))

    width = 0.13
    offsets = [-1.5, -0.5, 0.5, 1.5]

    for E_nu, color, offset in zip(energies, colors, offsets):
        fractions = [data[E_nu].get(level, 0) for level in all_levels]
        plt.bar(all_levels + offset * width, fractions, width=width, color=color, label=rf"$E_\nu={E_nu}$ MeV")

    plt.xlabel(r"Excitation Energy $E_x$ [MeV]")
    plt.ylabel("Fraction of Events")
    plt.xlim(1, 26)
    plt.legend()
    plt.grid(True, alpha = 0.3)
    plt.title(r"MARLEY $^{56}$Fe Excitation Energy Distribution SAM .react file")
    plt.savefig("Marley_helper/Ex_comparison_SAM.png")
    plt.close()

def plot_xsection():

    file1 = MARLEY/"data_xsec"/f"Fe_Ar_continuum.txt"
    file2 = MARLEY/"data_xsec"/f"Fe_Ar_discrete.txt"

    data1 = np.loadtxt(file1)
    data2 = np.loadtxt(file2)

    xsec1 = data1[:, 1]

    energy = data2[:, 0]
    xsec2 = data2[:, 1]

    print(np.array_equal(xsec1, xsec2))
  

    #plt.axvline(x = i - Q,  linestyle='--', color= color , label=r"$T_e = E_\nu-Q$" if j == 0 else "_nolegend_")
    plt.plot(energy, xsec1, label = "continuum Ar")
    plt.plot(energy, xsec2, label = "discrete Fe only")
    plt.xlim(0, 100)
    plt.xlabel(r"Neutrino energy $E_\nu$ [MeV]")
    plt.ylabel(r"cross section $10^{-42}$ cm$^2$")
    plt.legend()
    
    plt.grid(True, alpha = 0.3)
    plt.title(r"56Fe CC cross sections, only discrete vs. using 40Ar continuum files")

    plt.savefig("Marley_helper/Fe_Ar_xsec_comparison.png")
    plt.close()

    
def compare_xsection():

    
    file1 = MARLEY/f"Pb_NONE.txt"
    file2 = MARLEY/f"Pb_FERMI.txt"
    file3 = MARLEY/f"Pb_MEMA.txt"
    file4 = MARLEY/f"Pb_Fermi-MEMA.txt"

    data1 = np.loadtxt(file1)
    data2 = np.loadtxt(file2)
    data3 = np.loadtxt(file3)
    data4 = np.loadtxt(file4)

    energy = data1[:, 0]

    xsec1 = data1[:, 1]
    xsec2 = data2[:, 1]
    xsec3 = data3[:, 1]
    xsec4 = data4[:, 1]


  

    #plt.axvline(x = i - Q,  linestyle='--', color= color , label=r"$T_e = E_\nu-Q$" if j == 0 else "_nolegend_")
    plt.plot(energy, xsec1, label = "NONE")
    plt.plot(energy, xsec2, label = "FERMI")
    plt.plot(energy, xsec3, label = "MEMA")
    plt.plot(energy, xsec4, label = "FERMI-MEMA")

    plt.xlim(0, 100)
    plt.xlabel(r"Neutrino energy $E_\nu$ [MeV]")
    plt.ylabel(r"cross section $10^{-42}$ cm$^2$")
    
    plt.grid(True, alpha = 0.3)
    plt.title(r"NC Fe cross section, Shizuma 2013")
    plt.legend()
    plt.savefig("Marley_helper/comparexsec.png")
    plt.close()


def plot_other_primaries():
    energies = [10, 20, 30, 40]

    gamma_fraction = []
    neutron_fraction = []
    proton_fraction = []

    for E_nu in energies:
        file = uproot.open(OUT / f"Fe_{E_nu}MeV_summary.root")
        tree = file["mst"]
        pdg = tree["pdgp"].array()

        has_gamma = ak.any(pdg == 22, axis=1)
        has_neutron = ak.any(pdg == 2112, axis=1)
        has_proton = ak.any(pdg == 2212, axis=1)

        gamma_fraction.append(float(ak.mean(has_gamma)) * 100)
        neutron_fraction.append(float(ak.mean(has_neutron)) * 100)
        proton_fraction.append(float(ak.mean(has_proton)) * 100)
        print(proton_fraction)

    plt.plot(energies, gamma_fraction, marker="o", label=r"$\gamma$")
    plt.plot(energies, neutron_fraction, marker="o", label=r"$n$")
    plt.plot(energies, proton_fraction, marker="o", label=r"$p$")

    plt.xlabel(r"Neutrino Energy $E_\nu$ [MeV]")
    plt.ylabel(r"Interactions with $\geq 1$ Particle [%]")
    plt.xticks(energies)
    plt.ylim(0, 100)
    plt.grid(axis="y", alpha=0.3)
    plt.legend()
    plt.title(r"MARLEY $^{56}$Fe Particle Emission Probability")
    plt.tight_layout()
    plt.savefig("Marley_helper/particle_emission_probability_incltheo.png", dpi=300, bbox_inches="tight")
    plt.show()
    plt.close()


def compare_xsec_effect_on_response():
    TMS = Path.home()/"software"/"geant4"/"geant4-work"/"TMS"
    energies = [10, 20, 30, 40]
    bin_edges = np.linspace(0.5, 100, 201)
    columns_discrete = []
    columns_continuum = []
    for E in energies:
        file_discrete = uproot.open(TMS/"build"/"data_marley"/"MARLEY_compare_xsec_effect_CC"/f"MARLEY_TMS_{E:.5f}_discrete.root")
        file_continuum = uproot.open(TMS/"build"/"data_marley"/"MARLEY_compare_xsec_effect_CC"/f"MARLEY_TMS_{E:.5f}_Ar_dummy_continuum.root")

        tree_discrete = file_discrete["TMS"]
        tree_continumm = file_continuum["TMS"]
                                        
        Escint_discrete= tree_discrete["Escint"].array(library = "np")
        Escint_continuum = tree_continumm["Escint"].array(library = "np")

        print(f"discrete mean for E = {E}:", np.mean(Escint_discrete))
        print(f"continuum mean for E = {E}:", np.mean(Escint_continuum))

    
        counts, edges = np.histogram(Escint_discrete, bins = bin_edges)
        column_discrete = counts/len(Escint_discrete)
        columns_discrete.append(column_discrete)

        counts, edges = np.histogram(Escint_continuum, bins = bin_edges)
        column_continuum = counts/len(Escint_continuum)
        columns_continuum.append(column_continuum)       

    matrix_discrete = np.column_stack(columns_discrete)
    matrix_continuum = np.column_stack(columns_continuum)
    diff_matrix = matrix_discrete - matrix_continuum

    energy_edges = [5, 15, 25, 35, 45]
    max_abs = np.max(np.abs(diff_matrix))
    norm = SymLogNorm(linthresh=1e-5,linscale=1,vmin=-max_abs,vmax=max_abs,base=10)
    masked_diff = np.ma.masked_where(diff_matrix == 0, diff_matrix)

    cmap = plt.cm.viridis.copy()
    cmap.set_bad("white")

    #norm=LogNorm(vmin=1e-5, vmax=matrix_discrete.max())
    print(matrix_discrete.shape)
    for i, E in enumerate(energies):
        plt.pcolormesh(
            [E - 1, E + 1],
            bin_edges,
            masked_diff[:, i:i+1],
            norm=norm,
            shading="flat",
            cmap = cmap
        )

    plt.xlabel("True neutrino energy")
    plt.ylabel("Scintillator energy")
    plt.colorbar(label = "Probability")
    plt.title("Difference Matrix (discrete - continuum) for CC Fe")
    plt.savefig("Marley_helper/test_smear.png")


if __name__ == "__main__":
    #plot_electron_kinetic_energy()
    #plot_excited_energy()
    #plot_xsection()
    #plot_other_primaries()
    #compare_xsection()
    compare_xsec_effect_on_response()