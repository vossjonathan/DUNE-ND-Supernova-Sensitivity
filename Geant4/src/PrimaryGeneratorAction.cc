//
// ********************************************************************
// * License and Disclaimer                                           *
// *                                                                  *
// * The  Geant4 software  is  copyright of the Copyright Holders  of *
// * the Geant4 Collaboration.  It is provided  under  the terms  and *
// * conditions of the Geant4 Software License,  included in the file *
// * LICENSE and available at  http://cern.ch/geant4/license .  These *
// * include a list of copyright holders.                             *
// *                                                                  *
// * Neither the authors of this software system, nor their employing *
// * institutes,nor the agencies providing financial support for this *
// * work  make  any representation or  warranty, express or implied, *
// * regarding  this  software system or assume any liability for its *
// * use.  Please see the license in the file  LICENSE  and URL above *
// * for the full disclaimer and the limitation of liability.         *
// *                                                                  *
// * This  code  implementation is the result of  the  scientific and *
// * technical work of the GEANT4 collaboration.                      *
// * By using,  copying,  modifying or  distributing the software (or *
// * any work based  on the software)  you  agree  to acknowledge its *
// * use  in  resulting  scientific  publications,  and indicate your *
// * acceptance of all terms of the Geant4 Software license.          *
// ********************************************************************
//
/// \file PrimaryGeneratorAction.cc
/// \brief Implementation of the B4::PrimaryGeneratorAction class

#include "PrimaryGeneratorAction.hh"

#include "G4Box.hh"
#include "G4LogicalVolume.hh"
#include "G4LogicalVolumeStore.hh"
#include "G4ParticleGun.hh"
#include "G4ParticleTable.hh"
#include "G4SystemOfUnits.hh"
#include "globals.hh"
#include "Randomize.hh"
#include "G4PhysicalConstants.hh"
#include <cmath>
#include <iostream>
#include "SimulationConfig.hh"
#include "G4GenericMessenger.hh"
#include "EcoMug.h"


namespace B4
{

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

PrimaryGeneratorAction::PrimaryGeneratorAction()
{
  fMessenger = new G4GenericMessenger(this,"/tms/","TMS generator controls");

  fMessenger->DeclarePropertyWithUnit("nuEnergy","MeV",nuEnergy,"Set true neutrino energy");
  fMessenger->DeclareProperty("channel", channel,"Set interaction channel");
  G4int nofParticles = 1;
  fParticleGun = new G4ParticleGun(nofParticles);

  
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

PrimaryGeneratorAction::~PrimaryGeneratorAction()
{
        
  G4cout << "\n===== Cosmic muon statistics =====" << G4endl;
  G4cout << "Total EcoMug trials: " << fNTrialsTotal << G4endl;
  delete fParticleGun;
  delete fMessenger;
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void PrimaryGeneratorAction::GenerateNueFe(G4Event* event)
{
  auto particle = G4ParticleTable::GetParticleTable()->FindParticle("e-");

  fParticleGun->SetParticleDefinition(particle);

  //source https://arxiv.org/pdf/1507.06872, page 6
  G4double Q = 4.56 * MeV;
  G4double energy = B4::nuEnergy - Q;
    G4cout << "E_nu = " << B4::nuEnergy / MeV
       << " MeV, E_e = " << energy / MeV
       << " MeV" << G4endl;

  fParticleGun->SetParticleEnergy(energy);
  fParticleGun->SetParticlePosition(SampleFePosition());
  fParticleGun->SetParticleMomentumDirection(SampleIsotropicDirection());

  fParticleGun->GeneratePrimaryVertex(event);
}

void PrimaryGeneratorAction::GenerateNuebarFe(G4Event* event)
{
  auto particle = G4ParticleTable::GetParticleTable()->FindParticle("e+");

  fParticleGun->SetParticleDefinition(particle);

  //source https://arxiv.org/pdf/1507.06872, page 6
  G4double Q = 4.71 * MeV;
  G4double energy = B4::nuEnergy - Q;
    G4cout << "E_nu = " << B4::nuEnergy / MeV
       << " MeV, E_e = " << energy / MeV
       << " MeV" << G4endl;

  fParticleGun->SetParticleEnergy(energy);
  fParticleGun->SetParticlePosition(SampleFePosition());
  fParticleGun->SetParticleMomentumDirection(SampleIsotropicDirection());

  fParticleGun->GeneratePrimaryVertex(event);
}

void PrimaryGeneratorAction::GenerateIBD(G4Event* event)
{
  auto particle = G4ParticleTable::GetParticleTable()->FindParticle("e+");

  fParticleGun->SetParticleDefinition(particle);

  //source https://journals.aps.org/prd/pdf/10.1103/PhysRevD.60.053003, page 9
  G4double Q = 1.804 * MeV;
  G4double energy = B4::nuEnergy - Q;
    G4cout << "E_nu = " << B4::nuEnergy / MeV
       << " MeV, E_e = " << energy / MeV
       << " MeV" << G4endl;

  fParticleGun->SetParticleEnergy(energy);
  fParticleGun->SetParticlePosition(SampleScintPosition());
  fParticleGun->SetParticleMomentumDirection(SampleIsotropicDirection());

  fParticleGun->GeneratePrimaryVertex(event);
}

void PrimaryGeneratorAction::GenerateESiron(G4Event* event)
{
  auto particle = G4ParticleTable::GetParticleTable()->FindParticle("e-");

  fParticleGun->SetParticleDefinition(particle);

  G4double energy = B4::nuEnergy; // no shift for ES
    //G4cout  << "E_e = " << energy / MeV << " MeV" << G4endl;

  fParticleGun->SetParticleEnergy(energy);
  fParticleGun->SetParticlePosition(SampleFePosition());
  fParticleGun->SetParticleMomentumDirection(SampleIsotropicDirection());

  fParticleGun->GeneratePrimaryVertex(event);
}

void PrimaryGeneratorAction::GenerateESscint(G4Event* event)
{
  auto particle = G4ParticleTable::GetParticleTable()->FindParticle("e-");

  fParticleGun->SetParticleDefinition(particle);

  G4double energy = B4::nuEnergy; // no shift for ES
    //G4cout  << "E_e = " << energy / MeV << " MeV" << G4endl;

  fParticleGun->SetParticleEnergy(energy);
  fParticleGun->SetParticlePosition(SampleScintPosition());
  fParticleGun->SetParticleMomentumDirection(SampleIsotropicDirection());

  fParticleGun->GeneratePrimaryVertex(event);
}

void PrimaryGeneratorAction::GenerateCosmicMu(G4Event* event)
{
    EcoMug gen;

    gen.SetUseSky();

    // EcoMug coordinates:
    // x, y = horizontal plane
    // z = vertical
    gen.SetSkySize({{7.0, 7.31}});
    gen.SetSkyCenterPosition({{0.0, 0.0, 1.8}});
    gen.SetMinimumMomentum(38.11); // GeV/c
    const double mass_mu = 0.1056583755; // GeV/c^2

    double p;
    double theta;
    double E_kin_surf;
    double energy_loss;

    // Generate until the muon has enough energy
    // to reach the ND through the rock
    do
    {   
        fNTrialsTotal++;
        gen.Generate();

        p = gen.GetGenerationMomentum();
        theta = gen.GetGenerationTheta();

        E_kin_surf =
            std::sqrt(p * p + mass_mu * mass_mu) - mass_mu;

        double cos_zenith = std::abs(std::cos(theta));

        energy_loss = 36.2 / cos_zenith; // GeV

    } while (E_kin_surf <= energy_loss);


    auto pos = gen.GetGenerationPosition();
    double phi = gen.GetGenerationPhi();
    double charge = gen.GetCharge();

    double E_kin_ND = E_kin_surf - energy_loss;


    if (charge < 0)
    {
        auto particle = G4ParticleTable::GetParticleTable()->FindParticle("mu-");
        fParticleGun->SetParticleDefinition(particle);
    }
    else
    {
        auto particle = G4ParticleTable::GetParticleTable()->FindParticle("mu+");
        fParticleGun->SetParticleDefinition(particle);
    }

    fParticleGun->SetParticleEnergy(E_kin_ND * GeV);

    // EcoMug: z = vertical
    // TMS: y = vertical
    G4ThreeVector direction(std::sin(theta) * std::cos(phi),std::cos(theta),std::sin(theta) * std::sin(phi));

    fParticleGun->SetParticleMomentumDirection(direction);


    G4ThreeVector position(pos[0] * m,pos[2] * m,pos[1] * m);

    fParticleGun->SetParticlePosition(position);

    fParticleGun->GeneratePrimaryVertex(event);
}

G4ThreeVector PrimaryGeneratorAction::SampleFePosition()
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

void PrimaryGeneratorAction::GenerateScintNC(G4Event* event)
{
  auto particle = G4ParticleTable::GetParticleTable()->FindParticle("gamma");

  fParticleGun->SetParticleDefinition(particle);

  //source https://journals.aps.org/prd/pdf/10.1103/PhysRevD.108.043035
  G4double energy = 15.11 * MeV;

  fParticleGun->SetParticleEnergy(energy);
  fParticleGun->SetParticlePosition(SampleScintPosition());
  fParticleGun->SetParticleMomentumDirection(SampleIsotropicDirection());

  fParticleGun->GeneratePrimaryVertex(event);
}

G4ThreeVector PrimaryGeneratorAction::SampleScintPosition()
{
  auto fNironThin = 34;
  auto fNironMiddle = 22;
  auto fNironThick = 24;
  auto fNscint = 80;

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


  auto totalLengthThin = fNironThin * oneThinModule; //total length of thin iron plates including the scint plates and air between the iron
  auto totalLengthMiddle = fNironMiddle * oneMiddleModule;
  auto totalLengthThick = fNironThick * oneThickModule;
  auto totalDetectorLength = totalLengthThin + totalLengthMiddle + totalLengthThick;
  
  auto scintPlateId = static_cast<G4int>((fNscint) * G4UniformRand());
  

  G4double zpos;
  G4double xpos = (G4UniformRand() - 0.5) * 7000*mm;
  G4double ypos = (G4UniformRand() - 0.5) * 3200*mm;

  G4double random_inside = G4UniformRand() * scintThickness;

  if (scintPlateId < 34)
  {
  zpos = -totalDetectorLength / 2 + scintPlateId*oneThinModule + ironThin + airThickness + random_inside;
  }
  else if (scintPlateId < 56)
  {
    zpos = -totalDetectorLength / 2 + totalLengthThin + (scintPlateId - fNironThin)*oneMiddleModule + ironMiddle + airThickness + random_inside;
  }
  else
  {
    zpos = -totalDetectorLength / 2 + totalLengthThin + totalLengthMiddle + (scintPlateId - fNironThin - fNironMiddle)*oneThickModule + ironThick + airThickness + random_inside;
  }
  return G4ThreeVector(xpos, ypos, zpos);
}

G4ThreeVector PrimaryGeneratorAction::SampleIsotropicDirection()
{
  G4double u = G4UniformRand();
  G4double v = G4UniformRand();

  G4double phi = 2*pi*u;
  G4double cos_theta = 2*v - 1;
  G4double sin_theta = std::sqrt(1 - cos_theta * cos_theta);

  G4double x = sin_theta * std::cos(phi);
  G4double y = sin_theta * std::sin(phi);
  G4double z = cos_theta;
  return G4ThreeVector(x, y, z);
}


void PrimaryGeneratorAction::GeneratePrimaries(G4Event* event)
{
  // This function is called at the begining of event

  // In order to avoid dependence of PrimaryGeneratorAction
  // on DetectorConstruction class we get world volume
  // from G4LogicalVolumeStore
  //

 
  if (channel == "nue_Fe")
  {
    GenerateNueFe(event);
  }
  else if (channel == "nuebar_Fe")
  {
    GenerateNuebarFe(event);
  }
  else if (channel == "IBD")
  {
    GenerateIBD(event);
  }
  else if (channel == "ESiron")
  {
    GenerateESiron(event);
  }
  else if (channel == "ESscint")
  {
    GenerateESscint(event);
  }
  else if (channel == "ScintNC")
  {
    GenerateScintNC(event);
  }
  else if (channel == "CosmicMu")
  {
    GenerateCosmicMu(event);
  }
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

}  // namespace B4
