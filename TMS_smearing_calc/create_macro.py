import numpy as np
from pathlib import Path



TMS = Path.home()/"software"/"geant4"/"geant4-work"/"TMS"


def printMacro():
    with open(TMS/"build"/"energyScan.mac", "w") as f:

        
        print("/run/initialize", file = f)
        print("/tracking/storeTrajectory 0", file = f)
        print("/run/printProgress 1000\n", file = f)
        print("/tms/channel ESiron", file = f)
        bin_edges = np.linspace(0.5, 100, 201)
        bin_centers = 0.5 * (bin_edges[:-1] + bin_edges[1:])
        bin_centers = bin_centers[bin_centers >= 4.71]


        for i in bin_centers:
            print(f"/tms/nuEnergy {i:.5f} MeV", file = f)
            print(f"/analysis/setFileName CC_nuebar_56Fe_correct_grid_100k/TMS_{i:.5f}_nuebar_Fe56_MeV.root", file = f)
            print("/run/beamOn 100000 \n", file = f)



def printMacroFindPeak():
        with open(TMS/"build"/"peakScan.mac", "w") as f:

        
            print("/run/initialize", file = f)
            print("/tracking/storeTrajectory 0", file = f)
            print("/run/printProgress 1000\n", file = f)
            print("/tms/channel ESiron", file = f)
            bin_centers = np.linspace(10,100,10)

            

            for i in bin_centers:
                print(f"/tms/nuEnergy {i:.5f} MeV", file = f)
                print(f"/analysis/setFileName explain_peak_data32scint/TMS_{i:.5f}_nuebar_Fe56_MeV.root", file = f)
                print("/run/beamOn 100000 \n", file = f)


def printMacroMarley(n_events):
     with open(TMS/"build"/"marleyScan1.mac", "w") as f:
            print("/run/numberOfThreads 1", file = f)
            print("/run/initialize", file = f)
            print("/tracking/storeTrajectory 0", file = f)
            print("/run/printProgress 1000\n", file = f)
            bin_edges = np.linspace(0.5, 100, 201)
            bin_centers = 0.5 * (bin_edges[:-1] + bin_edges[1:])
            bin_centers = bin_centers[(bin_centers >= 6.31) & (bin_centers <= 25)]


            for i in bin_centers:
                print(f"/marley/nuEnergy {i:.5f} MeV", file = f)
                print(f"/analysis/setFileName data_marley/MARLEY_CC_nue/MARLEY_TMS_{i:.5f}_CC_nue_Fe56_MeV.root", file = f)
                print(f"/run/beamOn {n_events} \n", file = f)

     with open(TMS/"build"/"marleyScan2.mac", "w") as f:
            print("/run/numberOfThreads 1", file = f)
            print("/run/initialize", file = f)
            print("/tracking/storeTrajectory 0", file = f)
            print("/run/printProgress 1000\n", file = f)
            bin_edges = np.linspace(0.5, 100, 201)
            bin_centers = 0.5 * (bin_edges[:-1] + bin_edges[1:])
            bin_centers = bin_centers[(bin_centers > 25) & (bin_centers <= 50)]


            for i in bin_centers:
                print(f"/marley/nuEnergy {i:.5f} MeV", file = f)
                print(f"/analysis/setFileName data_marley/MARLEY_CC_nue/MARLEY_TMS_{i:.5f}_CC_nue_Fe56_MeV.root", file = f)
                print(f"/run/beamOn {n_events} \n", file = f)    
     with open(TMS/"build"/"marleyScan3.mac", "w") as f:
            print("/run/numberOfThreads 1", file = f)
            print("/run/initialize", file = f)
            print("/tracking/storeTrajectory 0", file = f)
            print("/run/printProgress 1000\n", file = f)
            bin_edges = np.linspace(0.5, 100, 201)
            bin_centers = 0.5 * (bin_edges[:-1] + bin_edges[1:])
            bin_centers = bin_centers[(bin_centers > 50) & (bin_centers <= 75)]


            for i in bin_centers:
                print(f"/marley/nuEnergy {i:.5f} MeV", file = f)
                print(f"/analysis/setFileName data_marley/MARLEY_CC_nue/MARLEY_TMS_{i:.5f}_CC_nue_Fe56_MeV.root", file = f)
                print(f"/run/beamOn {n_events} \n", file = f)  

     with open(TMS/"build"/"marleyScan4.mac", "w") as f:
            print("/run/numberOfThreads 1", file = f)
            print("/run/initialize", file = f)
            print("/tracking/storeTrajectory 0", file = f)
            print("/run/printProgress 1000\n", file = f)
            bin_edges = np.linspace(0.5, 100, 201)
            bin_centers = 0.5 * (bin_edges[:-1] + bin_edges[1:])
            bin_centers = bin_centers[bin_centers > 75]


            for i in bin_centers:
                print(f"/marley/nuEnergy {i:.5f} MeV", file = f)
                print(f"/analysis/setFileName data_marley/MARLEY_CC_nue/MARLEY_TMS_{i:.5f}_CC_nue_Fe56_MeV.root", file = f)
                print(f"/run/beamOn {n_events} \n", file = f)    

#printMacro()
#printMacroFindPeak()
#printMacroMarley(10000)


def printMacroMarley100k(n_events, n_jobs):

    bin_edges = np.linspace(0.5, 100, 201)
    bin_centers = 0.5 * (bin_edges[:-1] + bin_edges[1:])
    bin_centers = bin_centers[bin_centers >= 6.31]

    build_dir = TMS / "build"

    for job in range(n_jobs):

        energies = bin_centers[job::n_jobs]

        with open(build_dir / "marley100kscanNC"/ f"marleyScan100k{job+1}.mac", "w") as f:

            print("/run/numberOfThreads 1", file=f)
            print("/run/initialize", file=f)
            print("/tracking/storeTrajectory 0", file=f)
            print("/run/printProgress 10000\n", file=f)

            for E in energies:

                print(f"/marley/nuEnergy {E:.5f} MeV", file=f)

                print(
                    f"/analysis/setFileName "
                    f"data_marley/MARLEY_NC_nue100k/"
                    f"MARLEY_TMS_{E:.5f}_NC_nue_Fe56_MeV.root",
                    file=f
                )

                print(f"/run/beamOn {n_events}\n", file=f)


#printMacroMarley100k(100000, 8)

def printMacroMissing(n_events):
    bin_edges = np.linspace(0.5, 100, 201)
    bin_centers = 0.5 * (bin_edges[:-1] + bin_edges[1:])
    bin_centers = bin_centers[(bin_centers < 6.31) & (bin_centers > 3.4)]

    build_dir = TMS / "build"



    with open(build_dir / "marley100kscanNC"/ f"marleyScan100kMissing.mac", "w") as f:

        print("/run/numberOfThreads 1", file=f)
        print("/run/initialize", file=f)
        print("/tracking/storeTrajectory 0", file=f)
        print("/run/printProgress 10000\n", file=f)

        for E in bin_centers:

            print(f"/marley/nuEnergy {E:.5f} MeV", file=f)

            print(
                f"/analysis/setFileName "
                f"data_marley/MARLEY_NC_nue100k/"
                f"MARLEY_TMS_{E:.5f}_NC_nue_Fe56_MeV.root",
                file=f
            )

            print(f"/run/beamOn {n_events}\n", file=f)

printMacroMissing(100000)