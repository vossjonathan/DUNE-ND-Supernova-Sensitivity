import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib  import Path
import uproot
from scripts.config import DETECTOR_SMEARING_CONFIG, ENERGY_GRID, ALL_DETECTOR, iron_channels, argon_channels, lead_channels, scint_channels
from scripts.helper import load_events_weighted

SNOWGLOBES = Path.home()/"software"/"snowglobes"
OUT = Path.home()/"software"/"snowglobes"/"out"

def plot_all_TMS_iron_scint(flux):
    #channels with geant4 smearing matrix
    channels_scint = ALL_DETECTOR["TMS_scint"]["channels"] #import from config.py
    channels_iron = ALL_DETECTOR["TMS_iron"]["channels"]

    total_iron_ES = np.zeros(200)
    total_scint_ES = np.zeros(200)
    total_events = np.zeros(200)
    total_C12_NC = np.zeros(200)

    #iron ES
    for name in channels_iron.keys():
        if name[-1] == "e":

            events_smeared_w = load_events_weighted(flux, name, "TMS_iron", smeared = True)
            total_iron_ES += events_smeared_w
            total_events += events_smeared_w

    
    for name in channels_scint.keys():
        #scint ES
        if name[-1] == "e":
            events_smeared_w = load_events_weighted(flux, name, "TMS_scint", smeared = True)
            total_scint_ES += events_smeared_w
            total_events += events_smeared_w
        #C12 NC
        if name[-1] == "2":
            events_smeared_w = load_events_weighted(flux, name, "TMS_scint", smeared = True)
            total_C12_NC += events_smeared_w
            total_events += events_smeared_w
            

    #scint IBD

    events_smeared_IBD_w = load_events_weighted(flux, "ibd", "TMS_scint", True)
    total_events += events_smeared_IBD_w
    
    energy = ENERGY_GRID#data_smeared_IBD[:, 0] * 1000 #using this for all channels as energy binning is same for all

    #iron CC nue
    events_smeared_nue_w = load_events_weighted(flux, "nue_Fe56", "TMS_iron", True)
    total_events += events_smeared_nue_w
    

    #iron CC nuebar
    events_smeared_nuebar_w = load_events_weighted(flux, "nuebar_Fe56", "TMS_iron", True)
    total_events += events_smeared_nuebar_w

    #iron NC all channels
    NC_channels = ["nc_nue_Fe56", "nc_nuebar_Fe56", "nc_numu_Fe56", "nc_numubar_Fe56", "nc_nutau_Fe56", "nc_nutaubar_Fe56"]
    NC_Fe_events_total = np.zeros(200)
    for channel in NC_channels:
        events = load_events_weighted(flux, channel, "TMS_iron", True)
        NC_Fe_events_total += events

    total_events += NC_Fe_events_total

    print("NC on Fe: ", np.sum(NC_Fe_events_total))
    print("NC on C12: ", np.sum(total_C12_NC))
    print("ES on Fe: ", np.sum(total_iron_ES))
    print("ES on Scint: ", np.sum(total_scint_ES))
    print("IBD on Scint ", np.sum(events_smeared_IBD_w))
    print("CC nue on Fe: ", np.sum(events_smeared_nue_w))
    print("CC nuebar on Fe: ", np.sum(events_smeared_nuebar_w))
    print("Total events: ", np.sum(total_events))
    mask = energy[1:] <= 15.0
    total_events_cut = np.sum(total_events[mask])
    print("Total events <= 15 Mev", total_events_cut)
    print("Ratio cut / total: ", total_events_cut / np.sum(total_events))

    plt.stairs(NC_Fe_events_total, energy, baseline = None, label="NC on Fe", color="cyan", linestyle = "-")
    plt.stairs(total_C12_NC, energy, baseline = None, label = r"NC on C12", color = "grey", linestyle = "-")
    plt.stairs(total_iron_ES, energy, baseline = None, label=r"$\nu, e^-$ scattering in Fe", color="blue", linestyle = "-")
    plt.stairs(total_scint_ES,energy, baseline = None,label=r"$\nu, e^-$ scattering in scint", color="red", linestyle = "-")
    plt.stairs(events_smeared_IBD_w,energy, baseline = None,label="IBD on scint", color="orange", linestyle = "-")
    plt.stairs(events_smeared_nue_w,energy, baseline = None,label=r"CC $\nu_e$ on Fe ", color="green", linestyle = "-")
    plt.stairs(events_smeared_nuebar_w,energy, baseline = None,label=r"CC $\bar\nu_e$ on Fe ", color="purple", linestyle = "-")
    plt.stairs(total_events, energy, baseline = None,label="Total", color="black", linestyle = "-", linewidth = 1.6)
 
    plt.legend()
    plt.grid(True, alpha = 0.3)
    plt.xlim(0, 20)
    plt.text(0.56, 0.46, f"Total events smeared: {total_events.sum():.2f}", transform=plt.gca().transAxes)
    plt.xlabel("Deposited E in scint [MeV]")
    plt.ylabel("Number of events per 0.5 MeV bin")
    #plt.title("Supernova Signal in TMS Detector\n Garching flux, no additional Threshold ")
    plt.savefig(f"debug_plots/{flux}_TMS_signal_preliminary_NC_C12.svg", bbox_inches = "tight")


def plot_total_and_unsmeared_argon(detector, flux):
    #enter detector and flux as strings, e.g. detector = "ar40kt", flux = "livermore"


    total_events_unsmeared = np.zeros(200)
    total_events_smeared = np.zeros(200)


    for channel in ALL_DETECTOR[detector]["channels"].keys():

        events_unsmeared = load_events_weighted(flux, channel, detector, smeared = False)
        events_smeared = load_events_weighted(flux, channel, detector, smeared = True)

        total_events_unsmeared += events_unsmeared
        total_events_smeared += events_smeared

    print("unsmeared", np.sum(total_events_unsmeared))
    print("smeared", np.sum(total_events_smeared))

    plt.stairs(total_events_smeared, ENERGY_GRID, label="Smeared: reconstructed E", color="blue")
    plt.stairs(total_events_unsmeared, ENERGY_GRID,  label="Unsmeared: true E", color="red")
    plt.xlabel(r" E [MeV]")
    plt.ylabel("Number of Events")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.title(f"{flux} {detector} smeared/unsmeared across all channels")
    plt.savefig(f"debug_plots/{flux}_{detector}_smeared_unsmeared_all_channels.png")


def plot_different_smeared_signals_argon(detector, flux):
    #enter detector and flux as strings, e.g. detector = "ar40kt", flux = "livermore"


    channels = ALL_DETECTOR[detector]["channels"]
    total_nu_e_events_smeared = np.zeros(200)
    total_nc_events_smeared = np.zeros(200)
   

    for channel, weight in list(channels.items())[:6]:

        smeared = OUT/f"{flux}_{channel}_{detector}_events_smeared_unweighted.dat"

        data_smeared = np.loadtxt(smeared, max_rows=200)

        #energy_smeared = data_smeared[:, 0] * 1000
        events_smeared = data_smeared[:, 1]

        events_smeared_w = events_smeared * weight
        total_nu_e_events_smeared += events_smeared_w

    smeared_nue_Ar40 = OUT/f"{flux}_nue_Ar40_{detector}_events_smeared_unweighted.dat"
    data_smeared_nue_Ar40 = np.loadtxt(smeared_nue_Ar40, max_rows=200)
    events_smeared_nue_Ar40 = data_smeared_nue_Ar40[:, 1]
    energy_smeared = np.linspace(0.5, 100, 201) #in MeV

    smeared_nuebar_Ar40 = OUT/f"{flux}_nuebar_Ar40_{detector}_events_smeared_unweighted.dat"
    data_smeared_nuebar_Ar40 = np.loadtxt(smeared_nuebar_Ar40, max_rows=200)
    events_smeared_nuebar_Ar40 = data_smeared_nuebar_Ar40[:, 1]


    for channel, weight in list(channels.items())[8:]:

        smeared = OUT/f"{flux}_{channel}_{detector}_events_smeared_unweighted.dat"

        data_smeared = np.loadtxt(smeared, max_rows=200)

        #energy_smeared = data_smeared[:, 0] * 1000
        events_smeared = data_smeared[:, 1]

        events_smeared_w = events_smeared * weight
        total_nc_events_smeared += events_smeared_w

    total_events = total_nu_e_events_smeared + total_nc_events_smeared + events_smeared_nue_Ar40 + events_smeared_nuebar_Ar40
    
    plt.figure()
    plt.stairs(total_nu_e_events_smeared, energy_smeared, label=r"$\nu, e^-$ scattering", color="blue", baseline = None, linestyle = "-")
    plt.stairs(total_nc_events_smeared,energy_smeared, label="NC Interactions", color="red", baseline = None, linestyle = "-")
    plt.stairs(events_smeared_nue_Ar40,energy_smeared,label=r"$\nu_e$ Ar40", color="green", baseline = None, linestyle = "-")
    plt.stairs(events_smeared_nuebar_Ar40, energy_smeared,label=r"$\bar{\nu}_e$ Ar40", color="orange", baseline = None, linestyle = "-")
    plt.stairs(total_events, energy_smeared,label="Total", color="black", baseline = None, linestyle = "-", linewidth = 1.6)
    total_count = np.sum(total_events)
    plt.text(0.92, 0.665,f"Total events: {total_count:.2f}", transform=plt.gca().transAxes,ha="right",va="top")
#'''f"CC nue: {np.sum(events_smeared_nue_Ar40):.2f}\n"
#f"CC nuebar: {np.sum(events_smeared_nuebar_Ar40):.2f}\n"
#f"NC combined: {np.sum(total_nc_events_smeared):.2f}\n"
##f"eES combined: {np.sum(total_nu_e_events_smeared):.2f}\n",
#transform=plt.gca().transAxes,ha="right",va="top")'''

    plt.xlabel(r"Detected energy $E_{det}$ [MeV]")
    plt.ylabel("Number of Events per 0.5 MeV energy bin")
    plt.xlim(0,50)
    plt.legend()
    plt.grid(True, alpha=0.3)
    #plt.title(f"{flux} {detector} smeared signal for differend channels")
    #plt.title(rf"""NDLAr supernova signal across all channels
    #basic ar40kt response, {flux}, no additional Threshold""")
    plt.savefig(f"debug_plots/{flux}_{detector}_different_smeared_channels_stairs.svg", bbox_inches = "tight", dpi = 900)
    plt.close()
    return total_count

def plot_different_smeared_signals_scint(detector, flux):
    #enter detector and flux as strings, e.g. detector = "ar40kt", flux = "livermore"
    if detector == "TMS_scint":
        detector_name = "TMS (only Scintillator)"
    else:
        detector_name = detector

    channels = ALL_DETECTOR[detector]["channels"]

    total_nu_e_events_smeared = np.zeros(200)
    total_C12_events_smeared = np.zeros(200)
    total_C13_events_smeared = np.zeros(200)  

    #ibd channel
    smeared_ibd = OUT/f"{flux}_ibd_{detector}_events_smeared_unweighted.dat"
    data_smeared_ibd = np.loadtxt(smeared_ibd, max_rows=200)
    events_smeared_ibd = data_smeared_ibd[:, 1]
    energy_smeared = np.linspace(0.5, 100, 201)
    events_smeared_ibd_w = events_smeared_ibd * channels["ibd"]



    for channel, weight in list(channels.items())[1:7]:

        smeared = OUT/f"{flux}_{channel}_{detector}_events_smeared_unweighted.dat"

        data_smeared = np.loadtxt(smeared, max_rows=200)

        #energy_smeared = data_smeared[:, 0] * 1000
        events_smeared = data_smeared[:, 1]

        events_smeared_w = events_smeared * weight
        total_nu_e_events_smeared += events_smeared_w

    total_C12_NC_events = np.zeros(200)
    total_C12_nue_events = np.zeros(200)
    total_C12_nuebar_events = np.zeros(200)


    for channel, weight in list(channels.items())[7:15]:

        smeared = OUT/f"{flux}_{channel}_{detector}_events_smeared_unweighted.dat"

        data_smeared = np.loadtxt(smeared, max_rows=200)

        #energy_smeared = data_smeared[:, 0] * 1000
        events_smeared = data_smeared[:, 1]

        events_smeared_w = events_smeared * weight

        if channel == "nue_C12":
            total_C12_nue_events += events_smeared_w

        elif channel == "nuebar_C12":
            total_C12_nuebar_events += events_smeared_w

        else:
            total_C12_NC_events += events_smeared_w
            
        total_C12_events_smeared += events_smeared_w


    for channel, weight in list(channels.items())[15:]:

        smeared = OUT/f"{flux}_{channel}_{detector}_events_smeared_unweighted.dat"

        data_smeared = np.loadtxt(smeared, max_rows=200)

        #energy_smeared = data_smeared[:, 0] * 1000
        events_smeared = data_smeared[:, 1]

        events_smeared_w = events_smeared * weight
        total_C13_events_smeared += events_smeared_w

    total_events = total_nu_e_events_smeared + total_C12_events_smeared + total_C13_events_smeared + events_smeared_ibd_w

    i = np.argmax(total_C13_events_smeared)

    print("C13 peak energy:", energy_smeared[i], "MeV")
    print("C13 peak height:", total_C13_events_smeared[i])
    
    print("ES:", np.sum(total_nu_e_events_smeared))
    print("NC C12: ", np.sum(total_C12_NC_events))
    print("nue C12: ", np.sum(total_C12_nue_events))
    print("nuebar C12: ", np.sum(total_C12_nuebar_events))
    print("Summed C12:", np.sum(total_C12_events_smeared))
    print("C13:", np.sum(total_C13_events_smeared))
    print("IBD:", np.sum(events_smeared_ibd_w))
    print("Total:", np.sum(total_events))
    plt.figure()
    plt.stairs( total_nu_e_events_smeared,energy_smeared, label=r"$\nu, e^-$ scattering", color="blue", baseline = None, linestyle = "-")
    plt.stairs(total_C12_events_smeared, energy_smeared, label="C12 Interactions", color="red", baseline = None, linestyle = "-")
    plt.stairs( total_C13_events_smeared,energy_smeared, label="C13 Interactions", color="orange", baseline = None,  linestyle = "-")
    plt.stairs(events_smeared_ibd_w, energy_smeared, label="IBD", color="green", baseline = None, linestyle = "-")
    plt.stairs(total_events,energy_smeared,  label="Total", color="black", baseline = None, linestyle = "-", linewidth = 1.6)

    plt.xlabel(r" Deposited E in Scint$ [MeV]")
    plt.ylabel("Number of Events / 0.5 MeV bin")
    plt.legend()
    plt.xlim(0,30)
    plt.ylim(bottom = 0)
    plt.grid(True, alpha=0.3)
    total_count = np.sum(total_events)
    #plt.title(f"{flux} {detector} smeared signal for differend channels")
    plt.text(0.905, 0.66,f"Total events: {total_count:.2f}",transform=plt.gca().transAxes,ha="right",va="top")
    plt.title(fr"""{detector_name} SN signal (10kpc) across all channels
    {flux.capitalize()}, no additional threshold""")
    plt.savefig(f"debug_plots/{flux}_{detector}_different_smeared_channels_stairs.png")
    plt.close()
    return total_count



def plot_different_smeared_signals_lead(detector, flux):
    #enter detector and flux as strings, e.g. detector = "ar40kt", flux = "livermore"

    channels = ALL_DETECTOR[detector]["channels"]


    total_nu_e_events_smeared = np.zeros(200)
    total_nc_1n_events_smeared = np.zeros(200)
    total_nc_2n_events_smeared = np.zeros(200)  

    #cc 1n channel
    smeared_cc_1n = OUT/f"{flux}_nue_Pb208_1n_{detector}_events_smeared_unweighted.dat"
    data_smeared_cc_1n = np.loadtxt(smeared_cc_1n, max_rows=200)
    events_smeared_cc_1n = data_smeared_cc_1n[:, 1]
    energy_smeared = data_smeared_cc_1n[:, 0] * 1000
    events_smeared_cc_1n_w = events_smeared_cc_1n * channels["nue_Pb208_1n"]

    #cc 2n channel
    smeared_cc_2n = OUT/f"{flux}_nue_Pb208_2n_{detector}_events_smeared_unweighted.dat"
    data_smeared_cc_2n = np.loadtxt(smeared_cc_2n, max_rows=200)
    events_smeared_cc_2n = data_smeared_cc_2n[:, 1]
    energy_smeared = np.linspace(0.5, 100, 201)
    events_smeared_cc_2n_w = events_smeared_cc_2n * channels["nue_Pb208_2n"]

    for channel, weight in list(channels.items())[:6]:

        smeared = OUT/f"{flux}_{channel}_{detector}_events_smeared_unweighted.dat"

        data_smeared = np.loadtxt(smeared, max_rows=200)

        #energy_smeared = data_smeared[:, 0] * 1000
        events_smeared = data_smeared[:, 1]

        events_smeared_w = events_smeared * weight
        total_nu_e_events_smeared += events_smeared_w

    for channel, weight in list(channels.items())[8:14]:

        smeared = OUT/f"{flux}_{channel}_{detector}_events_smeared_unweighted.dat"

        data_smeared = np.loadtxt(smeared, max_rows=200)

        #energy_smeared = data_smeared[:, 0] * 1000
        events_smeared = data_smeared[:, 1]

        events_smeared_w = events_smeared * weight
        total_nc_1n_events_smeared += events_smeared_w


    for channel, weight in list(channels.items())[14:]:

        smeared = OUT/f"{flux}_{channel}_{detector}_events_smeared_unweighted.dat"

        data_smeared = np.loadtxt(smeared, max_rows=200)

        #energy_smeared = data_smeared[:, 0] * 1000
        events_smeared = data_smeared[:, 1]

        events_smeared_w = events_smeared * weight
        total_nc_2n_events_smeared += events_smeared_w

    total_events = total_nu_e_events_smeared + total_nc_1n_events_smeared + total_nc_2n_events_smeared + events_smeared_cc_1n_w + events_smeared_cc_2n_w
    #i = np.argmax(total_nc_2n_events_smeared)

    #print("C13 peak energy:", energy_smeared[i], "MeV")
    #print("C13 peak height:", total_C13_events_smeared[i])
    
    print("ES:", np.sum(total_nu_e_events_smeared))
    print("NC 1n:", np.sum(total_nc_1n_events_smeared))
    print("NC 2n:", np.sum(total_nc_2n_events_smeared))
    print("CC 1n:", np.sum(events_smeared_cc_1n_w))
    print("CC 2n:", np.sum(events_smeared_cc_2n_w))
    print("Total:", np.sum(total_events))

    plt.figure()
    plt.stairs(total_nu_e_events_smeared, energy_smeared, label=r"$\nu, e^-$ scattering", color="blue", linestyle = "-")
    plt.stairs( total_nc_1n_events_smeared, energy_smeared,label="NC 1n Interactions", color="red", linestyle = "-")
    plt.stairs( total_nc_2n_events_smeared, energy_smeared,label="NC 2n Interactions", color="orange", linestyle = "-")
    plt.stairs(events_smeared_cc_1n_w,energy_smeared,  label="CC 1n", color="green", linestyle = "-")
    plt.stairs(events_smeared_cc_2n_w, energy_smeared, label="CC 2n", color="purple", linestyle = "-")
    plt.stairs(total_events, energy_smeared,  label=f"Total", color="black", linestyle = "-")

    total_count = np.sum(total_events)
    #plt.text(0.97, 0.73, f"total events: {total_count:.2f}")
    plt.text(0.88, 0.605,f"Total events: {total_count:.2f}",transform=plt.gca().transAxes,ha="right",va="top")
    plt.xlabel(r" true neutrino energy $E_\nu$ [MeV]")
    plt.ylabel("Number of Events per 0.5 MeV energy bin")
    plt.xlim(0, 60)
    plt.legend()
    plt.grid(True, alpha=0.3)
    #plt.title(f"{flux} {detector} smeared signal for differend channels")
    plt.title(f"ECAL (only lead) supernova signal across all channels\n {flux}, unsmeared signal")
    plt.savefig(f"debug_plots/{flux}_{detector}_different_smeared_channels_stairs.png")
    plt.close()
    return total_count

def plot_different_smeared_signals_iron(detector, flux):
    #enter detector and flux as strings, e.g. detector = "ar40kt", flux = "livermore"

    if detector == "TMS_iron":
        detector_name = "TMS (only iron)"
    else:
        detector_name = detector 

    channels = ALL_DETECTOR[detector]["channels"]

    total_nu_e_events_smeared = np.zeros(200)
    total_nc_events_smeared = np.zeros(200)
  

    #nue_Fe56 channel
    smeared_nue_Fe56 = OUT/f"{flux}_nue_Fe56_{detector}_events_smeared_unweighted.dat"
    data_smeared_nue_Fe56 = np.loadtxt(smeared_nue_Fe56, max_rows=200)
    events_smeared_nue_Fe56 = data_smeared_nue_Fe56[:, 1]
    energy_smeared = np.linspace(0.5, 100, 201)
    events_smeared_nue_Fe56_w = events_smeared_nue_Fe56 * channels["nue_Fe56"]

    #nuebar_Fe56 channel
    smeared_nuebar_Fe56 = OUT/f"{flux}_nuebar_Fe56_{detector}_events_smeared_unweighted.dat"
    data_smeared_nuebar_Fe56 = np.loadtxt(smeared_nuebar_Fe56, max_rows=200)
    events_smeared_nuebar_Fe56 = data_smeared_nuebar_Fe56[:, 1]
    energy_smeared = np.linspace(0.5, 100, 201)
    events_smeared_nuebar_Fe56_w = events_smeared_nuebar_Fe56 * channels["nuebar_Fe56"]



    for channel, weight in list(channels.items())[0:6]:

        smeared = OUT/f"{flux}_{channel}_{detector}_events_smeared_unweighted.dat"

        data_smeared = np.loadtxt(smeared, max_rows=200)

        #energy_smeared = data_smeared[:, 0] * 1000
        events_smeared = data_smeared[:, 1]

        events_smeared_w = events_smeared * weight
        total_nu_e_events_smeared += events_smeared_w

    for channel, weight in list(channels.items())[8:]:

        smeared = OUT/f"{flux}_{channel}_{detector}_events_smeared_unweighted.dat"

        data_smeared = np.loadtxt(smeared, max_rows=200)

        #energy_smeared = data_smeared[:, 0] * 1000
        events_smeared = data_smeared[:, 1]

        events_smeared_w = events_smeared * weight
        total_nc_events_smeared += events_smeared_w


    energy = np.linspace(0.5, 100, 201)
    total_events = total_nu_e_events_smeared + total_nc_events_smeared + events_smeared_nue_Fe56_w + events_smeared_nuebar_Fe56_w

    
    print("ES:", np.sum(total_nu_e_events_smeared))
    print("NC:", np.sum(total_nc_events_smeared))
    print("nue_Fe56:", np.sum(events_smeared_nue_Fe56_w))
    print("nuebar_Fe56:", np.sum(events_smeared_nuebar_Fe56_w))
    print("Total:", np.sum(total_events))
    
    plt.figure()
    plt.stairs(total_nu_e_events_smeared, energy , label=r"$\nu, e^-$ scattering", baseline = None, color="blue", linestyle = "-")
    plt.stairs(total_nc_events_smeared,energy , label="NC on Fe", color="red", baseline = None, linestyle = "-")
    plt.stairs(events_smeared_nue_Fe56_w,energy , label=r"CC $\nu_e$ on Fe", color="orange", baseline = None, linestyle = "-")
    plt.stairs(events_smeared_nuebar_Fe56_w,energy , label=r"CC $\bar\nu_e$ on Fe", color="green", baseline = None, linestyle = "-")
    plt.stairs(total_events,energy , label="Total", color="black", baseline = None, linestyle = "-", linewidth = 1.6)

    plt.xlabel(r" Deposited E in Scint [MeV]")
    plt.ylabel("Number of Events / 0.5 MeV bin")
    plt.legend()
    plt.xlim(0,20)
    plt.ylim(bottom = 0)
    plt.grid(True, alpha=0.3)
    total_count = np.sum(total_events)
    plt.title(f" {detector_name} SN signal (10kpc) for different channels\n{flux.capitalize()} flux, no additional threshold")
    plt.text(0.92, 0.67,f"Total events: {total_count:.2f}",transform=plt.gca().transAxes,ha="right",va="top")
    #plt.title("TMS (scintillator only) supernova signal across all channels\n basic scint20kt response")
    plt.savefig(f"debug_plots/{flux}_{detector}_different_smeared_channels.png")
    plt.close()
    total_count = np.sum(total_events)
    return total_count


def compare_detectors_bar_plot(flux, smeared):
    #working TMS iron channels, existing smearing matrix:

    total_TMS_iron = 0
    for channel in ALL_DETECTOR["TMS_iron"]["channels"].keys():
        events = load_events_weighted(flux, channel, "TMS_iron", smeared).sum()
        total_TMS_iron += events
    #working TMS scint channels, existing smearing matrix:
    TMS_scint_channel = ["ibd","nue_e", "nuebar_e", "numu_e", "numubar_e", "nutau_e", "nutaubar_e", "nc_nue_C12", "nc_nuebar_C12", "nc_numu_C12", "nc_numubar_C12", "nc_nutau_C12", "nc_nutaubar_C12"]
    all_scint = ALL_DETECTOR["TMS_scint"]["channels"].keys()
    total_TMS_scint = 0
    total_STT = 0
    total_ECAL_scint = 0
    if smeared:
        for channel in DETECTOR_SMEARING_CONFIG["TMS_scint"]["channels"].keys():
            events = load_events_weighted(flux, channel, "TMS_scint", smeared).sum()
            total_TMS_scint += events

    else:
        for channel in all_scint:
            events = load_events_weighted(flux, channel, "TMS_scint", smeared).sum()
            total_TMS_scint += events


    for channel in all_scint:

        events_STT = load_events_weighted(flux, channel, "STT", smeared).sum()
        total_STT += events_STT

        events_ECAL_scint = load_events_weighted(flux, channel, "ECAL_scint", smeared).sum()
        total_ECAL_scint += events_ECAL_scint


    #argon_channel =  ["nc_nue_Ar40","nc_nuebar_Ar40", "nc_numu_Ar40", "nc_numubar_Ar40", "nc_nutau_Ar40", "nc_nutaubar_Ar40","nue_e", "nuebar_e", "numu_e", "numubar_e", "nutau_e", "nutaubar_e"]
    all_argon = ALL_DETECTOR["NDLAr"]["channels"].keys()
    total_NDLAr = 0
    total_GRAIN = 0
    

    for channel in all_argon:
        events_NDLAr = load_events_weighted(flux, channel, "NDLAr", smeared).sum()
        events_GRAIN = load_events_weighted(flux, channel, "GRAIN", smeared).sum()

        total_NDLAr += events_NDLAr
        total_GRAIN += events_GRAIN


    all_lead = ALL_DETECTOR["ECAL_lead"]["channels"].keys()
    total_ECAL_lead = 0
    for channel in all_lead:
        events_ECAL_lead = load_events_weighted(flux, channel, "ECAL_lead", smeared).sum()
        total_ECAL_lead += events_ECAL_lead
             
    count_NDLAr = total_NDLAr
    count_TMS_scint = total_TMS_scint
    count_ECAL_lead= total_ECAL_lead
    count_ECAL_scint = total_ECAL_scint
    count_STT = total_STT
    count_GRAIN = total_GRAIN
    count_TMS_iron = total_TMS_iron

    counts = [count_NDLAr, count_TMS_scint, count_TMS_iron, count_ECAL_lead, count_ECAL_scint, count_STT, count_GRAIN]
    total_counts = [count_NDLAr, count_TMS_scint + count_TMS_iron, count_ECAL_lead + count_ECAL_scint, count_STT, count_GRAIN]

    material_colors = {'Argon': 'tab:green', 'Scintillator': 'tab:blue', 'Iron': 'tab:red', 'Lead': 'tab:purple'}   

    legend_patches = [
        mpatches.Patch(color="tab:green", label="Argon"),
        mpatches.Patch(color="tab:blue", label="Scintillator"),
        mpatches.Patch(color="tab:red", label="Iron"),
        mpatches.Patch(
            facecolor="tab:purple",
            #hatchcolor="white",
            #hatch="////",
            label="Lead"
        )
    ]
    
    plt.rcParams.update({'font.size': 16})
    plt.figure(figsize=(8, 5))
    plt.legend(handles=legend_patches, loc='upper right', framealpha=1.0)
    
    plt.bar(0, count_NDLAr, label="NDLAr: argon",color = "tab:green")
    plt.bar(1, count_TMS_iron, label="TMS: scint + iron",color = "tab:red")
    plt.bar(1, count_TMS_scint, bottom = count_TMS_iron, color = "tab:blue")
    
    plt.bar(2, count_ECAL_lead, label="ECAL: lead + scint", color = "tab:purple")#, hatch = "////", hatchcolor = "white")
    plt.bar(2, count_ECAL_scint, bottom=count_ECAL_lead,  color = "tab:blue")

    
    plt.bar(3, count_STT, label="STT: scint", color = "tab:blue")
    plt.bar(4, count_GRAIN, label="GRAIN: argon", color = "tab:green")

    #plt.text(2, count_ECAL_lead / 2,"lead", ha="center", va="center", color="black", fontsize=12)
    #plt.text(2, count_ECAL_lead + count_ECAL_scint / 2,"scint", ha="center", va="center", color="black", fontsize=12)
    #plt.text(0, count_NDLAr/ 2,"argon", ha="center", va="center", color="black", fontsize=12)
    #plt.text(1, count_TMS_scint/ 2,"scint", ha="center", va="center", color="black", fontsize=12)
    #plt.text(1, count_TMS_scint + count_TMS_iron / 2,"iron", ha="center", va="center", color="black", fontsize=12)
    #plt.text(3, count_STT / 2,"scint", ha="center", va="center", color="black", fontsize=12)
    off= 2
    plt.text(2, count_ECAL_lead + count_ECAL_scint + off,f"{(count_ECAL_scint + count_ECAL_lead):.2f}", ha="center", va="center", color="black")
    plt.text(0, count_NDLAr + off ,f"{count_NDLAr:.2f}", ha="center", va="center", color="black")
    plt.text(1, count_TMS_scint + count_TMS_iron + off,f"{count_TMS_scint + count_TMS_iron:.2f}", ha="center", va="center", color="black")
    plt.text(3, count_STT + off,f"{count_STT:.2f}", ha="center", va="center", color="black")
    plt.text(4, count_GRAIN + off,f"{count_GRAIN:.2f}", ha="center", va="center", color="black")
    plt.text(x = 0.695, y = 0.61, s = f"Total: {sum(counts):.2f}",transform=plt.gca().transAxes, ha = "left", va = "top")


    plt.xticks([0, 1, 2, 3, 4], ["ND-LAr", "TMS", "ECAL", "STT", "GRAIN"])

    plt.ylabel("Expected number of interactions")
    plt.ylim(0, 1.3*max(total_counts))
    #plt.legend(handlelength = 0, handletextpad = 0)
    #plt.bar(detectors, counts)    if smeared: 
    if smeared:
        word = "smeared" 
    else:
        word = "unsmeared"
    #plt.title(f"Expected supernova events in DUNE near detectors, {word}, {flux.capitalize()} flux")
    plt.tight_layout()
    plt.savefig(f"debug_plots/{flux}_{word}_detector_comparison_new.svg")
    #plt.savefig(f"plotting/{flux}_{word}_detector_comparison_new.pdf", bbox_inches = "tight")
    plt.close()

if __name__ == "__main__":
    #plot_all_TMS_iron_scint(flux)
    #plot_total_and_unsmeared_argon(detector, flux)
    #plot_different_smeared_signals_argon(detector, flux)
    #plot_different_smeared_signals_scint(detector, flux)
    #plot_different_smeared_signals_lead(detector, flux)
    #plot_different_smeared_signals_iron(detector, flux)
    #compare_detectors_bar_plot(flux, smeared)
    pass