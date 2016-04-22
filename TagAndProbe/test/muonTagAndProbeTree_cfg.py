import FWCore.ParameterSet.Config as cms
from FWCore.ParameterSet.VarParsing import VarParsing
import sys

process = cms.Process("tnp")

###################################################################
options = dict()
varOptions = VarParsing('analysis')
varOptions.register(
    "isMC",
    True,
    VarParsing.multiplicity.singleton,
    VarParsing.varType.bool,
    "Compute MC efficiencies"
    )

varOptions.parseArguments()

#isolationDef = "(chargedHadronIso+max(photonIso+neutralHadronIso-0.5*puChargedHadronIso,0.0))/pt"
isolationDef = '(pfIsolationR04().sumChargedHadronPt + max(0., pfIsolationR04().sumNeutralHadronEt + pfIsolationR04().sumPhotonEt - 0.5*pfIsolationR04().sumPUPt))/pt()'
options['HLTProcessName']          = "HLT"
options['MUON_COLL']               = "slimmedMuons"
options['MUON_CUTS']               = "((isTrackerMuon || isGlobalMuon) && abs(eta)<2.4 && pt>5)"
options['MUON_TAG_CUTS']           = "(userInt('isTightMuon')==1 && pt > 25 && abs(eta) < 2.1 && "+isolationDef+" < 0.2)"
options['MAXEVENTS']               = cms.untracked.int32(-1) 
options['useAOD']                  = cms.bool(False)
options['DOTRIGGER']               = cms.bool(False)
options['DORECO']                  = cms.bool(False)
options['DOID']                    = cms.bool(True)
options['OUTPUTEDMFILENAME']       = 'edmFile.root'
options['DEBUG']                   = cms.bool(False)

from PhysicsTools.TagAndProbe.treeMakerOptions_cfi import *

if (varOptions.isMC):
    options['INPUT_FILE_NAME']     = '/store/mc/RunIIFall15MiniAODv2/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/00000/06532BBC-05C8-E511-A60A-F46D043B3CE5.root'
    options['OUTPUT_FILE_NAME']    = "TnPTree_mc_muon.root"
    options['TnPPATHS']            = cms.vstring("HLT_IsoTkMu20_v*")
    options['TnPHLTTagFilters']    = cms.vstring("hltL3crIsoL1sMu16L1f0L2f10QL3f20QL3trkIsoFiltered0p09")
    options['TnPHLTProbeFilters']  = cms.vstring()
    options['HLTFILTERTOMEASURE']  = cms.vstring("")
    options['GLOBALTAG']           = '76X_mcRun2_asymptotic_v12'
    options['EVENTSToPROCESS']     = cms.untracked.VEventRange()
else:
    options['INPUT_FILE_NAME']     = "/store/data/Run2015D/SingleMuon/MINIAOD/16Dec2015-v1/10000/00006301-CAA8-E511-AD39-549F35AD8BC9.root"
    options['OUTPUT_FILE_NAME']    = "TnPTree_data_muon.root"
    options['TnPPATHS']            = ["HLT_IsoTkMu20_v*",]
    options['TnPHLTTagFilters']    = ["hltL3crIsoL1sMu16L1f0L2f10QL3f20QL3trkIsoFiltered0p09"]
    options['TnPHLTProbeFilters']  = cms.vstring()
    options['HLTFILTERTOMEASURE']  = cms.vstring("")
    options['GLOBALTAG']           = '76X_dataRun2_v15'
    options['EVENTSToPROCESS']     = cms.untracked.VEventRange()

###################################################################

#setModules(process, options)
from PhysicsTools.TagAndProbe.treeContent_cfi import *

process.load("Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff")
process.load("Configuration.Geometry.GeometryRecoDB_cff")
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
process.GlobalTag.globaltag = options['GLOBALTAG']

process.load('FWCore.MessageService.MessageLogger_cfi')
process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(False) )

process.MessageLogger.cerr.threshold = ''
process.MessageLogger.cerr.FwkReport.reportEvery = 1000

process.source = cms.Source("PoolSource",
                            fileNames = cms.untracked.vstring(options['INPUT_FILE_NAME']),
                            eventsToProcess = options['EVENTSToPROCESS']
                            )

process.maxEvents = cms.untracked.PSet( input = options['MAXEVENTS'])

###################################################################
## ID
###################################################################
process.mID = cms.EDProducer(
    "MuonIdEmbedder",
    src = cms.InputTag(options['MUON_COLL']),
    vertexSrc = cms.InputTag("offlineSlimmedPrimaryVertices"),
)
process.idEmbedSequence = cms.Sequence(process.mID)
muonSource = 'mID'


############
### Tags ###
############
process.tagMuons = cms.EDFilter("PATMuonRefSelector",
    src = cms.InputTag(muonSource),
    cut = cms.string(options['MUON_TAG_CUTS']),
    filter = cms.bool(True)
)

process.tagMuonsTriggerMatched = cms.EDProducer("PatMuonTriggerCandProducer",
    filterNames = cms.vstring(options['TnPHLTTagFilters']),
    inputs      = cms.InputTag("tagMuons"),
    bits        = cms.InputTag('TriggerResults::HLT'),
    objects     = cms.InputTag('selectedPatTrigger'),
    dR          = cms.double(0.4),
    isAND       = cms.bool(True)
    )

process.probeMuons = cms.EDFilter("PATMuonRefSelector",
    src = cms.InputTag(muonSource),
    cut = cms.string(options['MUON_CUTS']), 
)

###################################################################
## TnP PAIRS
###################################################################

process.tpPairs = cms.EDProducer("CandViewShallowCloneCombiner",
    decay = cms.string("tagMuonsTriggerMatched@+ probeMuons@-"), # charge coniugate states are implied
    cut   = cms.string("40 < mass < 200")
)

#process.tpPairsMCEmbedded = cms.EDProducer("pairMCInfoEmbedder",
#    input = cms.InputTag("tpPairs"),
#    leg1Matches = cms.InputTag("muMcMatch"),
#    leg2Matches = cms.InputTag("muMcMatch")
#)

process.muMcMatch = cms.EDProducer("MCTruthDeltaRMatcherNew",
    pdgId = cms.vint32(13),
    src = cms.InputTag(muonSource),
    distMin = cms.double(0.3),
    matched = cms.InputTag("prunedGenParticles"),
    checkCharge = cms.bool(True)
)

##############
### Pileup ###
##############
from SimGeneral.MixingModule.mix_2015_25ns_FallMC_matchData_PoissonOOTPU_cfi import mix
pu_distribs = { "mc" : mix.input.nbPileupEvents.probValue }

#### DATA PU DISTRIBUTIONS
data_pu_distribs = { "Jamboree_golden_JSON" : [5.12e+04,3.66e+05,5.04e+05,4.99e+05,7.5e+05,1.1e+06,2.53e+06,9.84e+06,4.4e+07,1.14e+08,1.94e+08,2.63e+08,2.96e+08,2.74e+08,2.06e+08,1.26e+08,6.38e+07,2.73e+07,1.1e+07,5.2e+06,3.12e+06,1.87e+06,9.35e+05,3.64e+05,1.1e+05,2.64e+04,5.76e+03,1.53e+03,594,278,131,59.8,26,10.8,4.29,1.62,0.587,0.203,0.0669,0.0211,0.00633,0.00182,0.000498,0.00013,3.26e-05,7.77e-06,1.77e-06,3.85e-07,7.99e-08,1.58e-08,3e-09,5.43e-10] }


process.pileupReweightingProducer = cms.EDProducer("PileupWeightProducer",
                                                   #hardcodedWeights = cms.untracked.bool(True),
                                                   pileupInfoTag    = cms.InputTag("slimmedAddPileupInfo"),
                                                   PileupMC = cms.vdouble(pu_distribs["mc"]),
                                                   PileupData = cms.vdouble(data_pu_distribs["Jamboree_golden_JSON"]),
                                                   )


##########################################################################
## TREE MAKER OPTIONS
##########################################################################
ZVariablesToStore = cms.PSet(
    eta = cms.string("eta"),
    abseta = cms.string("abs(eta)"),
    pt  = cms.string("pt"),
    mass  = cms.string("mass"),
    )   

ProbeVariablesToStore = cms.PSet(
    probe_eta    = cms.string("eta"),
    probe_abseta = cms.string("abs(eta)"),
    probe_pt     = cms.string("pt"),
    probe_et     = cms.string("et"),
    probe_e      = cms.string("energy"),
    probe_q      = cms.string("charge"),
    )

TagVariablesToStore = cms.PSet(
    tag_eta    = cms.string("eta"),
    tag_abseta = cms.string("abs(eta)"),
    tag_pt     = cms.string("pt"),
    tag_et     = cms.string("et"),
    tag_e      = cms.string("energy"),
    tag_q      = cms.string("charge"),
    )

CommonStuffForMuonProbe = cms.PSet(
    variables = cms.PSet(ProbeVariablesToStore),
    ignoreExceptions =  cms.bool (True),
    addRunLumiInfo   =  cms.bool (True),
    pileupInfoTag = cms.InputTag("slimmedAddPileupInfo"),
    addEventVariablesInfo   =  cms.bool(True),
    vertexCollection = cms.InputTag("offlineSlimmedPrimaryVertices"),
    beamSpot = cms.InputTag("offlineBeamSpot"),
    #pfMet = cms.InputTag(""),
    pairVariables =  cms.PSet(ZVariablesToStore),
    pairFlags     =  cms.PSet(
        mass60to120 = cms.string("60 < mass < 120")
        ),
    tagVariables   =  cms.PSet(TagVariablesToStore),
    tagFlags       =  cms.PSet(),    
    )

#mcTruthCommonStuff = cms.PSet(
#    isMC = cms.bool(False),
#    tagMatches = cms.InputTag("muMcMatch"),
#    probeMatches = cms.InputTag("muMcMatch"),
#    motherPdgId = cms.vint32(22,23),
#    #motherPdgId = cms.vint32(443), # JPsi
#    #motherPdgId = cms.vint32(553), # Yupsilon
#    makeMCUnbiasTree = cms.bool(False),
#    checkMotherInUnbiasEff = cms.bool(False),
#    mcVariables = cms.PSet(
#        probe_eta = cms.string("eta"),
#        probe_abseta = cms.string("abs(eta)"),
#        probe_et  = cms.string("et"),
#        probe_e  = cms.string("energy"),
#        ),
#    mcFlags     =  cms.PSet(
#        probe_isPromptFinalState = cms.string("isPromptFinalState")
#        ),      
#    )
mcTruthCommonStuff = cms.PSet(
    isMC = cms.bool(True),
    #tagMatches = cms.InputTag("McMatchTag"),
    #motherPdgId = cms.vint32(),
    motherPdgId = cms.vint32(22,23),
    #motherPdgId = cms.vint32(443), # JPsi
    #motherPdgId = cms.vint32(553), # Yupsilon
    #makeMCUnbiasTree = cms.bool(False),
    #checkMotherInUnbiasEff = cms.bool(False),
    genParticles = cms.InputTag("prunedGenParticles"),
    useTauDecays = cms.bool(False),
    checkCharge = cms.bool(False),
    pdgId = cms.int32(13),
    mcVariables = cms.PSet(
        probe_eta = cms.string("eta"),
        probe_abseta = cms.string("abs(eta)"),
        probe_et  = cms.string("et"),
        probe_e  = cms.string("energy"),
        ),
    mcFlags     =  cms.PSet(
        probe_flag = cms.string("pt>0")
        ),
    )

if (not varOptions.isMC):
    mcTruthCommonStuff = cms.PSet(
        isMC = cms.bool(False)
        )


process.muonEffs = cms.EDAnalyzer("TagProbeFitTreeProducer",
    CommonStuffForMuonProbe, mcTruthCommonStuff,
    tagProbePairs = cms.InputTag("tpPairs"),
    arbitration   = cms.string("Random2"),
    flags         = cms.PSet(
        passingMedium = cms.string("isMediumMuon"),
        passingTight  = cms.string("userInt('isTightMuon')==1"), 
        passingIsoLoose = cms.string(isolationDef+" < 0.4"),
        passingIsoTight = cms.string(isolationDef+" < 0.12"),
    ),
    allProbes     = cms.InputTag("probeMuons"),
    )

process.tpPairSeq = cms.Sequence(
    process.tpPairs
)

if varOptions.isMC :
    process.tpPairSeq += process.muMcMatch
    #process.tpPairSeq += process.tpPairsMCEmbedded
    process.tpPairSeq += process.pileupReweightingProducer
    process.muonEffs.isMC = cms.bool(True)
    process.muonEffs.eventWeight   = cms.InputTag("generator")
    process.muonEffs.PUWeightSrc   = cms.InputTag("pileupReweightingProducer","pileupWeights")
    #setattr(process.muonEffs.pairVariables, 'mc_mass', cms.string("userFloat('mc_mass')"))
    process.muonEffs.tagProbePairs = cms.InputTag("tpPairs")

#if not options.isMC :
#    import FWCore.PythonUtilities.LumiList as LumiList
#    process.source.lumisToProcess = LumiList.LumiList(filename = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/'+options['json']).getVLuminosityBlockRange()

process.p = cms.Path(
    process.idEmbedSequence *
    (process.tagMuons + process.probeMuons) *
    (process.tagMuonsTriggerMatched) *
    process.tpPairSeq *
    process.muonEffs
    )

process.out = cms.OutputModule("PoolOutputModule",
                               fileName = cms.untracked.string(options['OUTPUTEDMFILENAME']),
                               SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring("p"))
                               )
process.outpath = cms.EndPath(process.out)
if (not options['DEBUG']):
    process.outpath.remove(process.out)

process.TFileService = cms.Service(
    "TFileService", fileName = cms.string(options['OUTPUT_FILE_NAME']),
    closeFileFast = cms.untracked.bool(True)
    )

