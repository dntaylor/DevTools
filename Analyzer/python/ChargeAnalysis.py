# ChargeAnalysis.py
# for DY analysis

from AnalysisBase import AnalysisBase
from utilities import ZMASS, deltaPhi, deltaR
from leptonId import passWZLoose, passWZMedium, passWZTight

import itertools
import operator

import ROOT

class ChargeAnalysis(AnalysisBase):
    '''
    Charge analysis
    '''

    def __init__(self,**kwargs):
        outputFileName = kwargs.pop('outputFileName','chargeTree.root')
        outputTreeName = kwargs.pop('outputTreeName','ChargeTree')
        super(ChargeAnalysis, self).__init__(outputFileName=outputFileName,outputTreeName=outputTreeName,**kwargs)

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
        self.tree.add(lambda rtrow,cands: len(self.getCands(rtrow,'electrons',self.passLoose)), 'numLooseElectrons', 'I')
        self.tree.add(lambda rtrow,cands: len(self.getCands(rtrow,'electrons',self.passMedium)), 'numMediumElectrons', 'I')
        self.tree.add(lambda rtrow,cands: len(self.getCands(rtrow,'electrons',self.passTight)), 'numTightElectrons', 'I')
        self.tree.add(lambda rtrow,cands: len(self.getCands(rtrow,'muons',self.passLoose)), 'numLooseMuons', 'I')
        self.tree.add(lambda rtrow,cands: len(self.getCands(rtrow,'muons',self.passMedium)), 'numMediumMuons', 'I')
        self.tree.add(lambda rtrow,cands: len(self.getCands(rtrow,'muons',self.passTight)), 'numTightMuons', 'I')

        # pileup
        self.tree.add(lambda rtrow,cands: self.getTreeVariable(rtrow,'vertices_count'), 'numVertices', 'I')

        # gen
        self.tree.add(lambda rtrow,cands: self.getTreeVariable(rtrow,'nTrueVertices'), 'numTrueVertices', 'I')
        self.tree.add(lambda rtrow,cands: self.getTreeVariable(rtrow,'NUP'), 'NUP', 'I')
        self.tree.add(lambda rtrow,cands: self.getTreeVariable(rtrow,'isData'), 'isData', 'I')
        self.tree.add(lambda rtrow,cands: self.getTreeVariable(rtrow,'genWeight'), 'genWeight', 'I')

        # trigger
        self.tree.add(lambda rtrow,cands: self.getTreeVariable(rtrow,'Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZPass'), 'pass_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ', 'I')
        self.tree.add(lambda rtrow,cands: self.getTreeVariable(rtrow,'Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZPass'), 'pass_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ', 'I')
        self.tree.add(lambda rtrow,cands: self.getTreeVariable(rtrow,'Ele17_Ele12_CaloIdL_TrackIdL_IsoVL_DZPass'), 'pass_Ele17_Ele12_CaloIdL_TrackIdL_IsoVL_DZ', 'I')
        self.tree.add(lambda rtrow,cands: self.getTreeVariable(rtrow,'IsoMu20Pass'), 'pass_IsoMu20', 'I')
        self.tree.add(lambda rtrow,cands: self.getTreeVariable(rtrow,'IsoTkMu20Pass'), 'pass_IsoTkMu20', 'I')
        self.tree.add(lambda rtrow,cands: self.getTreeVariable(rtrow,'Ele23_WPLoose_GsfPass'), 'pass_Ele23_WPLoose_Gsf', 'I')
        self.tree.add(self.triggerEfficiency, 'triggerEfficiency', 'F')

        # z leptons
        self.addDiLepton('z','z1','z2')
        self.addDiCandVar('z','z1','z2','mass_uncorrected','mass','F',uncorrected=True)
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
        colls = ['electrons','muons']
        pts = {}
        p4s = {}
        charges = {}
        leps = []
        leps = self.getPassingCands(rtrow,'Loose')
        if len(leps)<2: return candidate # need at least 3 leptons

        for cand in leps:
            pts[cand] = self.getObjectVariable(rtrow,cand,'pt')
            p4s[cand] = self.getObjectVariable(rtrow,cand,'p4')
            charges[cand] = self.getObjectVariable(rtrow,cand,'charge')

        # get invariant masses
        massDiffs = {}
        for zpair in itertools.combinations(pts.keys(),2):
            #if zpair[0][0]!=zpair[1][0]: continue # SF
            #if charges[zpair[0]]==charges[zpair[1]]: continue # OS
            zp4 = p4s[zpair[0]] + p4s[zpair[1]]
            zmass = zp4.M()
            massDiffs[zpair] = abs(zmass-ZMASS)

        if not massDiffs: return candidate # need a z candidate

        # sort by closest z
        bestZ = sorted(massDiffs.items(), key=operator.itemgetter(1))[0][0]

        # now get the highest pt w
        zpts = {}
        zpts[bestZ[0]] = pts.pop(bestZ[0])
        zpts[bestZ[1]] = pts.pop(bestZ[1])

        # and sort pt of Z
        z = sorted(zpts.items(), key=operator.itemgetter(1))
        z1 = z[1][0]
        z2 = z[0][0]

        candidate['z1'] = z1
        candidate['z2'] = z2


        return candidate

    #################
    ### lepton id ###
    #################
    def passLoose(self,rtrow,cand):
        return passWZLoose(self,rtrow,cand)

    def passMedium(self,rtrow,cand):
        return passWZMedium(self,rtrow,cand)

    def passTight(self,rtrow,cand):
        return passWZTight(self,rtrow,cand)

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
        for coll in ['electrons','muons']:
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
            'DoubleMuon'     : [
                'Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ',
                'Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ',
            ],
            'DoubleEG'       : [
                'Ele17_Ele12_CaloIdL_TrackIdL_IsoVL_DZ',
            ],
            'MuonEG'         : [
                'Mu8_TrkIsoVVL_Ele17_CaloIdL_TrackIdL_IsoVL',
                'Mu17_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL',
            ],
            'SingleMuon'     : [
                'IsoMu20',
                'IsoTkMu20',
            ],
            'SingleElectron' : [
                'Ele23_WPLoose_Gsf',
            ],
        }
        # the order here defines the heirarchy
        # first dataset, any trigger passes
        # second dataset, if a trigger in the first dataset is found, reject event
        # so forth
        datasets = [
            'DoubleMuon', 
            'DoubleEG', 
            'MuonEG',
            'SingleMuon',
            'SingleElectron',
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
        candList = [cands[c] for c in ['z1','z2']]
        triggerList = ['IsoMu20_OR_IsoTkMu20','Ele23_WPLoose','Mu17_Mu8','Ele17_Ele12']
        return self.triggerScales.getDataEfficiency(rtrow,triggerList,candList)









