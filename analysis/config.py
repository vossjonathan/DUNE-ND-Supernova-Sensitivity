


import numpy as np

ENERGY_GRID = np.linspace(0.5, 100, 201)


# Configuration for all channels where the smearing matrix is created
# with MARLEY + Geant4 or Geant4-only.
# threshold is minimum energy for Geant4 scan
DETECTOR_SMEARING_CONFIG = {


    "TMS_iron": {

        "material": "iron",

        "channels": {

            #"G4_only_nue_Fe56": {
            #   "folder": "G4_ONLY_CC_nue_100k",
            #   "threshold": 4.6,
            #    "filename": "TMS_{E:.5f}_nue_Fe56_MeV.root",
            #    "ES": False,
            #    "weight": 1,
            #},

            "nue_Fe56": {
                "folder": "MARLEY_CC_nue100k_ALLOWED",
                "threshold": 6.31,
                "filename": "MARLEY_TMS_{E:.5f}_CC_ALLOWED_Fe56_MeV.root",
                "ES": False,
                "weight": 1,
            },


            "nuebar_Fe56": {
                "folder": "MARLEY_CC_nuebar_100k_ALLOWED",
                "threshold": 5.1,
                "filename": "MARLEY_TMS_{E:.5f}_CC_nuebar_ALLOWED_Fe56_MeV.root",
                "ES": False,
                "weight": 1,
            },
    

            "nc_nue_Fe56": {
                "folder": "MARLEY_NC_nue100k",
                "threshold": 3.4,
                "filename": "MARLEY_TMS_{E:.5f}_NC_nue_Fe56_MeV.root",
                "ES": False,
                "weight": 1,
            },

            "nc_nuebar_Fe56": {
                "folder": "MARLEY_NC_nue100k",
                "threshold": 3.4,
                "filename": "MARLEY_TMS_{E:.5f}_NC_nue_Fe56_MeV.root",
                "ES": False,
                "weight": 1,
            },

            "nc_numu_Fe56": {
                "folder": "MARLEY_NC_nue100k",
                "threshold": 3.4,
                "filename": "MARLEY_TMS_{E:.5f}_NC_nue_Fe56_MeV.root",
                "ES": False,
                "weight": 1,
            },

            "nc_numubar_Fe56": {
                "folder": "MARLEY_NC_nue100k",
                "threshold": 3.4,
                "filename": "MARLEY_TMS_{E:.5f}_NC_nue_Fe56_MeV.root",
                "ES": False,
                "weight": 1,
            },

            "nc_nutau_Fe56": {
                "folder": "MARLEY_NC_nue100k",
                "threshold": 3.4,
                "filename": "MARLEY_TMS_{E:.5f}_NC_nue_Fe56_MeV.root",
                "ES": False,
                "weight": 1,
            },

            "nc_nutaubar_Fe56": {
                "folder": "MARLEY_NC_nue100k",
                "threshold": 3.4,
                "filename": "MARLEY_TMS_{E:.5f}_NC_nue_Fe56_MeV.root",
                "ES": False,
                "weight": 1,
            },

            "nue_e": {
                "folder": "G4_ES_Fe56_data",
                "threshold": 0.5,
                "filename": "TMS_{E:.5f}_ES_Fe56_MeV.root",
                "ES": True,
                "weight": 26,
                "G4_channel": "ESiron",
            },

            "nuebar_e": {
                "folder": "G4_ES_Fe56_data",
                "threshold": 0.5,
                "filename": "TMS_{E:.5f}_ES_Fe56_MeV.root",
                "ES": True,
                "weight": 26,
                "G4_channel": "ESiron",
            },

            "numu_e": {
                "folder": "G4_ES_Fe56_data",
                "threshold": 0.5,
                "filename": "TMS_{E:.5f}_ES_Fe56_MeV.root",
                "ES": True,
                "weight": 26,
                "G4_channel": "ESiron",
            },

            "numubar_e": {
                "folder": "G4_ES_Fe56_data",
                "threshold": 0.5,
                "filename": "TMS_{E:.5f}_ES_Fe56_MeV.root",
                "ES": True,
                "weight": 26,
                "G4_channel": "ESiron",
            },

            "nutau_e": {
                "folder": "G4_ES_Fe56_data",
                "threshold": 0.5,
                "filename": "TMS_{E:.5f}_ES_Fe56_MeV.root",
                "ES": True,
                "weight": 26,
                "G4_channel": "ESiron",
            },

            "nutaubar_e": {
                "folder": "G4_ES_Fe56_data",
                "threshold": 0.5,
                "filename": "TMS_{E:.5f}_ES_Fe56_MeV.root",
                "ES": True,
                "weight": 26,
                "G4_channel": "ESiron",
            },
        },
    },


    "TMS_scint": {

        "material": "scint",

        "channels": {

            "ibd": {
                "folder": "G4_IBD_scint_data",
                "threshold": 1.806,
                "filename": "TMS_{E:.5f}_IBD_scint_MeV.root",
                "ES": False,
                "weight": 1,
                "G4_channel": "IBD",
            },


            "nue_e": {
                "folder": "G4_ES_scint_data",
                "threshold": 0.5,
                "filename": "TMS_{E:.5f}_ES_scint_MeV.root",
                "ES": True,
                "weight": 4,
                "G4_channel": "ESscint",
            },

            "nuebar_e": {
                "folder": "G4_ES_scint_data",
                "threshold": 0.5,
                "filename": "TMS_{E:.5f}_ES_scint_MeV.root",
                "ES": True,
                "weight": 4,
                "G4_channel": "ESscint",
            },

            "numu_e": {
                "folder": "G4_ES_scint_data",
                "threshold": 0.5,
                "filename": "TMS_{E:.5f}_ES_scint_MeV.root",
                "ES": True,
                "weight": 4,
                "G4_channel": "ESscint",
            },

            "numubar_e": {
                "folder": "G4_ES_scint_data",
                "threshold": 0.5,
                "filename": "TMS_{E:.5f}_ES_scint_MeV.root",
                "ES": True,
                "weight": 4,
                "G4_channel": "ESscint",
            },

            "nutau_e": {
                "folder": "G4_ES_scint_data",
                "threshold": 0.5,
                "filename": "TMS_{E:.5f}_ES_scint_MeV.root",
                "ES": True,
                "weight": 4,
                "G4_channel": "ESscint",
            },

            "nutaubar_e": {
                "folder": "G4_ES_scint_data",
                "threshold": 0.5,
                "filename": "TMS_{E:.5f}_ES_scint_MeV.root",
                "ES": True,
                "weight": 4,
                "G4_channel": "ESscint",
            },


            "nc_nue_C12": {
                "folder": "G4_NC_scint",
                "threshold": 15.1,
                "filename": "TMS_{E:.5f}_Scint_MeV.root",
                "ES": False,
                "weight": 0.4945,
                "G4_channel": "ScintNC",
            },

            "nc_nuebar_C12": {
                "folder": "G4_NC_scint",
                "threshold": 15.1,
                "filename": "TMS_{E:.5f}_Scint_MeV.root",
                "ES": False,
                "weight": 0.4945,
                "G4_channel": "ScintNC",
            },

            "nc_numu_C12": {
                "folder": "G4_NC_scint",
                "threshold": 15.1,
                "filename": "TMS_{E:.5f}_Scint_MeV.root",
                "ES": False,
                "weight": 0.4945,
                "G4_channel": "ScintNC",
            },

            "nc_numubar_C12": {
                "folder": "G4_NC_scint",
                "threshold": 15.1,
                "filename": "TMS_{E:.5f}_Scint_MeV.root",
                "ES": False,
                "weight": 0.4945,
                "G4_channel": "ScintNC",
            },

            "nc_nutau_C12": {
                "folder": "G4_NC_scint",
                "threshold": 15.1,
                "filename": "TMS_{E:.5f}_Scint_MeV.root",
                "ES": False,
                "weight": 0.4945,
                "G4_channel": "ScintNC",
            },

            "nc_nutaubar_C12": {
                "folder": "G4_NC_scint",
                "threshold": 15.1,
                "filename": "TMS_{E:.5f}_Scint_MeV.root",
                "ES": False,
                "weight": 0.4945,
                "G4_channel": "ScintNC",
            },
        },
    },
}


argon_channels = {
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


scint_channels = {
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

lead_channels = {
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

iron_channels = {
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

# Collection of all detector interaction channels
# For majority no realistic detector response was developed
# see DETECTOR_CONFIG for all channels with detector response simulation
# For every channel the snowglobes channel weight is added
# From snowglobes, only unweighted files are used (weighting does not 100% work right now)
# The weighting is done in an extra step in Python with the help of the following dictionary

ALL_DETECTOR = {
    "NDLAr": {"material": "argon", "channels" : argon_channels},
    "ECAL_lead":  {"material": "lead", "channels" : lead_channels},
    "ECAL_scint":  {"material": "scint", "channels" : scint_channels},
    "TMS_iron":  {"material": "iron", "channels" : iron_channels},
    "TMS_scint":  {"material": "scint", "channels" : scint_channels},
    "STT":  {"material": "scint", "channels" : scint_channels},
    "GRAIN":  {"material": "argon", "channels" : argon_channels},
}