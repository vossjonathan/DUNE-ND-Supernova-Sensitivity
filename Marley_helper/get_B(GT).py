import numpy as np
import matplotlib.pyplot as plt

def print_experimental():
    file = "Marley_helper/56Fe_B(GT)_digitized.csv"

    data = np.loadtxt(file, delimiter = ",")

    g_A = 1.26

    B_GT = data[:, 1]

    B_GT = B_GT * g_A**2

    for E, B in zip(data[:, 0], B_GT):
        print(f"{E:.2f}   {B:.2f}   1")

def get_theoretical():
    file = "Marley_helper/56Fe_theo_B(GT).csv"
    data = np.loadtxt(file, delimiter=",")

    data = data[data[:, 0] >= 16]
    data = data[np.argsort(data[:, 0])]

    E = data[:, 0]
    B = data[:, 1]

    gap_indices = np.where(np.diff(E) > 0.2)[0] + 1
    E_segments = np.split(E, gap_indices)
    B_segments = np.split(B, gap_indices)

    bin_edges = np.arange(16, 41, 1)

    Ex_bins = []
    BGT_bins = []

    for E_low, E_high in zip(bin_edges[:-1], bin_edges[1:]):
        B_integral = 0

        for E_seg, B_seg in zip(E_segments, B_segments):
            if E_seg[-1] < E_low or E_seg[0] > E_high:
                continue

            mask = (E_seg >= E_low) & (E_seg <= E_high)
            E_bin = E_seg[mask]
            B_bin = B_seg[mask]

            if E_seg[0] < E_low < E_seg[-1]:
                E_bin = np.insert(E_bin, 0, E_low)
                B_bin = np.insert(B_bin, 0, np.interp(E_low, E_seg, B_seg))

            if E_seg[0] < E_high < E_seg[-1]:
                E_bin = np.append(E_bin, E_high)
                B_bin = np.append(B_bin, np.interp(E_high, E_seg, B_seg))

            if len(E_bin) >= 2:
                B_integral += np.trapezoid(B_bin, E_bin)

        if B_integral > 0:
            Ex_bins.append((E_low + E_high) / 2)
            BGT_bins.append(B_integral)

    Ex_bins = np.array(Ex_bins)
    BGT_bins = np.array(BGT_bins)

    for Ex, BGT in zip(Ex_bins, BGT_bins):
        print(f"{Ex:.2f}   {(BGT*1.26*1.26):.4f}   1")

    plt.bar(Ex_bins, BGT_bins, width=0.8)
    plt.xlabel(r"Excitation Energy $E_x$ [MeV]")
    plt.ylabel(r"Integrated $B(GT)$ per 1 MeV bin")
    plt.savefig("Marley_helper/theoretical_BGT_binned.png", dpi=300)
  

get_theoretical()