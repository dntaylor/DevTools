import FWCore.ParameterSet.Config as cms

genTreePath = cms.Path()

# first create collections to analyze

# hard process
higgsPruned = cms.EDProducer(
    "GenParticlePruner",
    src = cms.InputTag("prunedGenParticles"),
    select = cms.vstring(
    'drop *',
    'keep abs(pdgId)==9900041 && isLastCopy', # H++
    'keep abs(pdgId)==25 && isLastCopy',      # h0
    'keep abs(pdgId)==35 && isLastCopy',      # H0
    'keep abs(pdgId)==36 && isLastCopy',      # A0
    'keep abs(pdgId)==37 && isLastCopy',      # H+
    )
)
genTreePath += higgsPruned

# muons
muonsPruned = cms.EDProducer(
    "GenParticlePruner",
    src = cms.InputTag("prunedGenParticles"),
    select = cms.vstring(
    'keep status==1 && abs(pdgId)==13 && pt>4'
    )
)
genTreePath += muonsPruned

# electrons
electronsPruned = cms.EDProducer(
    "GenParticlePruner",
    src = cms.InputTag("prunedGenParticles"),
    select = cms.vstring(
    'keep status==1 && abs(pdgId)==11 && pt>4'
    )
)
genTreePath += electronsPruned

# photons
photonsPruned = cms.EDProducer(
    "GenParticlePruner",
    src = cms.InputTag("prunedGenParticles"),
    select = cms.vstring(
    'keep status==1 && pdgId==22 && pt>4'
    )
)
genTreePath += photonsPruned

# hadronic taus
from PhysicsTools.JetMCAlgos.TauGenJets_cfi import tauGenJets
tauGenJets.GenParticles = cms.InputTag("prunedGenParticles")
genTreePath += tauGenJets

from AnalysisTools.GenNtuplizer.branchTemplates import *

genTree = cms.EDAnalyzer("GenTree",
    genParticles = cms.InputTag("prunedGenParticles"),
    genParticleBranches = cms.PSet(
        allGenParticles = cms.PSet(
            maxCount = cms.uint32(10000),
            branches = allGenParticleBranches,
        ),
    ),
    higgs = cms.InputTag("higgsPruned"),
    higgsBranches = cms.PSet(
        higgs = cms.PSet(
            maxCount = cms.uint32(100),
            branches = higgsBranches,
        ),
    ),
    muons = cms.InputTag("muonsPruned"),
    muonBranches = cms.PSet(
        muons = cms.PSet(
            maxCount = cms.uint32(100),
            branches = muonBranches,
        ),
    ),
    electrons = cms.InputTag("electronsPruned"),
    electronBranches = cms.PSet(
        electrons = cms.PSet(
            maxCount = cms.uint32(100),
            branches = electronBranches,
        ),
    ),
    photons = cms.InputTag("photonsPruned"),
    photonBranches = cms.PSet(
        photons = cms.PSet(
            maxCount = cms.uint32(100),
            branches = photonBranches,
        ),
    ),
    taus = cms.InputTag("tauGenJets"),
    tauBranches = cms.PSet(
        taus = cms.PSet(
            maxCount = cms.uint32(100),
            branches = tauBranches,
        ),
    ),
)
genTreePath += genTree
