import FWCore.ParameterSet.Config as cms

from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing('analysis')

options.outputFile = 'miniTree.root'
#options.inputFiles= '/store/mc/RunIIFall15MiniAODv2/WZTo3LNu_TuneCUETP8M1_13TeV-powheg-pythia8/MINIAODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/10000/022EC2EB-90B8-E511-AED0-0026B937D37D.root'
options.inputFiles = '/store/user/dntaylor/HPlusPlusHMinusMinusHTo4L_M-500_13TeV-pythia8/RunIIFall15MiniAODv2_MINIAODSIM/160210_132739/0000/dblh_m500_13tev_miniAODv2_1.root'
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

# the selections for each object (to be included in ntuple)
# will always be the last thing done to the collection, so can use embedded things from previous steps
selections = {
    'electrons' : 'pt>7 && abs(eta)<3.0',
    'muons'     : 'pt>4 && abs(eta)<2.5',
    'taus'      : 'pt>17 && abs(eta)<2.3 && tauID("decayModeFinding")>0.5', # remove 2 prong taus
    'photons'   : 'pt>10 && abs(eta)<3.0',
    'jets'      : 'pt>15 && abs(eta)<4.7',
}

# selection for cleaning (objects should match final selection)
cleaning = {
    'jets' : {
        'electrons' : {
            'cut' : 'pt>10 && abs(eta)<2.5 && userInt("cutBasedElectronID-Spring15-25ns-V1-standalone-medium")>0.5',
            'dr'  : 0.3,
        },
        'muons' : {
            'cut' : 'pt>10 && abs(eta)<2.4 && isMediumMuon>0.5',
            'dr'  : 0.3,
        },
        'taus' : {
            'cut' : 'pt>20 && abs(eta)<2.3 && tauID("byMediumCombinedIsolationDeltaBetaCorr3Hits")>0.5 && tauID("decayModeFinding")>0.5',
            'dr'  : 0.3,
        },
    },
}

# now do any customization/cleaning
from AnalysisTools.MiniNtuplizer.customizeElectrons import customizeElectrons
collections['electrons'] = customizeElectrons(
    process,
    collections['electrons'],
)

from AnalysisTools.MiniNtuplizer.customizeMuons import customizeMuons
collections['muons'] = customizeMuons(
    process,
    collections['muons'],
)

from AnalysisTools.MiniNtuplizer.customizeTaus import customizeTaus
collections['taus'] = customizeTaus(
    process,
    collections['taus'],
)

from AnalysisTools.MiniNtuplizer.customizePhotons import customizePhotons
collections['photons'] = customizePhotons(
    process,
    collections['photons'],
)

from AnalysisTools.MiniNtuplizer.customizeJets import customizeJets
collections['jets'] = customizeJets(
    process,
    collections['jets'],
)

from AnalysisTools.MiniNtuplizer.customizeMets import customizeMets
collections['pfmet'] = customizeMets(
    process,
    collections['pfmet'],
)

# select desired objects
from AnalysisTools.MiniNtuplizer.objectTools import objectSelector, objectCleaner
for coll in selections:
    collections[coll] = objectSelector(process,coll,collections[coll],selections[coll])
for coll in cleaning:
    collections[coll] = objectCleaner(process,coll,collections[coll],collections,cleaning[coll])

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
