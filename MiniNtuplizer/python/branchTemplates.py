import FWCore.ParameterSet.Config as cms

commonCandidates = cms.PSet(
    pt     = cms.vstring('pt()','F'),
    eta    = cms.vstring('eta()','F'),
    phi    = cms.vstring('phi()','F'),
    energy = cms.vstring('energy()','F'),
    charge = cms.vstring('charge()','F'),
    mass   = cms.vstring('mass()','F'),
)

commonGenCandidates = commonCandidates.clone(
    pdgId             = cms.vstring('pdgId()','I'),
    status            = cms.vstring('status()','I'),
)

statusOneCandidates = commonGenCandidates.clone(
    isPrompt               = cms.vstring('isPromptFinalState()','I'),
    isFromTau              = cms.vstring('isDirectPromptTauDecayProductFinalState()','I'),
    fromHardProcess        = cms.vstring('fromHardProcessFinalState()','I'),
    fromHardProcessDecayed = cms.vstring('fromHardProcessDecayed()','I'),
    fromHardProcessTau     = cms.vstring('isDirectHardProcessTauDecayProductFinalState()','I'),
)

commonGenJetCandidates = commonGenCandidates.clone(
    emEnergy         = cms.vstring('emEnergy()','F'),
    hadEnergy        = cms.vstring('hadEnergy()','F'),
    invisibileEnergy = cms.vstring('invisibleEnergy()','F'),
    nConstituents    = cms.vstring('nConstituents','I'),
    
)


# genParticles
genParticleBranches = commonGenCandidates.clone()

# electrons
electronBranches = commonCandidates.clone(

)

# muons
muonBranches = commonCandidates.clone(

)

# taus
tauBranches = commonCandidates.clone(

)

# photons
photonBranches = commonCandidates.clone(

)

# jets
jetBranches = commonCandidates.clone(

)
