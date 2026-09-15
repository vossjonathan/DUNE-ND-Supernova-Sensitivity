import numpy as np
import matplotlib.pyplot as plt
from pathlib  import Path
from scipy.interpolate import interp1d
from scipy.interpolate import PchipInterpolator


#linear interpolation and extrapolation

SNOWGLOBES = Path.home()/"software"/"snowglobes"
XSCNS = SNOWGLOBES/"xscns"
MARLEY = Path.home()/"software"/"marley"

def calc_iron_nue_Fe56():


    

    # KOLBE:
    # cross sections in 10^-42 cm^2, source: 1, 23, column 1
    #energies_paper = np.arange(10,105,5) #in MeV
    #cross_section_paper = np.array([0.661, 6.45, 29.3, 73.3, 140, 236, 371, 555, 798, 1100, 1480, 1920, 2420, 2990, 3600, 4270, 4980, 5730, 6520])

    # LAZAUSKAS:
    #cross sections in 10^-42 cm^2, source 4
    energies_paper = np.array([7.5, 10, 12.5, 15, 20, 25, 30, 40, 50, 60, 70, 80, 90, 100])
    cross_section_paper = np.array([0.877, 3.63, 8.94, 17.3, 52.6, 125, 233, 544, 983, 1670, 2590, 3730, 5070, 6600])

    template = np.loadtxt(XSCNS / "xs_nue_Ar40.dat")
    logE = template[:,0] #in log10(energy in GeV)
    
    energies_GeV = 10**logE #in GeV
    energies_MeV = 10**logE * 1000 #in MeV
    #cross_sections_interp = np.interp(energies_MeV, energies_paper, cross_section_paper, left = 0)
    
    linear = interp1d(energies_paper,cross_section_paper,kind="linear",fill_value="extrapolate")
    func = PchipInterpolator(energies_paper, cross_section_paper, extrapolate= False)

    inside = ((energies_MeV >= energies_paper[0]) & (energies_MeV <= energies_paper[-1]))
    cross_sections_interp_extrap = np.where(inside, func(energies_MeV), linear(energies_MeV))

    cross_sections_interp_extrap = np.maximum(cross_sections_interp_extrap, 0)
    #print("only interp ", cross_sections_interp[700:800])
    #print('interp, extrap ', cross_sections_interp_extrap[700:800])
    #cross_sections_interp_extrap = np.maximum(0, cross_sections_interp_extrap) #cut of negative values

    cross_sections_globes = cross_sections_interp_extrap * 1e-4 / energies_GeV #in 10^-38cm^2 /GeV
    zeros = np.zeros(len(energies_MeV))

    output = np.column_stack((logE, cross_sections_globes, zeros, zeros, zeros, zeros, zeros))

    outfile = XSCNS / "xs_nue_Fe56.dat"

    header = ("Neutrino-56Fe cc cross section (10^-38 cm^2/GeV)\n"
              "log(energy in GeV) nu_e nu_mu nu_tau nu_e_bar nu_mu_bar nu_tau_bar\n")

    np.savetxt(outfile, output, fmt = "%.6e", header=header, comments="# ")



def calc_iron_nuebar_Fe56():
    

    #SOURCE: 2, 7, Table 2, Hybrid column 
    #energies_paper = np.array([10, 12.5, 15, 20, 25, 30, 40, 50])
    #cross sections in 10^-42 cm^2
    #cross_section_paper = np.array([0, 0, 2, 7, 16, 30, 84, 181])


    #SOURCE : 3, 8 Table 3, column Fe56
    #energies_paper = np.arange(5, 51, 2.5)
    #cross sections in 10^-42cm^2
    #cross_section_paper = np.array([0,0,0, 1, 2, 4, 7, 11, 16, 22, 30, 40, 52, 67, 84, 104, 127, 152, 181])


    #SOURCE: 4, 8 table 1
    energies_paper = np.array([7.5, 10, 12.5, 15, 20, 25, 30, 40, 50, 60, 70, 80, 90, 100])
    #cross sections in 10^-42cm^2
    cross_section_paper = np.array([0.841, 2.95 , 6.09, 10.3, 21.7, 37.4, 57.4, 120, 209, 353, 526, 727, 940, 1140])

    template = np.loadtxt(XSCNS / "xs_nue_Ar40.dat")
    logE = template[:,0] #in log(energy in GeV)
    energies_GeV = 10**logE #in GeV
    energies_MeV = 10**logE * 1000 #in MeV

    #func = interp1d(energies_paper, cross_section_paper, kind = 'cubic', fill_value= 'extrapolate')

    linear = interp1d(energies_paper,cross_section_paper,kind="linear",fill_value="extrapolate")
    func = PchipInterpolator(energies_paper, cross_section_paper, extrapolate= False)

    inside = ((energies_MeV >= energies_paper[0]) & (energies_MeV <= energies_paper[-1]))
    cross_sections_interp_extrap = np.where(inside, func(energies_MeV), linear(energies_MeV))

    cross_sections_interp_extrap = np.maximum(cross_sections_interp_extrap, 0)
    #cross_sections_interp_extrap = np.maximum(0, cross_sections_interp_extrap) #cut of negative values

    cross_sections_globes = cross_sections_interp_extrap* 1e-4 / energies_GeV #in 10^-38cm^2 /GeV
    zeros = np.zeros(len(energies_MeV))

    output = np.column_stack((logE, zeros, zeros, zeros, cross_sections_globes, zeros, zeros))

    outfile = XSCNS / "xs_nuebar_Fe56.dat"

    header = ("Neutrino-56Fe cc cross section (10^-38 cm^2/GeV)\n"
              "log(energy in GeV) nu_e nu_mu nu_tau nu_e_bar nu_mu_bar nu_tau_bar\n")

    np.savetxt(outfile, output, fmt = "%.6e", header=header, comments="# ")



def calc_iron_nc_nux_Fe56():
    #assumption: same cross sections for all flavors and anti neutrinos

    energies_paper = np.arange(10,105,5) #in MeV

    #cross sections in 10^-42 cm^2, source: 1, 23, column 2
    cross_section_paper = np.array([0.191, 2.19, 6.90, 15.1, 28.5, 48.9, 78.6, 119, 172, 239, 320, 415, 525, 650, 789, 942, 1110, 1290, 1490])

    template = np.loadtxt(XSCNS / "xs_nue_Ar40.dat")
    logE = template[:,0] #in log(energy in GeV)
    energies_GeV = 10**logE #in GeV
    energies_MeV = 10**logE * 1000 #in MeV
    #cross_sections_interp = np.interp(energies_MeV, energies_paper, cross_section_paper, left = 0)

    #func = interp1d(energies_paper, cross_section_paper, kind = 'cubic', fill_value= 'extrapolate')

    linear = interp1d(energies_paper,cross_section_paper,kind="linear",fill_value="extrapolate")
    func = PchipInterpolator(energies_paper, cross_section_paper, extrapolate= False)

    inside = ((energies_MeV >= energies_paper[0]) & (energies_MeV <= energies_paper[-1]))
    cross_sections_interp_extrap = np.where(inside, func(energies_MeV), linear(energies_MeV))

    cross_sections_interp_extrap = np.maximum(cross_sections_interp_extrap, 0)

    cross_sections_globes = cross_sections_interp_extrap * 1e-4 / energies_GeV #in 10^-38cm^2 /GeV


    output = np.column_stack((logE, cross_sections_globes, cross_sections_globes, cross_sections_globes, cross_sections_globes, cross_sections_globes, cross_sections_globes))

    outfile = XSCNS / "xs_nc_nue_Fe56.dat"
    outfile2 = XSCNS / "xs_nc_numu_Fe56.dat"
    outfile3 = XSCNS / "xs_nc_nutau_Fe56.dat"
    outfile4 = XSCNS / "xs_nc_nuebar_Fe56.dat"
    outfile5 = XSCNS / "xs_nc_numubar_Fe56.dat"
    outfile6 = XSCNS / "xs_nc_nutaubar_Fe56.dat"

    header = ("Neutrino-56Fe neutral current cross section (10^-38 cm^2/GeV)\n"
              "log(energy in GeV) nu_e nu_mu nu_tau nu_e_bar nu_mu_bar nu_tau_bar\n")

    np.savetxt(outfile, output, fmt = "%.6e", header=header, comments="# ")
    np.savetxt(outfile2, output, fmt = "%.6e", header=header, comments="# ")
    np.savetxt(outfile3, output, fmt = "%.6e", header=header, comments="# ")
    np.savetxt(outfile4, output, fmt = "%.6e", header=header, comments="# ")
    np.savetxt(outfile5, output, fmt = "%.6e", header=header, comments="# ")
    np.savetxt(outfile6, output, fmt = "%.6e", header=header, comments="# ")


def calc_Pb_CC_nue():

    energies_paper = np.array([7.5, 10, 12.5, 15, 20, 25, 30, 40, 50, 60, 70, 80, 90, 100])
    #cross sections in 10^-42cm^2
    #Source 4, LAZAUSKAS, Table 1
    cross_section_paper = np.array([0.000247, 8.49, 46.8, 175, 853, 2860, 4900, 7130, 11300, 16300, 22000, 28300, 35000, 41600])

    template = np.loadtxt(XSCNS / "xs_nue_Ar40.dat")
    logE = template[:,0] #in log(energy in GeV)
    energies_GeV = 10**logE #in GeV
    energies_MeV = 10**logE * 1000 #in MeV

    #func = interp1d(energies_paper, cross_section_paper, kind = 'cubic', fill_value= 'extrapolate')

    linear = interp1d(energies_paper,cross_section_paper,kind="linear",fill_value="extrapolate")
    func = PchipInterpolator(energies_paper, cross_section_paper, extrapolate= False)

    inside = ((energies_MeV >= energies_paper[0]) & (energies_MeV <= energies_paper[-1]))
    cross_sections_interp_extrap = np.where(inside, func(energies_MeV), linear(energies_MeV))

    cross_sections_interp_extrap = np.maximum(cross_sections_interp_extrap, 0)
    #cross_sections_interp_extrap = np.maximum(0, cross_sections_interp_extrap) #cut of negative values

    cross_sections_globes = cross_sections_interp_extrap* 1e-4 / energies_GeV #in 10^-38cm^2 /GeV
    zeros = np.zeros(len(energies_MeV))

    output = np.column_stack((logE, zeros, zeros, zeros, cross_sections_globes, zeros, zeros))

    outfile = XSCNS / "CALC_xs_nue_Pb208.dat"

    header = ("Neutrino-208Pb cc cross section (10^-38 cm^2/GeV)\n"
              "log(energy in GeV) nu_e nu_mu nu_tau nu_e_bar nu_mu_bar nu_tau_bar\n")

    np.savetxt(outfile, output, fmt = "%.6e", header=header, comments="# ")




if __name__ == "__main__":
    calc_iron_nue_Fe56()
    #calc_iron_nuebar_Fe56()
    #calc_iron_nc_nux_Fe56()
    #calc_Pb_CC_nue()
