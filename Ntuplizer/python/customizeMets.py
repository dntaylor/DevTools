import FWCore.ParameterSet.Config as cms

def customizeMets(process,metSrc,**kwargs):
    '''Customize METs'''
    jSrc = kwargs.pop('jSrc','slimmedJets')
    pSrc = kwargs.pop('pSrc','slimmedPhotons')
    eSrc = kwargs.pop('eSrc','slimmedElectrons')
    mSrc = kwargs.pop('mSrc','slimmedMuons')
    tSrc = kwargs.pop('tSrc','slimmedTaus')
    pfSrc = kwargs.pop('pfSrc','packedPFCandidates')
    isMC = kwargs.pop('isMC',False)

    process.metCustomization = cms.Path()

    ################################
    ## recompute met uncertainty ###
    ###############################
    #postfix = "New"
    #from PhysicsTools.PatUtils.tools.runMETCorrectionsAndUncertainties import runMetCorAndUncFromMiniAOD
    #runMetCorAndUncFromMiniAOD(process,
    #                           jetCollUnskimmed="slimmedJets",
    #                           jetColl=jSrc,
    #                           photonColl=pSrc,
    #                           electronColl=eSrc,
    #                           muonColl=mSrc,
    #                           tauColl=tSrc,
    #                           pfCandColl=pfSrc,
    #                           isData=not isMC,
    #                           jetFlav="AK4PFchs",
    #                           postfix=postfix)

    ## this should be it, but fails
    ##process.applyCorrections = cms.Path(getattr(process,'fullPatMetSequence{0}'.format(postfix)))
    ## fix things
    #getattr(process,'patPFMetT1T2Corr{0}'.format(postfix)).src = cms.InputTag('patJets')
    #getattr(process,'patPFMetT2Corr{0}'.format(postfix)).src = cms.InputTag('patJets')
    #getattr(process,'patPFMetTxyCorr{0}'.format(postfix)).vertexCollection = cms.InputTag('offlineSlimmedPrimaryVertices')
    #getattr(process,'slimmedMETs{0}'.format(postfix)).t1Uncertainties = cms.InputTag('patPFMetT1{0}'.format(postfix))
    #del getattr(process,'slimmedMETs{0}'.format(postfix)).caloMET
    #process.metCustomization += process.patJets
    #if isMC: process.metCustomization += process.genMetExtractor
    #process.metCustomization += getattr(process,'pfMet{0}'.format(postfix))
    #process.metCustomization += getattr(process,'patPFMet{0}'.format(postfix))
    ##process.metCustomization += process.patJetCorrFactorsReapplyJEC
    ##process.metCustomization += process.patJets
    #process.metCustomization += getattr(process,'patPFMetT1T2Corr{0}'.format(postfix))
    #process.metCustomization += getattr(process,'patPFMetTxyCorr{0}'.format(postfix))
    #process.metCustomization += getattr(process,'patPFMetT1Txy{0}'.format(postfix))
    #process.metCustomization += getattr(process,'patPFMetT1{0}'.format(postfix))
    #process.metCustomization += getattr(process,'patPFMetTxy{0}'.format(postfix))
    #process.metCustomization += getattr(process,'slimmedMETs{0}'.format(postfix))

    #metSrc = "slimmedMETs{0}".format(postfix)
    
    ####################
    ### embed shifts ###
    ####################
    process.metShiftEmbed = cms.EDProducer(
        "METShiftEmbedder",
        src = cms.InputTag(metSrc),
    )
    process.metCustomization += process.metShiftEmbed

    metSrc = "metShiftEmbed"

    process.schedule.append(process.metCustomization)

    return metSrc
