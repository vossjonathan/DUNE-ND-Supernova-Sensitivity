import numpy as np
from pathlib import Path
from analysis.config import DETECTOR_SMEARING_CONFIG, ENERGY_GRID

#local Geant4 installation path
TMS = Path.home()/"software"/"geant4"/"geant4-work"/"TMS"



#Besides generating macro the corresponding settings must be adjusted in the Geant4 C++ files
def printMacroOnlyGeant4(detector, channel):
       
    config = DETECTOR_SMEARING_CONFIG[detector]["channels"][channel]

    if "G4_channel" not in config:
        raise ValueError(f"No Geant4 only implementation for {channel} in {detector}")


    min_energy = config["threshold"]
    bin_edges = ENERGY_GRID
    bin_centers = 0.5 * (bin_edges[:-1] + bin_edges[1:])
    bin_centers = bin_centers[bin_centers >= min_energy]

    build_dir = TMS/"build"
    macro_path = build_dir/"macros"

    channel_dir = config["folder"]
    output_path = build_dir/"data_without_marley"/channel_dir

    macro_path.mkdir(parents=True, exist_ok=True)
    output_path.mkdir(parents=True, exist_ok=True)    

    with open(TMS/"build"/"macros"/f"G4_only_{channel}_{detector}.mac", "w") as f:

        
        print("/run/initialize", file = f)
        print("/tracking/storeTrajectory 0", file = f)
        print("/run/printProgress 1000\n", file = f)
        print(f"/tms/channel {config["G4_channel"]}", file = f)
        
        bin_centers = 0.5 * (bin_edges[:-1] + bin_edges[1:])
        bin_centers = bin_centers[bin_centers >= min_energy]

        
        for E in bin_centers:

            file = config["filename"].format(E = E)
            print(f"/tms/nuEnergy {E:.5f} MeV", file = f)
            print(f"/analysis/setFileName {output_path}/{file}", file = f)
            print("/run/beamOn 100000 \n", file = f)



def printMacroMarley(n_events, n_jobs, detector, channel):

    config = DETECTOR_SMEARING_CONFIG[detector]["channels"][channel]
    min_energy = config["threshold"]
    bin_edges = ENERGY_GRID
    bin_centers = 0.5 * (bin_edges[:-1] + bin_edges[1:])
    bin_centers = bin_centers[bin_centers >= min_energy]

    build_dir = TMS / "build"

    macro_dir = f"marley_scan_100k_{channel}_{detector}"
    macro_path = build_dir/"macros"/macro_dir

    channel_dir = config["folder"]
    output_path = build_dir/"data_marley"/channel_dir

    macro_path.mkdir(parents=True, exist_ok=True)
    output_path.mkdir(parents=True, exist_ok=True)

    for job in range(n_jobs):

        energies = bin_centers[job::n_jobs]

        with open(macro_path/ f"marleyScan100k{job+1}.mac", "w") as f:

            print("/run/numberOfThreads 1", file=f)
            print("/run/initialize", file=f)
            print("/tracking/storeTrajectory 0", file=f)
            print("/run/printProgress 10000\n", file=f)

            for E in energies:

                print(f"/marley/nuEnergy {E:.5f} MeV", file=f)

                filename = config["filename"].format(E = E)

                print(
                    f"/analysis/setFileName "
                    f"{output_path}/"
                    f"{filename}",
                    file=f
                )

                print(f"/run/beamOn {n_events}\n", file=f)

    print("for i in $(seq 1 {n_jobs}); do\n"
    f"./exampleB4c -m macros/{macro_dir}/marleyScan100k${{i}}.mac &\n"
    "done")


def printMacroCosmic():
    with open(TMS/"build"/"macros"/"CosmicMuScan3.mac", "w") as f:

        
        print("/run/initialize", file = f)
        print("/tracking/storeTrajectory 0", file = f)
        print("/tracking/verbose 0", file=f)
        print("/run/printProgress 1000\n", file = f)
        print("/tms/channel CosmicMu", file = f)

        print(f"/analysis/setFileName data_without_marley/Cosmic_data_theta_36/TMS_cosmic_mu.root", file = f)
        print("/run/beamOn 100000 \n", file = f)


#only helper function for debugging missing events        
def printMacroMissing(n_events):
    bin_edges = np.linspace(0.5, 100, 201)
    bin_centers = 0.5 * (bin_edges[:-1] + bin_edges[1:])
    bin_centers = bin_centers[(bin_centers >= 4.82) & (bin_centers < 6.31)]

    build_dir = TMS / "build"



    with open(build_dir / f"marley_nuebar_missing.mac", "w") as f:

        print("/run/numberOfThreads 1", file=f)
        print("/run/initialize", file=f)
        print("/tracking/storeTrajectory 0", file=f)
        print("/run/printProgress 10000\n", file=f)

        for E in bin_centers:

            print(f"/marley/nuEnergy {E:.5f} MeV", file=f)

            print(
                f"/analysis/setFileName "
                f"data_marley/MARLEY_CC_nuebar_100k_ALLOWED/"
                f"MARLEY_TMS_{E:.5f}_CC_nuebar_ALLOWED_Fe56_MeV.root",
                file=f
            )

            print(f"/run/beamOn {n_events}\n", file=f)




if __name__ == "__main__":
    printMacroMarley(100000, 8, "TMS_iron", "nue_Fe56")