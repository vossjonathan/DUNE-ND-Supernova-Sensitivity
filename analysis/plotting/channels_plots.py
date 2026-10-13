import numpy as np
import matplotlib.pyplot as plt

from pathlib import Path
from analysis.config import ENERGY_GRID
from analysis.helper import load_events_weighted


SNOWGLOBES = Path.home()/"software"/"snowglobes"



def plot_one_channel_weighted(flux, channel, detector, smeared):
    events = load_events_weighted(flux, channel, detector, smeared)

    word = "smeared" if smeared else "unsmeared"
    color = "blue" if smeared else "red"

    plt.stairs(events, ENERGY_GRID, label = word + f" {channel}", color = color)
    plt.text(0.6, 0.86,f"Events {word}: {events.sum():.4f}",transform=plt.gca().transAxes)

    plt.xlim(0, 50)
    plt.xlabel(r"E [MeV]")
    plt.ylabel("Number of events per bin")
    plt.legend()
    plt.grid(True, alpha = 0.3)
    plt.title(f"{word.capitalize()} events for {detector}, {channel}, {flux} flux")
    plt.savefig(f"debug_plots/{flux}_{detector}_{channel}_{word}_events.svg", bbox_inches = "tight", dpi = 900)
    plt.close()
    
def plot_two_channel_smeared_unsmeared(title, save_as):

    energy = ENERGY_GRID
    file_unsmeared = SNOWGLOBES/"out"/"garching_nc_nue_C12_TMS_scint_events_unweighted.dat"
    data_unsmeared = np.loadtxt(file_unsmeared, max_rows=200)
    events_unsmeared = data_unsmeared[:, 1] * 0.4945

    file_smeared1 = SNOWGLOBES/"out"/"G4_garching_nc_nue_C12_TMS_scint_events_smeared_unweighted.dat"
    file_smeared2= SNOWGLOBES/"out"/"SCINT20KT_garching_nc_nue_C12_TMS_scint_events_smeared_unweighted.dat"

    data_smeared1 = np.loadtxt(file_smeared1, max_rows=200)
    data_smeared2 = np.loadtxt(file_smeared2, max_rows=200)

    events_smeared1 = data_smeared1[:, 1] * 0.4945
    events_smeared2 = data_smeared2[:, 1] * 0.4945

    plt.stairs(events_smeared1, energy, label="Geant4 response", color="blue", baseline = None)
    plt.stairs(events_smeared2, energy, label="Basic scint20kt response", color="red", baseline = None)
    plt.stairs(events_unsmeared, energy, label="Unsmeared Signal", color="black")
    plt.xlim(0,50)
    #plt.text(0.42, 0.75,f"Total events unsmeared: {events_unsmeared.sum():.2f}\nTotal events smeared: {events_smeared.sum():.2f}",transform=plt.gca().transAxes)#,ha="right",va="top")
    #plt.text(0.84, 0.77,f"Total events unsmeared: {events_unsmeared.sum():.2f}",transform=plt.gca().transAxes,ha="right",va="top")
    plt.xlabel(r" E [MeV]")
    plt.ylabel("Number of Events per bin")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.title(title)
    plt.savefig(f"debug_plots/{save_as}")

def plot_one_channel_smeared_vs_unsmeared(flux, channel, detector):

    events_unsmeared = load_events_weighted(flux, channel, detector, smeared = False)
    events_smeared = load_events_weighted(flux, channel, detector, smeared = True)

    plt.stairs(events_smeared, ENERGY_GRID, label = "Smeared: Reconstructed E", color = "blue")
    plt.stairs(events_unsmeared, ENERGY_GRID, label = "Unsmeared: True E", color = "red")

    plt.text(0.51, 0.75,f"Total events unsmeared: {events_unsmeared.sum():.2f}\nTotal events smeared: {events_smeared.sum():.2f}",transform=plt.gca().transAxes)

    plt.xlabel(r" E [MeV]")
    plt.xlim(0, 50)
    plt.ylabel("Number of Events per bin")
    plt.legend()
    plt.grid(True, alpha=0.3)

    plt.title(f"{detector}, {channel} unsmeared vs. smeared, {flux} flux")
    plt.savefig(f"debug_plots/{flux}_{channel}_{detector}_smeared_vs_unsmeared.svg", bbox_inches = "tight", dpi = 900)
    plt.close()

def plot_all_NC_channels_iron():
    channels = ['nc_nue_Fe56', 'nc_nuebar_Fe56', 'nc_numu_Fe56']
    total_nc_events_smeared = np.zeros(200)
    
    for channel in channels:
        smeared = load_events_weighted("garching", channel, "TMS_iron", True)
        unsmeared = load_events_weighted("garching", channel, "TMS_iron", False)
        total_nc_events_smeared += smeared

        plt.stairs(smeared, ENERGY_GRID, label=channel)
        plt.stairs(unsmeared, ENERGY_GRID, label=channel + " unsmeared")

    plt.xlabel(r" Detected $E_{det}$ [MeV]")
    plt.ylabel("Number of Events per 0.5 MeV energy bin")
    plt.xlim(0,50)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.title("TMS iron NC channels comparison")
    plt.savefig(f"debug_plots/NC_channels_comparison.png")
    plt.close()

def plot_missing_TMS_channels_unsmeared(flux):
    channels = {"nue_C12": 0, "nuebar_C12": 0, "nue_C13":0,  "nc_nue_C13":0, "nc_nuebar_C13":0, "nc_numu_C13":0, "nc_numubar_C13":0, "nc_nutau_C13":0, "nc_nutaubar_C13":0}

    total_nc_count = 0
    total_count = 0
    for channel in channels.keys():
        events_unsmeared = load_events_weighted(flux, channel, "TMS_scint", smeared = False)
        channels[channel] = events_unsmeared.sum()
        if channel.startswith("nc"):
            total_nc_count += events_unsmeared.sum()
        total_count += events_unsmeared.sum()
        plt.stairs(events_unsmeared, ENERGY_GRID, label = channel)

    text = "\n".join(f"{channel}: {events:.3f}" for channel, events in channels.items() if channel.startswith("nue"))
    text += f"\nNC C13: {total_nc_count:.3f}"
    text += f"\n\nTotal C13 events: {(round(total_nc_count, 3) + round(channels['nue_C13'], 3)):.3f}"
    text += f"\nTotal events: {total_count:.3f}"
    plt.text(0.66, 0.12, text, transform=plt.gca().transAxes, linespacing = 1.3)

    plt.xlabel(r" True $E_\nu$ [MeV]")
    plt.ylabel("Number of Events per 0.5 MeV energy bin")
    plt.xlim(0,70)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.title("Unsmeared spectra of additional scintillator channels")
    plt.savefig(f"scripts/debug_plots/{flux}_unsmeared_missing_scint_channels.svg", bbox_inches = "tight", dpi = 900)
    plt.close()



if __name__ == "__main__":
    plot_missing_TMS_channels_unsmeared("garching")
    #plot_one_channel_weighted(flux, channel, detector, smeared)
    #plot_two_channel_smeared_unsmeared(title, save_as)
    #plot_one_channel_smeared_vs_unsmeared(flux, channel, detector)
    #plot_all_NC_channels_iron()
    pass