import FWCore.ParameterSet.Config as cms

def customizeElectrons(process,coll,**kwargs):
    '''Customize electrons'''
    isMC = kwargs.pop('isMC',False)
    eSrc = coll['electrons']
    rhoSrc = coll['rho']
    pvSrc = coll['vertices']

    # customization path
    process.electronCustomization = cms.Path()

    ###################################
    ### scale and smear corrections ###
    ###################################
    # embed the uncorrected stuff
    process.uncorElec = cms.EDProducer(
        "ElectronSelfEmbedder",
        src=cms.InputTag(eSrc),
        label=cms.string('uncorrected'),
    )
    eSrc = "uncorElec"
    process.electronCustomization *= process.uncorElec

    ## first need to add a manual protection for the corrections
    #process.selectedElectrons = cms.EDFilter(
    #    "PATElectronSelector",
    #    src = cms.InputTag(eSrc),
    #    cut = cms.string("pt > 5 && abs(eta)<2.5")
    #)
    #eSrc = "selectedElectrons"
    #process.electronCustomization *= process.selectedElectrons

    #process.load('EgammaAnalysis.ElectronTools.calibratedElectronsRun2_cfi')
    #process.calibratedPatElectrons.electrons = eSrc
    #process.calibratedPatElectrons.isMC = isMC
    #process.electronCustomization *= process.calibratedPatElectrons
    #eSrc = 'calibratedPatElectrons'

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

    ##########################
    ### embed missing hits ###
    ##########################
    process.eMissingHits = cms.EDProducer(
        "ElectronMissingHitsEmbedder",
        src = cms.InputTag(eSrc),
    )
    eSrc = 'eMissingHits'

    process.electronCustomization *= process.eMissingHits

    ###################
    ### embed ww id ###
    ###################
    process.eWW = cms.EDProducer(
        "ElectronWWIdEmbedder",
        src = cms.InputTag(eSrc),
        vertexSrc = cms.InputTag(pvSrc),
    )
    eSrc = 'eWW'

    process.electronCustomization *= process.eWW

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

    ################
    ### embed pv ###
    ################
    process.ePV = cms.EDProducer(
        "ElectronIpEmbedder",
        src = cms.InputTag(eSrc),
        vertexSrc = cms.InputTag(pvSrc),
        beamspotSrc = cms.InputTag("offlineBeamSpot"),
    )
    eSrc = 'ePV'

    process.electronCustomization *= process.ePV

    ##############################
    ### embed trigger matching ###
    ##############################
    process.eTrig = cms.EDProducer(
        "ElectronHLTMatchEmbedder",
        src = cms.InputTag(eSrc),
        triggerResults = cms.InputTag('TriggerResults', '', 'HLT'),
        triggerObjects = cms.InputTag("selectedPatTrigger"),
        deltaR = cms.double(0.5),
        labels = cms.vstring(
            # single electron
            'matches_Ele12_CaloIdL_TrackIdL_IsoVL',
            'matches_Ele17_CaloIdL_TrackIdL_IsoVL',
            'matches_Ele23_CaloIdL_TrackIdL_IsoVL',
            'matches_Ele22_eta2p1_WPLoose_Gsf',
            'matches_Ele23_WPLoose_Gsf',
            'matches_Ele27_WPLoose_Gsf',
            # double electron
            'matches_Ele17_Ele12_CaloIdL_TrackIdL_IsoVL_DZ',
            # muon electron
            'matches_Mu8_TrkIsoVVL_Ele17_CaloIdL_TrackIdL_IsoVL',
            'matches_Mu17_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL',
            # electron tau
            'matches_Ele22_eta2p1_WPLoose_Gsf_LooseIsoPFTau20',
            'matches_Ele27_eta2p1_WPLoose_Gsf_LooseIsoPFTau20',
            # multi lepton
            'matches_Ele16_Ele12_Ele8_CaloIdL_TrackIdL',
            'matches_Mu8_DiEle12_CaloIdL_TrackIdL',
            'matches_DiMu9_Ele9_CaloIdL_TrackIdL',
        ),
        paths = cms.vstring(
            # single electron
            'HLT_Ele12_CaloIdL_TrackIdL_IsoVL_v\\[0-9]+',
            'HLT_Ele17_CaloIdL_TrackIdL_IsoVL_v\\[0-9]+',
            'HLT_Ele23_CaloIdL_TrackIdL_IsoVL_v\\[0-9]+',
            'HLT_Ele22_eta2p1_WPLoose_Gsf_v\\[0-9]+',
            'HLT_Ele23_WPLoose_Gsf_v\\[0-9]+',
            'HLT_Ele27_WPLoose_Gsf_v\\[0-9]+',
            # double electron
            'HLT_Ele17_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v\\[0-9]+',
            # muon electron
            'HLT_Mu8_TrkIsoVVL_Ele17_CaloIdL_TrackIdL_IsoVL_v\\[0-9]+',
            'HLT_Mu17_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v\\[0-9]+',
            # electron tau
            'HLT_Ele22_eta2p1_WPLoose_Gsf_LooseIsoPFTau20_v\\[0-9]+',
            'HLT_Ele27_eta2p1_WPLoose_Gsf_LooseIsoPFTau20_v\\[0-9]+',
            # multi lepton
            'HLT_Ele16_Ele12_Ele8_CaloIdL_TrackIdL_v\\[0-9]+',
            'HLT_Mu8_DiEle12_CaloIdL_TrackIdL_v\\[0-9]+',
            'HLT_DiMu9_Ele9_CaloIdL_TrackIdL_v\\[0-9]+',
        ),
    )
    eSrc = 'eTrig'

    process.electronCustomization *= process.eTrig

    # add to schedule
    process.schedule.append(process.electronCustomization)

    coll['electrons'] = eSrc

    return coll
