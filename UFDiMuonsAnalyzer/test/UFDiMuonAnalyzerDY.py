import FWCore.ParameterSet.Config as cms

process = cms.Process("UFDiMuonAnalyzer")

thisIsData = False

if thisIsData:
    print 'Running over data sample'
else:
    print 'Running over MC sample'

process.load("FWCore.MessageService.MessageLogger_cfi")
#process.MessageLogger.cerr.FwkReport.reportEvery = 1000
##process.MessageLogger.destinations.append("detailedInfo")
##process.MessageLogger.detailedInfo = cms.untracked.PSet(
##    threshold = cms.untracked.string("INFO"),
##    categories = cms.untracked.vstring("UFHLTTests")
##)

process.load("Configuration.StandardSequences.MagneticField_38T_cff")

## Geometry and Detector Conditions (needed for a few patTuple production steps)

process.load("Configuration.Geometry.GeometryIdeal_cff")

process.load('Configuration.EventContent.EventContent_cff')

process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
from Configuration.AlCa.autoCond import autoCond


# global tag
globalTag = "POSTLS170_V5"
print 'Loading Global Tag: '+globalTag
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.GlobalTag.globaltag = globalTag+"::All"


# ------------ PoolSource -------------
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
process.source = cms.Source("PoolSource",fileNames = cms.untracked.vstring())
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(False) )
process.source.lumisToProcess = cms.untracked.VLuminosityBlockRange()
# -------- PoolSource END -------------

#===============================================================================

# Clean the Jets from good muons, apply loose jet Id
ccMuPreSel = "pt > 15. && isGlobalMuon "
ccMuPreSel += " && globalTrack().normalizedChi2 < 10 "
ccMuPreSel += " && isPFMuon "
ccMuPreSel += " && innerTrack().hitPattern().trackerLayersWithMeasurement > 5 "
ccMuPreSel += " && innerTrack().hitPattern().numberOfValidPixelHits > 0 "
ccMuPreSel += " && globalTrack().hitPattern().numberOfValidMuonHits > 0 "
ccMuPreSel += " && numberOfMatchedStations > 1 && dB < 0.2 && abs(eta) < 2.4 "
ccMuPreSel += " && ( chargedHadronIso + max(0.,neutralHadronIso + photonIso - 0.5*puChargedHadronIso) ) < 0.12 * pt"

jetSelection = 'neutralEmEnergy/energy < 0.99 '
jetSelection += ' && neutralHadronEnergy/energy < 0.99 '
jetSelection += ' && (chargedMultiplicity + neutralMultiplicity) > 1 '
jetSelection += ' && ((abs(eta)>2.4) || (chargedMultiplicity > 0 '
jetSelection += ' && chargedHadronEnergy/energy > 0.0'
jetSelection += ' && chargedEmEnergy/energy < 0.99))'

process.cleanJets = cms.EDProducer("PATJetCleaner",
          src = cms.InputTag("slimmedJets"),
          preselection = cms.string(jetSelection),
          checkOverlaps = cms.PSet(
             muons = cms.PSet(
               src       = cms.InputTag("slimmedMuons"),
               algorithm = cms.string("byDeltaR"),
               preselection        = cms.string(ccMuPreSel),
               deltaR              = cms.double(0.5),
               checkRecoComponents = cms.bool(False),
               pairCut             = cms.string(""),
               requireNoOverlaps   = cms.bool(True),
             ),
             #electrons = cms.PSet(
             #  src       = cms.InputTag("slimmedElectrons"),
             #  algorithm = cms.string("byDeltaR"),
             #  preselection        = cms.string(ccElePreSel),
             #  deltaR              = cms.double(0.5),
             #  checkRecoComponents = cms.bool(False),
             #  pairCut             = cms.string(""),
             #  requireNoOverlaps   = cms.bool(True),
             #),
         ),
         finalCut = cms.string('')
)

#===============================================================================
# UFDiMuonAnalyzer

if thisIsData:
  process.load("UserArea.UFDiMuonsAnalyzer.UFDiMuonAnalyzer_cff")
else:
  process.load("UserArea.UFDiMuonsAnalyzer.UFDiMuonAnalyzer_MC_cff")

process.dimuons = process.DiMuons.clone()
process.dimuons.pfJetsTag = cms.InputTag("cleanJets")

#===============================================================================

process.p = cms.Path(#
                     process.cleanJets*
                     process.dimuons
                     )


#===============================================================================

# the max events to run over, -1 means all events
process.maxEvents.input = -1

process.source.fileNames.extend(
[
# put the input file names here
# prepend with "file:" if it is a normal file
# don't prepend anything if it is a file name from DAS
"file:/cms/data/store/mc/Spring14miniaod/DYJetsToLL_M-50_13TeV-madgraph-pythia8/MINIAODSIM/PU20bx25_POSTLS170_V5-v1/00000/029EA4C3-A007-E411-BE0B-D4AE529D9537.root",  
"file:/cms/data/store/mc/Spring14miniaod/DYJetsToLL_M-50_13TeV-madgraph-pythia8/MINIAODSIM/PU20bx25_POSTLS170_V5-v1/00000/2A0F865F-8F07-E411-BB92-0026181D28BB.root",
"file:/cms/data/store/mc/Spring14miniaod/DYJetsToLL_M-50_13TeV-madgraph-pythia8/MINIAODSIM/PU20bx25_POSTLS170_V5-v1/00000/6886FA67-8F07-E411-8DDA-001517FB2254.root",  
"file:/cms/data/store/mc/Spring14miniaod/DYJetsToLL_M-50_13TeV-madgraph-pythia8/MINIAODSIM/PU20bx25_POSTLS170_V5-v1/00000/BA8B865F-9607-E411-BB55-90B11C08AD1E.root",
"file:/cms/data/store/mc/Spring14miniaod/DYJetsToLL_M-50_13TeV-madgraph-pythia8/MINIAODSIM/PU20bx25_POSTLS170_V5-v1/00000/041B1709-A107-E411-BE7B-001E675A659A.root",  
"file:/cms/data/store/mc/Spring14miniaod/DYJetsToLL_M-50_13TeV-madgraph-pythia8/MINIAODSIM/PU20bx25_POSTLS170_V5-v1/00000/2E6FA03E-A007-E411-8A0D-D4AE52AAF583.root",  
"file:/cms/data/store/mc/Spring14miniaod/DYJetsToLL_M-50_13TeV-madgraph-pythia8/MINIAODSIM/PU20bx25_POSTLS170_V5-v1/00000/68C28598-A107-E411-8DF5-001E675A6AB8.root",  
"file:/cms/data/store/mc/Spring14miniaod/DYJetsToLL_M-50_13TeV-madgraph-pythia8/MINIAODSIM/PU20bx25_POSTLS170_V5-v1/00000/BC8E351A-A007-E411-B393-001E675A659A.root",
"file:/cms/data/store/mc/Spring14miniaod/DYJetsToLL_M-50_13TeV-madgraph-pythia8/MINIAODSIM/PU20bx25_POSTLS170_V5-v1/00000/061362C4-A007-E411-B6CF-001E67586629.root",  
"file:/cms/data/store/mc/Spring14miniaod/DYJetsToLL_M-50_13TeV-madgraph-pythia8/MINIAODSIM/PU20bx25_POSTLS170_V5-v1/00000/30D6147C-8F07-E411-B8E2-001517FB2250.root",  
"file:/cms/data/store/mc/Spring14miniaod/DYJetsToLL_M-50_13TeV-madgraph-pythia8/MINIAODSIM/PU20bx25_POSTLS170_V5-v1/00000/7254F076-8F07-E411-A2BC-001E675A5262.root",  
"file:/cms/data/store/mc/Spring14miniaod/DYJetsToLL_M-50_13TeV-madgraph-pythia8/MINIAODSIM/PU20bx25_POSTLS170_V5-v1/00000/C6B60720-A007-E411-AECA-90B11C04FAC6.root",
"file:/cms/data/store/mc/Spring14miniaod/DYJetsToLL_M-50_13TeV-madgraph-pythia8/MINIAODSIM/PU20bx25_POSTLS170_V5-v1/00000/088E0822-A207-E411-9941-90B11C1453E1.root",  
"file:/cms/data/store/mc/Spring14miniaod/DYJetsToLL_M-50_13TeV-madgraph-pythia8/MINIAODSIM/PU20bx25_POSTLS170_V5-v1/00000/36EC155D-A007-E411-86CD-001517F7F6A0.root",
"file:/cms/data/store/mc/Spring14miniaod/DYJetsToLL_M-50_13TeV-madgraph-pythia8/MINIAODSIM/PU20bx25_POSTLS170_V5-v1/00000/7290AD9D-A107-E411-866E-90B11C066D31.root",  
"file:/cms/data/store/mc/Spring14miniaod/DYJetsToLL_M-50_13TeV-madgraph-pythia8/MINIAODSIM/PU20bx25_POSTLS170_V5-v1/00000/C8BABFD0-A907-E411-945B-001517FB25E4.root",
"file:/cms/data/store/mc/Spring14miniaod/DYJetsToLL_M-50_13TeV-madgraph-pythia8/MINIAODSIM/PU20bx25_POSTLS170_V5-v1/00000/0A097C5B-9607-E411-A2A0-0026181D291E.root",  
"file:/cms/data/store/mc/Spring14miniaod/DYJetsToLL_M-50_13TeV-madgraph-pythia8/MINIAODSIM/PU20bx25_POSTLS170_V5-v1/00000/3A30AA02-A607-E411-993D-001E6758651B.root",  
"file:/cms/data/store/mc/Spring14miniaod/DYJetsToLL_M-50_13TeV-madgraph-pythia8/MINIAODSIM/PU20bx25_POSTLS170_V5-v1/00000/76399DCB-9F07-E411-ABE8-90B11C050371.root",  
"file:/cms/data/store/mc/Spring14miniaod/DYJetsToLL_M-50_13TeV-madgraph-pythia8/MINIAODSIM/PU20bx25_POSTLS170_V5-v1/00000/D00E79D7-A107-E411-B206-001E67586629.root",
"file:/cms/data/store/mc/Spring14miniaod/DYJetsToLL_M-50_13TeV-madgraph-pythia8/MINIAODSIM/PU20bx25_POSTLS170_V5-v1/00000/0C4273AF-A107-E411-9289-D4AE52AAF583.root",  
"file:/cms/data/store/mc/Spring14miniaod/DYJetsToLL_M-50_13TeV-madgraph-pythia8/MINIAODSIM/PU20bx25_POSTLS170_V5-v1/00000/3C8DEB33-A207-E411-B866-90B11C094A7E.root",
"file:/cms/data/store/mc/Spring14miniaod/DYJetsToLL_M-50_13TeV-madgraph-pythia8/MINIAODSIM/PU20bx25_POSTLS170_V5-v1/00000/800B0126-A107-E411-9A60-001517E74088.root",  
"file:/cms/data/store/mc/Spring14miniaod/DYJetsToLL_M-50_13TeV-madgraph-pythia8/MINIAODSIM/PU20bx25_POSTLS170_V5-v1/00000/D232D344-A007-E411-99FF-001517FB21BC.root",
"file:/cms/data/store/mc/Spring14miniaod/DYJetsToLL_M-50_13TeV-madgraph-pythia8/MINIAODSIM/PU20bx25_POSTLS170_V5-v1/00000/0CD3EB1A-A007-E411-B601-D4AE52AAF583.root",  
"file:/cms/data/store/mc/Spring14miniaod/DYJetsToLL_M-50_13TeV-madgraph-pythia8/MINIAODSIM/PU20bx25_POSTLS170_V5-v1/00000/3C977321-A007-E411-ABDF-90B11C066D31.root",  
"file:/cms/data/store/mc/Spring14miniaod/DYJetsToLL_M-50_13TeV-madgraph-pythia8/MINIAODSIM/PU20bx25_POSTLS170_V5-v1/00000/82AD85F2-A107-E411-A57F-001E675A6AB3.root",  
"file:/cms/data/store/mc/Spring14miniaod/DYJetsToLL_M-50_13TeV-madgraph-pythia8/MINIAODSIM/PU20bx25_POSTLS170_V5-v1/00000/D43B6191-A107-E411-9035-0026181D2917.root",
"file:/cms/data/store/mc/Spring14miniaod/DYJetsToLL_M-50_13TeV-madgraph-pythia8/MINIAODSIM/PU20bx25_POSTLS170_V5-v1/00000/104CA3E5-A007-E411-A18F-001517E74088.root",  
"file:/cms/data/store/mc/Spring14miniaod/DYJetsToLL_M-50_13TeV-madgraph-pythia8/MINIAODSIM/PU20bx25_POSTLS170_V5-v1/00000/4A9BB266-9607-E411-B543-001E675A6630.root",  
"file:/cms/data/store/mc/Spring14miniaod/DYJetsToLL_M-50_13TeV-madgraph-pythia8/MINIAODSIM/PU20bx25_POSTLS170_V5-v1/00000/8658020E-A107-E411-A780-90B11C070100.root",  
"file:/cms/data/store/mc/Spring14miniaod/DYJetsToLL_M-50_13TeV-madgraph-pythia8/MINIAODSIM/PU20bx25_POSTLS170_V5-v1/00000/D672AC6A-8F07-E411-B409-001E675A6928.root",
"file:/cms/data/store/mc/Spring14miniaod/DYJetsToLL_M-50_13TeV-madgraph-pythia8/MINIAODSIM/PU20bx25_POSTLS170_V5-v1/00000/10E1138B-9607-E411-9EBF-001517E73B9C.root",  
"file:/cms/data/store/mc/Spring14miniaod/DYJetsToLL_M-50_13TeV-madgraph-pythia8/MINIAODSIM/PU20bx25_POSTLS170_V5-v1/00000/4C10A1AF-A107-E411-8587-001E675A6C2A.root",  
"file:/cms/data/store/mc/Spring14miniaod/DYJetsToLL_M-50_13TeV-madgraph-pythia8/MINIAODSIM/PU20bx25_POSTLS170_V5-v1/00000/8864F22C-A207-E411-B568-001E67586629.root",  
"file:/cms/data/store/mc/Spring14miniaod/DYJetsToLL_M-50_13TeV-madgraph-pythia8/MINIAODSIM/PU20bx25_POSTLS170_V5-v1/00000/E0BAC66E-A107-E411-B95E-0026180A8746.root",
"file:/cms/data/store/mc/Spring14miniaod/DYJetsToLL_M-50_13TeV-madgraph-pythia8/MINIAODSIM/PU20bx25_POSTLS170_V5-v1/00000/1AF5235F-8F07-E411-9342-90B11C04FE0C.root",  
"file:/cms/data/store/mc/Spring14miniaod/DYJetsToLL_M-50_13TeV-madgraph-pythia8/MINIAODSIM/PU20bx25_POSTLS170_V5-v1/00000/52CDE7ED-9F07-E411-803C-001517F7F524.root",  
"file:/cms/data/store/mc/Spring14miniaod/DYJetsToLL_M-50_13TeV-madgraph-pythia8/MINIAODSIM/PU20bx25_POSTLS170_V5-v1/00000/90827F94-9607-E411-AD88-001517FB0F60.root",  
"file:/cms/data/store/mc/Spring14miniaod/DYJetsToLL_M-50_13TeV-madgraph-pythia8/MINIAODSIM/PU20bx25_POSTLS170_V5-v1/00000/E47E4E6F-A107-E411-B7F2-D4AE52AAF583.root",
"file:/cms/data/store/mc/Spring14miniaod/DYJetsToLL_M-50_13TeV-madgraph-pythia8/MINIAODSIM/PU20bx25_POSTLS170_V5-v1/00000/1AFA578D-A007-E411-BA93-90B11C06954E.root",  
"file:/cms/data/store/mc/Spring14miniaod/DYJetsToLL_M-50_13TeV-madgraph-pythia8/MINIAODSIM/PU20bx25_POSTLS170_V5-v1/00000/54F7A5B6-A107-E411-BF27-90B11C04FAC6.root",  
"file:/cms/data/store/mc/Spring14miniaod/DYJetsToLL_M-50_13TeV-madgraph-pythia8/MINIAODSIM/PU20bx25_POSTLS170_V5-v1/00000/A2063F20-A107-E411-8FD1-90B11C050371.root",  
"file:/cms/data/store/mc/Spring14miniaod/DYJetsToLL_M-50_13TeV-madgraph-pythia8/MINIAODSIM/PU20bx25_POSTLS170_V5-v1/00000/EA891D70-A207-E411-934E-001517FB21BC.root",
"file:/cms/data/store/mc/Spring14miniaod/DYJetsToLL_M-50_13TeV-madgraph-pythia8/MINIAODSIM/PU20bx25_POSTLS170_V5-v1/00000/1E2A638F-A007-E411-BA19-001E675A6AB3.root",  
"file:/cms/data/store/mc/Spring14miniaod/DYJetsToLL_M-50_13TeV-madgraph-pythia8/MINIAODSIM/PU20bx25_POSTLS170_V5-v1/00000/5C4B13EE-A007-E411-8803-001517FB0F60.root",  
"file:/cms/data/store/mc/Spring14miniaod/DYJetsToLL_M-50_13TeV-madgraph-pythia8/MINIAODSIM/PU20bx25_POSTLS170_V5-v1/00000/A22BD982-A207-E411-BED2-90B11C056AAD.root",  
"file:/cms/data/store/mc/Spring14miniaod/DYJetsToLL_M-50_13TeV-madgraph-pythia8/MINIAODSIM/PU20bx25_POSTLS170_V5-v1/00000/EE36FFE2-A107-E411-9C75-001E675A6928.root",
"file:/cms/data/store/mc/Spring14miniaod/DYJetsToLL_M-50_13TeV-madgraph-pythia8/MINIAODSIM/PU20bx25_POSTLS170_V5-v1/00000/205CCA64-8F07-E411-9313-001E67075FC4.root",  
"file:/cms/data/store/mc/Spring14miniaod/DYJetsToLL_M-50_13TeV-madgraph-pythia8/MINIAODSIM/PU20bx25_POSTLS170_V5-v1/00000/5E962231-A207-E411-A744-D4AE529D9537.root",  
"file:/cms/data/store/mc/Spring14miniaod/DYJetsToLL_M-50_13TeV-madgraph-pythia8/MINIAODSIM/PU20bx25_POSTLS170_V5-v1/00000/A2BCAF6A-8F07-E411-AF56-001E675A6928.root",  
"file:/cms/data/store/mc/Spring14miniaod/DYJetsToLL_M-50_13TeV-madgraph-pythia8/MINIAODSIM/PU20bx25_POSTLS170_V5-v1/00000/FE495960-A207-E411-95A2-90B11C070100.root",
"file:/cms/data/store/mc/Spring14miniaod/DYJetsToLL_M-50_13TeV-madgraph-pythia8/MINIAODSIM/PU20bx25_POSTLS170_V5-v1/00000/24539E63-8F07-E411-9E7C-90B11C050AD4.root",  
"file:/cms/data/store/mc/Spring14miniaod/DYJetsToLL_M-50_13TeV-madgraph-pythia8/MINIAODSIM/PU20bx25_POSTLS170_V5-v1/00000/5ED9ED82-A107-E411-B2EC-001517FB25E4.root",  
"file:/cms/data/store/mc/Spring14miniaod/DYJetsToLL_M-50_13TeV-madgraph-pythia8/MINIAODSIM/PU20bx25_POSTLS170_V5-v1/00000/A8050556-A007-E411-9E83-001E675A6AB8.root",
"file:/cms/data/store/mc/Spring14miniaod/DYJetsToLL_M-50_13TeV-madgraph-pythia8/MINIAODSIM/PU20bx25_POSTLS170_V5-v1/00000/2496ED62-8F07-E411-90BC-485B3919F0B9.root",  
"file:/cms/data/store/mc/Spring14miniaod/DYJetsToLL_M-50_13TeV-madgraph-pythia8/MINIAODSIM/PU20bx25_POSTLS170_V5-v1/00000/6483D764-8F07-E411-8880-001E67075FC4.root",  
"file:/cms/data/store/mc/Spring14miniaod/DYJetsToLL_M-50_13TeV-madgraph-pythia8/MINIAODSIM/PU20bx25_POSTLS170_V5-v1/00000/AE6BA846-9607-E411-9889-001E675A68C4.root",
"file:/cms/data/store/mc/Spring14miniaod/DYJetsToLL_M-50_13TeV-madgraph-pythia8/MINIAODSIM/PU20bx25_POSTLS170_V5-v1/00000/261FCA64-8F07-E411-95BC-001E67075FC4.root",  
"file:/cms/data/store/mc/Spring14miniaod/DYJetsToLL_M-50_13TeV-madgraph-pythia8/MINIAODSIM/PU20bx25_POSTLS170_V5-v1/00000/687CA766-A207-E411-81EC-90B11C050371.root",  
"file:/cms/data/store/mc/Spring14miniaod/DYJetsToLL_M-50_13TeV-madgraph-pythia8/MINIAODSIM/PU20bx25_POSTLS170_V5-v1/00000/AE94E965-8F07-E411-ABD8-90B11C056AAD.root",
]
)

# The output ntuple name
process.dimuons.getFilename    = cms.untracked.string("DYToLL13TeV.root")

### This is for debugging. It spits out a CMSSW ROOT file called dump.root with all of the data types in it
#process.output = cms.OutputModule("PoolOutputModule",
#                                  outputCommands = cms.untracked.vstring("keep *"),
#                                  fileName = cms.untracked.string('dump.root')
#                                  )
#
#process.out_step = cms.EndPath(process.output)
