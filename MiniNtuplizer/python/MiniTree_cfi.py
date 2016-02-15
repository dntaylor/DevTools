import FWCore.ParameterSet.Config as cms

# load branches
from AnalysisTools.MiniNtuplizer.branchTemplates import *

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
    collections = cms.PSet(
        #vertices = cms.PSet(
        #    collection = cms.InputTag("slimmedOfflinePrimaryVertices"),
        #    branches = vertexBranches,
        #),
        genParticles = cms.PSet(
            collection = cms.InputTag("prunedGenParticles"),
            branches = genParticleBranches,
        ),
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
