import FWCore.ParameterSet.Config as cms

def customizeTaus(process,coll,**kwargs):
    '''Customize taus'''
    isMC = kwargs.pop('isMC',False)
    tSrc = coll['taus']
    rhoSrc = coll['rho']
    pvSrc = coll['vertices']
    genSrc = coll['genParticles']

    # customization path
    process.tauCustomization = cms.Path()

    #################
    ### embed rho ###
    #################
    process.tRho = cms.EDProducer(
        "TauRhoEmbedder",
        src = cms.InputTag(tSrc),
        rhoSrc = cms.InputTag(rhoSrc),
        label = cms.string("rho"),
    )
    tSrc = 'tRho'

    process.tauCustomization *= process.tRho

    ################
    ### embed pv ###
    ################
    process.tPV = cms.EDProducer(
        "TauIpEmbedder",
        src = cms.InputTag(tSrc),
        vertexSrc = cms.InputTag(pvSrc),
        beamspotSrc = cms.InputTag("offlineBeamSpot"),
    )
    tSrc = 'tPV'

    process.tauCustomization *= process.tPV

    ##############################
    ### embed trigger matching ###
    ##############################
    process.tTrig = cms.EDProducer(
        "TauHLTMatchEmbedder",
        src = cms.InputTag(tSrc),
        triggerResults = cms.InputTag('TriggerResults', '', 'HLT'),
        triggerObjects = cms.InputTag("selectedPatTrigger"),
        deltaR = cms.double(0.5),
        labels = cms.vstring(
            # double tau
            'matches_DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg',
            'matches_DoubleMediumIsoPFTau40_Trk1_eta2p1_Reg',
            # muon tau
            'matches_IsoMu17_eta2p1_LooseIsoPFTau20',
            'matches_IsoMu20_eta2p1_LooseIsoPFTau20',
            # electron tau
            'matches_Ele22_eta2p1_WPLoose_Gsf_LooseIsoPFTau20',
            'matches_Ele27_eta2p1_WPLoose_Gsf_LooseIsoPFTau20',
        ),
        paths = cms.vstring(
            # double tau
            'HLT_DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg_v\\[0-9]+',
            'HLT_DoubleMediumIsoPFTau40_Trk1_eta2p1_Reg_v\\[0-9]+',
            # muon tau
            'HLT_IsoMu17_eta2p1_LooseIsoPFTau20_v\\[0-9]+',
            'HLT_IsoMu20_eta2p1_LooseIsoPFTau20_v\\[0-9]+',
            # electron tau
            'HLT_Ele22_eta2p1_WPLoose_Gsf_LooseIsoPFTau20_v\\[0-9]+',
            'HLT_Ele27_eta2p1_WPLoose_Gsf_LooseIsoPFTau20_v\\[0-9]+',
        ),
    )
    tSrc = 'tTrig'

    process.tauCustomization *= process.tTrig

    ##########################
    ### embed tau gen jets ###
    ##########################
    if isMC:
        from PhysicsTools.JetMCAlgos.TauGenJets_cfi import tauGenJets
        process.tauGenJets = tauGenJets.clone(GenParticles = cms.InputTag(genSrc))
        process.tauCustomization *= process.tauGenJets

        process.tGenJetMatching = cms.EDProducer(
            "TauGenJetEmbedder",
            src = cms.InputTag(tSrc),
            genJets = cms.InputTag("tauGenJets"),
            excludeLeptons = cms.bool(True),
            deltaR = cms.double(0.5),
        )
        tSrc = "tGenJetMatching"
        process.tauCustomization *= process.tGenJetMatching


    # add to schedule
    process.schedule.append(process.tauCustomization)

    coll['taus'] = tSrc

    return coll
