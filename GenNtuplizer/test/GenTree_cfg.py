import FWCore.ParameterSet.Config as cms

from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing('analysis')

options.outputFile = 'genTree.root'
options.inputFiles= '/store/user/dntaylor/HPlusPlusHMinusMinusHTo4L_M-500_13TeV-pythia8/RunIIFall15DR76_MINIAODSIM/160209_075744/0000/dblh_m500_13tev_step3_1.root'
options.maxEvents = -1

options.parseArguments()

process = cms.Process("GenNtuple")

process.load("FWCore.MessageService.MessageLogger_cfi")

process.MessageLogger.cerr.FwkReport.reportEvery = 100

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(options.maxEvents) )

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(options.inputFiles)
)

process.TFileService = cms.Service("TFileService", 
    fileName = cms.string(options.outputFile),
)

process.load("AnalysisTools.GenNtuplizer.GenTree_cfi")

