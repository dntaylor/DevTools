import glob

import ROOT

from DevTools.MVATrainer.Trainer import Trainer
from DevTools.Plotter.xsec import getXsec
from DevTools.Plotter.utilities import getLumi

class WZTrainer(Trainer):
    '''WZ MVA Trainer'''
    def __init__(self,**kwargs):
        inputTreeName = kwargs.pop('inputTreeName','WZTree')
        super(WZTrainer,self).__init__(**kwargs)
        
        sampleDir = 'ntuples/WZ'
        sampleMap = {
            "dy10"     : "DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8",
            "dy50"     : "DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8",
            "ggzz2e2m" : "GluGluToContinToZZTo2e2mu_13TeV_MCFM701_pythia8",
            "ggzz2e2t" : "GluGluToContinToZZTo2e2tau_13TeV_MCFM701_pythia8",
            "ggzz2m2t" : "GluGluToContinToZZTo2mu2tau_13TeV_MCFM701_pythia8",
            "ggzz4e"   : "GluGluToContinToZZTo4e_13TeV_MCFM701_pythia8",
            "ggzz4m"   : "GluGluToContinToZZTo4mu_13TeV_MCFM701_pythia8",
            "ggzz4t"   : "GluGluToContinToZZTo4tau_13TeV_MCFM701_pythia8",
            "tt"       : "TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8",
            "ttw"      : "TTWJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8",
            "w"        : "WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8",
            "ww"       : "WWTo2L2Nu_13TeV-powheg",
            "wz3lnu"   : "WZTo3LNu_TuneCUETP8M1_13TeV-powheg-pythia8",
            "wz2l2q"   : "WZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8",
            "wzz"      : "WZZ_TuneCUETP8M1_13TeV-amcatnlo-pythia8",
            "zg"       : "ZGTo2LG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8",
            "zz2l2n"   : "ZZTo2L2Nu_13TeV_powheg_pythia8",
            "zz2l2q"   : "ZZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8",
            "zz4l"     : "ZZTo4L_13TeV_powheg_pythia8",
            #"tzq"      : "tZq_ll_4f_13TeV-amcatnlo-pythia8_TuneCUETP8M1",
        }

        # get the trees
        intLumis = {}
        for s in sampleMap:
            summedWeights = 0.
            for f in glob.glob('{0}/{1}/*.root'.format(sampleDir, sampleMap[s])):
                tfile = ROOT.TFile.Open(f)
                hist = tfile.Get('summedWeights')
                summedWeights += hist.GetBinContent(1)
                tfile.Close()
            intLumis[s] = float(summedWeights)/getXsec(sampleMap[s])
        sigTrees = {}
        for sig in ['wz3lnu']:
            sigTrees[sig] = ROOT.TChain('WZTree')
            for f in glob.glob('{0}/{1}/*.root'.format(sampleDir,sampleMap[sig])):
                sigTrees[sig].Add(f)
        bgTrees = {}
        for bg in ['dy10','dy50','ggzz2e2m','ggzz2m2t','ggzz4e','ggzz4m','ggzz4t','tt','ttw','wzz','zg','zz2l2n','zz2l2q','zz4l']:
            bgTrees[bg] = ROOT.TChain('WZTree')
            for f in glob.glob('{0}/{1}/*.root'.format(sampleDir,sampleMap[bg])):
                bgTrees[bg].Add(f)

        intLumi = getLumi()

        # add to factory
        for sig in sigTrees:
            self.factory.AddSignalTree(sigTrees[sig],intLumi/intLumis[sig])
        for bg in bgTrees:
            self.factory.AddBackgroundTree(bgTrees[bg],intLumi/intLumis[bg])

        # per event weight
        weight = 'genWeight'
        self.factory.SetWeightExpression(weight)

        # variables
        self.factory.AddVariable('z1_pt','F')
        self.factory.AddVariable('z2_pt','F')
        self.factory.AddVariable('w1_pt','F')
        self.factory.AddVariable('z_mass','F')
        self.factory.AddVariable('met_pt','F')
        self.factory.AddVariable('numBjetsTight30','I')

        # preselection cut
        passCut = ROOT.TCut('z1_passMedium==1 && z2_passMedium==1 && w1_passTight==1')
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

        # book method
        method = self.factory.BookMethod(
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

