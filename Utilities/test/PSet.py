import FWCore.ParameterSet.Config as cms

process = cms.Process("CrabDummy")

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring('file:input.root')
)
process.output = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string('output.root'),
)

process.out = cms.EndPath(process.output)

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(1)
)
