import FWCore.ParameterSet.Config as cms

# load branches
from DevTools.Ntuplizer.branchTemplates import *

miniTree = cms.EDAnalyzer("MiniTree",
    isData = cms.bool(True),
    genEventInfo = cms.InputTag("generator"),
    lheEventProduct = cms.InputTag("externalLHEProducer"),
    rho = cms.InputTag("fixedGridRhoFastjetAll"),
    pileupSummaryInfo = cms.InputTag("slimmedAddPileupInfo"),
    triggerResults = cms.InputTag("TriggerResults","","HLT"),
    filterResults = cms.InputTag("TriggerResults","","PAT"),
    triggerObjects = cms.InputTag("selectedPatTrigger"),
    triggerPrescales = cms.InputTag("patTrigger"),
    triggerBranches = triggerBranches,
    filterBranches = filterBranches,
    vertexCollections = cms.PSet(
        vertices = cms.PSet(
            collection = cms.InputTag("slimmedOfflinePrimaryVertices"),
            branches = vertexBranches,
        ),
    ),
    collections = cms.PSet(
        electrons = cms.PSet(
            collection = cms.InputTag("slimmedElectrons"),
            branches = electronBranches,
        ),
        muons = cms.PSet(
            collection = cms.InputTag("slimmedMuons"),
            branches = muonBranches,
        ),
        taus = cms.PSet(
            collection = cms.InputTag("slimmedTaus"),
            branches = tauBranches,
        ),
        photons = cms.PSet(
            collection = cms.InputTag("slimmedPhotons"),
            branches = photonBranches,
        ),
        jets = cms.PSet(
            collection = cms.InputTag("slimmedJets"),
            branches = jetBranches,
        ),
        pfmet = cms.PSet(
            collection = cms.InputTag("slimmedMETs"),
            branches = metBranches,
        ),
    ),
)
