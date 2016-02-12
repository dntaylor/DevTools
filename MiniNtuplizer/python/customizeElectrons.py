import FWCore.ParameterSet.Config as cms

def customizeElectrons(process,eSrc,**kwargs):
    '''Customize electrons'''
    rhoSrc = kwargs.pop('rhoSrc','')
    # customization path
    process.electronCustomization = cms.Path()

    #################
    ### embed VID ###
    #################
    from PhysicsTools.SelectorUtils.tools.vid_id_tools import switchOnVIDElectronIdProducer, setupAllVIDIdsInModule, DataFormat, setupVIDElectronSelection
    switchOnVIDElectronIdProducer(process, DataFormat.MiniAOD)
    
    # define which IDs we want to produce
    my_id_modules = [
        'RecoEgamma.ElectronIdentification.Identification.cutBasedElectronID_Spring15_25ns_V1_cff',
        'RecoEgamma.ElectronIdentification.Identification.heepElectronID_HEEPV60_cff',
        'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Spring15_25ns_nonTrig_V1_cff',
        'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Spring15_25ns_Trig_V1_cff',
    ]
    
    # add them to the VID producer
    for idmod in my_id_modules:
        setupAllVIDIdsInModule(process,idmod,setupVIDElectronSelection)

    # update the collection
    process.egmGsfElectronIDs.physicsObjectSrc = cms.InputTag(eSrc)
    process.electronMVAValueMapProducer.srcMiniAOD = cms.InputTag(eSrc)
    process.electronRegressionValueMapProducer.srcMiniAOD = cms.InputTag(eSrc)

    idDecisionLabels = [
        'cutBasedElectronID-Spring15-25ns-V1-standalone-veto',
        'cutBasedElectronID-Spring15-25ns-V1-standalone-loose',
        'cutBasedElectronID-Spring15-25ns-V1-standalone-medium',
        'cutBasedElectronID-Spring15-25ns-V1-standalone-tight',
        'heepElectronID-HEEPV60',
        'mvaEleID-Spring15-25ns-nonTrig-V1-wp80',
        'mvaEleID-Spring15-25ns-nonTrig-V1-wp90',
        'mvaEleID-Spring15-25ns-Trig-V1-wp90',
        'mvaEleID-Spring15-25ns-Trig-V1-wp80',
    ]
    idDecisionTags = [
        cms.InputTag('egmGsfElectronIDs:cutBasedElectronID-Spring15-25ns-V1-standalone-veto'),
        cms.InputTag('egmGsfElectronIDs:cutBasedElectronID-Spring15-25ns-V1-standalone-loose'),
        cms.InputTag('egmGsfElectronIDs:cutBasedElectronID-Spring15-25ns-V1-standalone-medium'),
        cms.InputTag('egmGsfElectronIDs:cutBasedElectronID-Spring15-25ns-V1-standalone-tight'),
        cms.InputTag('egmGsfElectronIDs:heepElectronID-HEEPV60'),
        cms.InputTag('egmGsfElectronIDs:mvaEleID-Spring15-25ns-nonTrig-V1-wp80'),
        cms.InputTag('egmGsfElectronIDs:mvaEleID-Spring15-25ns-nonTrig-V1-wp90'),
        cms.InputTag('egmGsfElectronIDs:mvaEleID-Spring15-25ns-Trig-V1-wp90'),
        cms.InputTag('egmGsfElectronIDs:mvaEleID-Spring15-25ns-Trig-V1-wp80'),
    ]
    mvaValueLabels = [
        #"ElectronMVAEstimatorRun2Spring15NonTrig25nsV1Values",
        #"ElectronMVAEstimatorRun2Spring15Trig25nsV1Values",
    ]
    mvaValueTags = [
        #cms.InputTag("electronMVAValueMapProducer:ElectronMVAEstimatorRun2Spring15NonTrig25nsV1Values"),
        #cms.InputTag("electronMVAValueMapProducer:ElectronMVAEstimatorRun2Spring15Trig25nsV1Values"),
    ]
    mvaCategoryLabels = [
        #"ElectronMVAEstimatorRun2Spring15NonTrig25nsV1Categories",
        #"ElectronMVAEstimatorRun2Spring15Trig25nsV1Categories",
    ]
    mvaCategoryTags = [
        #cms.InputTag("electronMVAValueMapProducer:ElectronMVAEstimatorRun2Spring15NonTrig25nsV1Categories"),
        #cms.InputTag("electronMVAValueMapProducer:ElectronMVAEstimatorRun2Spring15Trig25nsV1Categories"),
    ]

    process.eidEmbedder = cms.EDProducer(
        "ElectronVIDEmbedder",
        src=cms.InputTag(eSrc),
        idLabels = cms.vstring(*idDecisionLabels),        # labels for bool maps
        ids = cms.VInputTag(*idDecisionTags),             # bool maps
        valueLabels = cms.vstring(*mvaValueLabels),       # labels for float maps
        values = cms.VInputTag(*mvaValueTags),            # float maps
        categoryLabels = cms.vstring(*mvaCategoryLabels), # labels for int maps
        categories = cms.VInputTag(*mvaCategoryTags),     # int maps
    )
    eSrc = 'eidEmbedder'

    process.electronCustomization *= process.egmGsfElectronIDSequence
    process.electronCustomization *= process.eidEmbedder

    #############################
    ### embed effective areas ###
    #############################
    eaFile = 'RecoEgamma/ElectronIdentification/data/Spring15/effAreaElectrons_cone03_pfNeuHadronsAndPhotons_25ns.txt'
    process.eEffArea = cms.EDProducer(
        "ElectronEffectiveAreaEmbedder",
        src = cms.InputTag(eSrc),
        label = cms.string("EffectiveArea"), # embeds a user float with this name
        configFile = cms.FileInPath(eaFile), # the effective areas file
    )
    eSrc = 'eEffArea'

    process.electronCustomization *= process.eEffArea

    #################
    ### embed rho ###
    #################
    process.eRho = cms.EDProducer(
        "ElectronRhoEmbedder",
        src = cms.InputTag(eSrc),
        rhoSrc = cms.InputTag(rhoSrc),
        label = cms.string("rho"),
    )
    eSrc = 'eRho'

    process.electronCustomization *= process.eRho

    # add to schedule
    process.schedule.append(process.electronCustomization)

    return eSrc
