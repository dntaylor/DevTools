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

    #################################
    ### recompute met uncertainty ###
    #################################
    postfix = "New"
    from PhysicsTools.PatUtils.tools.runMETCorrectionsAndUncertainties import runMetCorAndUncFromMiniAOD
    runMetCorAndUncFromMiniAOD(process,
                               jetCollUnskimmed="slimmedJets",
                               jetColl=jSrc,
                               photonColl=pSrc,
                               electronColl=eSrc,
                               muonColl=mSrc,
                               tauColl=tSrc,
                               pfCandColl=pfSrc,
                               isData=not isMC,
                               jetFlav="AK4PFchs",
                               postfix=postfix)

    # correct things to make it work
    getattr(process,'patPFMetTxyCorr{0}'.format(postfix)).vertexCollection = cms.InputTag('offlineSlimmedPrimaryVertices')
    del getattr(process,'slimmedMETs{0}'.format(postfix)).caloMET

    metSrc = "slimmedMETs{0}".format(postfix)
    
    ####################
    ### embed shifts ###
    ####################
    for shift in ['JetRes','JetEn','MuonEn','ElectronEn','TauEn','UnclusteredEn','PhotonEn']:
        for sign in ['Up','Down']:
            mod = cms.EDProducer(
                "ShiftedMETEmbedder",
                src = cms.InputTag(metSrc),
                label = cms.string('{0}{1}'.format(shift,sign)),
                shiftedSrc = cms.InputTag('patPFMetT1{0}{1}{2}'.format(shift,sign,postfix)),
            )
            modName = 'embed{0}{1}'.format(shift,sign)
            setattr(process,modName,mod)
            metSrc = modName
            process.metCustomization += getattr(process,modName)

    process.schedule.append(process.metCustomization)

    return metSrc
