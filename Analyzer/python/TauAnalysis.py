# TauAnalysis.py
import logging
import time
from AnalysisBase import AnalysisBase
from utilities import ZMASS, deltaPhi, deltaR

import itertools
import operator

import ROOT

class TauAnalysis(AnalysisBase):
    '''
    all taus
    '''

    def __init__(self,**kwargs):
        outputFileName = kwargs.pop('outputFileName','tTree.root')
        outputTreeName = kwargs.pop('outputTreeName','TTree')
        super(TauAnalysis, self).__init__(outputFileName=outputFileName,outputTreeName=outputTreeName,**kwargs)

        # setup analysis tree

        # w lepton
        self.addLeptonMet('w','t',('pfmet',0))
        self.addLepton('t')
        self.addDetailedTau('t')

        # met
        self.addMet('met',('pfmet',0))

    ####################################################
    ### override analyze to store after every lepton ###
    ####################################################
    def perRowAction(self,rtrow):
        '''Per row action, can be overridden'''
        self.cache = {} # cache variables so you dont read from tree as much
        taus = self.getCands(rtrow,'taus',lambda rtrow,cands: True)
        for tau in taus:
            cands = {'t':tau}
            self.tree.fill(rtrow,cands,allowDuplicates=True)

        self.eventsStored += 1

    #########################
    ### detailed  ###
    #########################
    def addDetailedTau(self,label):
        '''Add detailed  variables'''
        self.addCandVar(label,'againstMuonLoose3','againstMuonLoose3','I')
        self.addCandVar(label,'againstMuonTight3','againstMuonTight3','I')
        self.addCandVar(label,'againstElectronVLooseMVA6','againstElectronVLooseMVA6','I')
        self.addCandVar(label,'againstElectronLooseMVA6','againstElectronLooseMVA6','I')
        self.addCandVar(label,'againstElectronMediumMVA6','againstElectronMediumMVA6','I')
        self.addCandVar(label,'againstElectronTightMVA6','againstElectronTightMVA6','I')
        self.addCandVar(label,'againstElectronVTightMVA6','againstElectronVTightMVA6','I')
        self.addCandVar(label,'decayModeFinding','decayModeFinding','I')
        self.addCandVar(label,'byLooseIsolationMVArun2v1DBoldDMwLT','byLooseIsolationMVArun2v1DBoldDMwLT','I')
        self.addCandVar(label,'byMediumIsolationMVArun2v1DBoldDMwLT','byMediumIsolationMVArun2v1DBoldDMwLT','I')
        self.addCandVar(label,'byTightIsolationMVArun2v1DBoldDMwLT','byTightIsolationMVArun2v1DBoldDMwLT','I')
        self.addCandVar(label,'byVTightIsolationMVArun2v1DBoldDMwLT','byVTightIsolationMVArun2v1DBoldDMwLT','I')
