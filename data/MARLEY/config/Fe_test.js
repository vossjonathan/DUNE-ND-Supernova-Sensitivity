// Use this example job configuration file as a starting point for your own
// files.
{
  seed: 123456, // Random number seed (omit to use time since Unix epoch)

  // Pure 208Pb target
  target: {
    nuclides: [ 1000260560 ],
    atom_fractions: [ 1.0 ],
  },
  

  // Simulate ve scattering on 40Ar:
  reactions: [
    // Charged-current interactions on the nucleus using the
    // recommended MARLEY v2 cross-section models for both
    // continuum (HF-CRPA) and discrete (Bhattacharya2009)
    // nuclear transitions
    "data/react/ve56FeCC_Rapaport1983.react",
  ],

  // Neutrino source specification
  source: {
    type: "monoenergetic",
    neutrino: "ve",      // The source produces electron neutrinos
    energy: 40,             // Minimum neutrino energy (MeV)           // Pinching parameter (dimensionless, default 0)
  },

  // Incident neutrino direction 3-vector
  direction: { x: 0.0, y: 0.0, z: 1.0 },

  // Settings for the "marley generate" command
  generate: {

    // The number of events to generate
    events: 100,

    // Event output configuration
    //output: [ { file: "out/Fe_40MeV.root", format: "root", mode: "overwrite" } ],
    output: [ { file: "events.hepmc3", format: "ascii", mode: "overwrite" } ],
  },
  xsec: {
    KEmin: 0,
    KEmax: 100,
    steps: 1001,
    pdg: 12,
  },
}
