# WZAnalysis.py
# for WZ analysis

from AnalysisBase import AnalysisBase
from utilities import ZMASS, deltaPhi, deltaR

import itertools
import operator

import ROOT

class WZAnalysis(AnalysisBase):
    '''
    WZ analysis
    '''

    def __init__(self,**kwargs):
        outputFileName = kwargs.pop('outputFileName','wzTree.root')
        outputTreeName = kwargs.pop('outputTreeName','WZTree')
        super(WZAnalysis, self).__init__(outputFileName=outputFileName,outputTreeName=outputTreeName,**kwargs)

        # setup cut tree
        self.cutTree.add(self.threeLoose,'threeLooseLeptons')
        self.cutTree.add(self.vetoFourth,'noFourthTightLepton')
        self.cutTree.add(self.trigger,'trigger')

        # setup analysis tree

        # event counts
        self.tree.add(lambda rtrow,cands: self.numJets(rtrow,'isLoose',15), 'numJetsLoose15', 'I')
        self.tree.add(lambda rtrow,cands: self.numJets(rtrow,'isTight',15), 'numJetsTight15', 'I')
        self.tree.add(lambda rtrow,cands: self.numJets(rtrow,'passCSVv2T',15), 'numBjetsTight15', 'I')
        self.tree.add(lambda rtrow,cands: self.numJets(rtrow,'isLoose',20), 'numJetsLoose20', 'I')
        self.tree.add(lambda rtrow,cands: self.numJets(rtrow,'isTight',20), 'numJetsTight20', 'I')
        self.tree.add(lambda rtrow,cands: self.numJets(rtrow,'passCSVv2T',20), 'numBjetsTight20', 'I')
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
        triggers = [
            'Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ',
            'Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ',
            'Ele17_Ele12_CaloIdL_TrackIdL_IsoVL_DZ',
            'Mu8_TrkIsoVVL_Ele17_CaloIdL_TrackIdL_IsoVL',
            'Mu17_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL',
            'IsoMu20',
            'IsoTkMu20',
            'IsoMu27',
            'Ele23_WPLoose_Gsf',
        ]
        for trigger in triggers:
            self.tree.add(lambda rtrow,cands: self.getTreeVariable(rtrow,'{0}Pass'.format(trigger)), 'pass{0}'.format(trigger), 'I')

        # lead jet
        self.addJet('leadJet')

        # 3 lepton
        self.addComposite('3l','z1','z2','w1')

        # z leptons
        self.addDiLepton('z','z1','z2')
        self.addLepton('z1')
        self.tree.add(lambda rtrow,cands: self.passMedium(rtrow,cands['z1']), 'z1_passMedium', 'I')
        self.tree.add(lambda rtrow,cands: self.passTight(rtrow,cands['z1']), 'z1_passTight', 'I')
        self.addLepton('z2')
        self.tree.add(lambda rtrow,cands: self.passMedium(rtrow,cands['z2']), 'z2_passMedium', 'I')
        self.tree.add(lambda rtrow,cands: self.passTight(rtrow,cands['z2']), 'z2_passTight', 'I')

        # w lepton
        self.addLeptonMet('w','w1',('pfmet',0))
        self.addLepton('w1')
        self.tree.add(lambda rtrow,cands: self.passMedium(rtrow,cands['w1']), 'w1_passMedium', 'I')
        self.tree.add(lambda rtrow,cands: self.passTight(rtrow,cands['w1']), 'w1_passTight', 'I')

        # met
        self.addMet('met',('pfmet',0))

    ############################
    ### select WZ candidates ###
    ############################
    def selectCandidates(self,rtrow):
        candidate = {
            'z1' : (),
            'z2' : (),
            'w1' : (),
            'leadJet' : (),
        }

        # get leptons
        colls = ['electrons','muons']
        pts = {}
        p4s = {}
        charges = {}
        leps = []
        leps = self.getPassingCands(rtrow,'Loose')
        if len(leps)<3: return candidate # need at least 3 leptons

        for cand in leps:
            pts[cand] = self.getObjectVariable(rtrow,cand,'pt')
            p4s[cand] = self.getObjectVariable(rtrow,cand,'p4')
            charges[cand] = self.getObjectVariable(rtrow,cand,'charge')

        # get invariant masses
        massDiffs = {}
        for zpair in itertools.combinations(pts.keys(),2):
            if zpair[0][0]!=zpair[1][0]: continue # SF
            if charges[zpair[0]]==charges[zpair[1]]: continue # OS
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
        bestW = sorted(pts.items(), key=operator.itemgetter(1))[-1][0]

        # and sort pt of Z
        z = sorted(zpts.items(), key=operator.itemgetter(1))
        z1 = z[1][0]
        z2 = z[0][0]

        candidate['z1'] = z1
        candidate['z2'] = z2
        candidate['w1'] = bestW

        # add jet
        jets = self.getCands(rtrow, 'jets', lambda rtrow,cand: self.getObjectVariable(rtrow,cand,'isLoose')>0.5)
        if len(jets)>0:
            candidate['leadJet'] = jets[0]
        else:
            candidate['leadJet'] = ('jets',-1)

        return candidate

    ##################
    ### lepton IDs ###
    ##################
    def passLoose(self,rtrow,cand):
        pt = self.getObjectVariable(rtrow,cand,'pt')
        eta = self.getObjectVariable(rtrow,cand,'eta')
        if cand[0]=="electrons":
            if pt<=10: return False
            if abs(eta)>=2.5: return False
            if self.getObjectVariable(rtrow,cand,'wwLoose')<0.5: return False
        elif cand[0]=="muons":
            if pt<=10: return False
            if abs(eta)>=2.4: return False
            isMediumMuon = self.getObjectVariable(rtrow,cand,'isMediumMuon')
            if isMediumMuon<0.5: return False
            trackIso = self.getObjectVariable(rtrow,cand,'trackIso')
            if trackIso/pt>=0.4: return False
            pfRelIsoDB = self.getObjectVariable(rtrow,cand,'relPFIsoDeltaBetaR04')
            if pfRelIsoDB>=0.4: return False
        else:
            return False
        return True

    def passMedium(self,rtrow,cand):
        if not self.passLoose(rtrow,cand): return False
        if cand[0]=="electrons":
            if self.getObjectVariable(rtrow,cand,'cutBasedMedium')<0.5: return False
        elif cand[0]=="muons":
            dz = self.getObjectVariable(rtrow,cand,'dz')
            if abs(dz)>=0.1: return False
            pt = self.getObjectVariable(rtrow,cand,'pt')
            dxy = self.getObjectVariable(rtrow,cand,'dxy')
            if abs(dxy)>=0.01 and pt<20: return False
            if abs(dxy)>=0.02 and pt>=20: return False
            pfRelIsoDB = self.getObjectVariable(rtrow,cand,'relPFIsoDeltaBetaR04')
            if pfRelIsoDB>=0.15: return False
        else:
            return False
        return True

    def passTight(self,rtrow,cand):
        if not self.passLoose(rtrow,cand): return False
        if cand[0]=="electrons":
            if self.getObjectVariable(rtrow,cand,'cutBasedTight')<0.5: return False
        elif cand[0]=="muons":
            return self.passMedium(rtrow,cand)
        else:
            return False
        return True

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


    ###########################
    ### analysis selections ###
    ###########################
    def threeLoose(self,rtrow,cands):
        return len(self.getPassingCands(rtrow,'Loose'))>=3

    def vetoFourth(self,rtrow,cands):
        return len(self.getPassingCands(rtrow,'Medium'))<=3

    def trigger(self,rtrow,cands):
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
                'IsoMu27',
            ],
            'SingleEG' : [
                'Ele23_WPLoose_Gsf',
            ],
        }
        datasets = [
            'DoubleMuon', 
            'DoubleEG', 
            'MuonEG',
            'SingleMuon',
            'SingleEG'
        ]
        # reject triggers if the are in another dataset
        reject = True if self.sample in datasets else False
        for dataset in datasets:
            if dataset in self.sample: reject = False
            for trigger in triggerNames[dataset]:
                var = '{0}Pass'.format(trigger)
                passTrigger = self.getTreeVariable(rtrow,var)
                if passTrigger>0.5:
                    return False if reject else True
        return False











