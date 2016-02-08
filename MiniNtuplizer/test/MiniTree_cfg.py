import FWCore.ParameterSet.Config as cms

from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing('analysis')

options.outputFile = 'miniTree.root'
options.inputFiles= '/store/mc/RunIIFall15MiniAODv2/WZTo3LNu_TuneCUETP8M1_13TeV-powheg-pythia8/MINIAODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/10000/022EC2EB-90B8-E511-AED0-0026B937D37D.root'
options.maxEvents = -1
options.register('isMC', 0, VarParsing.multiplicity.singleton, VarParsing.varType.int, "Sample is MC")

options.parseArguments()

process = cms.Process("MiniNtuple")

process.load('Configuration.Geometry.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
process.load('Configuration.StandardSequences.Services_cff')

envvar = 'mcgt' if options.isMC else 'datagt'

from Configuration.AlCa.GlobalTag import GlobalTag
GT = {'mcgt': 'auto:run2_mc', 'datagt': 'auto:run2_data'}
process.GlobalTag = GlobalTag(process.GlobalTag, GT[envvar], '')

process.load("FWCore.MessageService.MessageLogger_cfi")

process.MessageLogger.cerr.FwkReport.reportEvery = 100

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(options.maxEvents) )

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(options.inputFiles)
)

process.TFileService = cms.Service("TFileService", 
    fileName = cms.string(options.outputFile),
)

process.schedule = cms.Schedule()

# first create collections to analyze
collections = {
    'genParticles' : 'prunedGenParticles',
    'electrons'    : 'slimmedElectrons',
    'muons'        : 'slimmedMuons',
    'taus'         : 'slimmedTaus',
    'photons'      : 'slimmedPhotons',
    'jets'         : 'slimmedJets',
    'pfmet'        : 'slimmedMETs',
}

from AnalysisTools.MiniNtuplizer.customizeElectrons import customizeElectrons
collections['electrons'] = customizeElectrons(process,collections['electrons'])

from AnalysisTools.MiniNtuplizer.customizeMuons import customizeMuons
collections['muons'] = customizeMuons(process,collections['muons'])

from AnalysisTools.MiniNtuplizer.customizeTaus import customizeTaus
collections['taus'] = customizeTaus(process,collections['taus'])

from AnalysisTools.MiniNtuplizer.customizePhotons import customizePhotons
collections['photons'] = customizePhotons(process,collections['photons'])

from AnalysisTools.MiniNtuplizer.customizeJets import customizeJets
collections['jets'] = customizeJets(process,collections['jets'])

from AnalysisTools.MiniNtuplizer.customizeMets import customizeMets
collections['pfmet'] = customizeMets(process,collections['pfmet'])

# add the analyzer
process.load("AnalysisTools.MiniNtuplizer.MiniTree_cfi")

process.miniTree.genParticles = collections['genParticles']
process.miniTree.electrons = collections['electrons']
process.miniTree.muons = collections['muons']
process.miniTree.taus = collections['taus']
process.miniTree.photons = collections['photons']
process.miniTree.jets = collections['jets']
process.miniTree.mets = collections['pfmet']

process.schedule.append(process.miniTreePath)
