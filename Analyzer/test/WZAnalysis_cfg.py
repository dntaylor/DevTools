#import FWCore.ParameterSet.Config as cms
#
#from FWCore.ParameterSet.VarParsing import VarParsing
#options = VarParsing('analysis')
#
#options.outputFile = 'wzTree.root'
#options.inputFiles= 'miniTree.root'
#options.register('isMC', 0, VarParsing.multiplicity.singleton, VarParsing.varType.int, "Sample is MC")
#
#options.parseArguments()
#
#process = cms.Process("WZNtuple")
#
#process.source = cms.Source("EmptySource")
#
#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1) )

# wz analysis

import logging
import sys

from DevTools.Analyzer.WZAnalysis import WZAnalysis

logger = logging.getLogger("WZAnalysis")
logging.basicConfig(level=logging.INFO, stream=sys.stderr)

wzAnalysis = WZAnalysis(
    sample='WZTo3LNu',
    #outputFileName=options.outputFile,
    outputFileName='wzTree.root',
    outputTreeName='WZTree',
    #inputFileNames=options.inputFiles,
    inputFileNames='miniTree.root',
    inputTreeName='MiniTree',
    inputLumiName='LumiTree',
    inputTreeDirectory='miniTree',
)

try:
   wzAnalysis.analyze()
   wzAnalysis.finish()
except KeyboardInterrupt:
   wzAnalysis.finish()
