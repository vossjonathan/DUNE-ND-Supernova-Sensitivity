/// @file
/// @copyright Copyright (C) 2016-2026 Steven Gardiner
/// @license GNU General Public License, version 3
//
// This file is part of MARLEY (Model of Argon Reaction Low Energy Yields)
//
// MARLEY is free software: you can redistribute it and/or modify it under the
// terms of version 3 of the GNU General Public License as published by the
// Free Software Foundation.
//
// For the full text of the license please see COPYING or
// visit http://opensource.org/licenses/GPL-3.0
//
// Please respect the MCnet academic usage guidelines. See GUIDELINES
// or visit https://www.montecarlonet.org/GUIDELINES for details.

// Standard library includes
#include <iostream>
#include <array>
#include <cmath>

// Geant4 includes
#include "G4Event.hh"
#include "G4ParticleTable.hh"
#include "G4ParticleDefinition.hh"
#include "G4PhysicalConstants.hh"
#include "G4PrimaryParticle.hh"
#include "G4PrimaryVertex.hh"
#include "G4SystemOfUnits.hh"
#include "G4ThreeVector.hh"
#include "Randomize.hh"
//#include "globals.hh"

// MARLEY includes
#include "marley/Error.hh"
#include "marley/JSONConfig.hh"
#include "marley/hepmc3_utils.hh"

// HepMC3 includes
#include "HepMC3/GenEvent.h"
#include "HepMC3/GenParticle.h"

// marg4 includes
#include "MarleyPrimaryGeneratorAction.hh"


namespace B4
{


MarleyPrimaryGeneratorAction::MarleyPrimaryGeneratorAction(
  const std::string& config_file_name) : G4VUserPrimaryGeneratorAction()
{
  // Create a new marley::Generator object using the settings from the
  // configuration file.
  
fEnu = 40.0 * MeV;
fMessenger = std::make_unique<G4GenericMessenger>(this,"/marley/","MARLEY primary generator control");

fMessenger->DeclarePropertyWithUnit("nuEnergy","MeV",fEnu,"Set the incoming neutrino energy.");
  marley::JSONConfig config( config_file_name );

  marley_generator_= config.create_generator();
}

void MarleyPrimaryGeneratorAction::GeneratePrimaries(G4Event* anEvent)
{
  // Create a new primary vertex at the spacetime origin.
  G4ThreeVector position = SampleFePosition();
  G4PrimaryVertex* vertex = new G4PrimaryVertex(position.x(), position.y(), position.z(), 0.); // x,y,z,t0

  // Generate a new MARLEY event using the owned marley::Generator object
   // MeV
  std::array<double, 3> nuDir = SampleIsotropicDirection();
  


  auto ev = marley_generator_.create_event(-12,fEnu / MeV,1000260560,nuDir);

  // Account for possibly different systems of units for the particle
  // 4-momenta by using this conversion factor
  auto mom4_conv_factor = MeV;

  // Query the event to determine what it uses for energy/momentum units
  auto ev_energy_unit = ev->momentum_unit();
  if ( ev_energy_unit == HepMC3::Units::GEV ) {
    mom4_conv_factor = GeV;
  }
  else if ( ev_energy_unit != HepMC3::Units::MEV ) {
    throw marley::Error( "Unrecognized momentum unit encountered in"
      " MarleyPrimaryGeneratorAction::GeneratePrimaries()" );
  }

  // Collect the final-state particles from the HepMC3 event
  auto finals = marley_hepmc3::get_particles_with_status(
    marley_hepmc3::NUHEPMC_FINAL_STATE_STATUS, *ev);

  // Loop over each of the final particles in the MARLEY event
  for ( const auto& fp : finals ) {

    // Access the 4-momentum from the HepMC3 particle
    const auto& mom = fp->momentum();

    // Convert each one from a HepMC3::GenParticle into a G4PrimaryParticle.
    // Do this by first setting the PDG code and the 4-momentum components.
    G4PrimaryParticle* particle;
    if (fp->pid() > 1000000000) {
    particle = new G4PrimaryParticle(
        fp->pid(),
        mom.px() * mom4_conv_factor,
        mom.py() * mom4_conv_factor,
        mom.pz() * mom4_conv_factor
    );
    }
    else{
      particle = new G4PrimaryParticle( fp->pid(),
      mom.px() * mom4_conv_factor,
      mom.py() * mom4_conv_factor,
      mom.pz() * mom4_conv_factor,
      mom.e() * mom4_conv_factor );
    }


    // Also set the charge of the G4PrimaryParticle appropriately.
    // Use the MARLEY utility function that checks for a stored charge
    // attribute before falling back to a PDG-code-based lookup.
    particle->SetCharge( marley_hepmc3::get_particle_charge( *fp ) );

    // Add the fully-initialized G4PrimaryParticle to the primary vertex
    vertex->SetPrimary( particle );
  }

  // The primary vertex has been fully populated with all final-state particles
  // from the MARLEY event. Add it to the G4Event object so that Geant4 can
  // begin tracking the particles through the simulated geometry.
  anEvent->AddPrimaryVertex( vertex );
}
G4ThreeVector MarleyPrimaryGeneratorAction::SampleFePosition()
{
  auto fNironThin = 34;
  auto fNironMiddle = 22;
  auto fNironThick = 24;

  auto ironThin = 15 * mm;
  auto ironMiddle = 40 * mm;
  auto ironThick = 80 * mm;
  auto scintThickness = 16 * mm;
  auto airThickness = 17* mm; 

  auto totalLengthIronThin = fNironThin * ironThin; //total length of thin iron plates added up
  auto totalLengthIronMiddle = fNironMiddle * ironMiddle;
  auto totalLengthIronThick = fNironThick * ironThick;

  auto oneThinModule = ironThin + airThickness + scintThickness + airThickness;
  auto oneMiddleModule = ironMiddle + airThickness + scintThickness + airThickness;  
  auto oneThickModule = ironThick + airThickness + scintThickness + airThickness;


  auto totalLengthThin = fNironThin * oneThinModule; //total length of thin iron plates including the scint plates between the iron
  auto totalLengthMiddle = fNironMiddle * oneMiddleModule;
  auto totalLengthThick = fNironThick * oneThickModule;
  auto totalDetectorLength = totalLengthThin + totalLengthMiddle + totalLengthThick;

  auto totalLengthIron = totalLengthIronThin + totalLengthIronMiddle + totalLengthIronThick; //total iron length without scint

  auto probSpawnThin = totalLengthIronThin / totalLengthIron; //probability that electron spawns in any thin iron plate
  auto probSpawnMiddle = totalLengthIronMiddle / totalLengthIron;
  auto probSpawnThick = totalLengthIronThick / totalLengthIron;


  G4double random = G4UniformRand(); //get random number between 0 and 1
  G4int indexSpawnPlate; //index of plate where the electron will spawn inside of

  if (random < probSpawnThin) //electron will be spawned in one of the thin iron plates
  {
    indexSpawnPlate = static_cast<G4int>((fNironThin) * G4UniformRand()); //get random index of a thin iron plate to spawn the electron 0 <= i <= 33
  }
  else if ((random >= probSpawnThin) && (random < probSpawnThin + probSpawnMiddle))
  {
    indexSpawnPlate = fNironThin + static_cast<G4int>((fNironMiddle) * G4UniformRand()); //get random index of a middle iron plate 34 <= i <= 55
  }
  else
  {
    indexSpawnPlate = fNironThin + fNironMiddle + static_cast<G4int>((fNironThick) * G4UniformRand()); //get random index of a thick iron plate 56 <= i <= 79
  }

  G4double zpos;
  G4double xpos = (G4UniformRand() - 0.5) * 7000*mm;
  G4double ypos = (G4UniformRand() - 0.5) * 3200*mm;


  if (indexSpawnPlate < 34)
  {
    G4double random_inside = G4UniformRand() * ironThin;
    zpos = -totalDetectorLength / 2 + indexSpawnPlate*oneThinModule + random_inside;
  }
  else if (indexSpawnPlate < 56)
  {
    G4double random_inside = G4UniformRand() * ironMiddle;
    zpos = -totalDetectorLength / 2 + totalLengthThin + (indexSpawnPlate - fNironThin)*oneMiddleModule+ random_inside;
  }
  else
  {
    G4double random_inside = G4UniformRand() * ironThick;
    zpos = -totalDetectorLength / 2 + totalLengthThin + totalLengthMiddle + (indexSpawnPlate - fNironThin - fNironMiddle)*oneThickModule + random_inside;
  }
  return G4ThreeVector(xpos, ypos, zpos);
}
std::array<double, 3> MarleyPrimaryGeneratorAction::SampleIsotropicDirection()
{
  double u = G4UniformRand();
  double v = G4UniformRand();

  double phi = 2*pi*u;
  double cos_theta = 2*v - 1;
  double sin_theta = std::sqrt(1 - cos_theta * cos_theta);

  double x = sin_theta * std::cos(phi);
  double y = sin_theta * std::sin(phi);
  double z = cos_theta;
  std::array<double, 3> nuDir = {x, y, z};
  return nuDir;
}

}