import FWCore.ParameterSet.Config as cms

miniTreePath = cms.Path()

# first create collections to analyze


from AnalysisTools.MiniNtuplizer.branchTemplates import *

miniTree = cms.EDAnalyzer("MiniTree",
    genEventInfo = cms.InputTag("generator"),
    genParticles = cms.InputTag("prunedGenParticles"),
    genParticleBranches = cms.PSet(
        genParticles = cms.PSet(
            maxCount = cms.uint32(10000),
            branches = genParticleBranches,
        ),
    ),
    electrons = cms.InputTag("slimmedElectrons"),
    electronBranches = cms.PSet(
        electrons = cms.PSet(
            maxCount = cms.uint32(100),
            branches = electronBranches,
        ),
    ),
    muons = cms.InputTag("slimmedMuons"),
    muonBranches = cms.PSet(
        muons = cms.PSet(
            maxCount = cms.uint32(100),
            branches = muonBranches,
        ),
    ),
    taus = cms.InputTag("slimmedTaus"),
    tauBranches = cms.PSet(
        taus = cms.PSet(
            maxCount = cms.uint32(100),
            branches = tauBranches,
        ),
    ),
    photons = cms.InputTag("slimmedPhotons"),
    photonBranches = cms.PSet(
        photons = cms.PSet(
            maxCount = cms.uint32(100),
            branches = photonBranches,
        ),
    ),
    jets = cms.InputTag("slimmedJets"),
    jetBranches = cms.PSet(
        jets = cms.PSet(
            maxCount = cms.uint32(100),
            branches = jetBranches,
        ),
    ),
    mets = cms.InputTag("slimmedMETs"),
    metBranches = cms.PSet(
        pfmet = cms.PSet(
            maxCount = cms.uint32(1),
            branches = metBranches,
        ),
    ),
)
miniTreePath += miniTree
