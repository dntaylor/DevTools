import glob
from itertools import product, combinations_with_replacement

import ROOT

from DevTools.MVATrainer.Trainer import Trainer
from DevTools.Plotter.xsec import getXsec
from DevTools.Plotter.utilities import getLumi
from DevTools.Analyzer.utilities import ZMASS

class Hpp4lTrainer(Trainer):
    '''Hpp4l MVA Trainer'''
    def __init__(self,**kwargs):
        inputTreeName = kwargs.pop('inputTreeName','Hpp4lTree')
        mass = kwargs.pop('mass',200)
        super(Hpp4lTrainer,self).__init__(**kwargs)
        
        sampleDir = 'ntuples/Hpp4l'
        sampleMap = {
            'WZTo3LNu'                  : 'WZTo3LNu_TuneCUETP8M1_13TeV-powheg-pythia8',
            'WZTo2L2Q'                  : 'WZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8',
            'WZTo1L3Nu'                 : 'WZTo1L3Nu_13TeV_amcatnloFXFX_madspin_pythia8',
            'WZTo1L1Nu2Q'               : 'WZTo1L1Nu2Q_13TeV_amcatnloFXFX_madspin_pythia8',
            'ZZTo4L'                    : 'ZZTo4L_13TeV_powheg_pythia8',
            'ggZZTo2e2mu'               : 'GluGluToContinToZZTo2e2mu_13TeV_MCFM701_pythia8',
            'ggZZTo2mu2tau'             : 'GluGluToContinToZZTo2mu2tau_13TeV_MCFM701_pythia8',
            'ggZZTo4e'                  : 'GluGluToContinToZZTo4e_13TeV_MCFM701_pythia8',
            'ggZZTo4mu'                 : 'GluGluToContinToZZTo4mu_13TeV_MCFM701_pythia8',
            'ggZZTo4tau'                : 'GluGluToContinToZZTo4tau_13TeV_MCFM701_pythia8',
            'ZZTo2L2Nu'                 : 'ZZTo2L2Nu_13TeV_powheg_pythia8',
            'ZZTo2L2Q'                  : 'ZZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8',
            'WZZ'                       : 'WZZ_TuneCUETP8M1_13TeV-amcatnlo-pythia8',
            'WWG'                       : 'WWG_TuneCUETP8M1_13TeV-amcatnlo-pythia8',
            'ttWJets'                   : 'ttWJets_13TeV_madgraphMLM',
            'ttZJets'                   : 'ttZJets_13TeV_madgraphMLM',
            'WWTo2L2Nu'                 : 'WWTo2L2Nu_13TeV-powheg',
            'WWToLNuQQ'                 : 'WWToLNuQQ_13TeV-powheg',
            'DYJetsToLL_M-50'           : 'DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8',
            'DYJetsToLL_M-10to50'       : 'DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8',
            'TTJets_DiLept'             : 'TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
            'TTJets_SingleLeptFromT'    : 'TTJets_SingleLeptFromT_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
            'TTJets_SingleLeptFromTbar' : 'TTJets_SingleLeptFromTbar_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
            'HppHmm200GeV'              : 'HPlusPlusHMinusMinusHTo4L_M-200_13TeV-pythia8',
            'HppHmm300GeV'              : 'HPlusPlusHMinusMinusHTo4L_M-300_13TeV-pythia8',
            'HppHmm400GeV'              : 'HPlusPlusHMinusMinusHTo4L_M-400_13TeV-pythia8',
            'HppHmm500GeV'              : 'HPlusPlusHMinusMinusHTo4L_M-500_13TeV-pythia8',
            'HppHmm600GeV'              : 'HPlusPlusHMinusMinusHTo4L_M-600_13TeV-pythia8',
            'HppHmm700GeV'              : 'HPlusPlusHMinusMinusHTo4L_M-700_13TeV-pythia8',
            'HppHmm800GeV'              : 'HPlusPlusHMinusMinusHTo4L_M-800_13TeV-pythia8',
            'HppHmm900GeV'              : 'HPlusPlusHMinusMinusHTo4L_M-900_13TeV-pythia8',
            'HppHmm1000GeV'             : 'HPlusPlusHMinusMinusHTo4L_M-1000_13TeV-pythia8',
        }

        # get the trees
        intLumis = {}
        for s in sampleMap:
            summedWeights = 0.
            f = '{0}/{1}.root'.format(sampleDir, sampleMap[s])
            tfile = ROOT.TFile.Open(f)
            hist = tfile.Get('summedWeights')
            summedWeights += hist.GetBinContent(1)
            tfile.Close()
            intLumis[s] = float(summedWeights)/getXsec(sampleMap[s])
        sigTrees = {}
        bgTrees = {}
        for sample in sampleMap:
            if 'HppHmm' in sample:
                if '{0}GeV'.format(mass) not in sample: continue
                sigTrees[sample] = ROOT.TChain(inputTreeName)
                f = '{0}/{1}.root'.format(sampleDir,sampleMap[sample])
                sigTrees[sample].Add(f)
            else:
                bgTrees[sample] = ROOT.TChain(inputTreeName)
                f = '{0}/{1}.root'.format(sampleDir,sampleMap[sample])
                bgTrees[sample].Add(f)

        intLumi = getLumi()

        # add to factory
        for sig in sigTrees:
            if not sigTrees[sig].GetEntries(): continue
            self.factory.AddSignalTree(sigTrees[sig],intLumi/intLumis[sig])
        for bg in bgTrees:
            if not bgTrees[bg].GetEntries(): continue
            self.factory.AddBackgroundTree(bgTrees[bg],intLumi/intLumis[bg])

        # per event weight
        weight = 'hpp1_mediumScale*hpp2_mediumScale*hmm1_mediumScale*hmm2_mediumScale*genWeight*pileupWeight*triggerEfficiency'
        self.factory.SetWeightExpression(weight)

        # variables
        self.factory.AddVariable('hppWindow := fabs(hpp_mass-{0})'.format(mass), '|m_{++}-m_{#Phi}|', 'GeV', 'F')  # h++ symmetric window
        #self.factory.AddVariable('hppUpperWindow := max(hpp_mass-{0},0)'.format(mass),'F') # h++ upper window
        #self.factory.AddVariable('hppLowerWindow := max({0}-hpp_mass,0)'.format(mass),'F') # h++ lower window
        #self.factory.AddVariable('hpp_pt','F')                           # h++ pt
        self.factory.AddVariable('hpp_deltaR', '#Delta R(++)', '', 'F')                                            # h++ dR
        self.factory.AddVariable('hmmWindow := fabs(hmm_mass-{0})'.format(mass), '|m_{--}-m_{#Phi}|', 'GeV', 'F')  # h-- symmetric window
        #self.factory.AddVariable('max(hmm_mass-{0},0)'.format(mass),'F') # h-- upper window
        #self.factory.AddVariable('max({0}-hmm_mass,0)'.format(mass),'F') # h-- lower window
        #self.factory.AddVariable('hmm_pt','F')                           # h-- pt
        self.factory.AddVariable('hmm_deltaR', '#Delta R(--)', '', 'F')                                             # h-- dR
        self.factory.AddVariable('st := hpp1_pt+hpp2_pt+hmm1_pt+hmm2_pt', 's_T', 'GeV', 'F')                        # 4l st
        self.factory.AddVariable('zWindow := fabs(z_mass-{0})'.format(ZMASS), '|m_{+-}-m_{Z}|', 'GeV', 'F')         # z symmetric window

        # preselection cut
        cutString = ' && '.join(['{0}_passMedium==1'.format(lep) for lep in ['hpp1','hpp2','hmm1','hmm2']])
        genChannelsPP = []
        genHiggsChannels = [''.join(x) for x in combinations_with_replacement('em',2)]
        for hpp in genHiggsChannels:
            for hmm in genHiggsChannels:
                genChannelsPP += [hpp+hmm]
        cutString += ' && ' + '(' + ' || '.join(['genChannel=="{0}"'.format(chan) for chan in genChannelsPP + ['a']]) + ')'
        passCut = ROOT.TCut(cutString)
        self.factory.PrepareTrainingAndTestTree(
            passCut,
            ":".join(
                [
                "nTrain_Signal=0",
                "nTrain_Background=0",
                "SplitMode=Random",
                "NormMode=NumEvents",
                "!V"
                ]
            )
        )

        # options:
        # H : display help
        # V : turn on verbosity
        # IgnoreNegWeightsInTraining : ignore events with negative weights for training, keep for testing

        # book methods
        cuts = self.factory.BookMethod(
            ROOT.TMVA.Types.kCuts,
            "Cuts",
            ":".join(
                [
                    "VarProp=FSmart",
                ]
            )
        )

        bdt = self.factory.BookMethod(
            ROOT.TMVA.Types.kBDT,
            "BDT",
            ":".join(
                [
                    "NTrees=850",
                    "MaxDepth=3",
                    "BoostType=AdaBoost",
                    "AdaBoostBeta=0.5",
                    "SeparationType=GiniIndex",
                    "nCuts=20",
                    "PruneMethod=NoPruning",
                ]
            )
        )

