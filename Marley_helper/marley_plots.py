import uproot
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import awkward as ak

MARLEY = Path.home()/"software"/"marley"
OUT = MARLEY/"out"

def plot_electron_kinetic_energy():
    energies = [10, 20, 30, 40]
    colors = ["blue", "red", "green", "orange"]
    for j,(i, color) in enumerate(zip(energies, colors)):
        Q = 4.567 #in MeV
        file = uproot.open(OUT/f"Fe_{i}MeV_summary.root")

        tree = file["mst"]

        T_e = tree["KEl"].array(library = "np")
        print(T_e)
        bins = np.linspace(0, 40, 81)
        plt.axvline(x = i - Q,  linestyle='--', color= color , label=r"$T_e = E_\nu-Q$" if j == 0 else "_nolegend_")
        plt.hist(T_e, bins=bins, label = r"$E_\nu$ = " + str(i) + " MeV", color = color)
        plt.xlabel("Electron Kinetic Energy [MeV]")
        plt.ylabel("Events")
        plt.legend(loc="upper left", bbox_to_anchor=(1.02, 1))
        plt.title(r"Electron Kinetic Energy Distribution for MARLEY 56Fe, Rapaport 1983")

    plt.savefig("Marley_helper/electron_energy_comparison_incltheo.png",bbox_inches="tight")
    plt.close()

def plot_excited_energy():
    energies = [10, 20, 30, 40]
    colors = ["blue", "red", "green", "orange"]
    data = {}

    for E_nu in energies:
        file = uproot.open(OUT / f"Fe_{E_nu}MeV_summary.root")
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
    plt.xlim(1, 16.5)
    plt.legend()
    plt.grid(True, alpha = 0.3)
    plt.title(r"MARLEY $^{56}$Fe Excitation Energy Distribution")
    plt.savefig("Marley_helper/Ex_comparison_incltheo.png")
    plt.close()

def plot_xsection():

    file = MARLEY/f"Fe_xsec.txt"

    data = np.loadtxt(file)
    
    energy = data[:, 0]
    xsec = data[:, 1]

  

    #plt.axvline(x = i - Q,  linestyle='--', color= color , label=r"$T_e = E_\nu-Q$" if j == 0 else "_nolegend_")
    plt.plot(energy, xsec)
    plt.xlim(0, 100)
    plt.xlabel(r"Neutrino energy $E_\nu$")
    plt.ylabel(r"cross section $10^{-42}$ cm$^2$")
    
    plt.grid(True, alpha = 0.3)
    plt.title(r"Fe cross section for MARLEY 56Fe, Rapaport 1983")

    plt.savefig("Marley_helper/xsection_comparison_incltheo.png")
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
plot_electron_kinetic_energy()
plot_excited_energy()
plot_xsection()
plot_other_primaries()