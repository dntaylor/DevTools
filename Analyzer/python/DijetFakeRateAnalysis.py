from AnalysisBase import AnalysisBase
from leptonId import passWZLoose, passWZMedium, passWZTight
from utilities import ZMASS, deltaPhi, deltaR

import sys
import itertools
import operator

sys.argv.append('-b')
import ROOT
sys.argv.pop()

class DijetFakeRateAnalysis(AnalysisBase):
    '''
    Select a single lepton to perform a dijet control fake rate
    '''

    def __init__(self,**kwargs):
        outputFileName = kwargs.pop('outputFileName','dijetFakeRateTree.root')
        outputTreeName = kwargs.pop('outputTreeName','DijetFakeRateTree')
        super(DijetFakeRateAnalysis, self).__init__(outputFileName=outputFileName,outputTreeName=outputTreeName,**kwargs)

        # setup cut tree
        self.cutTree.add(self.vetoSecond,'vetoSecond')
        self.cutTree.add(self.trigger,'trigger')

        # setup analysis tree

        # chan string
        self.tree.add(self.getChannelString, 'channel', ['C',2])

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

        # trigger
        self.tree.add(lambda rtrow,cands: self.getTreeVariable(rtrow,'Mu8_TrkIsoVVLPass'), 'pass_Mu8_TrkIsoVVL', 'I')
        self.tree.add(lambda rtrow,cands: self.getTreeVariable(rtrow,'Mu17_TrkIsoVVLPass'), 'pass_Mu17_TrkIsoVVL', 'I')
        self.tree.add(lambda rtrow,cands: self.getTreeVariable(rtrow,'Mu24_TrkIsoVVLPass'), 'pass_Mu24_TrkIsoVVL', 'I')
        self.tree.add(lambda rtrow,cands: self.getTreeVariable(rtrow,'Mu34_TrkIsoVVLPass'), 'pass_Mu34_TrkIsoVVL', 'I')
        self.tree.add(lambda rtrow,cands: self.getTreeVariable(rtrow,'Ele12_CaloIdL_TrackIdL_IsoVLPass'), 'pass_Ele12_CaloIdL_TrackIdL_IsoVL', 'I')
        self.tree.add(lambda rtrow,cands: self.getTreeVariable(rtrow,'Ele17_CaloIdL_TrackIdL_IsoVLPass'), 'pass_Ele17_CaloIdL_TrackIdL_IsoVL', 'I')
        self.tree.add(lambda rtrow,cands: self.getTreeVariable(rtrow,'Ele23_CaloIdL_TrackIdL_IsoVLPass'), 'pass_Ele23_CaloIdL_TrackIdL_IsoVL', 'I')
        self.tree.add(self.triggerEfficiency, 'triggerEfficiency', 'F')
        self.tree.add(self.triggerPrescale, 'triggerPrescale', 'F')

        # lead jet
        self.addJet('leadJet')

        # lepton
        self.addLeptonMet('w','l1',('pfmet',0))
        self.addLepton('l1')
        self.tree.add(lambda rtrow,cands: self.passMedium(rtrow,cands['l1']), 'l1_passMedium', 'I')
        self.tree.add(lambda rtrow,cands: self.passTight(rtrow,cands['l1']), 'l1_passTight', 'I')
        self.tree.add(lambda rtrow,cands: self.looseScale(rtrow,cands['l1']), 'l1_looseScale', 'F')
        self.tree.add(lambda rtrow,cands: self.mediumScale(rtrow,cands['l1']), 'l1_mediumScale', 'F')
        self.tree.add(lambda rtrow,cands: self.tightScale(rtrow,cands['l1']), 'l1_tightScale', 'F')

        # met
        self.addMet('met',('pfmet',0))

    #############################
    ### select fake candidate ###
    #############################
    def selectCandidates(self,rtrow):
        candidate = {
            'l1' : (),
            'leadJet' : (),
        }

        # get leptons
        colls = ['electrons','muons']
        pts = {}
        leps = []
        leps = self.getPassingCands(rtrow,'Loose')
        if len(leps)<1: return candidate # need at least 1 lepton

        for cand in leps:
            pts[cand] = self.getObjectVariable(rtrow,cand,'pt')

        # choose highest pt
        l = sorted(pts.items(), key=operator.itemgetter(1))[-1][0]

        candidate['l1'] = l

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
        for c in ['l1']:
            chanString += self.getCollectionString(cands[c])
        return chanString

    ###########################
    ### analysis selections ###
    ###########################
    def vetoSecond(self,rtrow,cands):
        return len(self.getPassingCands(rtrow,'Loose'))==1

    def trigger(self,rtrow,cands):
        # accept MC, check trigger for data
        if rtrow.isData<0.5: return True
        if not cands['l1']: return False
        triggerNames = {
            'DoubleMuon'     : [
                ['Mu8_TrkIsoVVL', 0],
                ['Mu17_TrkIsoVVL', 20],
                #['Mu24_TrkIsoVVL', 30],
                #['Mu34_TrkIsoVVL', 40],
            ],
            'DoubleEG'       : [
                ['Ele12_CaloIdL_TrackIdL_IsoVL', 0],
                ['Ele17_CaloIdL_TrackIdL_IsoVL', 20],
                #['Ele23_CaloIdL_TrackIdL_IsoVL', 30],
            ],
        }
        # here we need to accept only a specific trigger after a certain pt threshold
        pt = self.getObjectVariable(rtrow,cands['l1'],'pt')
        dataset = 'DoubleEG' if cands['l1'][0] == 'electrons' else 'DoubleMuon'
        # accept the event only if it is triggered in the current dataset
        reject = True if rtrow.isData>0.5 else False
        if dataset in self.fileNames[0]: reject = False
        # now pick the appropriate trigger for the pt
        theTrigger = ''
        for trig, ptThresh in triggerNames[dataset]:
            if pt < ptThresh: break
            theTrigger = trig
        # and check if we pass
        passTrigger = self.getTreeVariable(rtrow,'{0}Pass'.format(theTrigger))
        if passTrigger>0.5: return False if reject else True
        return False

    def triggerEfficiency(self,rtrow,cands):
        candList = [cands['l1']]
        # select via pt and flavor
        pt = self.getObjectVariable(rtrow,cands['l1'],'pt')
        if cands['l1'][0] == 'electrons':
            if pt<20:
                triggerList = ['Ele17_Ele12Leg2']
            else:
                triggerList = ['Ele17_Ele12Leg1']
        else:
            if pt<20:
                triggerList = ['Mu17_Mu8Leg2']
            else:
                triggerList = ['Mu17_Mu8Leg1']
        return self.triggerScales.getDataEfficiency(rtrow,triggerList,candList)

    def triggerPrescale(self,rtrow,cands):
        # select via pt and flavor
        pt = self.getObjectVariable(rtrow,cands['l1'],'pt')
        if cands['l1'][0] == 'electrons':
            if pt<20:
                trigger = 'Ele17_Ele12Leg2'
            else:
                trigger = 'Ele17_Ele12Leg1'
        else:
            if pt<20:
                trigger = 'Mu17_Mu8Leg2'
            else:
                trigger = 'Mu17_Mu8Leg1'
        return self.triggerPrescales.getPrescale(trigger)

