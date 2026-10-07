import numpy as np
import matplotlib.pyplot as plt
from pathlib  import Path
import matplotlib.patches as mpatches
import plotting.helper as helper
from config import iron_channels, scint_channels, lead_channels, argon_channels


SNOWGLOBES = Path.home()/"software"/"snowglobes"
OUT = Path.home()/"software"/"snowglobes"/"out"

def plot_total_and_unsmeared_argon(detector, flux):
    #enter detector and flux as strings, e.g. detector = "ar40kt", flux = "livermore"


    channels = argon_channels

    total_events_unsmeared = np.zeros(200)
    total_events_smeared = np.zeros(200)


    for channel, weight in channels.items():

        unsmeared = OUT/f"{flux}_{channel}_{detector}_events_unweighted.dat"
        smeared = OUT/f"{flux}_{channel}_{detector}_events_smeared_unweighted.dat"

        data_unsmeared = np.loadtxt(unsmeared, max_rows=200)  #only read 200 lines containing data
        data_smeared = np.loadtxt(smeared, max_rows=200)

        energy_unsmeared = data_unsmeared[:, 0] * 1000  # now in MeV
        energy_smeared = data_smeared[:, 0] * 1000
        events_unsmeared = data_unsmeared[:, 1]
        events_smeared = data_smeared[:, 1]

        events_unsmeared = events_unsmeared * weight
        events_smeared = events_smeared * weight

        total_events_unsmeared += events_unsmeared
        total_events_smeared += events_smeared

    print("unsmeared", np.sum(total_events_unsmeared))
    print("smeared", np.sum(total_events_smeared))

    plt.plot(energy_smeared, total_events_smeared, label="Smeared: reconstructed E", color="blue")
    plt.plot(energy_unsmeared, total_events_unsmeared, label="Unsmeared: true E", color="red")
    plt.xlabel(r" E [MeV]")
    plt.ylabel("Number of Events")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.title(f"{flux} {detector} smeared/unsmeared across all channels")
    plt.savefig(f"plotting/{flux}_{detector}_smeared_unsmeared_all_channels.png")



def plot_different_smeared_signals_argon(detector, flux):
    #enter detector and flux as strings, e.g. detector = "ar40kt", flux = "livermore"


    channels = argon_channels
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
    plt.savefig(f"plotting/{flux}_{detector}_different_smeared_channels_stairs.svg", bbox_inches = "tight", dpi = 900)
    plt.close()
    return total_count



def plot_different_smeared_signals_scint(detector, flux):
    #enter detector and flux as strings, e.g. detector = "ar40kt", flux = "livermore"
    if detector == "TMS_scint":
        detector_name = "TMS (only Scintillator)"
    else:
        detector_name = detector

    channels = scint_channels

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
    plt.savefig(f"plotting/{flux}_{detector}_different_smeared_channels_stairs.png")
    plt.close()
    return total_count



def plot_different_smeared_signals_lead(detector, flux):
    #enter detector and flux as strings, e.g. detector = "ar40kt", flux = "livermore"

    channels = lead_channels


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
    plt.savefig(f"plotting/{flux}_{detector}_different_smeared_channels_stairs.png")
    plt.close()
    return total_count

def plot_different_smeared_signals_iron(detector, flux):
    #enter detector and flux as strings, e.g. detector = "ar40kt", flux = "livermore"

    if detector == "TMS_iron":
        detector_name = "TMS (only iron)"
    else:
        detector_name = detector 

    channels = iron_channels

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
    plt.savefig(f"plotting/{flux}_{detector}_different_smeared_channels.png")
    plt.close()
    total_count = np.sum(total_events)
    return total_count


def compare_detectors_bar_plot(flux, smeared):
    #working TMS iron channels, existing smearing matrix:
    TMS_iron_channel = iron_channels.keys()
    total_TMS_iron= 0
    for channel in TMS_iron_channel:
        u, s =  helper.get_channel_totals("TMS_iron", "iron", channel, flux)
        if smeared:
            total_TMS_iron += s
        else:
            total_TMS_iron += u
    #working TMS scint channels, existing smearing matrix:
    TMS_scint_channel = ["ibd","nue_e", "nuebar_e", "numu_e", "numubar_e", "nutau_e", "nutaubar_e", "nc_nue_C12", "nc_nuebar_C12", "nc_numu_C12", "nc_numubar_C12", "nc_nutau_C12", "nc_nutaubar_C12"]
    all_scint = scint_channels.keys()
    total_TMS_scint = 0
    total_STT = 0
    total_ECAL_scint = 0
    for channel in all_scint:
        u, s = helper.get_channel_totals("TMS_scint", "scint", channel, flux)
        if smeared:
            total_TMS_scint += s
        else:
            total_TMS_scint += u


    for channel in all_scint:
        u_STT, s_STT = helper.get_channel_totals("STT", "scint", channel, flux)
        u_ECAL, s_ECAL = helper.get_channel_totals("ECAL_scint", "scint", channel, flux)

        if smeared:
            total_STT += s_STT
            total_ECAL_scint += s_ECAL
        else:
            total_STT += u_STT
            total_ECAL_scint += u_ECAL        



    #argon_channel =  ["nc_nue_Ar40","nc_nuebar_Ar40", "nc_numu_Ar40", "nc_numubar_Ar40", "nc_nutau_Ar40", "nc_nutaubar_Ar40","nue_e", "nuebar_e", "numu_e", "numubar_e", "nutau_e", "nutaubar_e"]
    all_argon = argon_channels.keys()
    total_NDLAr = 0
    total_GRAIN = 0
    

    for channel in all_argon:
        u_ND, s_ND = helper.get_channel_totals("NDLAr", "argon", channel, flux)
        u_G, s_G = helper.get_channel_totals("GRAIN", "argon", channel, flux)
        if smeared:
            total_NDLAr += s_ND  
            total_GRAIN += s_G
        else:
            total_NDLAr += u_ND
            total_GRAIN += u_G  


    all_lead = lead_channels.keys()
    total_ECAL_lead = 0
    for channel in all_lead:
        u, s = helper.get_channel_totals("ECAL_lead", "lead", channel, flux)
        if smeared:
            total_ECAL_lead += s  
        else:
            total_ECAL_lead += u
             
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
    plt.savefig(f"plotting/{flux}_{word}_detector_comparison.svg")
    #plt.savefig(f"plotting/{flux}_{word}_detector_comparison_new.pdf", bbox_inches = "tight")
    plt.close()


def plot_all_NC_channels_iron():
    channels = ['nc_nue_Fe56', 'nc_nuebar_Fe56', 'nc_numu_Fe56']
    total_nc_events_smeared = np.zeros(200)
    energy_smeared = np.linspace(0.5, 100, 201)
    for channel in channels:
        u, e = helper.get_channel_out_smeared_unsmeared("TMS_iron", "iron", channel, "garching")
        plt.stairs(e, energy_smeared, label=channel)
        plt.stairs(u, energy_smeared, label=channel + " unsmeared")

    plt.xlabel(r" Detected $E_{det}$ [MeV]")
    plt.ylabel("Number of Events per 0.5 MeV energy bin")
    plt.xlim(0,50)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.title("TMS iron NC channels comparison")
    plt.savefig(f"plotting/NC_channels_comparison.png")
    plt.close()


if __name__ == "__main__":
    #plot_total_and_unsmeared_argon("NDLAr", "garching")
    plot_different_smeared_signals_argon("NDLAr", "garching")
    #plot_different_smeared_signals_scint("TMS_scint", "garching")
    #plot_different_smeared_signals_lead("ECAL_lead", "garching")
    #plot_different_smeared_signals_iron("TMS_iron", "garching")
    #compare_detectors_bar_plot("garching", smeared = False)
    #plot_all_NC_channels_iron()
