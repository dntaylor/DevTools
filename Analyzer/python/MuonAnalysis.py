# MuonAnalysis.py
import logging
import time
from AnalysisBase import AnalysisBase
from utilities import ZMASS, deltaPhi, deltaR

import itertools
import operator

import ROOT

class MuonAnalysis(AnalysisBase):
    '''
    all s
    '''

    def __init__(self,**kwargs):
        outputFileName = kwargs.pop('outputFileName','mTree.root')
        outputTreeName = kwargs.pop('outputTreeName','MTree')
        super(MuonAnalysis, self).__init__(outputFileName=outputFileName,outputTreeName=outputTreeName,**kwargs)

        # setup analysis tree

        # pileup
        self.tree.add(lambda rtrow,cands: self.getTreeVariable(rtrow,'vertices_count'), 'numVertices', 'I')

        # gen
        self.tree.add(lambda rtrow,cands: self.getTreeVariable(rtrow,'nTrueVertices'), 'numTrueVertices', 'I')
        self.tree.add(lambda rtrow,cands: self.getTreeVariable(rtrow,'NUP'), 'NUP', 'I')
        self.tree.add(lambda rtrow,cands: self.getTreeVariable(rtrow,'isData'), 'isData', 'I')
        self.tree.add(lambda rtrow,cands: self.getTreeVariable(rtrow,'genWeight'), 'genWeight', 'I')

        # w lepton
        self.addLeptonMet('w','m',('pfmet',0))
        self.addLepton('m')
        self.addDetailedMuon('m')

        # met
        self.addMet('met',('pfmet',0))

    ####################################################
    ### override analyze to store after every lepton ###
    ####################################################
    def perRowAction(self,rtrow):
        '''Per row action, can be overridden'''
        self.cache = {} # cache variables so you dont read from tree as much
        muons = self.getCands(rtrow,'msons',lambda rtrow,cands: True)
        for muons in muons:
            cands = {'e':muon}
            self.tree.fill(rtrow,cands,allowDuplicates=True)

        self.eventsStored += 1

    #########################
    ### detailed  ###
    #########################
    def addDetailedMuon(self,label):
        '''Add detailed  variables'''
        self.addCandVar(label,'isLooseMuon','isLooseMuon','I')
        self.addCandVar(label,'isMediumMuon','isMediumMuon','I')
        self.addCandVar(label,'isTightMuon','isTightMuon','I')
        self.addCandVar(label,'isHighPtMuon','isHighPtMuon','I')
        self.addCandVar(label,'isPFMuon','isPFMuon','I')
        self.addCandVar(label,'isGlobalMuon','isGlobalMuon','I')
        self.addCandVar(label,'isTrackerMuon','isTrackerMuon','I')
        self.addCandVar(label,'muonBestTrackType','muonBestTrackType','I')
        self.tree.add(lambda rtrow,cands: self.getObjectVariable(rtrow,cands[label],'trackIso')/self.getObjectVariable(rtrow,cands[label],'pt'), '{0}_trackRelIso'.format(label), 'F')
