import FWCore.ParameterSet.Config as cms

def customizeMuons(process,mSrc,**kwargs):
    '''Customize muons'''
    rhoSrc = kwargs.pop('rhoSrc','')
    pvSrc = kwargs.pop('pvSrc','')

    # customization path
    process.muonCustomization = cms.Path()

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
    )
    mSrc = 'mPV'

    process.muonCustomization *= process.mPV

    # add to schedule
    process.schedule.append(process.muonCustomization)

    return mSrc
