import FWCore.ParameterSet.Config as cms

def customizeJets(process,jSrc,**kwargs):
    '''Customize jets'''
    rhoSrc = kwargs.pop('rhoSrc','')

    # customization path
    process.jetCustomization = cms.Path()

    ######################
    ### recorrect jets ###
    ######################
    from PhysicsTools.PatAlgos.producersLayer1.jetUpdater_cff import patJetCorrFactorsUpdated
    process.patJetCorrFactorsReapplyJEC = patJetCorrFactorsUpdated.clone(
        src = cms.InputTag(jSrc),
        levels = ['L1FastJet', 
                  'L2Relative', 
                  'L3Absolute'],
        payload = 'AK4PFchs' 
    )

    from PhysicsTools.PatAlgos.producersLayer1.jetUpdater_cff import patJetsUpdated
    process.patJetsReapplyJEC = patJetsUpdated.clone(
        jetSource = cms.InputTag(jSrc),
        jetCorrFactorsSource = cms.VInputTag(cms.InputTag("patJetCorrFactorsReapplyJEC"))
    )

    process.jetCustomization *= process.patJetCorrFactorsReapplyJEC
    process.jetCustomization *= process.patJetsReapplyJEC
    jSrc = "patJetsReapplyJEC"

    #################
    ### embed ids ###
    #################
    process.jID = cms.EDProducer(
        "JetIdEmbedder",
        src = cms.InputTag(jSrc),
    )
    process.jetCustomization *= process.jID
    jSrc = "jID"

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
