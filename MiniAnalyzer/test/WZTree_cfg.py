import FWCore.ParameterSet.Config as cms

from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing('analysis')

options.outputFile = 'wzTree.root'
options.inputFiles= 'miniTree.root'
options.maxEvents = -1

options.parseArguments()

process = cms.Process("MiniAnalyzer")

process.load("FWCore.MessageService.MessageLogger_cfi")

process.MessageLogger.cerr.FwkReport.reportEvery = 1000

process.source = cms.Source("EmptySource")

process.TFileService = cms.Service("TFileService",
    fileName = cms.string(options.outputFile),
)

process.load("AnalysisTools.MiniAnalyzer.WZTree_cfi")

process.wzTree.fileNames = cms.vstring(options.inputFiles)

process.wzTreePath = cms.Path(process.wzTree)
