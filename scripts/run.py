from scripts.plotting.detectors_plots import plot_all_TMS_iron_scint
import subprocess
from scripts.smearing_matrices.tms_smear import build_smearing_matrix, write_snowglobes_matrix
from scripts.config import DETECTOR_SMEARING_CONFIG, ALL_DETECTOR
from pathlib import Path

detectors = ["NDLAr", "ECAL_lead", "ECAL_scint", "TMS_iron", "TMS_scint", "GRAIN", "STT"]
fluxes = ["garching", "livermore"]

def main():

    print("Creating current TMS signal plot...")

    plot_all_TMS_iron_scint()

    print("Finished.")

def write_all_smearing_matrices():
    for detector in DETECTOR_SMEARING_CONFIG.keys():

        print(f"Writing to detector {detector}")

        channels = DETECTOR_SMEARING_CONFIG[detector]["channels"]

        for channel in channels.keys():
            print(f"writing to channel {channel}")
            
            matrix = build_smearing_matrix(detector, channel)
            write_snowglobes_matrix(matrix, detector, channel)

def run_snowglobes(flux, detector, material):
    SNOWGLOBES = Path.home()/"software"/"snowglobes"
    print(f"Running SNOwGLoBES: {flux}, {material}, {detector}")

    subprocess.run(["./supernova.pl","0", flux, material, detector],cwd=SNOWGLOBES,check=True,)


def run_all_detectors_snowglobes():
    for flux in fluxes:
        for detector in detectors:
            config = ALL_DETECTOR[detector]
            material = config["material"]
            run_snowglobes(flux, detector, material)

if __name__ == "__main__":
    #main()
    run_all_detectors_snowglobes()
    #write_all_smearing_matrices()
    #run_all_detectors_snowglobes()