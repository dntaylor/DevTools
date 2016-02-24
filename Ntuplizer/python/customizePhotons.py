import FWCore.ParameterSet.Config as cms

def customizePhotons(process,coll,**kwargs):
    '''Customize photons'''
    isMC = kwargs.pop('isMC',False)
    pSrc = coll['photons']
    rhoSrc = coll['rho']

    # customization path
    process.photonCustomization = cms.Path()

    ###################################
    ### scale and smear corrections ###
    ###################################
    #process.load('EgammaAnalysis.ElectronTools.calibratedPhotonsRun2_cfi')
    #process.calibratedPatPhotons.photons = pSrc
    #process.calibratedPatPhotons.isMC = isMC
    #process.photonCustomization *= process.calibratedPatPhotons
    #pSrc = 'calibratedPatPhotons'

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

    coll['photons'] = pSrc

    return coll
