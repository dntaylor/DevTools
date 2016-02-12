import FWCore.ParameterSet.Config as cms

def customizeTaus(process,tSrc,**kwargs):
    '''Customize taus'''
    rhoSrc = kwargs.pop('rhoSrc','')

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

    # add to schedule
    process.schedule.append(process.tauCustomization)

    return tSrc
