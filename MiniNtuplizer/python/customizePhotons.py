import FWCore.ParameterSet.Config as cms

def customizePhotons(process,pSrc,**kwargs):
    '''Customize photons'''
    rhoSrc = kwargs.pop('rhoSrc','')

    # customization path
    process.photonCustomization = cms.Path()

    #################
    ### embed rho ###
    #################
    process.pRho = cms.EDProducer(
        "PhotonRhoEmbedder",
        src = cms.InputTag(pSrc),
        rhoSrc = cms.InputTag(rhoSrc),
        label = cms.string("rho"),
    )
    pSrc = 'pRho'

    process.photonCustomization *= process.pRho

    # add to schedule
    process.schedule.append(process.photonCustomization)

    return pSrc
