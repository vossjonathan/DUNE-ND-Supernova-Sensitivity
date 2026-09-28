import numpy as np
from pathlib import Path
import subprocess
import shutil
from config import DETECTOR_SMEARING_CONFIG


SNOWGLOBES = Path.home()/"software"/"snowglobes"

EFFIC = SNOWGLOBES / "effic"
EFFIC_TMS_IRON = EFFIC / "TMS_iron"
EFFIC_TMS_SCINT = EFFIC / "TMS_scint"

OUT = SNOWGLOBES / "out"

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

def detector_comparison(flux):
    #sets all effiencies to 100%, so threshold 0.5 MeV

    detectors = ["TMS_iron", "TMS_scint", "ECAL_lead", "ECAL_scint", "STT", "GRAIN", "NDLAr"]
    for detector in detectors:
        pass

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
    threshold_study()
    reset_effic_to_100("TMS_scint")

    