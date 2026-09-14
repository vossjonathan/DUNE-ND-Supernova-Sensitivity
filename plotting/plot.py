import numpy as np
import matplotlib.pyplot as plt
from pathlib  import Path
import uproot
import helper

SNOWGLOBES = Path.home()/"software"/"snowglobes"

#weights not considered, basic plot
def plot_one_channel_smeared_unsmeared():

    file_smeared = SNOWGLOBES/"out"/"garching_nc_nue_Fe56_TMS_iron_events_smeared_unweighted.dat"
    file_unsmeared = SNOWGLOBES/"out"/"garching_nc_nue_Fe56_TMS_iron_events_unweighted.dat"

    data_smeared = np.loadtxt(file_smeared, max_rows=200)
    data_unsmeared = np.loadtxt(file_unsmeared, max_rows=200)

    energy = np.linspace(0.5, 100, 201)
    energy_smeared = data_smeared[:, 0] * 1000 #now in MeV
    energy_unsmeared = data_unsmeared[:, 0] * 1000 #now in MeV

    events_smeared = data_smeared[:, 1]
    events_unsmeared = data_unsmeared[:, 1]

    plt.stairs(events_smeared, energy, label="Smeared: scintillator deposited E", color="blue")
    plt.stairs(events_unsmeared, energy, label="Unsmeared: true E", color="red")
    plt.xlim(0,50)
    plt.text(0.42, 0.75,f"Total events unsmeared: {events_unsmeared.sum():.2f}\nTotal events smeared: {events_smeared.sum():.2f}",transform=plt.gca().transAxes)#,ha="right",va="top")
    #plt.text(0.84, 0.77,f"Total events unsmeared: {events_unsmeared.sum():.2f}",transform=plt.gca().transAxes,ha="right",va="top")
    plt.xlabel(r" E [MeV]")
    plt.ylabel("Number of Events per bin")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.title(r"NC nue Fe 56 smeared unsmeared")#0% efficiency $\leq$ 5 MeV")
    plt.savefig("plotting/garching_TMS_iron_NC_nue_smeared_unsmeared.png")

#plot_one_channel_smeared_unsmeared()

def plot_two_channel_smeared_unsmeared():

    energy = np.linspace(0.5, 100, 201)

    file_unsmeared = SNOWGLOBES/"out"/"garching_nue_Fe56_TMS_iron_events_unweighted.dat"
    data_unsmeared = np.loadtxt(file_unsmeared, max_rows=200)
    events_unsmeared = data_unsmeared[:, 1]

    file_smeared_ALLOWED = SNOWGLOBES/"out"/"ALLOWED_garching_nue_Fe56_TMS_iron_events_smeared_unweighted.dat"
    file_smeared_NOTALLOWED = SNOWGLOBES/"out"/"NOTALLOWED_garching_nue_Fe56_TMS_iron_events_smeared_unweighted.dat"

    data_smeared_ALLOWED = np.loadtxt(file_smeared_ALLOWED, max_rows=200)
    data_smeared_NOTALLOWED = np.loadtxt(file_smeared_NOTALLOWED, max_rows=200)

    events_smeared_ALLOWED = data_smeared_ALLOWED[:, 1]
    events_smeared_NOTALLOWED = data_smeared_NOTALLOWED[:, 1]

    

    plt.stairs(events_smeared_ALLOWED, energy, label="MARLEY AA", color="blue")
    plt.stairs(events_smeared_NOTALLOWED, energy, label="MARLEY Default", color="red")
    plt.stairs(events_unsmeared, energy, label="Unsmeared Signal", color="black")
    plt.xlim(0,50)
    #plt.text(0.42, 0.75,f"Total events unsmeared: {events_unsmeared.sum():.2f}\nTotal events smeared: {events_smeared.sum():.2f}",transform=plt.gca().transAxes)#,ha="right",va="top")
    #plt.text(0.84, 0.77,f"Total events unsmeared: {events_unsmeared.sum():.2f}",transform=plt.gca().transAxes,ha="right",va="top")
    plt.xlabel(r" E [MeV]")
    plt.ylabel("Number of Events per bin")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.title(r"CC $\nu_e$ MARLEY AA/Default comparison")#0% efficiency $\leq$ 5 MeV")
    plt.savefig("plotting/MARLEY_AA_Default_comparison.png")

plot_two_channel_smeared_unsmeared()

def plot_one_channel_iron_smeared_unsmeared(channel):
    channels = {
        "nue_e" : 26,
        "nuebar_e" : 26,
        "numu_e" : 26,
        "numubar_e" : 26,
        "nutau_e" : 26,
        "nutaubar_e" : 26,
        "nue_Fe56" : 1,
        "nuebar_Fe56" : 1,
        "nc_nue_Fe56" : 1,
        "nc_nuebar_Fe56" : 1,
        "nc_numu_Fe56" : 1,
        "nc_numubar_Fe56" : 1,
        "nc_nutau_Fe56" : 1,
        "nc_nutaubar_Fe56" : 1,
    }
    file_smeared = SNOWGLOBES/"out"/f"garching_{channel}_TMS_iron_events_smeared_unweighted.dat"
    file_unsmeared = SNOWGLOBES/"out"/f"garching_{channel}_TMS_iron_events_unweighted.dat"

    data_smeared = np.loadtxt(file_smeared, max_rows=200)
    data_unsmeared = np.loadtxt(file_unsmeared, max_rows=200)

    energy_smeared = data_smeared[:, 0] * 1000 #now in MeV
    energy_unsmeared = data_unsmeared[:, 0] * 1000 #now in MeV

    events_smeared = data_smeared[:, 1]
    events_unsmeared = data_unsmeared[:, 1]

    events_smeared_w = channels[channel] * events_smeared
    events_unsmeared_w = channels[channel] * events_unsmeared

    plt.plot(energy_smeared, events_smeared_w, label="Smeared: scintillator deposited E", color="blue")
    plt.plot(energy_unsmeared, events_unsmeared_w, label="Unsmeared: true E", color="red")
    plt.text(0.42, 0.75,f"Total events unsmeared: {events_unsmeared_w.sum():.2f}\nTotal events smeared: {events_smeared_w.sum():.2f}",transform=plt.gca().transAxes)#,ha="right",va="top")
    #plt.text(0.84, 0.77,f"Total events unsmeared: {events_unsmeared.sum():.2f}",transform=plt.gca().transAxes,ha="right",va="top")
    plt.xlabel(r" E [MeV]")
    plt.ylabel("Number of Events per bin")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.title(r"NC nue channel TMS iron, unsmeared smeared")
    plt.savefig("plotting/garching_TMS_iron_nc_nue_unsmeared_smeared_weighted.png")


#plot_one_channel_iron_smeared_unsmeared("nc_nue_Fe56")


def plot_one_channel_scint_smeared_unsmeared(channel):
    channels = {
        "ibd":1,
        "nue_e" : 4,
        "nuebar_e" : 4,
        "numu_e" : 4,
        "numubar_e" : 4,
        "nutau_e" : 4,
        "nutaubar_e" : 4,
        "nue_C12" : 0.4945,
        "nuebar_C12" : 0.4945,
        "nc_nue_C12" : 0.4945,
        "nc_nuebar_C12" : 0.4945,
        "nc_numu_C12" : 0.4945,
        "nc_numubar_C12" : 0.4945,
        "nc_nutau_C12" : 0.4945,
        "nc_nutaubar_C12" : 0.4945,
        "nue_C13" : 0.0055,
        "nc_nue_C13" : 0.0055,
        "nc_nuebar_C13" : 0.0055,
        "nc_numu_C13" : 0.0055,
        "nc_numubar_C13" : 0.0055,
        "nc_nutau_C13" : 0.0055,
        "nc_nutaubar_C13" : 0.0055

    }
    file_smeared = SNOWGLOBES/"out"/f"garching_{channel}_TMS_scint_events_smeared_unweighted.dat"
    file_unsmeared = SNOWGLOBES/"out"/f"garching_{channel}_TMS_scint_events_unweighted.dat"

    data_smeared = np.loadtxt(file_smeared, max_rows=200)
    data_unsmeared = np.loadtxt(file_unsmeared, max_rows=200)

    energy_smeared = data_smeared[:, 0] * 1000 #now in MeV
    energy_unsmeared = data_unsmeared[:, 0] * 1000 #now in MeV

    events_smeared = data_smeared[:, 1]
    events_unsmeared = data_unsmeared[:, 1]

    events_smeared_w = channels[channel] * events_smeared
    events_unsmeared_w = channels[channel] * events_unsmeared

    plt.plot(energy_smeared, events_smeared_w, label="Smeared: scintillator deposited E", color="blue")
    plt.plot(energy_unsmeared, events_unsmeared_w, label="Unsmeared: true E", color="red")
    plt.text(0.42, 0.75,f"Total events unsmeared: {events_unsmeared_w.sum():.2f}\nTotal events smeared: {events_smeared_w.sum():.2f}",transform=plt.gca().transAxes)#,ha="right",va="top")
    #plt.text(0.84, 0.77,f"Total events unsmeared: {events_unsmeared.sum():.2f}",transform=plt.gca().transAxes,ha="right",va="top")
    plt.xlabel(r" E [MeV]")
    plt.ylabel("Number of Events per bin")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.title(r"ES $\nu_e$ TMS (only scint), garching, $E_{th}$ = 0.5 MeV")
    plt.savefig("plotting/garching_TMS_scint_nue_e_unsmeared_smeared_weighted.png")


#plot_one_channel_scint_smeared_unsmeared("nue_e")

def plot_all_TMS_iron_scint():
    #channels with geant4 smearing matrix
    channels_scint = {        
        "ibd":1,
        "nue_e" : 4,
        "nuebar_e" : 4,
        "numu_e" : 4,
        "numubar_e" : 4,
        "nutau_e" : 4,
        "nutaubar_e" : 4,
    }
    channels_iron = {
        "nue_e" : 26,
        "nuebar_e" : 26,
        "numu_e" : 26,
        "numubar_e" : 26,
        "nutau_e" : 26,
        "nutaubar_e" : 26,
        "nue_Fe56" : 1,
        "nuebar_Fe56" : 1,
        "nc_nue_Fe56" : 1,
        "nc_nuebar_Fe56" : 1,
        "nc_numu_Fe56" : 1,
        "nc_numubar_Fe56" : 1,
        "nc_nutau_Fe56" : 1,
        "nc_nutaubar_Fe56" : 1,
    }

    total_iron_ES = np.zeros(200)
    total_scint_ES = np.zeros(200)
    total_events = np.zeros(200)

    #iron ES
    for name in channels_iron.keys():
        if name[-1] == "e":
            file = (SNOWGLOBES/"out"/f"garching_{name}_TMS_iron_events_smeared_unweighted.dat")
            data_smeared = np.loadtxt(file, max_rows= 200)
            events_smeared = data_smeared[:, 1]
            events_smeared_w = events_smeared * channels_iron[name]
            total_iron_ES += events_smeared_w
            total_events += events_smeared_w

    #scint ES
    for name in channels_scint.keys():
        if name[-1] == "e":
            file = (SNOWGLOBES/"out"/f"garching_{name}_TMS_scint_events_smeared_unweighted.dat")
            data_smeared = np.loadtxt(file, max_rows= 200)
            events_smeared = data_smeared[:, 1]
            events_smeared_w = events_smeared * channels_scint[name]
            total_scint_ES += events_smeared_w
            total_events += events_smeared_w
            

    #scint IBD
    file_IBD = SNOWGLOBES/"out"/f"garching_ibd_TMS_scint_events_smeared_unweighted.dat"
    data_smeared_IBD = np.loadtxt(file_IBD, max_rows= 200)
    events_smeared_IBD = data_smeared_IBD[:, 1]
    events_smeared_IBD_w = events_smeared_IBD * channels_scint["ibd"]
    total_events += events_smeared_IBD_w
    
    energy = np.linspace(0.5, 100, 201)#data_smeared_IBD[:, 0] * 1000 #using this for all channels as energy binning is same for all
    #print(energy)
    #iron CC nue
    file_nue = SNOWGLOBES/"out"/f"garching_nue_Fe56_TMS_iron_events_smeared_unweighted.dat"
    data_smeared_nue = np.loadtxt(file_nue, max_rows= 200)
    events_smeared_nue = data_smeared_nue[:, 1]
    events_smeared_nue_w = events_smeared_nue * channels_iron["nue_Fe56"]
    total_events += events_smeared_nue_w
    

    #iron CC nuebar
    file_nuebar = SNOWGLOBES/"out"/f"garching_nuebar_Fe56_TMS_iron_events_smeared_unweighted.dat"
    data_smeared_nuebar = np.loadtxt(file_nuebar, max_rows= 200)
    events_smeared_nuebar = data_smeared_nuebar[:, 1]
    events_smeared_nuebar_w = events_smeared_nuebar * channels_iron["nuebar_Fe56"]
    total_events += events_smeared_nuebar_w
    #iron NC all channels
    NC_channels = ["nc_nue_Fe56", "nc_nuebar_Fe56", "nc_numu_Fe56", "nc_numubar_Fe56", "nc_nutau_Fe56", "nc_nutaubar_Fe56"]
    NC_events_total = np.zeros(200)
    for channel in NC_channels:
        u, e = helper.get_channel_out_smeared_unsmeared("TMS_iron", "iron", channel, "garching")
        NC_events_total += e

    total_events += NC_events_total

    #background
    background_file = SNOWGLOBES/"out"/f"garching_bg_chan_TMS_iron_events_unweighted.dat"
    background_data = np.loadtxt(background_file, max_rows = 200)
    background_events = background_data[:, 1]


    plt.stairs(NC_events_total, energy, baseline = None, label="NC on Fe", color="cyan", linestyle = "-")
    plt.stairs(total_iron_ES, energy, baseline = None, label=r"$\nu, e^-$ scattering in Fe", color="blue", linestyle = "-")
    plt.stairs(total_scint_ES,energy, baseline = None,label=r"$\nu, e^-$ scattering in scint", color="red", linestyle = "-")
    plt.stairs(events_smeared_IBD_w,energy, baseline = None,label="IBD on scint", color="orange", linestyle = "-")
    plt.stairs(events_smeared_nue_w,energy, baseline = None,label=r"CC $\nu_e$ on Fe ", color="green", linestyle = "-")
    plt.stairs(events_smeared_nuebar_w,energy, baseline = None,label=r"CC $\bar\nu_e$ on Fe ", color="purple", linestyle = "-")
    plt.stairs(total_events, energy, baseline = None,label="Total", color="black", linestyle = "-")
    #plt.stairs(background_events, energy, baseline = None, label = "Background 800ft", color = "grey", linestyle = "-")
    #plt.plot(energy, total_events,  label="Total", color="red", linestyle = "-")
    print("NC total:", sum(NC_events_total))
    plt.legend()
    plt.grid(True, alpha = 0.3)
    plt.xlim(0, 20)
    plt.text(0.56, 0.51, f"Total events smeared: {total_events.sum():.2f}", transform=plt.gca().transAxes)
    plt.xlabel("Deposited E in scint [MeV]")
    plt.ylabel("Number of events per 0.5 MeV bin")
    plt.title("Supernova Signal in TMS Detector\n Garching flux, no additional Threshold ")
    plt.savefig("plotting/TMS_signal_preliminary.png")
    

#plot_all_TMS_iron_scint()

def plot_threshold_comparison():


    file_smeared_0_5 = SNOWGLOBES/"out"/"garching_nuebar_Fe56_TMS_iron_events_smeared_unweighted_newgrid0.5.dat"
    file_smeared_1_0 = SNOWGLOBES/"out"/"garching_nuebar_Fe56_TMS_iron_events_smeared_unweighted_newgrid1.0.dat"
    file_smeared_1_5 = SNOWGLOBES/"out"/"garching_nuebar_Fe56_TMS_iron_events_smeared_unweighted_newgrid1.5.dat"
    file_smeared_2_0 = SNOWGLOBES/"out"/"garching_nuebar_Fe56_TMS_iron_events_smeared_unweighted_newgrid2.0.dat"
    file_smeared_3_0 = SNOWGLOBES/"out"/"garching_nuebar_Fe56_TMS_iron_events_smeared_unweighted_newgrid3.0.dat"
    file_smeared_4_0 = SNOWGLOBES/"out"/"garching_nuebar_Fe56_TMS_iron_events_smeared_unweighted_newgrid4.0.dat"
    file_smeared_5_0 = SNOWGLOBES/"out"/"garching_nuebar_Fe56_TMS_iron_events_smeared_unweighted_newgrid5.0.dat"
    file_smeared_8_0 = SNOWGLOBES/"out"/"garching_nuebar_Fe56_TMS_iron_events_smeared_unweighted_newgrid8.0.dat"


    file_unsmeared = SNOWGLOBES/"out"/"garching_nuebar_Fe56_TMS_iron_events_unweighted.dat"

    data_smeared_0_5 = np.loadtxt(file_smeared_0_5, max_rows=200)
    data_smeared_1_0 = np.loadtxt(file_smeared_1_0, max_rows=200)
    data_smeared_1_5 = np.loadtxt(file_smeared_1_5, max_rows=200)
    data_smeared_2_0 = np.loadtxt(file_smeared_2_0, max_rows=200)
    data_smeared_3_0 = np.loadtxt(file_smeared_3_0, max_rows=200)
    data_smeared_4_0 = np.loadtxt(file_smeared_4_0, max_rows=200)
    data_smeared_5_0 = np.loadtxt(file_smeared_5_0, max_rows=200)
    data_smeared_8_0 = np.loadtxt(file_smeared_8_0, max_rows=200)

    data_unsmeared = np.loadtxt(file_unsmeared, max_rows=200)

    energy_smeared = data_smeared_0_5[:, 0] * 1000 #now in MeV
    energy_unsmeared = data_unsmeared[:, 0] * 1000 #now in MeV

    events_smeared_0_5 = data_smeared_0_5[:, 1]
    events_smeared_1_0 = data_smeared_1_0[:, 1]
    events_smeared_1_5 = data_smeared_1_5[:, 1]
    events_smeared_2_0 = data_smeared_2_0[:, 1]
    events_smeared_3_0 = data_smeared_3_0[:, 1]
    events_smeared_4_0 = data_smeared_4_0[:, 1]
    events_smeared_5_0 = data_smeared_5_0[:, 1]
    events_smeared_8_0 = data_smeared_8_0[:, 1]

    events_unsmeared = data_unsmeared[:, 1]

    plt.plot(energy_unsmeared, events_unsmeared, label=r"Unsmeared: true E$_\nu$", color="red")

    plt.plot(energy_smeared, events_smeared_0_5, label=r"Smeared, $E_{th}$ = 0.5 MeV", color="blue", linestyle = "-")


    plt.text(0.55, 0.40,f"Total true events: {events_unsmeared.sum():.2f}\nThreshold / detected events:\n0.5 MeV: {events_smeared_0_5.sum():.2f}\n1.0 MeV: {(events_smeared_1_0.sum()):.2f}\n1.5 MeV: {events_smeared_1_5.sum():.2f}\n2.0 MeV: {events_smeared_2_0.sum():.2f}\n"
    f"3.0 MeV: {events_smeared_3_0.sum():.2f}\n"
    f"4.0 MeV: {events_smeared_4_0.sum():.2f}\n"
    f"5.0 MeV: {events_smeared_5_0.sum():.2f}\n"
    f"8.0 MeV: {events_smeared_8_0.sum():.2f}",
    transform=plt.gca().transAxes)


    #plt.text(0.838, 0.84,f"Total events unsmeared: {events_unsmeared.sum():.2f}",transform=plt.gca().transAxes,ha="right",va="top")
    plt.xlabel(r" E [MeV]")
    plt.ylabel("Number of Events per 0.5 MeV bin")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.title(r"CC $\bar\nu_e$, TMS (only iron) threshold comparison, garching")#0% efficiency $\leq$ 5 MeV")
    plt.savefig("plotting/garching_TMS_iron_nuebar_Fe56_threshold_comparison_newgrid.png")


#plot_threshold_comparison()

def plot_threshold_comparison_scatter():
    #iron and scint events
    iron_ES_w = 26
    scint_ES_w = 4

    total_iron_ES_events_per_threshold = []
    total_scint_ES_events_per_threshold = []


    channels = ["nue_e", "nuebar_e", "numu_e", "numubar_e", "nutau_e", "nutaubar_e"]
    thresholds = np.arange(0.5, 8.2, 0.5)
    for threshold in thresholds:
        total_iron_ES_events = np.zeros(200)
        total_scint_ES_events = np.zeros(200)
        for channel in channels:
            #iron
            file_smeared_ES_iron = SNOWGLOBES/"out"/f"garching_{channel}_TMS_iron_events_smeared_unweighted_{threshold}MeV.dat"
            data_smeared_ES_iron = np.loadtxt(file_smeared_ES_iron, max_rows = 200)
            events_smeared_ES_iron_w = data_smeared_ES_iron[:,1] * iron_ES_w
            total_iron_ES_events += events_smeared_ES_iron_w
            #scint
            file_smeared_ES_scint = SNOWGLOBES/"out"/f"garching_{channel}_TMS_scint_events_smeared_unweighted_{threshold}MeV.dat"
            data_smeared_ES_scint = np.loadtxt(file_smeared_ES_scint, max_rows = 200)
            events_smeared_ES_scint_w = data_smeared_ES_scint[:,1] * scint_ES_w
            total_scint_ES_events += events_smeared_ES_scint_w            

        total_iron_ES_events_per_threshold.append(total_iron_ES_events.sum())
        total_scint_ES_events_per_threshold.append(total_scint_ES_events.sum())

    total_iron_ES_events_per_threshold = np.array(total_iron_ES_events_per_threshold)
    total_scint_ES_events_per_threshold = np.array(total_scint_ES_events_per_threshold)
    #get total unsmeared events
    
    unsmeared_ES_iron_events = np.zeros(200)
    unsmeared_ES_scint_events = np.zeros(200)
    
    for channel in channels:
        
        file_unsmeared_ES_iron = SNOWGLOBES/"out"/f"garching_{channel}_TMS_iron_events_unweighted.dat" 
        data_unsmeared_ES_iron = np.loadtxt(file_unsmeared_ES_iron, max_rows = 200)
        events_unsmeared_ES_iron_w = data_unsmeared_ES_iron[:, 1]* iron_ES_w
        unsmeared_ES_iron_events += events_unsmeared_ES_iron_w

        file_unsmeared_ES_scint = SNOWGLOBES/"out"/f"garching_{channel}_TMS_scint_events_unweighted.dat" 
        data_unsmeared_ES_scint = np.loadtxt(file_unsmeared_ES_scint, max_rows = 200)
        events_unsmeared_ES_scint_w = data_unsmeared_ES_scint[:, 1]* scint_ES_w
        unsmeared_ES_scint_events += events_unsmeared_ES_scint_w

        
    total_events_unsmeared_ES_iron = unsmeared_ES_iron_events.sum()
    total_events_unsmeared_ES_scint = unsmeared_ES_scint_events.sum()

    ratio_smeared_events_iron = total_iron_ES_events_per_threshold / total_events_unsmeared_ES_iron
    ratio_smeared_events_scint = total_scint_ES_events_per_threshold / total_events_unsmeared_ES_scint

    
    #CC nue_Fe56
    file_unsmeared_nue_Fe56 = SNOWGLOBES/"out"/"garching_nue_Fe56_TMS_iron_events_unweighted.dat"

    data_unsmeared_nue_Fe56 = np.loadtxt(file_unsmeared_nue_Fe56, max_rows=200)

    total_events_unsmeared_nue_Fe56 = sum(data_unsmeared_nue_Fe56[:, 1])

    events_nue_Fe56 = []

    for i in thresholds:
        file_smeared = SNOWGLOBES/"out"/f"garching_nue_Fe56_TMS_iron_events_smeared_unweighted_{i}MeV.dat"
        data_smeared = np.loadtxt(file_smeared, max_rows = 200)
        events_smeared = data_smeared[:, 1]
        events_nue_Fe56.append(events_smeared.sum())

    events_nue_Fe56 = np.array(events_nue_Fe56)
    ratio_nue_Fe56 = events_nue_Fe56 / total_events_unsmeared_nue_Fe56


    #CC nuebar_Fe56
    file_unsmeared_nuebar_Fe56 = SNOWGLOBES/"out"/"garching_nuebar_Fe56_TMS_iron_events_unweighted.dat"

    data_unsmeared_nuebar_Fe56 = np.loadtxt(file_unsmeared_nuebar_Fe56, max_rows=200)

    total_events_unsmeared_nuebar_Fe56 = sum(data_unsmeared_nuebar_Fe56[:, 1])
    
    
    events_nuebar_Fe56 = []

    for i in thresholds:
        file_smeared = SNOWGLOBES/"out"/f"garching_nuebar_Fe56_TMS_iron_events_smeared_unweighted_{i}MeV.dat"
        data_smeared = np.loadtxt(file_smeared, max_rows = 200)
        events_smeared = data_smeared[:, 1]
        events_nuebar_Fe56.append(events_smeared.sum())

    events_nuebar_Fe56 = np.array(events_nuebar_Fe56)
    ratio_nuebar_Fe56 = events_nuebar_Fe56 / total_events_unsmeared_nuebar_Fe56

    #IBD TMS scint
    file_unsmeared_ibd = SNOWGLOBES/"out"/"garching_ibd_TMS_scint_events_unweighted.dat"

    data_unsmeared_ibd = np.loadtxt(file_unsmeared_ibd, max_rows=200)

    total_events_unsmeared_ibd = sum(data_unsmeared_ibd[:, 1])

    events_ibd = []

    for i in thresholds:
        file_smeared = SNOWGLOBES/"out"/f"garching_ibd_TMS_scint_events_smeared_unweighted_{i}MeV.dat"
        data_smeared = np.loadtxt(file_smeared, max_rows = 200)
        events_smeared = data_smeared[:, 1]
        events_ibd.append(events_smeared.sum())
    event_ibd = np.array(events_ibd)
    ratio_ibd = events_ibd / total_events_unsmeared_ibd
   
    total_events_TMS = events_nue_Fe56 + events_nuebar_Fe56 + events_ibd + total_iron_ES_events_per_threshold + total_scint_ES_events_per_threshold

    plt.plot(thresholds, events_ibd, label = r"IBD on scint", linestyle = "--")
    plt.plot(thresholds, total_scint_ES_events_per_threshold, label = r"ES $\nu$ on scint (all flavors)", linestyle = "-")
    plt.plot(thresholds, total_iron_ES_events_per_threshold, label = r"ES $\nu$ on iron (all flavors)", linestyle = "--")
    plt.plot(thresholds, events_nue_Fe56, label = r"CC $\nu_e$ on iron", linestyle = "--")
    plt.plot(thresholds, events_nuebar_Fe56, label = r"CC $\bar\nu_e$ on iron", linestyle = "--")
    plt.plot(thresholds, total_events_TMS, label = "Total events", color = "black")
    plt.legend()
    plt.title(r"Threshold effect on detected events for TMS, Garching")
    plt.xlabel("Threshold Energy [MeV]")
    plt.ylabel(r"Detected events")
    #plt.ylim(0, 1)
    plt.grid(True, alpha = 0.3)
    #plt.axhline(events_unsmeared.sum(), linestyle="--", label=f"True interactions: {events_unsmeared.sum():.2f}", color = "black")

    plt.savefig("plotting/TMS_threshold_comparison_total_events.png")


#plot_threshold_comparison_scatter()


def findPeakFe():
    TMS = Path.home() / "software/geant4/geant4-work/TMS"
    DATA16 = TMS / "build" / "explain_peak_data"
    DATA32 = TMS / "build" / "explain_peak_data32scint"


    energies = np.array([30,70])

    for E_nu in energies:

        file16 = DATA16 / f"TMS_{E_nu:.5f}_nuebar_Fe56_MeV.root"

        with uproot.open(file16) as f:
            hist = f["Escint"]

            counts16, edges16 = hist.to_numpy()

    # relative Häufigkeit pro erzeugtem Eveng
    #counts = counts / 100000

        plt.stairs(
        counts16,
        edges16,
        label=fr"$E_e={E_nu:.0f}$ MeV, d = 16 mm",
        baseline=None,)
        file32 = DATA32 / f"TMS_{E_nu:.5f}_nuebar_Fe56_MeV.root"

        with uproot.open(file32) as f:
            hist = f["Escint"]

            counts32, edges32 = hist.to_numpy()

    # relative Häufigkeit pro erzeugtem Eveng
    #counts = counts / 100000

        plt.stairs(
        counts32,
        edges32,
        label=fr"$E_e={E_nu:.0f}$ MeV, d = 32 mm",
        baseline=None,
        linestyle = "--")

    plt.xlabel(r"Deposited scintillator energy $E_{\mathrm{scint}}$ [MeV]")
    plt.ylabel("Events per 0.5 MeV bin")
    plt.xlim(1, 15)
    plt.ylim(0,5000)
    plt.grid(True, alpha = 0.3)
    plt.legend()
    #plt.title("100,000 events per electron energy generated, uniformly and isotropically in Fe layers")
    plt.savefig("plotting/compare_peak_structure_16_32.png")

#findPeakFe()
def compare_MARLEY_NOMARLEY():

    file_MARLEY = SNOWGLOBES/"out"/"MARLEY100k_garching_nue_Fe56_TMS_iron_events_smeared_unweighted.dat"
    file_NOMARLEY = SNOWGLOBES/"out"/"NOMARLEY_garching_nue_Fe56_TMS_iron_events_smeared_unweighted.dat"

    data_MARLEY = np.loadtxt(file_MARLEY, max_rows=200)
    data_NOMARLEY = np.loadtxt(file_NOMARLEY, max_rows=200)

    energy = np.linspace(0.5, 100, 201)
    events_MARLEY = data_MARLEY[:, 1]
    events_NOMARLEY = data_NOMARLEY[:, 1]

    plt.stairs(events_MARLEY, energy, baseline = None, label="MARLEY + G4", color="blue")
    plt.stairs(events_NOMARLEY, energy, baseline = None, label=r"Only G4: T$_e$ = E$_\nu$ - Q ", color="red")
    plt.text(0.595, 0.75,f"MARLEY + G4 events: {events_MARLEY.sum():.2f}\nOnly G4 events: {events_NOMARLEY.sum():.2f}",transform=plt.gca().transAxes)#,ha="right",va="top")
    #plt.text(0.84, 0.77,f"Total events unsmeared: {events_unsmeared.sum():.2f}",transform=plt.gca().transAxes,ha="right",va="top")
    plt.xlabel(r" Deposited E in scint [MeV]")
    plt.xlim(0,20)
    plt.ylabel("Number of Events per bin")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.title(r"CC $\nu_e$ on $^{56}$Fe in TMS, MARLEY + G4 vs only G4 smearing matrx")#0% efficiency $\leq$ 5 MeV")
    plt.savefig("plotting/MARLEY100k_NOMARLEY_COMPARISON.png")

#compare_MARLEY_NOMARLEY()

def compare_settings_effects(
    tree_name="TMS",
    pdg_branch="PDG",
    kinetic_energy_branch="Ekin",
    bins=np.linspace(0, 40, 81)):

    plt.figure(figsize=(8, 5))

    folder = Path.home()/"software"/"geant4"/"geant4-work"/"TMS"/"build"/"data_marley"/"MARLEY_compare_settings"
    files = {
        "discrete": 
            "MARLEY_TMS_40.00000_only_discrete.root",

        "discrete + continuum":
            "MARLEY_TMS_40.00000_discrete_continuum.root",

        "discrete + allowed":
            "MARLEY_TMS_40.00000_only_discrete_allowed.root",

        "discrete + continuum + allowed":
            "MARLEY_TMS_40.00000_discrete_continuum_allowed.root",
    }

    for label, filename in files.items():

        path = Path(folder) / filename

        with uproot.open(path) as f:
            tree = f[tree_name]

            pdg = tree[pdg_branch].array(library="np")
            Ekin = tree[kinetic_energy_branch].array(library="np")

        # select electrons
        electron_Ekin = Ekin[pdg == 11]

        print(
            f"{label:35s}: "
            f"N_e = {len(electron_Ekin):7d}, "
            f"mean = {np.mean(electron_Ekin):6.3f} MeV, "
            f"median = {np.median(electron_Ekin):6.3f} MeV"
        )

        plt.hist(
            electron_Ekin,
            bins=bins,
            histtype="step",
            density=True,
            linewidth=1.8,
            label=label
        )

    plt.xlabel(r"Electron kinetic energy $T_e$ [MeV]")
    plt.ylabel("Probability density [1/MeV]")
    plt.title(r"$\nu_e + {}^{56}\mathrm{Fe}$ at $E_\nu = 40$ MeV")
    plt.legend()
    plt.grid(alpha=0.25)

    plt.tight_layout()
    plt.savefig("plotting/test.png")

#compare_settings_effects()