import FWCore.ParameterSet.Config as cms

def customizeJets(process,jSrc,**kwargs):
    '''Customize jets'''
    rhoSrc = kwargs.pop('rhoSrc','')

    # customization path
    process.jetCustomization = cms.Path()

    #################
    ### embed rho ###
    #################
    process.jRho = cms.EDProducer(
        "JetRhoEmbedder",
        src = cms.InputTag(jSrc),
        rhoSrc = cms.InputTag(rhoSrc),
        label = cms.string("rho"),
    )
    jSrc = 'jRho'

    process.jetCustomization *= process.jRho

    # add to schedule
    process.schedule.append(process.jetCustomization)

    return jSrc
