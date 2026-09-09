import numpy as np
import matplotlib.pyplot as plt
from pathlib  import Path
import matplotlib.patches as mpatches


SNOWGLOBES = Path.home()/"software"/"snowglobes"
OUT = Path.home()/"software"/"snowglobes"/"out"

def get_channel_totals(detector, material, channel, flux):
    channels_iron = {
        "nue_e" : 26,
        "nuebar_e" : 26,
        "numu_e" : 26,
        "numubar_e" : 26,
        "nutau_e" : 26,
        "nutaubar_e" : 26,
        "nue_Fe56" : 1,
        "nuebar_Fe56" : 1,
        "nc_nue_Fe56" : 1,
        "nc_nuebar_Fe56" : 1,
        "nc_numu_Fe56" : 1,
        "nc_numubar_Fe56" : 1,
        "nc_nutau_Fe56" : 1,
        "nc_nutaubar_Fe56" : 1,
    }
    channels_lead = {
        "nue_e" : 82,
        "nuebar_e" : 82,
        "numu_e" : 82,
        "numubar_e" : 82,
        "nutau_e" : 82,
        "nutaubar_e" : 82,
        "nue_Pb208_1n" : 1,
        "nue_Pb208_2n" : 1,
        "nc_nue_Pb208_1n" : 1,
        "nc_nuebar_Pb208_1n" : 1,
        "nc_numu_Pb208_1n" : 1,
        "nc_numubar_Pb208_1n" : 1,
        "nc_nutau_Pb208_1n" : 1,
        "nc_nutaubar_Pb208_1n" : 1,
        "nc_nue_Pb208_2n" : 1,
        "nc_nuebar_Pb208_2n" : 1,
        "nc_numu_Pb208_2n" : 1,
        "nc_numubar_Pb208_2n" : 1,
        "nc_nutau_Pb208_2n" : 1,
        "nc_nutaubar_Pb208_2n" : 1

    }
    channels_scint = {
        "ibd":1,
        "nue_e" : 4,
        "nuebar_e" : 4,
        "numu_e" : 4,
        "numubar_e" : 4,
        "nutau_e" : 4,
        "nutaubar_e" : 4,
        "nue_C12" : 0.4945,
        "nuebar_C12" : 0.4945,
        "nc_nue_C12" : 0.4945,
        "nc_nuebar_C12" : 0.4945,
        "nc_numu_C12" : 0.4945,
        "nc_numubar_C12" : 0.4945,
        "nc_nutau_C12" : 0.4945,
        "nc_nutaubar_C12" : 0.4945,
        "nue_C13" : 0.0055,
        "nc_nue_C13" : 0.0055,
        "nc_nuebar_C13" : 0.0055,
        "nc_numu_C13" : 0.0055,
        "nc_numubar_C13" : 0.0055,
        "nc_nutau_C13" : 0.0055,
        "nc_nutaubar_C13" : 0.0055

    }
    

    channels_argon = {
        "nue_e" : 18,
        "nuebar_e" : 18,
        "numu_e" : 18,
        "numubar_e" : 18,
        "nutau_e" : 18,
        "nutaubar_e" : 18,
        "nue_Ar40" : 1,
        "nuebar_Ar40" : 1,
        "nc_nue_Ar40" : 1,
        "nc_nuebar_Ar40" : 1,
        "nc_numu_Ar40" : 1,
        "nc_numubar_Ar40" : 1,
        "nc_nutau_Ar40" : 1,
        "nc_nutaubar_Ar40" : 1

    }

    channel_weights = {
        "iron": channels_iron,
        "argon": channels_argon,
        "scint": channels_scint,
        "lead": channels_lead,
    }

    weight = channel_weights[material][channel]


    smeared_file = OUT/f"{flux}_{channel}_{detector}_events_smeared_unweighted.dat"
    data_smeared = np.loadtxt(smeared_file, max_rows=200)
    events_smeared = data_smeared[:, 1]
    events_smeared_w = events_smeared * weight

    unsmeared_file = OUT/f"{flux}_{channel}_{detector}_events_unweighted.dat"
    data_unsmeared = np.loadtxt(unsmeared_file, max_rows=200)
    events_unsmeared = data_unsmeared[:, 1]
    events_unsmeared_w = events_unsmeared* weight

    return (events_unsmeared_w.sum(), events_smeared_w.sum())

#get_channel_totals("TMS_iron", "iron", "nue_e", "garching")

def get_channel_out_smeared_unsmeared(detector, material, channel, flux):
    channels_iron = {
        "nue_e" : 26,
        "nuebar_e" : 26,
        "numu_e" : 26,
        "numubar_e" : 26,
        "nutau_e" : 26,
        "nutaubar_e" : 26,
        "nue_Fe56" : 1,
        "nuebar_Fe56" : 1,
        "nc_nue_Fe56" : 1,
        "nc_nuebar_Fe56" : 1,
        "nc_numu_Fe56" : 1,
        "nc_numubar_Fe56" : 1,
        "nc_nutau_Fe56" : 1,
        "nc_nutaubar_Fe56" : 1,
    }
    channels_lead = {
        "nue_e" : 82,
        "nuebar_e" : 82,
        "numu_e" : 82,
        "numubar_e" : 82,
        "nutau_e" : 82,
        "nutaubar_e" : 82,
        "nue_Pb208_1n" : 1,
        "nue_Pb208_2n" : 1,
        "nc_nue_Pb208_1n" : 1,
        "nc_nuebar_Pb208_1n" : 1,
        "nc_numu_Pb208_1n" : 1,
        "nc_numubar_Pb208_1n" : 1,
        "nc_nutau_Pb208_1n" : 1,
        "nc_nutaubar_Pb208_1n" : 1,
        "nc_nue_Pb208_2n" : 1,
        "nc_nuebar_Pb208_2n" : 1,
        "nc_numu_Pb208_2n" : 1,
        "nc_numubar_Pb208_2n" : 1,
        "nc_nutau_Pb208_2n" : 1,
        "nc_nutaubar_Pb208_2n" : 1

    }
    channels_scint = {
        "ibd":1,
        "nue_e" : 4,
        "nuebar_e" : 4,
        "numu_e" : 4,
        "numubar_e" : 4,
        "nutau_e" : 4,
        "nutaubar_e" : 4,
        "nue_C12" : 0.4945,
        "nuebar_C12" : 0.4945,
        "nc_nue_C12" : 0.4945,
        "nc_nuebar_C12" : 0.4945,
        "nc_numu_C12" : 0.4945,
        "nc_numubar_C12" : 0.4945,
        "nc_nutau_C12" : 0.4945,
        "nc_nutaubar_C12" : 0.4945,
        "nue_C13" : 0.0055,
        "nc_nue_C13" : 0.0055,
        "nc_nuebar_C13" : 0.0055,
        "nc_numu_C13" : 0.0055,
        "nc_numubar_C13" : 0.0055,
        "nc_nutau_C13" : 0.0055,
        "nc_nutaubar_C13" : 0.0055

    }
    

    channels_argon = {
        "nue_e" : 18,
        "nuebar_e" : 18,
        "numu_e" : 18,
        "numubar_e" : 18,
        "nutau_e" : 18,
        "nutaubar_e" : 18,
        "nue_Ar40" : 1,
        "nuebar_Ar40" : 1,
        "nc_nue_Ar40" : 1,
        "nc_nuebar_Ar40" : 1,
        "nc_numu_Ar40" : 1,
        "nc_numubar_Ar40" : 1,
        "nc_nutau_Ar40" : 1,
        "nc_nutaubar_Ar40" : 1

    }

    channel_weights = {
        "iron": channels_iron,
        "argon": channels_argon,
        "scint": channels_scint,
        "lead": channels_lead,
    }

    weight = channel_weights[material][channel]


    smeared_file = OUT/f"{flux}_{channel}_{detector}_events_smeared_unweighted.dat"
    data_smeared = np.loadtxt(smeared_file, max_rows=200)
    events_smeared = data_smeared[:, 1]
    events_smeared_w = events_smeared * weight

    unsmeared_file = OUT/f"{flux}_{channel}_{detector}_events_unweighted.dat"
    data_unsmeared = np.loadtxt(unsmeared_file, max_rows=200)
    events_unsmeared = data_unsmeared[:, 1]
    events_unsmeared_w = events_unsmeared* weight

    return (events_unsmeared_w, events_smeared_w)
