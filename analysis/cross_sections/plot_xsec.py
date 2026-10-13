import numpy as np
import matplotlib.pyplot as plt
from pathlib  import Path
from scipy.interpolate import PchipInterpolator


#This file mostly contains debug plots and compares differenct cross section sources, channels and MARLEY calculations

REPO_ROOT = Path(__file__).resolve().parents[2]

#local SNOwGLoBES installation Path
SNOWGLOBES = Path.home()/"software"/"snowglobes"
XSCNS = SNOWGLOBES/"xscns"

#local MARLEY installation
MARLEY = Path.home()/"software"/"marley"
MARLEY_XSEC = MARLEY/ "data_xsec"

PLOT_DIR = REPO_ROOT /"analysis"/"debug_plots"


#plots cross section comparison of Lazauskas vs. Kolbe vs. MARLEY calculated cross section
def plot_iron_cross():

    marley_file = MARLEY_XSEC/"Fe_Fermi-MEMA.txt"
    data_marley = np.loadtxt(marley_file)
    energies_marley = data_marley[:, 0]
    xsec_marley = data_marley[:, 1]


    energies_paper = np.arange(10,105,5) #in MeV

    #cross sections in 10^-42 cm^2, source: 1, 23, column 1
    cross_section_paper_KOLBE = np.array([0.661, 6.45, 29.3, 73.3, 140, 236, 371, 555, 798, 1100, 1480, 1920, 2420, 2990, 3600, 4270, 4980, 5730, 6520])

    template = np.loadtxt(XSCNS / "xs_nue_Ar40.dat")
    logE = template[:,0] #in log10(energy in GeV)
    
    energies_GeV = 10**logE #in GeV
    energies_MeV = energies_GeV * 1000 #in MeV
    #cross_sections_interp = np.interp(energies_MeV, energies_paper, cross_section_paper, left = 0)

    cross_sections_interp_extrap = np.zeros(len(energies_MeV))
    #func = interp1d(energies_paper, cross_section_paper, kind = 'linear', fill_value= 'extrapolate')
    func = PchipInterpolator(energies_paper, cross_section_paper_KOLBE, extrapolate= False)
    cross_sections_interp_extrap += func(energies_MeV)

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
    plt.title("PCHIP interpolation of Kolbe cross sections")
    
    plt.savefig(PLOT_DIR/"iron_with_marley.png")
    plt.close()

#comparing different MARLEY settings and the resuling Fe56 cross sections, only debug plot
def compare_xsec_MARLEY():

    #includes dummy Ar continuum react file
    marley_file_continuum = MARLEY_XSEC/"Fe_Ar_copy.txt"
    marley_data_continuum = np.loadtxt(marley_file_continuum)
    marley_energy_continuum = marley_data_continuum[:, 0]
    marley_xsec_continuum = marley_data_continuum[:, 1]

    #only discrete react file
    marley_file_default = MARLEY_XSEC/"nuebarCCDEFAULT.txt"
    marley_data_default = np.loadtxt(marley_file_default)
    marley_energy_default = marley_data_default[:, 0]
    marley_xsec_default = marley_data_default[:, 1]

    #only dicrete react file, form factors: allowed
    marley_file_allowed = MARLEY_XSEC/"nuebarCCALLOWED.txt"
    marley_data_allowed = np.loadtxt(marley_file_allowed)
    marley_energy_allowed = marley_data_allowed[:, 0]
    marley_xsec_allowed = marley_data_allowed[:, 1]

    #discrete plus Ar dummy continuum file, form factors: allowed
    marley_file_4 = MARLEY_XSEC/f"Fe_allowed_Ar_dummy.txt"
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
    
    plt.savefig(PLOT_DIR/"nuebarCCFe.png")
    plt.close()

# helper function to get snowglobes cross section
# it returns the energies used and the cross section for the corresponding energy

def get_snowglobes_xsec(channel, column, suffix = ""):
    file = XSCNS/f"xs_{channel}{suffix}.dat"
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
    
    plt.savefig(PLOT_DIR/ "snowglobes_xsec_comparison.svg", bbox_inches="tight", dpi = 900)
    plt.close()

def compare_CC_C13_cross_sections():
    energies_MeV_extrap, xsec_nue_C13_extrap = get_snowglobes_xsec("nue_C13", 1)
    energies_snow, xsec_snow = get_snowglobes_xsec("nue_C13", 1, suffix = "_original_snowglobes")
    #SOURCE:
    energies_paper = np.arange(3, 55)  # MeV

    cross_section_paper = np.array([
        0.0221, 0.0939, 0.223, 0.439, 0.838, 1.41,
        2.16, 3.10, 4.20, 5.52, 7.09, 8.90, 10.9,
        13.2, 15.9, 18.6, 21.7, 25.1, 28.8, 32.7,
        37.0, 41.5, 46.2, 51.4, 56.9, 62.6,
        68.7, 75.0, 81.8, 88.9, 96.2, 104,
        112, 121, 129, 138, 148, 159, 170,
        180, 192, 203, 215, 228, 241, 256,
        270, 284, 299, 315, 331, 347
    ])

    
    
    plt.plot(energies_paper, cross_section_paper, label = "literature xsec, Suzuki 2019", color = "tab:orange")    
    plt.plot(energies_MeV_extrap, xsec_nue_C13_extrap, label = "Extrapolated cross sections", color = "tab:orange", linestyle = "--")
    plt.plot(energies_snow, xsec_snow, label = "snowglobes xsec C13", color = "tab:blue")
    plt.legend()
    plt.xlabel(r"Neutrino energy $E_\nu$ [MeV]")
    plt.ylabel(r"$\sigma$ in $10^{-42} cm^2$")
    plt.title(r"Comparison of C13 CC $\nu_e$ cross sections")
    plt.grid(True, alpha = 0.3)
    plt.savefig(PLOT_DIR/"C13_cross_section_snowglobes.svg", bbox_inches = "tight", dpi = 900)
    plt.close()

def compare_NC_C13_cross_sections():
    
    energies_MeV_extrap, xsec_nue_C13_extrap = get_snowglobes_xsec("nc_nue_C13", 1)
    energies_snow, xsec_snow = get_snowglobes_xsec("nc_nue_C13", 1, suffix = "_original_snowglobes")

    #SOURCE: 5, 8 (Table 4, Suzuki)
    energies_paper = np.arange(6, 61)  # MeV

    cross_section_paper = np.array([
        1.61144e-14, 4.98686e-7, 1.70467e-5, 1.44971e-4,
        0.00492129, 0.0208600, 0.0506791, 0.0947193,
        0.154234, 0.229880, 0.322241, 0.431917,
        0.559371, 0.705006, 0.869271, 1.05267,
        1.25572, 1.47902, 1.72324, 1.98912,
        2.27737, 2.58877, 2.92406, 3.28421,
        3.66993, 4.08214, 4.52166, 4.98929,
        5.48597, 6.01253, 6.56985, 7.15877,
        7.78015, 8.43485, 9.12365, 9.84743,
        10.6069, 11.4029, 12.2361, 13.1073,
        14.0169, 14.9658, 15.9545, 16.9835,
        18.0532, 19.1641, 20.3165, 21.5107,
        22.7470, 24.0256, 25.3465, 26.7098,
        28.1156, 29.5636, 31.0538
    ])
    
    
    plt.plot(energies_paper, cross_section_paper, label = "literature xsec, Suzuki 2019", color = "tab:orange")    
    plt.plot(energies_MeV_extrap, xsec_nue_C13_extrap, label = "Extrapolated cross sections", color = "tab:orange", linestyle = "--")
    plt.plot(energies_snow, xsec_snow, label = "snowglobes xsec C13", color = "tab:blue")
    plt.legend()
    plt.xlabel(r"Neutrino energy $E_\nu$ [MeV]")
    plt.ylabel(r"$\sigma$ in $10^{-42} cm^2$")
    plt.title(r"Comparison of C13 NC $\nu_e$ cross sections")
    plt.grid(True, alpha = 0.3)
    plt.savefig(PLOT_DIR/"NC_C13_cross_section_snowglobes.svg", bbox_inches = "tight", dpi = 900)
    plt.close()

def compare_xsec_Fe_Pb():

    marley_file_default = MARLEY_XSEC/"Fe_DEFAULT.txt"
    marley_data_default = np.loadtxt(marley_file_default)
    marley_energy_default = marley_data_default[:, 0]
    marley_xsec_default = marley_data_default[:, 1]

    Pb_file = MARLEY_XSEC/"Pb_xsec_data.txt"
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
    
    plt.savefig(PLOT_DIR/"comparison_Pb_paper.png")
    plt.close()

def flux_averaged_xsec():
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
    plt.savefig(PLOT_DIR/"xsec_CCnuebar_comparison.png")
    plt.close()

if __name__ == "__main__":
    #compare_CC_C13_cross_sections()
    #compare_NC_C13_cross_sections()
    plot_iron_cross()
    compare_Fe_cross_sections_snowglobes()
    compare_xsec_MARLEY()
    compare_xsec_Fe_Pb()
    flux_averaged_xsec()

    pass