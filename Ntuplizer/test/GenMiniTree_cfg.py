import os

import FWCore.ParameterSet.Config as cms

from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing('analysis')

options.outputFile = 'genMiniTree.root'
options.inputFiles = '/store/user/dntaylor/HPlusPlusHMinusMinusHTo4L_M-500_13TeV-pythia8/RunIIFall15MiniAODv2_MINIAODSIM_v3/160319_171922/0000/dblh_step1_1.root'
options.maxEvents = -1

options.parseArguments()

#####################
### setup process ###
#####################

process = cms.Process("GenMiniNtuple")

process.load('Configuration.Geometry.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
process.load('Configuration.StandardSequences.Services_cff')

process.options = cms.untracked.PSet(
    allowUnscheduled = cms.untracked.bool(True),
)

#################
### GlobalTag ###
#################
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_mc', '')

#############################
### Setup rest of running ###
#############################
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

###########################
### Profiling utilities ###
###########################

#process.ProfilerService = cms.Service (
#      "ProfilerService",
#       firstEvent = cms.untracked.int32(2),
#       lastEvent = cms.untracked.int32(500),
#       paths = cms.untracked.vstring('schedule') 
#)

#process.SimpleMemoryCheck = cms.Service(
#    "SimpleMemoryCheck",
#    ignoreTotal = cms.untracked.int32(1)
#)

### To use IgProf's neat memory profiling tools, uncomment the following 
### lines then run this cfg with igprof like so:
###      $ igprof -d -mp -z -o igprof.mp.gz cmsRun ... 
### this will create a memory profile every 250 events so you can track use
### Turn the profile into text with
###      $ igprof-analyse -d -v -g -r MEM_LIVE igprof.yourOutputFile.gz > igreport_live.res
### To do a performance profile instead of a memory profile, change -mp to -pp
### in the first command and remove  -r MEM_LIVE from the second
### For interpretation of the output, see http://igprof.org/text-output-format.html

#from IgTools.IgProf.IgProfTrigger import igprof
#process.load("IgTools.IgProf.IgProfTrigger")
#process.igprofPath = cms.Path(process.igprof)
#process.igprof.reportEventInterval     = cms.untracked.int32(250)
#process.igprof.reportToFileAtBeginJob  = cms.untracked.string("|gzip -c>igprof.begin-job.gz")
#process.igprof.reportToFileAtEvent = cms.untracked.string("|gzip -c>igprof.%I.%E.%L.%R.event.gz")
#process.schedule.append(process.igprofPath)

# first create collections to analyze
genColl = 'prunedGenParticles'
collections = {
    'electrons'    : genColl,
    'muons'        : genColl,
    'taus'         : genColl,
    'photons'      : genColl,
    'higgs'        : genColl,
}

# define each collection
# hard process higgs
process.higgsSelected = cms.EDFilter("GenParticleSelector",
    src = cms.InputTag(collections['higgs']),
    cut = cms.string('(abs(pdgId)==9900041 || abs(pdgId)==37) && isLastCopy'),
    filter = cms.bool(False)
)
collections['higgs'] = 'higgsSelected'
process.higgs = cms.Path(process.higgsSelected)
process.schedule.append(process.higgs)

# muons
process.muonsSelected = cms.EDFilter("GenParticleSelector",
    src = cms.InputTag(collections['muons']),
    cut = cms.string('status==1 && abs(pdgId)==13 && pt>4'),
    filter = cms.bool(False)
)
collections['muons'] = 'muonsSelected'
process.muons = cms.Path(process.muonsSelected)
process.schedule.append(process.muons)

# electrons
process.electronsSelected = cms.EDFilter("GenParticleSelector",
    src = cms.InputTag(collections['electrons']),
    cut = cms.string('status==1 && abs(pdgId)==11 && pt>4'),
    filter = cms.bool(False)
)
collections['electrons'] = 'electronsSelected'
process.electrons = cms.Path(process.electronsSelected)
process.schedule.append(process.electrons)

# photons
process.photonsSelected = cms.EDFilter("GenParticleSelector",
    src = cms.InputTag(collections['photons']),
    cut = cms.string('status==1 && pdgId==22 && pt>4'),
    filter = cms.bool(False)
)
collections['photons'] = 'photonsSelected'
process.photons = cms.Path(process.photonsSelected)
process.schedule.append(process.photons)

# taus
from PhysicsTools.JetMCAlgos.TauGenJets_cfi import tauGenJets
process.tauGenJets = tauGenJets.clone(GenParticles = cms.InputTag(collections['taus']))
collections['taus'] = 'tauGenJets'
process.taus = cms.Path(process.tauGenJets)
process.schedule.append(process.taus)

# add the analyzer
process.load("DevTools.Ntuplizer.GenMiniTree_cfi")
from DevTools.Ntuplizer.branchTemplates import genParticleBranches, genJetBranches
process.genMiniTree.collections = cms.PSet(
    higgs = cms.PSet(
        collection = cms.InputTag(collections['higgs']),
        branches = genParticleBranches,
    ),
    electrons = cms.PSet(
        collection = cms.InputTag(collections['electrons']),
        branches = genParticleBranches,
    ),
    muons = cms.PSet(
        collection = cms.InputTag(collections['muons']),
        branches = genParticleBranches,
    ),
    taus = cms.PSet(
        collection = cms.InputTag(collections['taus']),
        branches = genJetBranches,
    ),
    photons = cms.PSet(
        collection = cms.InputTag(collections['photons']),
        branches = genParticleBranches,
    ),
)
process.genMiniTreePath = cms.Path(process.genMiniTree)
process.schedule.append(process.genMiniTreePath)
