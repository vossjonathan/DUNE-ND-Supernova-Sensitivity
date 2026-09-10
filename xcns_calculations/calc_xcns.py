import numpy as np
import matplotlib.pyplot as plt
from pathlib  import Path
from scipy.interpolate import interp1d
from scipy.interpolate import PchipInterpolator


#linear interpolation and extrapolation

SNOWGLOBES = Path.home()/"software"/"snowglobes"
XSCNS = SNOWGLOBES/"xscns"

def calc_iron_nue_Fe56():


    

    # KOLBE:
    # cross sections in 10^-42 cm^2, source: 1, 23, column 1
    # energies_paper = np.arange(10,105,5) #in MeV
    # cross_section_paper = np.array([0.661, 6.45, 29.3, 73.3, 140, 236, 371, 555, 798, 1100, 1480, 1920, 2420, 2990, 3600, 4270, 4980, 5730, 6520])

    # LAZAUSKAS:
    # cross sections in 10^-42 cm^2, source 4
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


calc_iron_nue_Fe56()

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


calc_iron_nuebar_Fe56()

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


#calc_iron_nc_nux_Fe56()

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

#calc_Pb_CC_nue()

def plot_iron_cross():

    marley_file = Path.home()/"software"/"marley"/"Fe_Fermi-MEMA.txt"
    data_marley = np.loadtxt(marley_file)
    energies_marley = data_marley[:, 0]
    xsec_marley = data_marley[:, 1]


    energies_paper = np.arange(10,105,5) #in MeV

    #cross sections in 10^-42 cm^2, source: 1, 23, column 1
    cross_section_paper_KOLBE = np.array([0.661, 6.45, 29.3, 73.3, 140, 236, 371, 555, 798, 1100, 1480, 1920, 2420, 2990, 3600, 4270, 4980, 5730, 6520])

    template = np.loadtxt(XSCNS / "xs_nue_Ar40.dat")
    logE = template[:,0] #in log10(energy in GeV)
    
    energies_GeV = 10**logE #in GeV
    energies_MeV = 10**logE * 1000 #in MeV
    #cross_sections_interp = np.interp(energies_MeV, energies_paper, cross_section_paper, left = 0)

    cross_sections_interp_extrap = np.zeros(len(energies_MeV))
    #func = interp1d(energies_paper, cross_section_paper, kind = 'linear', fill_value= 'extrapolate')
    func = PchipInterpolator(energies_paper, cross_section_paper_KOLBE, extrapolate= False)
    cross_sections_interp_extrap += func(energies_MeV)
    #print("only interp ", cross_sections_interp[700:800])
    #print('interp, extrap ', cross_sections_interp_extrap[700:800])
    #cross_sections_interp_extrap = np.maximum(0, cross_sections_interp_extrap) #cut of negative values


    energies_paper2 = np.array([7.5, 10, 12.5, 15, 20, 25, 30, 40, 50, 60, 70, 80, 90, 100])
    #cross sections in 10^-42cm^2
    cross_section_paper2 = np.array([0.841, 2.95 , 6.09, 10.3, 21.7, 37.4, 57.4, 120, 209, 353, 526, 727, 940, 1140])

    energies_paper3 = np.arange(10,105,5) #in MeV

    #cross sections in 10^-42 cm^2, source: 1, 23, column 2
    cross_section_paper3 = np.array([0.191, 2.19, 6.90, 15.1, 28.5, 48.9, 78.6, 119, 172, 239, 320, 415, 525, 650, 789, 942, 1110, 1290, 1490])

    cross_section_paper_LAZAUSKAS = np.array([0.877, 3.63, 8.94, 17.3, 52.6, 125, 233, 544, 983, 1670, 2590, 3730, 5070, 6600])

    plt.plot(energies_marley, xsec_marley, label = "MARLEY", color = "purple")
    plt.scatter(energies_MeV, cross_sections_interp_extrap, label = "Inter/Extrapolatoin")
    plt.scatter(energies_paper, cross_section_paper_KOLBE, label = r"KOLBE: CC $\nu_e$ ")
    plt.scatter(energies_paper2, cross_section_paper_LAZAUSKAS, label = r"LAZAUSKAS: CC $\nu_e$ ")
    plt.scatter(energies_paper2, cross_section_paper2, label = r"CC $\bar\nu_e$")
    plt.scatter(energies_paper3, cross_section_paper3, label = "NC all flavors")
    plt.legend()
    plt.xlabel("E [MeV]")
    plt.ylabel(r"$\sigma$ in $10^{-42} cm^2$")
    plt.title("linear inter- and extrapolation")
    
    plt.savefig("xcns_calculations/iron_with_marley.png")


#plot_iron_cross()

def compare_CC_nue_xsec():

    #includes dummy Ar continuum react file
    marley_file_continuum = Path.home()/"software"/"marley"/"data_xsec"/f"Fe_Ar_continuum.txt"
    marley_data_continuum = np.loadtxt(marley_file_continuum)
    marley_energy_continuum = marley_data_continuum[:, 0]
    marley_xsec_continuum = marley_data_continuum[:, 1]

    #only discrete react file
    marley_file_default = Path.home()/"software"/"marley"/"data_xsec"/f"Fe_Ar_discrete.txt"
    marley_data_default = np.loadtxt(marley_file_default)
    marley_energy_default = marley_data_default[:, 0]
    marley_xsec_default = marley_data_default[:, 1]

    #form_factors: allowed, coulomb_mode: Fermi-MEMA
    marley_file_3 = Path.home()/"software"/"marley"/"data_xsec"/f"Fe_Fermi_Mema_and_allowed.txt"
    marley_data_3 = np.loadtxt(marley_file_3)
    marley_energy_3 = marley_data_3[:, 0]
    marley_xsec_3 = marley_data_3[:, 1]

    energies_KOLBE = np.arange(10,105,5) #in MeV
    cross_section_KOLBE = np.array([0.661, 6.45, 29.3, 73.3, 140, 236, 371, 555, 798, 1100, 1480, 1920, 2420, 2990, 3600, 4270, 4980, 5730, 6520])

    energies_LAZAUSKAS = np.array([7.5, 10, 12.5, 15, 20, 25, 30, 40, 50, 60, 70, 80, 90, 100])
    cross_section_LAZAUSKAS = np.array([0.877, 3.63, 8.94, 17.3, 52.6, 125, 233, 544, 983, 1670, 2590, 3730, 5070, 6600])

    x = np.arange(0, 100, 0.5)

    KOLBE_interp = np.zeros(len(x))
    func = PchipInterpolator(energies_KOLBE, cross_section_KOLBE, extrapolate= False)
    KOLBE_interp += func(x)

    LAZAUSKAS_interp = np.zeros(len(x))
    #func = interp1d(energies_paper, cross_section_paper, kind = 'linear', fill_value= 'extrapolate')
    func = PchipInterpolator(energies_LAZAUSKAS, cross_section_LAZAUSKAS, extrapolate= False)
    LAZAUSKAS_interp += func(x)


    #plt.plot(marley_energy_allowed, marley_xsec_allowed, label = "MARLEY: allowed", color = "red")
    plt.plot(marley_energy_default, marley_xsec_default, label = "MARLEY only discrete", color = "green")
    plt.plot(marley_energy_continuum, marley_xsec_continuum, label = "MARLEY continuum 40Ar Files", color = "red")
    plt.plot(marley_energy_3, marley_xsec_3, label = "form factor: allowed", color = "purple")
    plt.plot(x, KOLBE_interp, color = "tab:blue")
    plt.plot(x, LAZAUSKAS_interp, color = "tab:orange")
    plt.scatter(energies_KOLBE, cross_section_KOLBE, label = "Kolbe, 2001")
    plt.scatter(energies_LAZAUSKAS, cross_section_LAZAUSKAS, label = "Lazauskas, 2007")


    plt.legend()
    plt.grid(True, alpha = 0.3)
    plt.xlabel(r"Neutrino energy E$_\nu$ [MeV]")
    plt.ylabel(r"$\sigma$ in $10^{-42} cm^2$")
    plt.title(r"CC $\nu_e$ cross section on 56Fe comparison")
    
    plt.savefig("xcns_calculations/test.png")

compare_CC_nue_xsec()

def compare_xsec_Fe_Pb():

    marley_file_default = Path.home()/"software"/"marley"/"Fe_DEFAULT.txt"
    marley_data_default = np.loadtxt(marley_file_default)
    marley_energy_default = marley_data_default[:, 0]
    marley_xsec_default = marley_data_default[:, 1]

    Pb_file = Path.home()/"software"/"marley"/"Pb_xsec_data.txt"
    Pb_data = np.loadtxt(Pb_file)
    Pb_energy = Pb_data[:, 0]
    Pb_xsec = Pb_data[:, 1]

    x = np.arange(0, 100, 0.5)

    energies_Pb = np.array([7.5, 10, 12.5, 15, 20, 25, 30, 40, 50, 60, 70, 80, 90, 100])
    #cross sections in 10^-42cm^2
    #Source 4, LAZAUSKAS, Table 1
    cross_section_Pb = np.array([0.000247, 8.49, 46.8, 175, 853, 2860, 4900, 7130, 11300, 16300, 22000, 28300, 35000, 41600])
    CC_nue_Pb_interp = np.zeros(len(x))
    func = PchipInterpolator(energies_Pb, cross_section_Pb, extrapolate= False)
    CC_nue_Pb_interp += func(x)

    #plt.plot(marley_energy_allowed, marley_xsec_allowed, label = "MARLEY: allowed", color = "red")
    plt.plot(marley_energy_default, marley_xsec_default, label = "MARLEY v2 Fe", color = "green")
    plt.scatter(energies_Pb, cross_section_Pb, label = "LAZAUSKAS Pb", color = "tab:orange")
    plt.plot(x, CC_nue_Pb_interp, label = "LAZAUSKAS Pb interpolation", color = "tab:orange")
    plt.plot(Pb_energy, Pb_xsec, label = "MARLEY v2 Pb", color = "red")



    plt.legend()
    plt.grid(True, alpha = 0.3)
    plt.xlabel(r"Neutrino energy E$_\nu$ [MeV]")
    plt.ylabel(r"$\sigma$ in $10^{-42} cm^2$")
    plt.title(r"CC $\nu_e$ cross section on 56Fe vs 208Pb")
    
    plt.savefig("xcns_calculations/comparison_Pb_paper.png")

#compare_xsec_Fe_Pb()