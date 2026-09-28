import numpy as np
import matplotlib.pyplot as plt
from pathlib  import Path
from scipy.interpolate import interp1d
from scipy.interpolate import PchipInterpolator

SNOWGLOBES = Path.home()/"software"/"snowglobes"
XSCNS = SNOWGLOBES/"xscns"
MARLEY = Path.home()/"software"/"marley"

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

def compare_CC_nue_xsec():

    #includes dummy Ar continuum react file
    marley_file_continuum = Path.home()/"software"/"marley"/"data_xsec"/f"Fe_Ar_copy.txt"
    marley_data_continuum = np.loadtxt(marley_file_continuum)
    marley_energy_continuum = marley_data_continuum[:, 0]
    marley_xsec_continuum = marley_data_continuum[:, 1]

    #only discrete react file
    marley_file_default = Path.home()/"software"/"marley"/"data_xsec"/f"nuebarCCDEFAULT.txt"
    marley_data_default = np.loadtxt(marley_file_default)
    marley_energy_default = marley_data_default[:, 0]
    marley_xsec_default = marley_data_default[:, 1]

    #only dicrete react file, form factors: allowed
    marley_file_allowed = Path.home()/"software"/"marley"/"data_xsec"/f"nuebarCCALLOWED.txt"
    marley_data_allowed = np.loadtxt(marley_file_allowed)
    marley_energy_allowed = marley_data_allowed[:, 0]
    marley_xsec_allowed = marley_data_allowed[:, 1]

    #discrete plus Ar dummy continuum file, form factors: allowed
    marley_file_4 = Path.home()/"software"/"marley"/"data_xsec"/f"Fe_allowed_Ar_dummy.txt"
    marley_data_4 = np.loadtxt(marley_file_4)
    marley_energy_4 = marley_data_4[:, 0]
    marley_xsec_4 = marley_data_4[:, 1]

    '''#CC nue Data
    energies_KOLBE = np.arange(10,105,5) #in MeV
    cross_section_KOLBE = np.array([0.661, 6.45, 29.3, 73.3, 140, 236, 371, 555, 798, 1100, 1480, 1920, 2420, 2990, 3600, 4270, 4980, 5730, 6520])

    energies_LAZAUSKAS = np.array([7.5, 10, 12.5, 15, 20, 25, 30, 40, 50, 60, 70, 80, 90, 100])
    cross_section_LAZAUSKAS = np.array([0.877, 3.63, 8.94, 17.3, 52.6, 125, 233, 544, 983, 1670, 2590, 3730, 5070, 6600])'''
    #CC nuebar Data
    energies_LAZAUSKAS = np.array([7.5, 10, 12.5, 15, 20, 25, 30, 40, 50, 60, 70, 80, 90, 100])
    #cross sections in 10^-42cm^2
    cross_section_LAZAUSKAS = np.array([0.841, 2.95 , 6.09, 10.3, 21.7, 37.4, 57.4, 120, 209, 353, 526, 727, 940, 1140])

    x = np.arange(0, 100, 0.5)

    '''KOLBE_interp = np.zeros(len(x))
    func = PchipInterpolator(energies_KOLBE, cross_section_KOLBE, extrapolate= False)
    KOLBE_interp += func(x)'''

    LAZAUSKAS_interp = np.zeros(len(x))
    #func = interp1d(energies_paper, cross_section_paper, kind = 'linear', fill_value= 'extrapolate')
    func = PchipInterpolator(energies_LAZAUSKAS, cross_section_LAZAUSKAS, extrapolate= False)
    LAZAUSKAS_interp += func(x)


    #plt.plot(marley_energy_allowed, marley_xsec_allowed, label = "MARLEY: allowed", color = "red")
    #plt.xlim(0, 30)
    #plt.ylim(0,300)
    #plt.yscale('log')
    plt.plot(marley_energy_default, marley_xsec_default, label = "MARLEY only discrete", color = "green")
    #plt.plot(marley_energy_continuum, marley_xsec_continuum, label = "MARLEY discrete + continuum 40Ar Files", color = "red")
    plt.plot(marley_energy_allowed, marley_xsec_allowed, label = "MARLEY discrete, allowed", color = "purple")
    #plt.plot(marley_energy_4, marley_xsec_4, label = "MARLEY discrete + continuum 40Ar, allowed", color = "grey")
    #plt.plot(x, KOLBE_interp, color = "tab:blue")
    plt.plot(x, LAZAUSKAS_interp, color = "tab:orange", label = "Lazauskas, 2007")
    #plt.scatter(energies_KOLBE, cross_section_KOLBE, label = "Kolbe, 2001")
    plt.scatter(energies_LAZAUSKAS, cross_section_LAZAUSKAS, label = "Lazauskas, 2007")


    plt.legend()
    plt.grid(True, alpha = 0.3)
    plt.xlabel(r"Neutrino energy E$_\nu$ [MeV]")
    plt.ylabel(r"$\sigma$ in $10^{-42} cm^2$")
    plt.title(r"CC $\bar\nu_e$ cross section on 56Fe comparison")
    
    plt.savefig("xcns_calculations/nuebarCCFe.png")
    plt.close()

def get_snowglobes_xsec(channel, column):
    file = XSCNS/f"xs_{channel}.dat"
    data = np.loadtxt(file)

    energies = data[:, 0] #log(GeV)
    energies_GeV = 10**energies
    energies_MeV = energies_GeV * 1000
    xsec = data[:, column]*energies_GeV*1e4
    return (energies_MeV, xsec)

def compare_Fe_cross_sections_snowglobes():

    e_CC_nue, x_CC_nue = get_snowglobes_xsec("nue_Fe56", 1)

    e_CC_nuebar, x_CC_nuebar = get_snowglobes_xsec("nuebar_Fe56", 4)

    e_ES_nue, x_ES_nue = get_snowglobes_xsec("nue_e", 1)

    e_NC_nue, x_NC_nue = get_snowglobes_xsec("nc_nue_Fe56", 1)

    energies_CC_nue_scatter = np.array([7.5, 10, 12.5, 15, 20, 25, 30, 40, 50, 60, 70, 80, 90, 100])
    cross_section_CC_nue_scatter = np.array([0.877, 3.63, 8.94, 17.3, 52.6, 125, 233, 544, 983, 1670, 2590, 3730, 5070, 6600])

    energies_CC_nuebar_scatter = np.array([7.5, 10, 12.5, 15, 20, 25, 30, 40, 50, 60, 70, 80, 90, 100])
    cross_section_CC_nuebar_scatter = np.array([0.841, 2.95 , 6.09, 10.3, 21.7, 37.4, 57.4, 120, 209, 353, 526, 727, 940, 1140])

    energies_NC_scatter = np.arange(10,105,5) #in MeV
    
        #cross sections in 10^-42 cm^2, source: 1, 23, column 2
    cross_section_NC_scatter = np.array([0.191, 2.19, 6.90, 15.1, 28.5, 48.9, 78.6, 119, 172, 239, 320, 415, 525, 650, 789, 942, 1110, 1290, 1490])


    #plt.plot(marley_energy_allowed, marley_xsec_allowed, label = "MARLEY: allowed", color = "red")
    #plt.xlim(0, 30)
    #plt.ylim(0,300)
    #plt.yscale('log')
    plt.plot(e_CC_nue, x_CC_nue, color = "tab:green")
    plt.scatter(energies_CC_nue_scatter, cross_section_CC_nue_scatter, label = r"CC $\nu_e$ Lazauskas, 2007", color = "tab:green")

    plt.plot(e_CC_nuebar, x_CC_nuebar, color = "tab:orange")
    plt.scatter(energies_CC_nuebar_scatter, cross_section_CC_nuebar_scatter, label = r"CC $\bar\nu_e$ Lazauskas, 2007", color = "tab:orange")

    plt.plot(e_NC_nue, x_NC_nue, color = "tab:blue")
    plt.scatter(energies_NC_scatter, cross_section_NC_scatter, label = r"NC $\nu_x$ Kolbe, 2001", color = "tab:blue")

    #plt.plot(e_ES_nue, x_ES_nue, color = "red", label = r"eES $\nu_e$ from SNOwGLoBES")

    plt.legend()
    plt.grid(True, alpha = 0.3)
    plt.xlabel(r"Neutrino energy E$_\nu$ [MeV]")
    plt.ylabel(r"$\sigma$ in $10^{-42} cm^2$")
   # plt.title(r"CC $\bar\nu_e$ cross section on 56Fe comparison")
    
    plt.savefig("plotting/snowglobes_xsec_comparison.svg", bbox_inches="tight", dpi = 900)
    plt.close()


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


def flux_averaged_xsec_CC_nue():
    energy_common = np.linspace(0, 100, 10001)

    file_flux = SNOWGLOBES/"fluxes"/"garching.dat"
    data_flux = np.loadtxt(file_flux)
    energy_flux = data_flux[:, 0] * 1000
    flux = data_flux[:, 4]
    flux_common = np.interp(energy_common, energy_flux, flux, left = 0.0, right = 0.0)
    flux_integral = np.trapezoid(flux_common, energy_common)

    file_snowglobes = XSCNS/ "xs_nuebar_Fe56.dat"
    data_snowglobes = np.loadtxt(file_snowglobes)
    logGeV = data_snowglobes[:, 0]
    energy_snowglobes_GeV = 10 ** logGeV
    energy_snowglobes = energy_snowglobes_GeV * 1000

    xsec_snowglobes = data_snowglobes[:, 4] * energy_snowglobes_GeV * 1e4
    snowglobes_common = np.interp(energy_common, energy_snowglobes, xsec_snowglobes, left = 0.0, right = 0.0)
    snowglobes_intergal = np.trapezoid(flux_common * snowglobes_common, energy_common)
    snowglobes_avg = snowglobes_intergal / flux_integral

    file_marley = MARLEY/"data_xsec"/"Fe_CCnuebar.txt"
    data_marley = np.loadtxt(file_marley)
    energy_marley = data_marley[:, 0]
    xsec_marley = data_marley[:, 1]
    marley_common = np.interp(energy_common, energy_marley, xsec_marley, left = 0.0, right = 0.0)
    marley_integral = np.trapezoid(flux_common * marley_common,energy_common)
    marley_avg = marley_integral / flux_integral


    file_marley_discrete = MARLEY/"data_xsec"/"Fe_Ar_discrete.txt"
    data_marley_discrete = np.loadtxt(file_marley_discrete)
    energy_marley_discrete = data_marley_discrete[:, 0]
    xsec_marley_discrete = data_marley_discrete[:, 1]
    marley_discrete_common = np.interp(energy_common, energy_marley_discrete, xsec_marley_discrete, left = 0.0, right = 0.0)
    marley_discrete_integral = np.trapezoid(flux_common * marley_discrete_common, energy_common)
    marley_discrete_avg = marley_discrete_integral / flux_integral

    print(data_snowglobes[:5])
    print("SG energy range:", energy_snowglobes.min(), energy_snowglobes.max())
    print("SG xsec range:", xsec_snowglobes.min(), xsec_snowglobes.max())

    print("MARLEY energy range:", energy_marley.min(), energy_marley.max())
    print("MARLEY xsec range:", xsec_marley.min(), xsec_marley.max())
    print("SNOWGLOBES flux-averaged xsec:", snowglobes_avg)
    print("MARLEY flux-averaged xsec:", marley_avg)
    print("RATIO xsec:", marley_avg/snowglobes_avg)

    plt.plot(energy_common, snowglobes_common, label = "SNOwGLoBES, Lazauskas 2007")
    plt.plot(energy_common, marley_common, label = "MARLEY, discrete + allowed form factors")
    #plt.plot(energy_common, marley_discrete_common, label = "MARLEY, discrete", color = "green", linestyle = "--")
    plt.text(0.02, 0.74, rf"""SNOwGLoBES $\langle\sigma\rangle = $ {snowglobes_avg:.2f}  $\times$ 10$^{{-42}}$ cm$^2$
MARLEY AA $\langle\sigma\rangle = $ {marley_avg:.2f} $\times$ 10$^{{-42}}$ cm$^2$"""
#MARLEY Default $\langle\sigma\rangle = $ {marley_discrete_avg:.2f}  $\times$ 10$^{{-42}}$ cm$^2$"""


, transform=plt.gca().transAxes)
    #plt.xlim(10, 30)
    #plt.ylim(0,200)
    plt.grid(True, alpha = 0.3)
    plt.legend()
    plt.title(r"MARLEY / SNOwGLoBES cross section comparison for CC $\bar\nu_e$")
    plt.xlabel(r"Neutrino energy E$_\nu$ [MeV]")
    plt.ylabel(r"cross section $\sigma$ in 10$^{-42}$ cm$^2$")
    plt.savefig("xcns_calculations/xsec_CCnuebar_comparison.png")


if __name__ == "__main__":
    #plot_iron_cross()
    compare_Fe_cross_sections_snowglobes()
    #compare_CC_nue_xsec()
    #compare_xsec_Fe_Pb()
    #flux_averaged_xsec_CC_nue()

    