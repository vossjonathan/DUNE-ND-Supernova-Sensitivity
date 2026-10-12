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
/// \file DetectorConstruction.cc
/// \brief Implementation of the B4c::DetectorConstruction class

#include "DetectorConstruction.hh"

#include "CalorimeterSD.hh"

#include "G4AutoDelete.hh"
#include "G4Box.hh"
#include "G4Colour.hh"
#include "G4GlobalMagFieldMessenger.hh"
#include "G4LogicalVolume.hh"
#include "G4Material.hh"
#include "G4NistManager.hh"
#include "G4PVPlacement.hh"
#include "G4PVReplica.hh"
#include "G4PhysicalConstants.hh"
#include "G4SDManager.hh"
#include "G4SystemOfUnits.hh"
#include "G4VisAttributes.hh"

namespace B4c
{

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

G4ThreadLocal G4GlobalMagFieldMessenger* DetectorConstruction::fMagFieldMessenger = nullptr;

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

G4VPhysicalVolume* DetectorConstruction::Construct()
{
  // Define materials
  DefineMaterials();
  

  // Define volumes
  return DefineVolumes();
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

void DetectorConstruction::DefineMaterials()
{
  // Lead material defined using NIST Manager
  auto nistManager = G4NistManager::Instance();
  nistManager->FindOrBuildMaterial("G4_Fe");
  nistManager->FindOrBuildMaterial("G4_PLASTIC_SC_VINYLTOLUENE");
  nistManager->FindOrBuildMaterial("G4_AIR");

  // Vacuum
  G4double z;
  G4double a;
  G4double density;
  new G4Material("Galactic", z = 1., a = 1.01 * g / mole, density = universe_mean_density,
                 kStateGas, 2.73 * kelvin, 3.e-18 * pascal);

  // Print materials
  G4cout << *(G4Material::GetMaterialTable()) << G4endl;
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

G4VPhysicalVolume* DetectorConstruction::DefineVolumes()
{
  // Geometry parameters
  //fNofLayers = 10;
  fNironthin = 34;
  fNironmiddle = 22;
  fNironthick = 24;
  G4double ironThin = 15. * mm;
  G4double ironMiddle = 40. *mm;
  G4double ironThick = 80. *mm;
  //G4double absoThickness = 10. * mm;
  G4double scintThickness = 16. * mm;
  G4double airThickness = 17. *mm;
  G4double calorSizeX = 7000. * mm;
  G4double calorSizeY = 3200. * mm;

  auto layerThicknessThin = ironThin + scintThickness + 2 * airThickness; //Fe (15mm) | Air (17mm) | Scint (16mm)| Air (17mm) ...
  auto layerThicknessMiddle = ironMiddle + scintThickness + 2 * airThickness;
  auto layerThicknessThick = ironThick + scintThickness + 2 * airThickness;


  auto calorThicknessThin = fNironthin * layerThicknessThin; //whole block of thin iron plates
  auto calorThicknessMiddle = fNironmiddle * layerThicknessMiddle;
  auto calorThicknessThick = fNironthick * layerThicknessThick;
  auto totalCalorThickness = calorThicknessThin + calorThicknessMiddle + calorThicknessThick;

  auto worldSizeX = 1.2 * calorSizeX;
  auto worldSizeY = 1.2 * calorSizeY;
  auto worldSizeZ = 1.2 * (calorThicknessThin + calorThicknessMiddle + calorThicknessThick);

  // Get materials
  auto defaultMaterial = G4Material::GetMaterial("Galactic");
  auto ironMaterial = G4Material::GetMaterial("G4_Fe");
  auto scintMaterial = G4Material::GetMaterial("G4_PLASTIC_SC_VINYLTOLUENE");
  auto airMaterial = G4Material::GetMaterial("G4_AIR");

  if (!defaultMaterial || !ironMaterial || !scintMaterial || !airMaterial)  {
    G4ExceptionDescription msg;
    msg << "Cannot retrieve materials already defined.";
    G4Exception("DetectorConstruction::DefineVolumes()", "MyCode0001", FatalException, msg);
  }

  //
  // World
  //
  auto worldS = new G4Box("World",  // its name
                          worldSizeX / 2, worldSizeY / 2, worldSizeZ / 2);  // its size

  auto worldLV = new G4LogicalVolume(worldS,  // its solid
                                     defaultMaterial,  // its material
                                     "World");  // its name

  auto worldPV = new G4PVPlacement(nullptr,  // no rotation
                                   G4ThreeVector(),  // at (0,0,0)
                                   worldLV,  // its logical volume
                                   "World",  // its name
                                   nullptr,  // its mother  volume
                                   false,  // no boolean operation
                                   0,  // copy number
                                   fCheckOverlaps);  // checking overlaps

  //
  // Calorimeter
  //
  auto calorimeterS = new G4Box("TMS",  // its name
                                calorSizeX / 2, calorSizeY / 2, (calorThicknessThin + calorThicknessMiddle + calorThicknessThick) / 2);  // its size

  auto calorLV = new G4LogicalVolume(calorimeterS,  // its solid
                                     defaultMaterial,  // its material
                                     "TMS");  // its name

  new G4PVPlacement(nullptr,  // no rotation
                    G4ThreeVector(),  // at (0,0,0)
                    calorLV,  // its logical volume
                    "TMS",  // its name
                    worldLV,  // its mother  volume
                    false,  // no boolean operation
                    0,  // copy number
                    fCheckOverlaps);  // checking overlaps

  //
  // Layer
  //

  auto ironThinS = new G4Box("ironThin", calorSizeX / 2, calorSizeY /2, ironThin / 2);
  auto ironMiddleS = new G4Box("ironMiddle", calorSizeX / 2, calorSizeY /2, ironMiddle / 2);
  auto ironThickS = new G4Box("ironThick", calorSizeX / 2, calorSizeY /2, ironThick / 2);
  auto scintS = new G4Box("scint", calorSizeX / 2, calorSizeY /2 , scintThickness / 2 );
  auto airS = new G4Box("air", calorSizeX / 2, calorSizeY / 2, airThickness / 2);

  auto ironThinLV = new G4LogicalVolume(ironThinS, ironMaterial, "ironThin");
  auto ironMiddleLV = new G4LogicalVolume(ironMiddleS, ironMaterial, "ironMiddle");
  auto ironThickLV = new G4LogicalVolume(ironThickS, ironMaterial, "ironThick");
  auto scintLV = new G4LogicalVolume(scintS, scintMaterial, "scint");
  auto airLV = new G4LogicalVolume(airS, airMaterial, "air");

  //auto ironVis = new G4VisAttributes(G4Colour::Red());
  //ironVis->SetForceSolid(true);

  //auto scintVis = new G4VisAttributes(G4Colour::Blue());
  //scintVis->SetForceSolid(true);

  ironThinLV->SetVisAttributes(G4VisAttributes(G4Color::Red()));
  ironMiddleLV->SetVisAttributes(G4VisAttributes(G4Color::Red()));
  ironThickLV->SetVisAttributes(G4VisAttributes(G4Color::Red()));
  //scintLV->SetVisAttributes(G4VisAttributes(G4Colour::Blue())); 
  //airLV->SetVisAttributes(G4VisAttributes(G4Colour::Green())); 

  auto zStartDetector = -totalCalorThickness / 2;

  //placing thin iron plates

  for(int i = 0; i < fNironthin; i++)
  {
    auto zIron = zStartDetector + i*layerThicknessThin + ironThin / 2;
    auto zAirFront = zStartDetector + i*layerThicknessThin + ironThin + airThickness / 2;
    auto zScint = zStartDetector + i*layerThicknessThin + ironThin + airThickness + scintThickness / 2;
    auto zAirBack = zStartDetector + i*layerThicknessThin + ironThin + airThickness + scintThickness + airThickness / 2;

    new G4PVPlacement(nullptr, G4ThreeVector(0., 0., zIron), ironThinLV,"ironThin", calorLV, false, i, fCheckOverlaps);
    new G4PVPlacement(nullptr, G4ThreeVector(0., 0., zAirFront), airLV, "air", calorLV, false, 2*i + 1, fCheckOverlaps);
    new G4PVPlacement(nullptr, G4ThreeVector(0., 0., zScint), scintLV, "scint", calorLV, false, i, fCheckOverlaps);
    new G4PVPlacement(nullptr, G4ThreeVector(0., 0., zAirBack), airLV, "air", calorLV, false, 2*i + 2, fCheckOverlaps);
  }
  //Placing middle iron plates

  for(int i = 0; i < fNironmiddle; i++)
  {
    auto zIron = zStartDetector + calorThicknessThin + i*layerThicknessMiddle + ironMiddle / 2;
    auto zAirFront = zStartDetector + calorThicknessThin + i*layerThicknessMiddle + ironMiddle + airThickness / 2;
    auto zScint = zStartDetector + calorThicknessThin + i*layerThicknessMiddle + ironMiddle + airThickness + scintThickness / 2;
    auto zAirBack = zStartDetector + calorThicknessThin + i*layerThicknessMiddle + ironMiddle + airThickness + scintThickness + airThickness / 2;

    new G4PVPlacement(nullptr, G4ThreeVector(0., 0., zIron), ironMiddleLV,"ironMiddle", calorLV, false, fNironthin + i, fCheckOverlaps);
    new G4PVPlacement(nullptr, G4ThreeVector(0., 0., zAirFront), airLV, "air", calorLV, false, 2*fNironthin + 2*i + 1, fCheckOverlaps);
    new G4PVPlacement(nullptr, G4ThreeVector(0., 0., zScint), scintLV, "scint", calorLV, false, fNironthin + i, fCheckOverlaps);
    new G4PVPlacement(nullptr, G4ThreeVector(0., 0., zAirBack), airLV, "air", calorLV, false, 2*fNironthin + 2*i + 2, fCheckOverlaps);
  }
  
  //Placing thick iron plates
  for(int i = 0; i < fNironthick; i++)
  {
    auto zIron = zStartDetector + calorThicknessThin + calorThicknessMiddle + i*layerThicknessThick + ironThick / 2;
    auto zAirFront = zStartDetector + calorThicknessThin + calorThicknessMiddle + i*layerThicknessThick + ironThick + airThickness / 2;
    auto zScint = zStartDetector + calorThicknessThin + calorThicknessMiddle + i*layerThicknessThick + ironThick + airThickness + scintThickness / 2;
    auto zAirBack = zStartDetector + calorThicknessThin + calorThicknessMiddle + i*layerThicknessThick + ironThick + airThickness + scintThickness + airThickness / 2;

    new G4PVPlacement(nullptr, G4ThreeVector(0., 0., zIron), ironThickLV,"ironThick", calorLV, false, fNironthin + fNironmiddle + i, fCheckOverlaps);
    new G4PVPlacement(nullptr, G4ThreeVector(0., 0., zAirFront), airLV, "air", calorLV, false, 2*fNironthin + 2*fNironmiddle + 2*i + 1, fCheckOverlaps);
    new G4PVPlacement(nullptr, G4ThreeVector(0., 0., zScint), scintLV, "scint", calorLV, false, fNironthin + fNironmiddle + i, fCheckOverlaps);
    new G4PVPlacement(nullptr, G4ThreeVector(0., 0., zAirBack), airLV, "air", calorLV, false, 2*fNironthin + 2*fNironmiddle + 2*i + 2, fCheckOverlaps);
  }

  //
  // Gap
  //
  // print parameters
  //
  G4cout << G4endl << "------------------------------------------------------------" << G4endl
         << "---> The calorimeter is " << fNironthin << " layers of: [ " << ironThin / mm
         << "mm of " << ironMaterial->GetName() << " + " << airThickness / mm << "mm of "
         << airMaterial->GetName() << " + " << scintThickness / mm << "mm of "
         << scintMaterial->GetName() << " + " << airThickness / mm << "mm of "
         << airMaterial->GetName() << "] " ", " << fNironmiddle << " layers of: [ " << ironMiddle / mm
         << "mm of " << ironMaterial->GetName() << " + " << airThickness / mm << "mm of "
         << airMaterial->GetName() << " + " << scintThickness / mm << "mm of "
         << scintMaterial->GetName() << " + " << airThickness / mm << "mm of "
         << airMaterial->GetName() << "] " ", " << fNironthick << " layers of: [ " << ironThick / mm
         << "mm of " << ironMaterial->GetName() << " + " << airThickness / mm << "mm of "
         << airMaterial->GetName() << " + " << scintThickness / mm << "mm of "
         << scintMaterial->GetName() << " + " << airThickness / mm << "mm of "
         << airMaterial->GetName() << "] " << G4endl
         << "------------------------------------------------------------" << G4endl;

  //
  // Visualization attributes
  //
  worldLV->SetVisAttributes(G4VisAttributes::GetInvisible());
  calorLV->SetVisAttributes(G4VisAttributes(G4Colour::White()));

  //
  // Always return the physical World
  //
  return worldPV;
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

void DetectorConstruction::ConstructSDandField()
{
  // G4SDManager::GetSDMpointer()->SetVerboseLevel(1);

  //
  // Sensitive detectors
  //
  /*auto ironThinSD = new CalorimeterSD("IronThinSD", "AbsorberHitsCollection", fNironthin);
  G4SDManager::GetSDMpointer()->AddNewDetector(ironThinSD);
  SetSensitiveDetector("ironThinLV", ironThinSD);
  
  auto ironMiddleSD = new CalorimeterSD("IronMiddleSD", "AbsorberHitsCollection", fNironmiddle);
  G4SDManager::GetSDMpointer()->AddNewDetector(ironMiddleSD);
  SetSensitiveDetector("ironMiddleLV", ironMiddleSD);
  
  auto ironThickSD = new CalorimeterSD("IronThickSD", "AbsorberHitsCollection", fNironthick);
  G4SDManager::GetSDMpointer()->AddNewDetector(ironThickSD);
  SetSensitiveDetector("ironThickLV", ironThickSD);*/

  auto scintSD = new CalorimeterSD("ScintSD", "ScintHitsCollection", fNironthin + fNironmiddle + fNironthick);
  G4SDManager::GetSDMpointer()->AddNewDetector(scintSD);
  SetSensitiveDetector("scint", scintSD);

  //
  // Magnetic field
  //
  // Create global magnetic field messenger.
  // Uniform magnetic field is then created automatically if
  // the field value is not zero.
  G4ThreeVector fieldValue;
  fMagFieldMessenger = new G4GlobalMagFieldMessenger(fieldValue);
  fMagFieldMessenger->SetVerboseLevel(1);

  // Register the field messenger for deleting
  G4AutoDelete::Register(fMagFieldMessenger);
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

}  // namespace B4c
