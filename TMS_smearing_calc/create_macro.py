import numpy as np
from pathlib import Path



TMS = Path.home()/"software"/"geant4"/"geant4-work"/"TMS"


def printMacro():
    with open(TMS/"build"/"energyScan.mac", "w") as f:

        
        print("/run/initialize", file = f)
        print("/tracking/storeTrajectory 0", file = f)
        print("/run/printProgress 1000\n", file = f)
        print("/tms/channel nuebar_Fe", file = f)
        bin_edges = np.linspace(0.5, 100, 201)
        bin_centers = 0.5 * (bin_edges[:-1] + bin_edges[1:])
        bin_centers = bin_centers[bin_centers >= 4.71]


        for i in bin_centers:
            print(f"/tms/nuEnergy {i:.5f} MeV", file = f)
            print(f"/analysis/setFileName CC_nuebar_56Fe_correct_grid_100k/TMS_{i:.5f}_nuebar_Fe56_MeV.root", file = f)
            print("/run/beamOn 100000 \n", file = f)

printMacro()