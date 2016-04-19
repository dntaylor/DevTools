import FWCore.ParameterSet.Config as cms

commonCandidates = cms.PSet(
    pt     = cms.vstring('pt()','F'),
    eta    = cms.vstring('eta()','F'),
    phi    = cms.vstring('phi()','F'),
    energy = cms.vstring('energy()','F'),
    charge = cms.vstring('charge()','F'),
    mass   = cms.vstring('mass()','F'),
    vz     = cms.vstring('vz()','F'),
    pdgId  = cms.vstring('pdgId()','I'),
)

commonGenCandidates = commonCandidates.clone(
    status                 = cms.vstring('status()','I'),
    numberOfDaughters      = cms.vstring('numberOfDaughters()','I'),
    daughter_1             = cms.vstring('? numberOfDaughters()>0 ? daughter(0).pdgId() : 0','I'),
    daughter_2             = cms.vstring('? numberOfDaughters()>1 ? daughter(1).pdgId() : 0','I'),
    numberOfMothers        = cms.vstring('numberOfMothers()','I'),
    mother_1               = cms.vstring('? numberOfMothers()>0 ? mother(0).pdgId() : 0','I'),
    mother_2               = cms.vstring('? numberOfMothers()>1 ? mother(1).pdgId() : 0','I'),
    isPrompt               = cms.vstring('isPromptFinalState()','I'),
    isFromTau              = cms.vstring('isDirectPromptTauDecayProductFinalState()','I'),
    isPromptDecayed        = cms.vstring('isPromptDecayed()','I'),
    isFromHadron           = cms.vstring('statusFlags().isDirectHadronDecayProduct()','I'),
    fromHardProcess        = cms.vstring('fromHardProcessFinalState()','I'),
    fromHardProcessDecayed = cms.vstring('fromHardProcessDecayed()','I'),
    fromHardProcessTau     = cms.vstring('isDirectHardProcessTauDecayProductFinalState()','I'),
)

commonPatCandidates = commonCandidates.clone(
    genMatch                  = cms.vstring('genParticleRef.isNonnull()','I'),
    genPdgId                  = cms.vstring('? (genParticleRef.isNonnull() ) ? genParticleRef().pdgId() : 0', 'I'),
    genPt                     = cms.vstring('? (genParticleRef.isNonnull() ) ? genParticleRef().pt() : 0', 'F'),
    genEta                    = cms.vstring('? (genParticleRef.isNonnull() ) ? genParticleRef().eta() : 0', 'F'),
    genPhi                    = cms.vstring('? (genParticleRef.isNonnull() ) ? genParticleRef().phi() : 0', 'F'),
    genMass                   = cms.vstring('? (genParticleRef.isNonnull() ) ? genParticleRef().mass() : 0', 'F'),
    genEnergy                 = cms.vstring('? (genParticleRef.isNonnull() ) ? genParticleRef().energy() : 0', 'F'),
    genCharge                 = cms.vstring('? (genParticleRef.isNonnull() ) ? genParticleRef().charge() : 0', 'F'),
    genVZ                     = cms.vstring('? (genParticleRef.isNonnull() ) ? genParticleRef().vz() : 0', 'F'),
    genStatus                 = cms.vstring('? (genParticleRef.isNonnull() ) ? genParticleRef().status() : 0', 'I'),
    genIsPrompt               = cms.vstring('? (genParticleRef.isNonnull() ) ? genParticleRef().isPromptFinalState() : 0', 'I'),
    genIsFromTau              = cms.vstring('? (genParticleRef.isNonnull() ) ? genParticleRef().isDirectPromptTauDecayProductFinalState() : 0', 'I'),
    genIsPromptDecayed        = cms.vstring('? (genParticleRef.isNonnull() ) ? genParticleRef().isPromptDecayed() : 0', 'I'),
    genIsFromHadron           = cms.vstring('? (genParticleRef.isNonnull() ) ? genParticleRef().statusFlags().isDirectHadronDecayProduct() : 0', 'I'),
    genFromHardProcess        = cms.vstring('? (genParticleRef.isNonnull() ) ? genParticleRef().fromHardProcessFinalState() : 0', 'I'),
    genFromHardProcessDecayed = cms.vstring('? (genParticleRef.isNonnull() ) ? genParticleRef().fromHardProcessDecayed() : 0', 'I'),
    genFromHardProcessTau     = cms.vstring('? (genParticleRef.isNonnull() ) ? genParticleRef().isDirectHardProcessTauDecayProductFinalState() : 0', 'I'),
)

commonJetCandidates = commonPatCandidates.clone(
    genJetMatch               = cms.vstring('userCand("genJet").isNonnull()','I'),
    genJetPdgId               = cms.vstring('? (userCand("genJet").isNonnull() ) ? userCand("genJet").pdgId() : 0', 'I'),
    genJetPt                  = cms.vstring('? (userCand("genJet").isNonnull() ) ? userCand("genJet").pt() : 0', 'F'),
    genJetEta                 = cms.vstring('? (userCand("genJet").isNonnull() ) ? userCand("genJet").eta() : 0', 'F'),
    genJetPhi                 = cms.vstring('? (userCand("genJet").isNonnull() ) ? userCand("genJet").phi() : 0', 'F'),
    genJetMass                = cms.vstring('? (userCand("genJet").isNonnull() ) ? userCand("genJet").mass() : 0', 'F'),
    genJetEnergy              = cms.vstring('? (userCand("genJet").isNonnull() ) ? userCand("genJet").energy() : 0', 'F'),
    genJetCharge              = cms.vstring('? (userCand("genJet").isNonnull() ) ? userCand("genJet").charge() : 0', 'F'),
    genJetVZ                  = cms.vstring('? (userCand("genJet").isNonnull() ) ? userCand("genJet").vz() : 0', 'F'),
    genJetStatus              = cms.vstring('? (userCand("genJet").isNonnull() ) ? userCand("genJet").status() : 0', 'I'),
    genJetEMEnergy            = cms.vstring('? (userCand("genJet").isNonnull() ) ? userCand("genJet").emEnergy() : 0', 'F'),
    genJetHadEnergy           = cms.vstring('? (userCand("genJet").isNonnull() ) ? userCand("genJet").hadEnergy() : 0', 'F'),
    genJetInvisibleEnergy     = cms.vstring('? (userCand("genJet").isNonnull() ) ? userCand("genJet").invisibleEnergy() : 0', 'F'),
    genJetNConstituents       = cms.vstring('? (userCand("genJet").isNonnull() ) ? userCand("genJet").nConstituents() : 0', 'I'),
)

#statusOneCandidates = commonGenCandidates.clone(
#    isPrompt               = cms.vstring('isPromptFinalState()','I'),
#    isFromTau              = cms.vstring('isDirectPromptTauDecayProductFinalState()','I'),
#    isPromptDecayed        = cms.vstring('isPromptDecayed()','I'),
#    fromHardProcess        = cms.vstring('fromHardProcessFinalState()','I'),
#    fromHardProcessDecayed = cms.vstring('fromHardProcessDecayed()','I'),
#    fromHardProcessTau     = cms.vstring('isDirectHardProcessTauDecayProductFinalState()','I'),
#)

commonGenJetCandidates = commonCandidates.clone(
    status           = cms.vstring('status()','I'),
    emEnergy         = cms.vstring('emEnergy()','F'),
    hadEnergy        = cms.vstring('hadEnergy()','F'),
    invisibileEnergy = cms.vstring('invisibleEnergy()','F'),
    nConstituents    = cms.vstring('nConstituents','I'),
    
)

commonMet = cms.PSet(
    et  = cms.vstring('pt()','F'),
    phi = cms.vstring('phi()','F'),
)

commonVertex = cms.PSet(
    x              = cms.vstring('x','F'),
    y              = cms.vstring('y','F'),
    z              = cms.vstring('z','F'),
    xError         = cms.vstring('xError','F'),
    yError         = cms.vstring('yError','F'),
    zError         = cms.vstring('zError','F'),
    chi2           = cms.vstring('chi2','F'),
    ndof           = cms.vstring('ndof','F'),
    normalizedChi2 = cms.vstring('normalizedChi2','F'),
    isValid        = cms.vstring('isValid', 'I'),
    isFake         = cms.vstring('isFake', 'I'),
    rho            = cms.vstring('position.Rho','F'),
)

# trigger
triggerBranches = cms.PSet(
    # single muon
    Mu8_TrkIsoVVL                               = cms.PSet(
                                                    path  = cms.string('HLT_Mu8_TrkIsoVVL_v\\[0-9]+'),
                                                ),
    Mu17_TrkIsoVVL                              = cms.PSet(
                                                    path  = cms.string('HLT_Mu17_TrkIsoVVL_v\\[0-9]+'),
                                                ),
    Mu24_TrkIsoVVL                              = cms.PSet(
                                                    path  = cms.string('HLT_Mu24_TrkIsoVVL_v\\[0-9]+'),
                                                ),
    Mu34_TrkIsoVVL                              = cms.PSet(
                                                    path  = cms.string('HLT_Mu34_TrkIsoVVL_v\\[0-9]+'),
                                                ),
    IsoMu20                                     = cms.PSet(
                                                    path  = cms.string('HLT_IsoMu20_v\\[0-9]+'),
                                                ),
    IsoTkMu20                                   = cms.PSet(
                                                    path  = cms.string('HLT_IsoTkMu20_v\\[0-9]+'),
                                                ),
    IsoMu27                                     = cms.PSet(
                                                    path  = cms.string('HLT_IsoMu27_v\\[0-9]+'),
                                                ),
    IsoTkMu27                                   = cms.PSet(
                                                    path  = cms.string('HLT_IsoTkMu27_v\\[0-9]+'),
                                                ),
    Mu45_eta2p1                                 = cms.PSet(
                                                    path  = cms.string('HLT_Mu45_eta2p1_v\\[0-9]+'),
                                                ),
    Mu50                                        = cms.PSet(
                                                    path  = cms.string('HLT_Mu50_v\\[0-9]+'),
                                                ),
    # single electron
    Ele12_CaloIdL_TrackIdL_IsoVL                = cms.PSet(
                                                    path  = cms.string('HLT_Ele12_CaloIdL_TrackIdL_IsoVL_v\\[0-9]+'),
                                                ),
    Ele17_CaloIdL_TrackIdL_IsoVL                = cms.PSet(
                                                    path  = cms.string('HLT_Ele17_CaloIdL_TrackIdL_IsoVL_v\\[0-9]+'),
                                                ),
    Ele23_CaloIdL_TrackIdL_IsoVL                = cms.PSet(
                                                    path  = cms.string('HLT_Ele23_CaloIdL_TrackIdL_IsoVL_v\\[0-9]+'),
                                                ),
    Ele22_eta2p1_WPLoose_Gsf                    = cms.PSet(
                                                    path  = cms.string('HLT_Ele22_eta2p1_WPLoose_Gsf_v\\[0-9]+'),
                                                ),
    Ele23_WPLoose_Gsf                           = cms.PSet(
                                                    path  = cms.string('HLT_Ele23_WPLoose_Gsf_v\\[0-9]+'),
                                                ),
    Ele27_WPLoose_Gsf                           = cms.PSet(
                                                    path  = cms.string('HLT_Ele27_WPLoose_Gsf_v\\[0-9]+'),
                                                ),
    # double muon
    Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ             = cms.PSet(
                                                    path  = cms.string('HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_v\\[0-9]+'),
                                                ),
    Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ           = cms.PSet(
                                                    path  = cms.string('HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ_v\\[0-9]+'),
                                                ),
    # double electron
    Ele17_Ele12_CaloIdL_TrackIdL_IsoVL_DZ       = cms.PSet(
                                                    path  = cms.string('HLT_Ele17_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v\\[0-9]+'),
                                                ),
    # electron muon
    Mu8_TrkIsoVVL_Ele17_CaloIdL_TrackIdL_IsoVL  = cms.PSet(
                                                    path  = cms.string('HLT_Mu8_TrkIsoVVL_Ele17_CaloIdL_TrackIdL_IsoVL_v\\[0-9]+'),
                                                ),
    Mu17_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL = cms.PSet(
                                                    path  = cms.string('HLT_Mu17_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v\\[0-9]+'),
                                                ),
    # double tau
    DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg      = cms.PSet(
                                                    path  = cms.string('HLT_DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg_v\\[0-9]+'),
                                                ),
    DoubleMediumIsoPFTau40_Trk1_eta2p1_Reg      = cms.PSet(
                                                    path  = cms.string('HLT_DoubleMediumIsoPFTau40_Trk1_eta2p1_Reg_v\\[0-9]+'),
                                                ),
    # muon tau
    IsoMu17_eta2p1_LooseIsoPFTau20              = cms.PSet(
                                                    path  = cms.string('HLT_IsoMu17_eta2p1_LooseIsoPFTau20_v\\[0-9]+'),
                                                ),
    IsoMu20_eta2p1_LooseIsoPFTau20              = cms.PSet(
                                                    path  = cms.string('HLT_IsoMu20_eta2p1_LooseIsoPFTau20_v\\[0-9]+'),
                                                ),
    # electron tau
    Ele22_eta2p1_WPLoose_Gsf_LooseIsoPFTau20    = cms.PSet(
                                                    path  = cms.string('HLT_Ele22_eta2p1_WPLoose_Gsf_LooseIsoPFTau20_v\\[0-9]+'),
                                                ),
    Ele27_eta2p1_WPLoose_Gsf_LooseIsoPFTau20    = cms.PSet(
                                                    path  = cms.string('HLT_Ele27_eta2p1_WPLoose_Gsf_LooseIsoPFTau20_v\\[0-9]+'),
                                                ),
    # triple lepton
    Ele16_Ele12_Ele8_CaloIdL_TrackIdL           = cms.PSet(
                                                    path  = cms.string('HLT_Ele16_Ele12_Ele8_CaloIdL_TrackIdL_v\\[0-9]+'),
                                                ),
    Mu8_DiEle12_CaloIdL_TrackIdL                = cms.PSet(
                                                    path  = cms.string('HLT_Mu8_DiEle12_CaloIdL_TrackIdL_v\\[0-9]+'),
                                                ),
    DiMu9_Ele9_CaloIdL_TrackIdL                 = cms.PSet(
                                                    path  = cms.string('HLT_DiMu9_Ele9_CaloIdL_TrackIdL_v\\[0-9]+'),
                                                ),
    TripleMu_12_10_5                            = cms.PSet(
                                                    path  = cms.string('HLT_TripleMu_12_10_5_v\\[0-9]+'),
                                                ),
)

# filters
filterBranches = cms.PSet(
    HBHENoiseFilter                    = cms.PSet(
                                           path  = cms.string('Flag_HBHENoiseFilter'),
                                       ),
    HBHENoiseIsoFilter                 = cms.PSet(
                                           path  = cms.string('Flag_HBHENoiseIsoFilter'),
                                       ),
    CSCTightHalo2015Filter             = cms.PSet(
                                           path  = cms.string('Flag_CSCTightHalo2015Filter'),
                                       ),
    EcalDeadCellTriggerPrimitiveFilter = cms.PSet(
                                           path  = cms.string('Flag_EcalDeadCellTriggerPrimitiveFilter'),
                                       ),
    goodVertices                       = cms.PSet(
                                           path  = cms.string('Flag_goodVertices'),
                                       ),
    eeBadScFilter                      = cms.PSet(
                                           path  = cms.string('Flag_eeBadScFilter'),
                                       ),
)

# vertices
vertexBranches = commonVertex.clone()

# genParticles
genParticleBranches = commonGenCandidates.clone()
genJetBranches = commonGenJetCandidates.clone()

# electrons
electronBranches = commonPatCandidates.clone(
    # supercluster
    superClusterEta                = cms.vstring('superCluster().eta','F'),
    superClusterPhi                = cms.vstring('superCluster().phi','F'),
    superClusterEnergy             = cms.vstring('superCluster().energy','F'),
    superClusterRawEnergy          = cms.vstring('superCluster().rawEnergy','F'),
    superClusterPreshowerEnergy    = cms.vstring('superCluster().preshowerEnergy','F'),
    superClusterPhiWidth           = cms.vstring('superCluster().phiWidth','F'),
    superClusterEtaWidth           = cms.vstring('superCluster().etaWidth','F'),
    # isolation
    pfChargedHadronIso             = cms.vstring('userIsolation("PfChargedHadronIso")','F'),
    pfNeutralHadronIso             = cms.vstring('userIsolation("PfNeutralHadronIso")','F'),
    pfGammaIso                     = cms.vstring('userIsolation("PfGammaIso")','F'),
    pfPUChargedHadronIso           = cms.vstring('userIsolation("PfPUChargedHadronIso")','F'),
    dr03TkSumPt                    = cms.vstring('dr03TkSumPt()','F'),
    dr03EcalRecHitSumEt            = cms.vstring('dr03EcalRecHitSumEt()','F'),
    dr03HcalTowerSumEt             = cms.vstring('dr03HcalTowerSumEt()','F'),
    effectiveArea                  = cms.vstring('userFloat("EffectiveArea")','F'),
    relPFIsoDeltaBetaR03           = cms.vstring(
        '(userIsolation("PfChargedHadronIso")'
        '+max(userIsolation("PfNeutralHadronIso")'
        '+userIsolation("PfGammaIso")'
        '-0.5*userIsolation("PfPUChargedHadronIso"),0.0))'
        '/pt()',
        'F'
    ),
    relPFIsoRhoR03                 = cms.vstring(
        '(chargedHadronIso()'
        '+max(0.0,neutralHadronIso()'
        '+photonIso()'
        '-userFloat("rho")*userFloat("EffectiveArea")))'
        '/pt()',
        'F'
    ),
    # shower shape / ID variables
    passConversionVeto             = cms.vstring('passConversionVeto()','I'),
    hcalOverEcal                   = cms.vstring('hcalOverEcal','F'),
    hcalDepth1OverEcal             = cms.vstring('hcalDepth1OverEcal','F'),
    hcalDepth2OverEcal             = cms.vstring('hcalDepth2OverEcal','F'),
    sigmaIetaIeta                  = cms.vstring('sigmaIetaIeta','F'),
    deltaEtaSuperClusterTrackAtVtx = cms.vstring('deltaEtaSuperClusterTrackAtVtx','F'),
    deltaPhiSuperClusterTrackAtVtx = cms.vstring('deltaPhiSuperClusterTrackAtVtx','F'),
    fbrem                          = cms.vstring('fbrem','F'),
    eSuperClusterOverP             = cms.vstring('eSuperClusterOverP','F'),
    ecalEnergy                     = cms.vstring('ecalEnergy','F'),
    scE1x5                         = cms.vstring('scE1x5','F'),
    scE2x5Max                      = cms.vstring('scE2x5Max','F'),
    scE5x5                         = cms.vstring('scE5x5','F'),
    missingHits                    = cms.vstring('userInt("missingHits")','I'),
    # charge id
    isGsfCtfScPixChargeConsistent  = cms.vstring('isGsfCtfScPixChargeConsistent','I'),
    isGsfScPixChargeConsistent     = cms.vstring('isGsfScPixChargeConsistent','I'),
    isGsfCtfChargeConsistent       = cms.vstring('isGsfCtfChargeConsistent','I'),
    # ID
    cutBasedVeto                   = cms.vstring('userInt("cutBasedElectronID-Spring15-25ns-V1-standalone-veto")','I'),
    cutBasedLoose                  = cms.vstring('userInt("cutBasedElectronID-Spring15-25ns-V1-standalone-loose")','I'),
    cutBasedMedium                 = cms.vstring('userInt("cutBasedElectronID-Spring15-25ns-V1-standalone-medium")','I'),
    cutBasedTight                  = cms.vstring('userInt("cutBasedElectronID-Spring15-25ns-V1-standalone-tight")','I'),
    heepV60                        = cms.vstring('userInt("heepElectronID-HEEPV60")','I'),
    mvaNonTrigWP90                 = cms.vstring('userInt("mvaEleID-Spring15-25ns-nonTrig-V1-wp90")','I'),
    mvaNonTrigWP80                 = cms.vstring('userInt("mvaEleID-Spring15-25ns-nonTrig-V1-wp80")','I'),
    mvaTrigWP90                    = cms.vstring('userInt("mvaEleID-Spring15-25ns-Trig-V1-wp90")','I'),
    mvaTrigWP80                    = cms.vstring('userInt("mvaEleID-Spring15-25ns-Trig-V1-wp80")','I'),
    mvaNonTrigValues               = cms.vstring('userFloat("ElectronMVAEstimatorRun2Spring15NonTrig25nsV1Values")','F'),
    mvaTrigValues                  = cms.vstring('userFloat("ElectronMVAEstimatorRun2Spring15Trig25nsV1Values")','F'),
    mvaNonTrigCategories           = cms.vstring('userInt("ElectronMVAEstimatorRun2Spring15NonTrig25nsV1Categories")','I'),
    mvaTrigCategories              = cms.vstring('userInt("ElectronMVAEstimatorRun2Spring15Trig25nsV1Categories")','I'),
    wwLoose                        = cms.vstring('userInt("WWLoose")','I'),
    # pv
    dz                             = cms.vstring('userFloat("dz")','F'),
    dxy                            = cms.vstring('userFloat("dxy")','F'),
    dz_beamspot                    = cms.vstring('userFloat("dz_beamspot")','F'),
    dxy_beamspot                   = cms.vstring('userFloat("dxy_beamspot")','F'),
    dz_zero                        = cms.vstring('userFloat("dz_zero")','F'),
    dxy_zero                       = cms.vstring('userFloat("dxy_zero")','F'),
    dB2D                           = cms.vstring('userFloat("dB2D")','F'),
    dB3D                           = cms.vstring('userFloat("dB3D")','F'),
    edB2D                          = cms.vstring('userFloat("edB2D")','F'),
    edB3D                          = cms.vstring('userFloat("edB3D")','F'),
    # trigger matching
    # single electron
    matches_Ele12_CaloIdL_TrackIdL_IsoVL                = cms.vstring('userInt("matches_Ele12_CaloIdL_TrackIdL_IsoVL")','I'),
    matches_Ele17_CaloIdL_TrackIdL_IsoVL                = cms.vstring('userInt("matches_Ele17_CaloIdL_TrackIdL_IsoVL")','I'),
    matches_Ele23_CaloIdL_TrackIdL_IsoVL                = cms.vstring('userInt("matches_Ele23_CaloIdL_TrackIdL_IsoVL")','I'),
    matches_Ele22_eta2p1_WPLoose_Gsf                    = cms.vstring('userInt("matches_Ele22_eta2p1_WPLoose_Gsf")','I'),
    matches_Ele23_WPLoose_Gsf                           = cms.vstring('userInt("matches_Ele23_WPLoose_Gsf")','I'),
    matches_Ele27_WPLoose_Gsf                           = cms.vstring('userInt("matches_Ele27_WPLoose_Gsf")','I'),
    # double electron
    matches_Ele17_Ele12_CaloIdL_TrackIdL_IsoVL_DZ       = cms.vstring('userInt("matches_Ele17_Ele12_CaloIdL_TrackIdL_IsoVL_DZ")','I'),
    # muon electron
    matches_Mu8_TrkIsoVVL_Ele17_CaloIdL_TrackIdL_IsoVL  = cms.vstring('userInt("matches_Mu8_TrkIsoVVL_Ele17_CaloIdL_TrackIdL_IsoVL")','I'),
    matches_Mu17_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL = cms.vstring('userInt("matches_Mu17_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL")','I'),
    # electron tau
    matches_Ele22_eta2p1_WPLoose_Gsf_LooseIsoPFTau20    = cms.vstring('userInt("matches_Ele22_eta2p1_WPLoose_Gsf_LooseIsoPFTau20")','I'),
    matches_Ele27_eta2p1_WPLoose_Gsf_LooseIsoPFTau20    = cms.vstring('userInt("matches_Ele27_eta2p1_WPLoose_Gsf_LooseIsoPFTau20")','I'),
    # multi lepton
    matches_Ele16_Ele12_Ele8_CaloIdL_TrackIdL           = cms.vstring('userInt("matches_Ele16_Ele12_Ele8_CaloIdL_TrackIdL")','I'),
    matches_Mu8_DiEle12_CaloIdL_TrackIdL                = cms.vstring('userInt("matches_Mu8_DiEle12_CaloIdL_TrackIdL")','I'),
    matches_DiMu9_Ele9_CaloIdL_TrackIdL                 = cms.vstring('userInt("matches_DiMu9_Ele9_CaloIdL_TrackIdL")','I'),
    # energy shifts
    pt_electronEnUp                                     = cms.vstring('userCand("ElectronEnUp").pt()','F'),
    eta_electornEnUp                                    = cms.vstring('userCand("ElectronEnUp").eta()','F'),
    phi_electronEnUp                                    = cms.vstring('userCand("ElectronEnUp").phi()','F'),
    energy_electronEnUp                                 = cms.vstring('userCand("ElectronEnUp").energy()','F'),
    pt_electronEnDown                                   = cms.vstring('userCand("ElectronEnDown").pt()','F'),
    eta_electronEnDown                                  = cms.vstring('userCand("ElectronEnDown").eta()','F'),
    phi_electronEnDown                                  = cms.vstring('userCand("ElectronEnDown").phi()','F'),
    energy_electronEnDown                               = cms.vstring('userCand("ElectronEnDown").energy()','F'),
    # uncorrected objects
    pt_uncorrected                                      = cms.vstring('userCand("uncorrected").pt()','F'),
    eta_uncorrected                                     = cms.vstring('userCand("uncorrected").eta()','F'),
    phi_uncorrected                                     = cms.vstring('userCand("uncorrected").phi()','F'),
    energy_uncorrected                                  = cms.vstring('userCand("uncorrected").energy()','F'),
    
)

# muons
muonBranches = commonPatCandidates.clone(
    # type
    isPFMuon                = cms.vstring('isPFMuon','I'),
    isGlobalMuon            = cms.vstring('isGlobalMuon','I'),
    isTrackerMuon           = cms.vstring('isTrackerMuon','I'),
    muonBestTrackType       = cms.vstring('muonBestTrackType','I'),
    pt_tuneP                = cms.vstring('? tunePMuonBestTrack.isNonnull ? tunePMuonBestTrack().pt : -1','F'),
    muonBestTrackType_tuneP = cms.vstring('tunePMuonBestTrackType','I'),
    # isolation
    sumChargedHadronPtR03 = cms.vstring('pfIsolationR03().sumChargedHadronPt','F'),
    sumNeutralHadronEtR03 = cms.vstring('pfIsolationR03().sumNeutralHadronEt','F'),
    sumPhotonEtR03        = cms.vstring('pfIsolationR03().sumPhotonEt','F'),
    sumPUPtR03            = cms.vstring('pfIsolationR03().sumPUPt','F'),
    trackIso              = cms.vstring('trackIso()','F'),
    ecalIso               = cms.vstring('ecalIso()','F'),
    hcalIso               = cms.vstring('hcalIso()','F'),
    sumChargedHadronPtR04 = cms.vstring('pfIsolationR04().sumChargedHadronPt','F'),
    sumNeutralHadronEtR04 = cms.vstring('pfIsolationR04().sumNeutralHadronEt','F'),
    sumPhotonEtR04        = cms.vstring('pfIsolationR04().sumPhotonEt','F'),
    sumPUPtR04            = cms.vstring('pfIsolationR04().sumPUPt','F'),
    relPFIsoDeltaBetaR04  = cms.vstring(
        '(pfIsolationR04().sumChargedHadronPt'
        '+ max(0., pfIsolationR04().sumNeutralHadronEt'
        '+ pfIsolationR04().sumPhotonEt'
        '- 0.5*pfIsolationR04().sumPUPt))'
        '/pt()',
        'F'
    ),
    relPFIsoDeltaBetaR03  = cms.vstring(
        '(pfIsolationR03().sumChargedHadronPt'
        '+ max(0., pfIsolationR03().sumNeutralHadronEt'
        '+ pfIsolationR03().sumPhotonEt'
        '- 0.5*pfIsolationR03().sumPUPt))'
        '/pt()',
        'F'
    ),
    # ID
    isTightMuon           = cms.vstring('userInt("isTightMuon")','I'),
    isHighPtMuon          = cms.vstring('userInt("isHighPtMuon")','I'),
    isSoftMuon            = cms.vstring('userInt("isSoftMuon")','I'),
    isMediumMuon          = cms.vstring('isMediumMuon','I'),
    isLooseMuon           = cms.vstring('isLooseMuon','I'),
    segmentCompatibility  = cms.vstring('userFloat("segmentCompatibility")','F'),
    isGoodMuon            = cms.vstring('userInt("isGoodMuon")','I'),
    highPurityTrack       = cms.vstring('userInt("highPurityTrack")','I'),
    matchedStations       = cms.vstring('numberOfMatchedStations','I'),
    validMuonHits         = cms.vstring('? globalTrack.isNonnull ? globalTrack().hitPattern().numberOfValidMuonHits : -1','I'),
    normalizedChi2        = cms.vstring('? globalTrack.isNonnull ? globalTrack().normalizedChi2 : -1','F'),
    validPixelHits        = cms.vstring('? innerTrack.isNonnull ? innerTrack().hitPattern().numberOfValidPixelHits : -1','I'),
    trackerLayers         = cms.vstring('? innerTrack.isNonnull ? innerTrack().hitPattern().trackerLayersWithMeasurement : -1','I'),
    pixelLayers           = cms.vstring('? innerTrack.isNonnull ? innerTrack().hitPattern().pixelLayersWithMeasurement : -1','I'),
    validTrackerFraction  = cms.vstring('? innerTrack.isNonnull ? innerTrack().validFraction : -1','F'),
    bestTrackPtError      = cms.vstring('? muonBestTrack.isNonnull ? muonBestTrack().ptError : -1','F'),
    bestTrackPt           = cms.vstring('? muonBestTrack.isNonnull ? muonBestTrack().pt : -1','F'),
    trackerStandaloneMatch= cms.vstring('combinedQuality().chi2LocalPosition','F'),
    trackKink             = cms.vstring('combinedQuality().trkKink','F'),
    # pv
    dz                    = cms.vstring('userFloat("dz")','F'),
    dxy                   = cms.vstring('userFloat("dxy")','F'),
    dz_beamspot           = cms.vstring('userFloat("dz_beamspot")','F'),
    dxy_beamspot          = cms.vstring('userFloat("dxy_beamspot")','F'),
    dz_zero               = cms.vstring('userFloat("dz_zero")','F'),
    dxy_zero              = cms.vstring('userFloat("dxy_zero")','F'),
    dB2D                  = cms.vstring('userFloat("dB2D")','F'),
    dB3D                  = cms.vstring('userFloat("dB3D")','F'),
    edB2D                 = cms.vstring('userFloat("edB2D")','F'),
    edB3D                 = cms.vstring('userFloat("edB3D")','F'),
    # corrections
    rochesterPt           = cms.vstring('userFloat("rochesterPt")','F'),
    rochesterEta          = cms.vstring('userFloat("rochesterEta")','F'),
    rochesterPhi          = cms.vstring('userFloat("rochesterPhi")','F'),
    rochesterEnergy       = cms.vstring('userFloat("rochesterEnergy")','F'),
    rochesterError        = cms.vstring('userFloat("rochesterError")','F'),
    # trigger matching
    # single muon
    matches_Mu8_TrkIsoVVL                               = cms.vstring('userInt("matches_Mu8_TrkIsoVVL")','I'),
    matches_Mu17_TrkIsoVVL                              = cms.vstring('userInt("matches_Mu17_TrkIsoVVL")','I'),
    matches_Mu24_TrkIsoVVL                              = cms.vstring('userInt("matches_Mu24_TrkIsoVVL")','I'),
    matches_Mu34_TrkIsoVVL                              = cms.vstring('userInt("matches_Mu34_TrkIsoVVL")','I'),
    matches_IsoMu20                                     = cms.vstring('userInt("matches_IsoMu20")','I'),
    matches_IsoTkMu20                                   = cms.vstring('userInt("matches_IsoTkMu20")','I'),
    matches_IsoMu27                                     = cms.vstring('userInt("matches_IsoMu27")','I'),
    matches_IsoTkMu27                                   = cms.vstring('userInt("matches_IsoTkMu27")','I'),
    matches_Mu45_eta2p1                                 = cms.vstring('userInt("matches_Mu45_eta2p1")','I'),
    matches_Mu50                                        = cms.vstring('userInt("matches_Mu50")','I'),
    # double muon
    matches_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ             = cms.vstring('userInt("matches_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ")','I'),
    matches_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ           = cms.vstring('userInt("matches_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ")','I'),
    # muon electron
    matches_Mu8_TrkIsoVVL_Ele17_CaloIdL_TrackIdL_IsoVL  = cms.vstring('userInt("matches_Mu8_TrkIsoVVL_Ele17_CaloIdL_TrackIdL_IsoVL")','I'),
    matches_Mu17_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL = cms.vstring('userInt("matches_Mu17_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL")','I'),
    # muon tau
    matches_IsoMu17_eta2p1_LooseIsoPFTau20              = cms.vstring('userInt("matches_IsoMu17_eta2p1_LooseIsoPFTau20")','I'),
    matches_IsoMu20_eta2p1_LooseIsoPFTau20              = cms.vstring('userInt("matches_IsoMu20_eta2p1_LooseIsoPFTau20")','I'),
    # multi lepton
    matches_Mu8_DiEle12_CaloIdL_TrackIdL                = cms.vstring('userInt("matches_Mu8_DiEle12_CaloIdL_TrackIdL")','I'),
    matches_DiMu9_Ele9_CaloIdL_TrackIdL                 = cms.vstring('userInt("matches_DiMu9_Ele9_CaloIdL_TrackIdL")','I'),
    matches_TripleMu_12_10_5                            = cms.vstring('userInt("matches_TripleMu_12_10_5")','I'),
    # energy shifts
    pt_muonEnUp                                         = cms.vstring('userCand("MuonEnUp").pt()','F'),
    eta_muonEnUp                                        = cms.vstring('userCand("MuonEnUp").eta()','F'),
    phi_muonEnUp                                        = cms.vstring('userCand("MuonEnUp").phi()','F'),
    energy_muonEnUp                                     = cms.vstring('userCand("MuonEnUp").energy()','F'),
    pt_muonEnDown                                       = cms.vstring('userCand("MuonEnDown").pt()','F'),
    eta_muonEnDown                                      = cms.vstring('userCand("MuonEnDown").eta()','F'),
    phi_muonEnDown                                      = cms.vstring('userCand("MuonEnDown").phi()','F'),
    energy_muonEnDown                                   = cms.vstring('userCand("MuonEnDown").energy()','F'),

)

# taus
tauBranches = commonJetCandidates.clone(
    # Against Electron
    # mva5
    againstElectronVLooseMVA5                       = cms.vstring('tauID("againstElectronVLooseMVA5")','I'), 
    againstElectronLooseMVA5                        = cms.vstring('tauID("againstElectronLooseMVA5")','I'),
    againstElectronMediumMVA5                       = cms.vstring('tauID("againstElectronMediumMVA5")','I'),
    againstElectronTightMVA5                        = cms.vstring('tauID("againstElectronTightMVA5")','I'),
    againstElectronVTightMVA5                       = cms.vstring('tauID("againstElectronVTightMVA5")','I'),
    againstElectronMVA5category                     = cms.vstring('tauID("againstElectronMVA5category")','I'),
    againstElectronMVA5raw                          = cms.vstring('tauID("againstElectronMVA5raw")','F'),
    # mva6
    againstElectronVLooseMVA6                       = cms.vstring('tauID("againstElectronVLooseMVA6")','I'),
    againstElectronLooseMVA6                        = cms.vstring('tauID("againstElectronLooseMVA6")','I'),
    againstElectronMediumMVA6                       = cms.vstring('tauID("againstElectronMediumMVA6")','I'),
    againstElectronTightMVA6                        = cms.vstring('tauID("againstElectronTightMVA6")','I'),
    againstElectronVTightMVA6                       = cms.vstring('tauID("againstElectronVTightMVA6")','I'),
    againstElectronMVA6category                     = cms.vstring('tauID("againstElectronMVA6category")','I'),
    againstElectronMVA6raw                          = cms.vstring('tauID("againstElectronMVA6raw")','F'),
    # Against Muon
    againstMuonLoose3                               = cms.vstring('tauID("againstMuonLoose3")','I'),
    againstMuonTight3                               = cms.vstring('tauID("againstMuonTight3")','I'),
    #  PileupWeighted cut-based isolation discriminators
    byLoosePileupWeightedIsolation3Hits             = cms.vstring('tauID("byLoosePileupWeightedIsolation3Hits")','I'),
    byMediumPileupWeightedIsolation3Hits            = cms.vstring('tauID("byMediumPileupWeightedIsolation3Hits")','I'),
    byTightPileupWeightedIsolation3Hits             = cms.vstring('tauID("byTightPileupWeightedIsolation3Hits")','I'),
    # And the raw values of the isolation:
    byPileupWeightedIsolationRaw3Hits               = cms.vstring('tauID("byPileupWeightedIsolationRaw3Hits")','I'),
    neutralIsoPtSumWeight                           = cms.vstring('tauID("neutralIsoPtSumWeight")','F'),
    footprintCorrection                             = cms.vstring('tauID("footprintCorrection")','F'),
    photonPtSumOutsideSignalCone                    = cms.vstring('tauID("photonPtSumOutsideSignalCone")','F'),
    neutralIsoPtSum                                 = cms.vstring('tauID("neutralIsoPtSum")','F'),
    chargedIsoPtSum                                 = cms.vstring('tauID("chargedIsoPtSum")','F'),
    puCorrPtSum                                     = cms.vstring('tauID("puCorrPtSum")','F'),
    # combined isolation DB corr 3 hits
    byLooseCombinedIsolationDeltaBetaCorr3Hits      = cms.vstring('tauID("byLooseCombinedIsolationDeltaBetaCorr3Hits")','I'),
    byMediumCombinedIsolationDeltaBetaCorr3Hits     = cms.vstring('tauID("byMediumCombinedIsolationDeltaBetaCorr3Hits")', 'I'),
    byTightCombinedIsolationDeltaBetaCorr3Hits      = cms.vstring('tauID("byTightCombinedIsolationDeltaBetaCorr3Hits")','I'),
    byCombinedIsolationDeltaBetaCorrRaw3Hits        = cms.vstring('tauID("byCombinedIsolationDeltaBetaCorrRaw3Hits")','I'),
    # New Tau Isolation Discriminators with cone size DeltaR = 0.3 7_6_x
    byLooseCombinedIsolationDeltaBetaCorr3HitsdR03  = cms.vstring('tauID("byLooseCombinedIsolationDeltaBetaCorr3HitsdR03")','I'),
    byMediumCombinedIsolationDeltaBetaCorr3HitsdR03 = cms.vstring('tauID("byMediumCombinedIsolationDeltaBetaCorr3HitsdR03")', 'I'),
    byTightCombinedIsolationDeltaBetaCorr3HitsdR03  = cms.vstring('tauID("byTightCombinedIsolationDeltaBetaCorr3HitsdR03")','I'),
    # BDT based tau ID discriminator based on isolation Pt sums plus tau lifetime information, trained on 1-prong, "2-prong" and 3-prong tau candidates 
    byVLooseIsolationMVA3newDMwLT                   = cms.vstring('tauID("byVLooseIsolationMVA3newDMwLT")','I'),
    byLooseIsolationMVA3newDMwLT                    = cms.vstring('tauID("byLooseIsolationMVA3newDMwLT")','I'),
    byMediumIsolationMVA3newDMwLT                   = cms.vstring('tauID("byMediumIsolationMVA3newDMwLT")', 'I'),
    byTightIsolationMVA3newDMwLT                    = cms.vstring('tauID("byTightIsolationMVA3newDMwLT")','I'),
    byVTightIsolationMVA3newDMwLT                   = cms.vstring('tauID("byVTightIsolationMVA3newDMwLT")', 'I'),
    byVVTightIsolationMVA3newDMwLT                  = cms.vstring('tauID("byVVTightIsolationMVA3newDMwLT")', 'I'),
    byIsolationMVA3newDMwLTraw                      = cms.vstring('tauID("byIsolationMVA3newDMwLTraw")','F'),
    # BDT based tau ID discriminator based on isolation Pt sums plus tau lifetime information, trained on 1-prong and 3-prong tau candidates 
    byVLooseIsolationMVA3oldDMwLT                   = cms.vstring('tauID("byVLooseIsolationMVA3oldDMwLT")', 'I'),
    byLooseIsolationMVA3oldDMwLT                    = cms.vstring('tauID("byLooseIsolationMVA3oldDMwLT")', 'I'),
    byMediumIsolationMVA3oldDMwLT                   = cms.vstring('tauID("byMediumIsolationMVA3oldDMwLT")', 'I'),
    byTightIsolationMVA3oldDMwLT                    = cms.vstring('tauID("byTightIsolationMVA3oldDMwLT")', 'I'),
    byVTightIsolationMVA3oldDMwLT                   = cms.vstring('tauID("byVTightIsolationMVA3oldDMwLT")', 'I'),
    byVVTightIsolationMVA3oldDMwLT                  = cms.vstring('tauID("byVVTightIsolationMVA3oldDMwLT")','I'),
    byIsolationMVA3oldDMwLTraw                      = cms.vstring('tauID("byIsolationMVA3oldDMwLTraw")', 'F'),
    # MVA based tau isolation discriminators new 7_6_x
    # With Old Decay Mode reconstruction:
    byLooseIsolationMVArun2v1DBoldDMwLT             = cms.vstring('tauID("byLooseIsolationMVArun2v1DBoldDMwLT")','I'),
    byMediumIsolationMVArun2v1DBoldDMwLT            = cms.vstring('tauID("byMediumIsolationMVArun2v1DBoldDMwLT")','I'),
    byTightIsolationMVArun2v1DBoldDMwLT             = cms.vstring('tauID("byTightIsolationMVArun2v1DBoldDMwLT")','I'),
    byVTightIsolationMVArun2v1DBoldDMwLT            = cms.vstring('tauID("byVTightIsolationMVArun2v1DBoldDMwLT")','I'),
    # Same but with Iso dR = 0.3
    byLooseIsolationMVArun2v1DBdR03oldDMwLT         = cms.vstring('tauID("byLooseIsolationMVArun2v1DBdR03oldDMwLT")','I'),
    byMediumIsolationMVArun2v1DBdR03oldDMwLT        = cms.vstring('tauID("byMediumIsolationMVArun2v1DBdR03oldDMwLT")','I'),
    byTightIsolationMVArun2v1DBdR03oldDMwLT         = cms.vstring('tauID("byTightIsolationMVArun2v1DBdR03oldDMwLT")','I'),
    byVTightIsolationMVArun2v1DBdR03oldDMwLT        = cms.vstring('tauID("byVTightIsolationMVArun2v1DBdR03oldDMwLT")','I'),
    #With New Decay Mode Reconstruction:
    byLooseIsolationMVArun2v1DBnewDMwLT             = cms.vstring('tauID("byLooseIsolationMVArun2v1DBnewDMwLT")','I'),
    byMediumIsolationMVArun2v1DBnewDMwLT            = cms.vstring('tauID("byMediumIsolationMVArun2v1DBnewDMwLT")','I'),
    byTightIsolationMVArun2v1DBnewDMwLT             = cms.vstring('tauID("byTightIsolationMVArun2v1DBnewDMwLT")','I'),
    byVTightIsolationMVArun2v1DBnewDMwLT            = cms.vstring('tauID("byVTightIsolationMVArun2v1DBnewDMwLT")','I'),
    #MVA tau ID using Pileup Weighted isolation: new 7_6_x
    #With Old Decay Mode reconstruction:
    byLooseIsolationMVArun2v1PWoldDMwLT             = cms.vstring('tauID("byLooseIsolationMVArun2v1PWoldDMwLT")','I'),
    byMediumIsolationMVArun2v1PWoldDMwLT            = cms.vstring('tauID("byMediumIsolationMVArun2v1PWoldDMwLT")','I'),
    byTightIsolationMVArun2v1PWoldDMwLT             = cms.vstring('tauID("byTightIsolationMVArun2v1PWoldDMwLT")','I'),
    byVTightIsolationMVArun2v1PWoldDMwLT            = cms.vstring('tauID("byVTightIsolationMVArun2v1PWoldDMwLT")','I'),
    # Same but with Iso dR = 0.3
    byLooseIsolationMVArun2v1PWdR03oldDMwLT         = cms.vstring('tauID("byLooseIsolationMVArun2v1PWdR03oldDMwLT")','I'),
    byMediumIsolationMVArun2v1PWdR03oldDMwLT        = cms.vstring('tauID("byMediumIsolationMVArun2v1PWdR03oldDMwLT")','I'),
    byTightIsolationMVArun2v1PWdR03oldDMwLT         = cms.vstring('tauID("byTightIsolationMVArun2v1PWdR03oldDMwLT")','I'),
    byVTightIsolationMVArun2v1PWdR03oldDMwLT        = cms.vstring('tauID("byVTightIsolationMVArun2v1PWdR03oldDMwLT")','I'),
    #With New Decay Mode Reconstruction:
    byLooseIsolationMVArun2v1PWnewDMwLT             = cms.vstring('tauID("byLooseIsolationMVArun2v1PWnewDMwLT")','I'),
    byMediumIsolationMVArun2v1PWnewDMwLT            = cms.vstring('tauID("byMediumIsolationMVArun2v1PWnewDMwLT")','I'),
    byTightIsolationMVArun2v1PWnewDMwLT             = cms.vstring('tauID("byTightIsolationMVArun2v1PWnewDMwLT")','I'),
    byVTightIsolationMVArun2v1PWnewDMwLT            = cms.vstring('tauID("byVTightIsolationMVArun2v1PWnewDMwLT")','I'),
    # DecayModeFinding
    decayModeFinding                                = cms.vstring('tauID("decayModeFinding")','I'),
    decayModeFindingNewDMs                          = cms.vstring('tauID("decayModeFindingNewDMs")','I'),
    # pv
    dz                                              = cms.vstring('userFloat("dz")','F'),
    dxy                                             = cms.vstring('userFloat("dxy")','F'),
    dz_beamspot                                     = cms.vstring('userFloat("dz_beamspot")','F'),
    dxy_beamspot                                    = cms.vstring('userFloat("dxy_beamspot")','F'),
    dz_zero                                         = cms.vstring('userFloat("dz_zero")','F'),
    dxy_zero                                        = cms.vstring('userFloat("dxy_zero")','F'),
    # trigger matching
    # double tau
    matches_DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg   = cms.vstring('userInt("matches_DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg")','I'),
    matches_DoubleMediumIsoPFTau40_Trk1_eta2p1_Reg   = cms.vstring('userInt("matches_DoubleMediumIsoPFTau40_Trk1_eta2p1_Reg")','I'),
    # muon tau
    matches_IsoMu17_eta2p1_LooseIsoPFTau20           = cms.vstring('userInt("matches_IsoMu17_eta2p1_LooseIsoPFTau20")','I'),
    matches_IsoMu20_eta2p1_LooseIsoPFTau20           = cms.vstring('userInt("matches_IsoMu20_eta2p1_LooseIsoPFTau20")','I'),
    # electron tau
    matches_Ele22_eta2p1_WPLoose_Gsf_LooseIsoPFTau20 = cms.vstring('userInt("matches_Ele22_eta2p1_WPLoose_Gsf_LooseIsoPFTau20")','I'),
    matches_Ele27_eta2p1_WPLoose_Gsf_LooseIsoPFTau20 = cms.vstring('userInt("matches_Ele27_eta2p1_WPLoose_Gsf_LooseIsoPFTau20")','I'),
    # energy shifts
    pt_tauEnUp                                       = cms.vstring('userCand("TauEnUp").pt()','F'),
    eta_tauEnUp                                      = cms.vstring('userCand("TauEnUp").eta()','F'),
    phi_tauEnUp                                      = cms.vstring('userCand("TauEnUp").phi()','F'),
    energy_tauEnUp                                   = cms.vstring('userCand("TauEnUp").energy()','F'),
    pt_tauEnDown                                     = cms.vstring('userCand("TauEnDown").pt()','F'),
    eta_tauEnDown                                    = cms.vstring('userCand("TauEnDown").eta()','F'),
    phi_tauEnDown                                    = cms.vstring('userCand("TauEnDown").phi()','F'),
    energy_tauEnDown                                 = cms.vstring('userCand("TauEnDown").energy()','F'),
)

# photons
photonBranches = commonPatCandidates.clone(

)

# jets
jetBranches = commonJetCandidates.clone(
    # btagging
    pfJetProbabilityBJetTags                     = cms.vstring('bDiscriminator("pfJetProbabilityBJetTags")','F'),
    pfCombinedInclusiveSecondaryVertexV2BJetTags = cms.vstring('bDiscriminator("pfCombinedInclusiveSecondaryVertexV2BJetTags")','F'),
    pfCombinedMVAV2BJetTags                      = cms.vstring('bDiscriminator("pfCombinedMVAV2BJetTags")','F'),
    passJPL                                      = cms.vstring('? bDiscriminator("pfJetProbabilityBJetTags")>0.245 ? 1 : 0','I'),
    passJPM                                      = cms.vstring('? bDiscriminator("pfJetProbabilityBJetTags")>0.515 ? 1 : 0','I'),
    passJPT                                      = cms.vstring('? bDiscriminator("pfJetProbabilityBJetTags")>0.760 ? 1 : 0','I'),
    passCSVv2L                                   = cms.vstring('? bDiscriminator("pfCombinedInclusiveSecondaryVertexV2BJetTags")>0.460 ? 1 : 0','I'),
    passCSVv2M                                   = cms.vstring('? bDiscriminator("pfCombinedInclusiveSecondaryVertexV2BJetTags")>0.800 ? 1 : 0','I'),
    passCSVv2T                                   = cms.vstring('? bDiscriminator("pfCombinedInclusiveSecondaryVertexV2BJetTags")>0.935 ? 1 : 0','I'),
    passCMVAv2L                                  = cms.vstring('? bDiscriminator("pfCombinedMVAV2BJetTags")>-0.715 ? 1 : 0','I'),
    passCMVAv2M                                  = cms.vstring('? bDiscriminator("pfCombinedMVAV2BJetTags")>0.185 ? 1 : 0','I'),
    passCMVAv2T                                  = cms.vstring('? bDiscriminator("pfCombinedMVAV2BJetTags")>0.875 ? 1 : 0','I'),
    # flavor
    partonFlavour                                = cms.vstring('partonFlavour','I'),
    # id variables
    neutralHadronEnergyFraction                  = cms.vstring('neutralHadronEnergyFraction','F'),
    neutralEmEnergyFraction                      = cms.vstring('neutralEmEnergyFraction','F'),
    chargedHadronEnergyFraction                  = cms.vstring('chargedHadronEnergyFraction','F'),
    muonEnergyFraction                           = cms.vstring('muonEnergyFraction','F'),
    chargedEmEnergyFraction                      = cms.vstring('chargedEmEnergyFraction','F'),
    chargedMultiplicity                          = cms.vstring('chargedMultiplicity','I'),
    neutralMultiplicity                          = cms.vstring('neutralMultiplicity','I'),
    # ids
    isLoose                                      = cms.vstring('userInt("idLoose")','I'),
    isTight                                      = cms.vstring('userInt("idTight")','I'),
    isTightLepVeto                               = cms.vstring('userInt("idTightLepVeto")','I'),
    puID                                         = cms.vstring('userInt("puID")','I'),
    # energy shifts
    pt_jetEnUp                                   = cms.vstring('userCand("JetEnUp").pt()','F'),
    eta_jetEnUp                                  = cms.vstring('userCand("JetEnUp").eta()','F'),
    phi_jetEnUp                                  = cms.vstring('userCand("JetEnUp").phi()','F'),
    energy_jetEnUp                               = cms.vstring('userCand("JetEnUp").energy()','F'),
    pt_jetEnDown                                 = cms.vstring('userCand("JetEnDown").pt()','F'),
    eta_jetEnDown                                = cms.vstring('userCand("JetEnDown").eta()','F'),
    phi_jetEnDown                                = cms.vstring('userCand("JetEnDown").phi()','F'),
    energy_jetEnDown                             = cms.vstring('userCand("JetEnDown").energy()','F'),
)

# mets
metBranches = commonMet.clone(
    uncorEt               = cms.vstring('uncorPt','F'),
    uncorPhi              = cms.vstring('uncorPhi','F'),
    # shifts
    et_jetResUp           = cms.vstring('userCand("JetResUp").pt()','F'),
    et_jetResDown         = cms.vstring('userCand("JetResDown").pt()','F'),
    et_jetEnUp            = cms.vstring('userCand("JetEnUp").pt()','F'),
    et_jetEnDown          = cms.vstring('userCand("JetEnDown").pt()','F'),
    et_muonEnUp           = cms.vstring('userCand("MuonEnUp").pt()','F'),
    et_muonEnDown         = cms.vstring('userCand("MuonEnDown").pt()','F'),
    et_electronEnUp       = cms.vstring('userCand("ElectronEnUp").pt()','F'),
    et_electronEnDown     = cms.vstring('userCand("ElectronEnDown").pt()','F'),
    et_tauEnUp            = cms.vstring('userCand("TauEnUp").pt()','F'),
    et_tauEnDown          = cms.vstring('userCand("TauEnDown").pt()','F'),
    et_unclusteredEnUp    = cms.vstring('userCand("UnclusteredEnUp").pt()','F'),
    et_unclusteredEnDown  = cms.vstring('userCand("UnclusteredEnDown").pt()','F'),
    et_photonEnUp         = cms.vstring('userCand("PhotonEnUp").pt()','F'),
    et_photonEnDown       = cms.vstring('userCand("PhotonEnDown").pt()','F'),
    phi_jetResUp          = cms.vstring('userCand("JetResUp").phi()','F'),
    phi_jetResDown        = cms.vstring('userCand("JetResDown").phi()','F'),
    phi_jetEnUp           = cms.vstring('userCand("JetEnUp").phi()','F'),
    phi_jetEnDown         = cms.vstring('userCand("JetEnDown").phi()','F'),
    phi_muonEnUp          = cms.vstring('userCand("MuonEnUp").phi()','F'),
    phi_muonEnDown        = cms.vstring('userCand("MuonEnDown").phi()','F'),
    phi_electronEnUp      = cms.vstring('userCand("ElectronEnUp").phi()','F'),
    phi_electronEnDown    = cms.vstring('userCand("ElectronEnDown").phi()','F'),
    phi_tauEnUp           = cms.vstring('userCand("TauEnUp").phi()','F'),
    phi_tauEnDown         = cms.vstring('userCand("TauEnDown").phi()','F'),
    phi_unclusteredEnUp   = cms.vstring('userCand("UnclusteredEnUp").phi()','F'),
    phi_unclusteredEnDown = cms.vstring('userCand("UnclusteredEnDown").phi()','F'),
    phi_photonEnUp        = cms.vstring('userCand("PhotonEnUp").phi()','F'),
    phi_photonEnDown      = cms.vstring('userCand("PhotonEnDown").phi()','F'),
)
