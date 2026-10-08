import numpy as np
import matplotlib.pyplot as plt
from pathlib  import Path
import uproot
from scripts.config import DETECTOR_SMEARING_CONFIG, ENERGY_GRID, ALL_DETECTOR, iron_channels, argon_channels, lead_channels, scint_channels
from scripts.helper import load_events_weighted, load_smeared_data_threshold
import subprocess
import shutil

SNOWGLOBES = Path.home()/"software"/"snowglobes"
EFFIC = SNOWGLOBES / "effic"
EFFIC_TMS_IRON = EFFIC / "TMS_iron"
EFFIC_TMS_SCINT = EFFIC / "TMS_scint"
OUT = SNOWGLOBES / "out"

def plot_threshold_comparison():
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
    plt.savefig("debug_plots/new_threshold_comparison.svg", bbox_inches = "tight", dpi = 900)


def threshold_study():
    #channels = ["nue_e", "nuebar_e", "numu_e", "numubar_e", "nutau_e", "nutaubar_e"]
    #channels = ["nue_Fe56", "nuebar_Fe56"]
    #channels = ["ibd"]
    detectors = ["TMS_iron", "TMS_scint"]

    thresholds = np.arange(0.5, 8.05, 0.5)
    print(thresholds)
    for threshold in thresholds:

        index = int(2*threshold - 1)
        for detector in detectors:
            material = DETECTOR_SMEARING_CONFIG[detector]["material"]
            channels = DETECTOR_SMEARING_CONFIG[detector]["channels"]
            for channel in channels:
                file = EFFIC / detector / f"effic_{channel}_{detector}.dat"
                
                
                values = np.ones(200)
                    
                    
                values[:index] = 0.0
            

                with open(file, "w") as f:
                    f.write(
                        "{" + ",".join(f"{x:.1f}" for x in values) + "}\n"
                    )

            
            subprocess.run(
                ["./supernova.pl", "0", "garching", material, detector],
                cwd=SNOWGLOBES,
                check=True
            )

        # save outputs before next run overwrites them
            for channel in channels:

                source = (
                    OUT /
                    f"garching_{channel}_{detector}_events_smeared_unweighted.dat"
                )

                target = (
                    OUT /
                    f"garching_{channel}_{detector}_events_smeared_unweighted_{threshold}MeV.dat"
                )

                shutil.copy(source, target)


def reset_effic_to_100(detector):

    detectors = ["TMS_iron", "TMS_scint"]
    for detector in detectors:
        channels = DETECTOR_SMEARING_CONFIG[detector]["channels"]
        for channel in channels:
            file = EFFIC / detector / f"effic_{channel}_{detector}.dat"
            values = np.ones(200)
        

            with open(file, "w") as f:
                f.write(
                    "{" + ",".join(f"{x:.1f}" for x in values) + "}\n"
                )

if __name__ == "__main__":
    #plot_threshold_comparison()
    pass