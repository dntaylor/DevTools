import FWCore.ParameterSet.Config as cms

def customizeTaus(process,tSrc,**kwargs):
    '''Customize taus'''
    rhoSrc = kwargs.pop('rhoSrc','')
    pvSrc = kwargs.pop('pvSrc','')

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
    )
    tSrc = 'tPV'

    process.tauCustomization *= process.tPV

    # add to schedule
    process.schedule.append(process.tauCustomization)

    return tSrc
