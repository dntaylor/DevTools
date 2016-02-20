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
    inputFileNames='/hdfs/store/user/dntaylor/2016-02-19_DevTools_v1/WZTo3LNu_TuneCUETP8M1_13TeV-powheg-pythia8/2016-02-19_DevTools_v1/160219_162545/0000/miniTree_1.root',
    inputTreeName='MiniTree',
    inputLumiName='LumiTree',
    inputTreeDirectory='miniTree',
)

try:
   wzAnalysis.analyze()
   wzAnalysis.finish()
except KeyboardInterrupt:
   wzAnalysis.finish()
