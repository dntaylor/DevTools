import FWCore.ParameterSet.Config as cms

wzTree = cms.EDAnalyzer("WZTree",
    fileNames = cms.vstring(),
    inputDirectoryName = cms.string("miniTree"),
    inputLumiName = cms.string("LumiTree"),
    inputTreeName = cms.string("MiniTree"),
    ouputTreeName = cms.string("WZTree"),
)
