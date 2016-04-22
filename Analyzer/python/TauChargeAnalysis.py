# TauChargeAnalysis.py
# for DY analysis

from AnalysisBase import AnalysisBase
from utilities import ZMASS, deltaPhi, deltaR
from leptonId import passWZLoose, passWZMedium, passWZTight, passHppLoose, passHppMedium, passHppTight

import itertools
import operator

import ROOT

class TauChargeAnalysis(AnalysisBase):
    '''
    TauCharge analysis
    '''

    def __init__(self,**kwargs):
        outputFileName = kwargs.pop('outputFileName','tauChargeTree.root')
        outputTreeName = kwargs.pop('outputTreeName','TauChargeTree')
        super(TauChargeAnalysis, self).__init__(outputFileName=outputFileName,outputTreeName=outputTreeName,**kwargs)

        # setup cut tree
        self.cutTree.add(self.twoLoose,'twoLooseLeptons')
        self.cutTree.add(self.trigger,'trigger')

        # setup analysis tree

        # chan string
        self.tree.add(self.getChannelString, 'channel', ['C',3])

        # event counts
        self.tree.add(lambda rtrow,cands: self.numJets(rtrow,'isLoose',30), 'numJetsLoose30', 'I')
        self.tree.add(lambda rtrow,cands: self.numJets(rtrow,'isTight',30), 'numJetsTight30', 'I')
        self.tree.add(lambda rtrow,cands: self.numJets(rtrow,'passCSVv2T',30), 'numBjetsTight30', 'I')
        #self.tree.add(lambda rtrow,cands: len(self.getCands(rtrow,'electrons',self.passLoose)), 'numLooseElectrons', 'I')
        #self.tree.add(lambda rtrow,cands: len(self.getCands(rtrow,'electrons',self.passMedium)), 'numMediumElectrons', 'I')
        #self.tree.add(lambda rtrow,cands: len(self.getCands(rtrow,'electrons',self.passTight)), 'numTightElectrons', 'I')
        #self.tree.add(lambda rtrow,cands: len(self.getCands(rtrow,'muons',self.passLoose)), 'numLooseMuons', 'I')
        #self.tree.add(lambda rtrow,cands: len(self.getCands(rtrow,'muons',self.passMedium)), 'numMediumMuons', 'I')
        #self.tree.add(lambda rtrow,cands: len(self.getCands(rtrow,'muons',self.passTight)), 'numTightMuons', 'I')
        #self.tree.add(lambda rtrow,cands: len(self.getCands(rtrow,'taus',self.passLoose)), 'numLooseTaus', 'I')
        #self.tree.add(lambda rtrow,cands: len(self.getCands(rtrow,'taus',self.passMedium)), 'numMediumTaus', 'I')
        #self.tree.add(lambda rtrow,cands: len(self.getCands(rtrow,'taus',self.passTight)), 'numTightTaus', 'I')

        # trigger
        #self.tree.add(lambda rtrow,cands: self.getTreeVariable(rtrow,'Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZPass'), 'pass_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ', 'I')
        #self.tree.add(lambda rtrow,cands: self.getTreeVariable(rtrow,'Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZPass'), 'pass_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ', 'I')
        #self.tree.add(lambda rtrow,cands: self.getTreeVariable(rtrow,'Ele17_Ele12_CaloIdL_TrackIdL_IsoVL_DZPass'), 'pass_Ele17_Ele12_CaloIdL_TrackIdL_IsoVL_DZ', 'I')
        self.tree.add(lambda rtrow,cands: self.getTreeVariable(rtrow,'IsoMu20Pass'), 'pass_IsoMu20', 'I')
        self.tree.add(lambda rtrow,cands: self.getTreeVariable(rtrow,'IsoTkMu20Pass'), 'pass_IsoTkMu20', 'I')
        #self.tree.add(lambda rtrow,cands: self.getTreeVariable(rtrow,'Ele23_WPLoose_GsfPass'), 'pass_Ele23_WPLoose_Gsf', 'I')
        self.tree.add(self.triggerEfficiency, 'triggerEfficiency', 'F')

        # z leptons
        self.addDiLepton('z','z1','z2')
        #self.addDiCandVar('z','z1','z2','mass_uncorrected','mass','F',uncorrected=True)
        self.addLepton('z1')
        self.tree.add(lambda rtrow,cands: self.passMedium(rtrow,cands['z1']), 'z1_passMedium', 'I')
        self.tree.add(lambda rtrow,cands: self.passTight(rtrow,cands['z1']), 'z1_passTight', 'I')
        self.tree.add(lambda rtrow,cands: self.looseScale(rtrow,cands['z1']), 'z1_looseScale', 'F')
        self.tree.add(lambda rtrow,cands: self.mediumScale(rtrow,cands['z1']), 'z1_mediumScale', 'F')
        self.tree.add(lambda rtrow,cands: self.tightScale(rtrow,cands['z1']), 'z1_tightScale', 'F')
        self.addLepton('z2')
        self.tree.add(lambda rtrow,cands: self.passMedium(rtrow,cands['z2']), 'z2_passMedium', 'I')
        self.tree.add(lambda rtrow,cands: self.passTight(rtrow,cands['z2']), 'z2_passTight', 'I')
        self.tree.add(lambda rtrow,cands: self.looseScale(rtrow,cands['z2']), 'z2_looseScale', 'F')
        self.tree.add(lambda rtrow,cands: self.mediumScale(rtrow,cands['z2']), 'z2_mediumScale', 'F')
        self.tree.add(lambda rtrow,cands: self.tightScale(rtrow,cands['z2']), 'z2_tightScale', 'F')

        # w lepton
        self.addLeptonMet('w1','z1',('pfmet',0))
        self.addLeptonMet('w2','z2',('pfmet',0))

        # met
        self.addMet('met',('pfmet',0))

    ############################
    ### select DY candidates ###
    ############################
    def selectCandidates(self,rtrow):
        candidate = {
            'z1' : (),
            'z2' : (),
        }

        # get leptons
        colls = ['muons','taus']
        pts = {}
        etas = {}
        phis = {}
        leps = []
        leps = self.getPassingCands(rtrow,'Loose')
        if len(leps)<2: return candidate # need at least 2 leptons

        for cand in leps:
            pts[cand] = self.getObjectVariable(rtrow,cand,'pt')
            etas[cand] = self.getObjectVariable(rtrow,cand,'eta')
            phis[cand] = self.getObjectVariable(rtrow,cand,'phi')

        # get invariant masses
        massDiffs = {}
        sts = {}
        for zpair in itertools.combinations(pts.keys(),2):
            # mt, tm
            candFlavors = [zpair[0][0],zpair[1][0]]
            if candFlavors.count('muons')!=1 and candFlavors.count('taus')!=1: continue
            # require pt 20 for muon as well as tau
            pt0 = pts[zpair[0]]
            pt1 = pts[zpair[1]]
            if pt0<20 or pt1<20: continue
            # require deltaR 0.02
            eta0 = etas[zpair[0]]
            eta1 = etas[zpair[1]]
            phi0 = phis[zpair[0]]
            phi1 = phis[zpair[1]]
            if deltaR(eta0,phi0,eta1,phi1)<0.02: continue
            sts[zpair] = pt0 + pt1

        if not sts: return candidate # need a z candidate

        # sort by highest pt pair
        bestZ = sorted(sts.items(), key=operator.itemgetter(1))[-1][0]

        # make it mt
        z1 = bestZ[0] if bestZ[0][0]=='muons' else bestZ[1]
        z2 = bestZ[1] if bestZ[0][0]=='muons' else bestZ[0]

        candidate['z1'] = z1
        candidate['z2'] = z2

        return candidate

    #################
    ### lepton id ###
    #################
    def passLoose(self,rtrow,cand):
        return passHppLoose(self,rtrow,cand)

    def passMedium(self,rtrow,cand):
        return passHppMedium(self,rtrow,cand)

    def passTight(self,rtrow,cand):
        return passHppTight(self,rtrow,cand)

    def looseScale(self,rtrow,cand):
        if cand[0]=='muons':
            return self.leptonScales.getScale(rtrow,'MediumIDLooseIso',cand)
        elif cand[0]=='electrons':
            return self.leptonScales.getScale(rtrow,'CutbasedVeto',cand) # TODO, fix
        else:
            return 1.

    def mediumScale(self,rtrow,cand):
        if cand[0]=='muons':
            return self.leptonScales.getScale(rtrow,'MediumIDTightIso',cand)
        elif cand[0]=='electrons':
            return self.leptonScales.getScale(rtrow,'CutbasedMedium',cand)
        else:
            return 1.

    def tightScale(self,rtrow,cand):
        if cand[0]=='muons':
            return self.leptonScales.getScale(rtrow,'MediumIDTightIso',cand)
        elif cand[0]=='electrons':
            return self.leptonScales.getScale(rtrow,'CutbasedTight',cand)
        else:
            return 1.

    def getPassingCands(self,rtrow,mode):
        if mode=='Loose':
            passMode = self.passLoose
        elif mode=='Medium':
            passMode = self.passMedium
        elif mode=='Tight':
            passMode = self.passTight
        else:
            return []
        cands = []
        for coll in ['muons','taus']:
            cands += self.getCands(rtrow,coll,passMode)
        return cands

    def numJets(self,rtrow,mode,pt):
        return len(
            self.getCands(
                rtrow,
                'jets',
                lambda rtrow,cand: self.getObjectVariable(rtrow,cand,mode)>0.5 
                                   and self.getObjectVariable(rtrow,cand,'pt')>pt
            )
        )

    ######################
    ### channel string ###
    ######################
    def getChannelString(self,rtrow,cands):
        '''Get the channel string'''
        chanString = ''
        for c in ['z1','z2']:
            chanString += self.getCollectionString(cands[c])
        return chanString

    ###########################
    ### analysis selections ###
    ###########################
    def twoLoose(self,rtrow,cands):
        return len(self.getPassingCands(rtrow,'Loose'))>=2

    def trigger(self,rtrow,cands):
        # accept MC, check trigger for data
        if rtrow.isData<0.5: return True
        triggerNames = {
            #'DoubleMuon'     : [
            #    'Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ',
            #    'Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ',
            #],
            #'DoubleEG'       : [
            #    'Ele17_Ele12_CaloIdL_TrackIdL_IsoVL_DZ',
            #],
            #'MuonEG'         : [
            #    'Mu8_TrkIsoVVL_Ele17_CaloIdL_TrackIdL_IsoVL',
            #    'Mu17_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL',
            #],
            'SingleMuon'     : [
                'IsoMu20',
                'IsoTkMu20',
            ],
            #'SingleElectron' : [
            #    'Ele23_WPLoose_Gsf',
            #],
        }
        # the order here defines the heirarchy
        # first dataset, any trigger passes
        # second dataset, if a trigger in the first dataset is found, reject event
        # so forth
        datasets = [
            #'DoubleMuon', 
            #'DoubleEG', 
            #'MuonEG',
            'SingleMuon',
            #'SingleElectron',
        ]
        # reject triggers if they are in another dataset
        # looks for the dataset name in the filename
        # for MC it accepts all
        reject = True if rtrow.isData>0.5 else False
        for dataset in datasets:
            # if we match to the dataset, start accepting triggers
            if dataset in self.fileNames[0]: reject = False
            for trigger in triggerNames[dataset]:
                var = '{0}Pass'.format(trigger)
                passTrigger = self.getTreeVariable(rtrow,var)
                if passTrigger>0.5:
                    # it passed the trigger
                    # in data: reject if it corresponds to a higher dataset
                    return False if reject else True
            # dont check the rest of data
            if dataset in self.fileNames[0]: break
        return False

    def triggerEfficiency(self,rtrow,cands):
        candList = [cands[c] for c in ['z1','z2'] if c[0]=='muons']
        triggerList = ['IsoMu20_OR_IsoTkMu20']
        return self.triggerScales.getDataEfficiency(rtrow,triggerList,candList)










