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

    #################################
    ### recompute met uncertainty ###
    ################################
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
    #                           postfix="New")

    ##process.applyCorrections = cms.Path(process.fullPatMetSequenceNew)
    #process.patPFMetT1T2CorrNew.src = cms.InputTag('patJets')
    #process.patPFMetT2CorrNew.src = cms.InputTag('patJets')
    #process.patPFMetTxyCorrNew.vertexCollection = cms.InputTag('offlineSlimmedPrimaryVertices')
    #process.applyCorrections = cms.Path()
    #if isMC: process.applyCorrections += process.genMetExtractor
    #process.applyCorrections += process.pfMetNew
    #process.applyCorrections += process.patPFMetNew
    #process.applyCorrections += process.patJetCorrFactorsReapplyJEC
    #process.applyCorrections += process.patJets
    #process.applyCorrections += process.patPFMetT1T2CorrNew
    #process.applyCorrections += process.patPFMetTxyCorrNew
    #process.applyCorrections += process.patPFMetT1TxyNew
    #process.applyCorrections += process.patPFMetT1New
    #process.applyCorrections += process.patPFMetTxyNew
    #process.applyCorrections += process.patJetsResUpNew
    #process.applyCorrections += process.patJetsResDownNew
    #process.applyCorrections += process.patPFMetT2CorrNew
    #process.applyCorrections += process.patPFMetT2CorrUnclusteredEnUpNew
    #process.applyCorrections += process.patPFMetT2CorrUnclusteredEnDownNew
    #for shift in ['JetEn','JetRes','ElectronEn','MuonEn','TauEn','PhotonEn','UnclusteredEn']:
    #    for direction in ['Up','Down']:
    #        if shift not in ['UnclusteredEn']:
    #            process.applyCorrections += getattr(process,"shiftedPat{0}{1}New".format(shift,direction))
    #            process.applyCorrections += getattr(process,"shiftedPatMETCorr{0}{1}New".format(shift,direction))
    #        process.applyCorrections += getattr(process,"patPFMetT1{0}{1}New".format(shift,direction))
    #process.applyCorrections += process.metcalo
    #process.applyCorrections += process.patCaloMet
    #process.applyCorrections += process.slimmedMETsNew
    #process.schedule.append(process.applyCorrections)
    #metSrc = "slimmedMETsNew"

    return metSrc
