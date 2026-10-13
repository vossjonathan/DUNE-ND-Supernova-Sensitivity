# DUNE Near Detector Supernova Sensitivity Study

This repository contains the simulation and analysis code developed during a research internship at Duke University to investigate the sensitivity of the DUNE near detector complex to neutrinos from a Galactic core-collapse supernova, with particular emphasis on The Muon Spectrometer (TMS).

## Overview

The study combines three simulation tools:

- **SNOwGLoBES:** Calculation of supernova neutrino interaction rates for the near detector components.
- **MARLEY:** Generation of low-energy neutrino interaction final states.
- **Geant4:** Simulation of a simplified TMS detector geometry to obtain detector response matrices and estimate cosmic-muon backgrounds, using EcoMug for cosmic-muon generation.

The resulting detector response matrices are incorporated into SNOwGLoBES to estimate observable supernova neutrino signals.

## Main Results

For a supernova at 10 kpc, the study predicts approximately 10.5 TMS events using the Garching flux model and 52.3 events using the Livermore model.

Applying simplified energy-deposition and track-length cuts yields approximately 8.3 signal events and 17.8 cosmic-muon background events for the Garching model.

These results represent first-order estimates based on simplified detector and background models.

## Repository Structure

- `Geant4/` TMS detector simulation and event generation (C++)
- `MARLEY/` Neutrino interaction configurations and reaction files
- `SNOwGLoBES/` Detector configurations, cross sections, and smearing matrices
- `analysis/` Python analysis and visualization
- `figures/` Selected simulation results and plots
- `data/` Root data for smearing matrices etc.

The repository contains the project-specific code, configurations, and results. The original simulations were performed using separate local installations of Geant4, MARLEY, and SNOwGLoBES. The corresponding directories in this repository contain the relevant project files, not complete installations of these software packages.

## Compiling the Geant4 Simulation

The Geant4 model requires external installations of Geant4, MARLEY, and HepMC3, along with CMake and a C++17-compatible compiler.

Running the simulations additionally requires selecting the appropriate event generator, MARLEY configuration, and simulation macros. The SNOwGLoBES calculations and Python analyses are performed separately.
## MARLEY Reaction Data

The MARLEY reaction files for charged current and neutral current electron-neutrino interactions on 56Fe and were created by Sam Hedges. The corresponding file is not redistributed in this repository.

The charged-current electron-antineutrino reaction file (`vebar56FeCC_Scott2014.react`) was prepared as part of this project based on experimental data from Scott et al. (2014).

