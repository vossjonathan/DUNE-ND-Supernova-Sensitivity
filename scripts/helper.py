import numpy as np
import matplotlib.pyplot as plt
from pathlib  import Path
import matplotlib.patches as mpatches
from scripts.config import DETECTOR_SMEARING_CONFIG, ALL_DETECTOR

SNOWGLOBES = Path.home()/"software"/"snowglobes"
OUT = Path.home()/"software"/"snowglobes"/"out"

def load_events_weighted(flux, channel, detector, smeared):
    weight = ALL_DETECTOR[detector]["channels"][channel]

    if (flux != "garching") and (flux != "livermore"):
        raise ValueError("This flux does not exist.")

    if smeared:
        file = SNOWGLOBES/"out"/f"{flux}_{channel}_{detector}_events_smeared_unweighted.dat"
    else:
        file = SNOWGLOBES/"out"/f"{flux}_{channel}_{detector}_events_unweighted.dat"

    data = np.loadtxt(file, max_rows = 200)
    events = data[:, 1]
    return events * weight

def load_smeared_data_threshold(detector, channel, threshold):
    file_smeared = SNOWGLOBES/"out"/f"garching_{channel}_{detector}_events_smeared_unweighted_{threshold}MeV.dat"
    data_smeared = np.loadtxt(file_smeared, max_rows = 200)
    events_unweighted = data_smeared[:, 1]
    return events_unweighted


def calculate_DUNE_ND_energy_lost():
    
    DEPTH = 60 * 100 #in cm

    ROCK_DENSITY = 2.7 #in g/cm^3

    X = ROCK_DENSITY * DEPTH # in

    print(X) #1.6 10^4
    #https://pdg.lbl.gov/2017/AtomicNuclearProperties/MUE/muE_standard_rock.pdf
    #--> Energy Loss in 60m around 38 GeV

def get_smeared_unsmeared_TMS_total():
    detectors = ["TMS_iron", "TMS_scint"]
    total_u = 0
    total_s = 0
    for detector in detectors:
        config = DETECTOR_SMEARING_CONFIG[detector]
        channel_config = config["channels"]

        for channel in channel_config.keys():
            total_u += load_events_weighted("garching", channel, detector, smeared = False).sum()
            total_s += load_events_weighted("garching", channel, detector, smeared = True).sum()

    print("Total unsmeared TMS: ", total_u)
    print("Total smeared TMS: ", total_s)

def efficiency_per_channel():
    detectors = ["TMS_iron", "TMS_scint"]
    for detector in detectors:
        config = DETECTOR_SMEARING_CONFIG[detector]

        for channel in config["channels"]:
            u = load_events_weighted("garching", channel, detector, smeared = False).sum()
            s = load_events_weighted("garching", channel, detector, smeared = True).sum()

            eff = s / u if u > 0 else 0

            print(
                f"{detector:12} "
                f"{channel:20} "
                f"unsmeared={u:8.3f} "
                f"smeared={s:8.3f} "
                f"eff={100*eff:6.1f}%"
            )

if __name__ == "__main__":
    #calculate_DUNE_ND_energy_lost()
    #get_smeared_unsmeared_TMS_total()
    efficiency_per_channel()

