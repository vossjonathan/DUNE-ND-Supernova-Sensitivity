import numpy as np
import matplotlib.pyplot as plt
from pathlib  import Path
import uproot
import plotting.helper as helper
from config import DETECTOR_SMEARING_CONFIG, ALL_DETECTOR, iron_channels, argon_channels, lead_channels, scint_channels

SNOWGLOBES = Path.home()/"software"/"snowglobes"
THRESHOLDS = np.arange(0.5, 8.2, 0.5)

#weights not considered, basic plot
def plot_one_channel_smeared_unsmeared(flux, channel, detector):

    file_smeared = SNOWGLOBES/"out"/f"{flux}_{channel}_{detector}_events_smeared_unweighted.dat"
    file_unsmeared = SNOWGLOBES/"out"/f"{flux}_{channel}_{detector}_events_unweighted.dat"

    data_smeared = np.loadtxt(file_smeared, max_rows=200)
    data_unsmeared = np.loadtxt(file_unsmeared, max_rows=200)

    energy = np.linspace(0.5, 100, 201)

    events_smeared = data_smeared[:, 1]
    events_unsmeared = data_unsmeared[:, 1]

    plt.stairs(events_smeared, energy, label="Smeared: LAr deposited E", color="blue")
    plt.stairs(events_unsmeared, energy, label=r"Unsmeared: true $E_\nu$", color="red")
    plt.xlim(0,50)
    plt.text(0.42, 0.76,f"Total events unsmeared: {events_unsmeared.sum():.2f}\nTotal events smeared: {events_smeared.sum():.2f}",transform=plt.gca().transAxes)#,ha="right",va="top")
    #plt.text(0.84, 0.77,f"Total events unsmeared: {events_unsmeared.sum():.2f}",transform=plt.gca().transAxes,ha="right",va="top")
    plt.xlabel(r" E [MeV]")
    plt.ylabel("Number of Events per bin")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.title(f"Smeared vs. unsmeared signal, {flux} flux, {channel}, {detector}")
    plt.savefig(f"plotting/{flux}_{channel}_{detector}_smeared_unsmeared.svg", bbox_inches="tight", dpi=900)
    plt.close()



def plot_two_channel_smeared_unsmeared(title, save_as):

    energy = np.linspace(0.5, 100, 201)

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
    plt.savefig(f"plotting/{save_as}")


def plot_one_channel_iron_smeared_unsmeared(channel):
    channels = iron_channels
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
    plt.title(fr"Channel: {channel} channel TMS iron, unsmeared smeared")
    plt.savefig(f"plotting/garching_TMS_iron_{channel}_unsmeared_smeared_weighted.png")


def plot_one_channel_scint_smeared_unsmeared(channel):
    channels = lead_channels
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
    plt.title(fr"Channel {channel} TMS (only scint), garching, $E_{{th}}$ = 0.5 MeV")
    plt.savefig(f"plotting/garching_TMS_scint_{channel}_unsmeared_smeared_weighted.png")



def plot_all_TMS_iron_scint(flux):
    #channels with geant4 smearing matrix
    channels_scint = scint_channels #import from config.py
    channels_iron = iron_channels

    total_iron_ES = np.zeros(200)
    total_scint_ES = np.zeros(200)
    total_events = np.zeros(200)
    total_C12_NC = np.zeros(200)

    #iron ES
    for name in channels_iron.keys():
        if name[-1] == "e":
            file = (SNOWGLOBES/"out"/f"{flux}_{name}_TMS_iron_events_smeared_unweighted.dat")
            data_smeared = np.loadtxt(file, max_rows= 200)
            events_smeared = data_smeared[:, 1]
            events_smeared_w = events_smeared * channels_iron[name]
            total_iron_ES += events_smeared_w
            total_events += events_smeared_w

    
    for name in channels_scint.keys():
        #scint ES
        if name[-1] == "e":
            file = (SNOWGLOBES/"out"/f"{flux}_{name}_TMS_scint_events_smeared_unweighted.dat")
            data_smeared = np.loadtxt(file, max_rows= 200)
            events_smeared = data_smeared[:, 1]
            events_smeared_w = events_smeared * channels_scint[name]
            total_scint_ES += events_smeared_w
            total_events += events_smeared_w
        #C12 NC
        if name[-1] == "2":
            file = (SNOWGLOBES/"out"/f"{flux}_{name}_TMS_scint_events_smeared_unweighted.dat")
            data_smeared = np.loadtxt(file, max_rows = 200)
            events_smeared = data_smeared[:, 1]
            events_smeared_w = events_smeared * channels_scint[name]
            total_C12_NC += events_smeared_w
            total_events += events_smeared_w
            

    #scint IBD
    file_IBD = SNOWGLOBES/"out"/f"{flux}_ibd_TMS_scint_events_smeared_unweighted.dat"
    data_smeared_IBD = np.loadtxt(file_IBD, max_rows= 200)
    events_smeared_IBD = data_smeared_IBD[:, 1]
    events_smeared_IBD_w = events_smeared_IBD * channels_scint["ibd"]
    total_events += events_smeared_IBD_w
    
    energy = np.linspace(0.5, 100, 201)#data_smeared_IBD[:, 0] * 1000 #using this for all channels as energy binning is same for all


    #iron CC nue
    file_nue = SNOWGLOBES/"out"/f"{flux}_nue_Fe56_TMS_iron_events_smeared_unweighted.dat"
    data_smeared_nue = np.loadtxt(file_nue, max_rows= 200)
    events_smeared_nue = data_smeared_nue[:, 1]
    events_smeared_nue_w = events_smeared_nue * channels_iron["nue_Fe56"]
    total_events += events_smeared_nue_w
    

    #iron CC nuebar
    file_nuebar = SNOWGLOBES/"out"/f"{flux}_nuebar_Fe56_TMS_iron_events_smeared_unweighted.dat"
    data_smeared_nuebar = np.loadtxt(file_nuebar, max_rows= 200)
    events_smeared_nuebar = data_smeared_nuebar[:, 1]
    events_smeared_nuebar_w = events_smeared_nuebar * channels_iron["nuebar_Fe56"]
    total_events += events_smeared_nuebar_w

    #iron NC all channels
    NC_channels = ["nc_nue_Fe56", "nc_nuebar_Fe56", "nc_numu_Fe56", "nc_numubar_Fe56", "nc_nutau_Fe56", "nc_nutaubar_Fe56"]
    NC_Fe_events_total = np.zeros(200)
    for channel in NC_channels:
        u, e = helper.get_channel_out_smeared_unsmeared("TMS_iron", "iron", channel, flux)
        NC_Fe_events_total += e

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
    plt.savefig(f"plotting/{flux}_TMS_signal_preliminary_NC_C12.svg", bbox_inches = "tight")
    

def load_smeared_data_threshold(detector, channel, threshold):
    file_smeared = SNOWGLOBES/"out"/f"garching_{channel}_{detector}_events_smeared_unweighted_{threshold}MeV.dat"
    data_smeared = np.loadtxt(file_smeared, max_rows = 200)
    events_unweighted = data_smeared[:, 1]
    return events_unweighted

def plot_threshold_comparison_new():
    detectors  = ["TMS_iron", "TMS_scint"]

    ES_group = ["nue_e", "nuebar_e", "numu_e", "numubar_e", "nutau_e", "nutaubar_e"]
    NC_iron = ["nc_nue_Fe56", "nc_nuebar_Fe56", "nc_numu_Fe56", "nc_numubar_Fe56", "nc_nutau_Fe56", "nc_nutaubar_Fe56"]
    NC_scint = ["nc_nue_C12", "nc_nuebar_C12", "nc_numu_C12", "nc_numubar_C12", "nc_nutau_C12", "nc_nutaubar_C12"]
    #groups to compare
    total_scint_ES = []
    total_iron_ES = []
    total_C12_NC = []
    total_iron_NC = []
    total_IBD = []
    total_nue_Fe = []
    total_nuebar_Fe = []


    thresholds = np.arange(0.5, 8.1, 0.5)
    #ES channels
    for threshold in thresholds:
        
        for detector in detectors:
            total = 0
            channels = DETECTOR_SMEARING_CONFIG[detector]["channels"]
            
            for channel in ES_group:
                weight = channels[channel]["weight"]
                events_unweighted = load_smeared_data_threshold(detector, channel, threshold)
                events_weighted = events_unweighted * weight
                sum_threshold = sum(events_weighted)
                total += sum_threshold

            if detector == "TMS_iron":
                total_iron_ES.append(total)
            else:
                total_scint_ES.append(total)

    #NC C12
    for threshold in thresholds:
        channels = DETECTOR_SMEARING_CONFIG["TMS_scint"]["channels"]
        total = 0
        for channel in NC_scint:
            weight = channels[channel]["weight"]
            events_unweighted = load_smeared_data_threshold("TMS_scint", channel, threshold)
            events_weighted = events_unweighted * weight
            total += sum(events_weighted)

        total_C12_NC.append(total)
            
    #NC iron
    for threshold in thresholds:
        channels = DETECTOR_SMEARING_CONFIG["TMS_iron"]["channels"]
        total = 0
        for channel in NC_iron:
            weight = channels[channel]["weight"]
            events_unweighted = load_smeared_data_threshold("TMS_iron", channel, threshold)
            events_weighted = events_unweighted * weight
            total += sum(events_weighted)
        total_iron_NC.append(total)

    #IBD
    for threshold in thresholds:
        weight = DETECTOR_SMEARING_CONFIG["TMS_scint"]["channels"]["ibd"]["weight"]
        events_weighted = load_smeared_data_threshold("TMS_scint","ibd", threshold) * weight
        total_IBD.append(sum(events_weighted))

    #CC nue Fe
    for threshold in thresholds:
        weight = DETECTOR_SMEARING_CONFIG["TMS_iron"]["channels"]["nue_Fe56"]["weight"]
        events_weighted = load_smeared_data_threshold("TMS_iron","nue_Fe56", threshold) * weight
        total_nue_Fe.append(sum(events_weighted))

    #CC nuebar Fe
    for threshold in thresholds:
        weight = DETECTOR_SMEARING_CONFIG["TMS_iron"]["channels"]["nuebar_Fe56"]["weight"]
        events_weighted = load_smeared_data_threshold("TMS_iron", "nuebar_Fe56", threshold) * weight
        total_nuebar_Fe.append(sum(events_weighted))

    total_events = np.array(total_scint_ES) + np.array(total_iron_ES) + np.array(total_C12_NC) + np.array(total_iron_NC) + np.array(total_nue_Fe) + np.array(total_nuebar_Fe) + np.array(total_IBD)

    plt.plot(thresholds, total_events, label = "Total events", color = "black", linewidth = 1.6)
    plt.plot(thresholds, total_scint_ES, label = r"eES scint", color = "grey", linestyle = "--")
    plt.plot(thresholds, total_iron_ES, label = "eES Fe", color = "red", linestyle = "--")
    plt.plot(thresholds, total_C12_NC, label = "NC on C12", color = "blue", linestyle = "--")
    plt.plot(thresholds, total_IBD, label = "IBD on scint", color = "orange", linestyle = "--")
    plt.plot(thresholds, total_iron_NC, label = "NC on Fe", color = "purple", linestyle = "--")
    plt.plot(thresholds, total_nue_Fe, label = r"CC $\nu_e$ on Fe", color = "green", linestyle = "--")
    plt.plot(thresholds, total_nuebar_Fe, label = r"CC $\bar\nu_e$ on Fe", color = "brown", linestyle = "--")
    plt.legend()
    plt.grid(True, alpha = 0.3)
    plt.xlabel("Threshold [MeV]")
    plt.ylabel("Expected event rate")
    #plt.title("Threshold comparison new")
    plt.savefig("plotting/new_threshold_comparison.svg", bbox_inches = "tight", dpi = 900)



    

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


#configname = garching_nc_nue_Fe56_TMS_iron
#title = NC nue Fe 56 smeared unsmeared
#save_as = "garching_TMS_iron_NC_nue_smeared_unsmeared.png"

if __name__ == "__main__":
    #plot_one_channel_smeared_unsmeared(flux = "garching", channel = "nue_Fe56", detector = "TMS_iron", title = "")


    """plot_two_channel_smeared_unsmeared(
        title = r"NC C12 $\nu_e$ TMS scint, basic scint20kt vs G4 response",
        save_as = "NC_C12_TMS_scint_response_comparison.png"
    )"""
    #plot_one_channel_iron_smeared_unsmeared("nue_Fe56")
    #plot_one_channel_scint_smeared_unsmeared("ibd")
    #plot_all_TMS_iron_scint("garching")
    #plot_threshold_comparison(flux="garching")
    plot_threshold_comparison_new()
    #plot_threshold_comparison()
    #plot_threshold_comparison_scatter()
    #findPeakFe()
    #compare_MARLEY_NOMARLEY()
    #compare_settings_effects()

