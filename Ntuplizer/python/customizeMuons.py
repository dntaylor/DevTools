import FWCore.ParameterSet.Config as cms

def customizeMuons(process,coll,**kwargs):
    '''Customize muons'''
    isMC = kwargs.pop('isMC',False)
    mSrc = coll['muons']
    rhoSrc = coll['rho']
    pvSrc = coll['vertices']

    # customization path
    process.muonCustomization = cms.Path()

    ###################################
    ### embed rochester corrections ###
    ###################################
    process.mRoch = cms.EDProducer(
        "RochesterCorrectionEmbedder",
        src = cms.InputTag(mSrc),
        isData = cms.bool(not isMC),
    )
    mSrc = 'mRoch'

    process.muonCustomization *= process.mRoch

    #####################
    ### embed muon id ###
    #####################
    process.mID = cms.EDProducer(
        "MuonIdEmbedder",
        src = cms.InputTag(mSrc),
        vertexSrc = cms.InputTag(pvSrc),
    )
    mSrc = 'mID'

    process.muonCustomization *= process.mID

    #################
    ### embed rho ###
    #################
    process.mRho = cms.EDProducer(
        "MuonRhoEmbedder",
        src = cms.InputTag(mSrc),
        rhoSrc = cms.InputTag(rhoSrc),
        label = cms.string("rho"),
    )
    mSrc = 'mRho'

    process.muonCustomization *= process.mRho

    ################
    ### embed pv ###
    ################
    process.mPV = cms.EDProducer(
        "MuonIpEmbedder",
        src = cms.InputTag(mSrc),
        vertexSrc = cms.InputTag(pvSrc),
        beamspotSrc = cms.InputTag("offlineBeamSpot"),
    )
    mSrc = 'mPV'

    process.muonCustomization *= process.mPV

    ##############################
    ### embed trigger matching ###
    ##############################
    process.mTrig = cms.EDProducer(
        "MuonHLTMatchEmbedder",
        src = cms.InputTag(mSrc),
        triggerResults = cms.InputTag('TriggerResults', '', 'HLT'),
        triggerObjects = cms.InputTag("selectedPatTrigger"),
        deltaR = cms.double(0.5),
        labels = cms.vstring(
            # single muon
            'matches_Mu8_TrkIsoVVL',
            'matches_Mu17_TrkIsoVVL',
            'matches_Mu24_TrkIsoVVL',
            'matches_Mu34_TrkIsoVVL',
            'matches_IsoMu20',
            'matches_IsoTkMu20',
            'matches_IsoMu27',
            'matches_IsoTkMu27',
            'matches_Mu45_eta2p1',
            'matches_Mu50',
            # double muon
            'matches_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ',
            'matches_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ',
            # muon electron
            'matches_Mu8_TrkIsoVVL_Ele17_CaloIdL_TrackIdL_IsoVL',
            'matches_Mu17_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL',
            # muon tau
            'matches_IsoMu17_eta2p1_LooseIsoPFTau20',
            'matches_IsoMu20_eta2p1_LooseIsoPFTau20',
            # multi lepton
            'matches_Mu8_DiEle12_CaloIdL_TrackIdL',
            'matches_DiMu9_Ele9_CaloIdL_TrackIdL',
            'matches_TripleMu_12_10_5',
        ),
        paths = cms.vstring(
            # single muon
            'HLT_Mu8_TrkIsoVVL_v\\[0-9]+',
            'HLT_Mu17_TrkIsoVVL_v\\[0-9]+',
            'HLT_Mu24_TrkIsoVVL_v\\[0-9]+',
            'HLT_Mu34_TrkIsoVVL_v\\[0-9]+',
            'HLT_IsoMu20_v\\[0-9]+',
            'HLT_IsoTkMu20_v\\[0-9]+',
            'HLT_IsoMu27_v\\[0-9]+',
            'HLT_IsoTkMu27_v\\[0-9]+',
            'HLT_Mu45_eta2p1_v\\[0-9]+',
            'HLT_Mu50_v\\[0-9]+',
            # double muon
            'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_v\\[0-9]+',
            'HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ_v\\[0-9]+',
            # muon electron
            'HLT_Mu8_TrkIsoVVL_Ele17_CaloIdL_TrackIdL_IsoVL_v\\[0-9]+',
            'HLT_Mu17_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v\\[0-9]+',
            # muon tau
            'HLT_IsoMu17_eta2p1_LooseIsoPFTau20_v\\[0-9]+',
            'HLT_IsoMu20_eta2p1_LooseIsoPFTau20_v\\[0-9]+',
            # multi lepton
            'HLT_Mu8_DiEle12_CaloIdL_TrackIdL_v\\[0-9]+',
            'HLT_DiMu9_Ele9_CaloIdL_TrackIdL_v\\[0-9]+',
            'HLT_TripleMu_12_10_5_v\\[0-9]+',
        ),
    )
    mSrc = 'mTrig'

    process.muonCustomization *= process.mTrig

    # add to schedule
    process.schedule.append(process.muonCustomization)

    coll['muons'] = mSrc

    return coll
