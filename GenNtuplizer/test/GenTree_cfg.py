import FWCore.ParameterSet.Config as cms

from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing('analysis')

options.outputFile = 'genTree.root'
options.inputFiles= 'file:/hdfs/store/user/dntaylor/DBLH_M-500_13TeV_MINIAODSIM_v1-dblh_m500_13tev_4_cfg/dblh_m500_13tev_4_cfg-dblh_m500_13tev_3_cfg-dblh_m500_13tev_2_cfg-DBLH_M-500_13TeV_GEN-SIM_v4-0000.root'
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

