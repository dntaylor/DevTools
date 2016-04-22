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
        muons = self.getCands(rtrow,'muons',lambda rtrow,cands: True)
        for muon in muons:
            cands = {'m':muon}
            pt = self.getObjectVariable(rtrow,cands['m'],'pt')
            if pt<10: continue
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
        self.addCandVar(label,'segmentCompatibility','segmentCompatibility','F')
        self.addCandVar(label,'isGoodMuon','isGoodMuon','I')
        self.addCandVar(label,'highPurityTrack','highPurityTrack','I')
        self.addCandVar(label,'matchedStations','matchedStations','I')
        self.addCandVar(label,'validMuonHits','validMuonHits','I')
        self.addCandVar(label,'normalizedChi2','normalizedChi2','F')
        self.addCandVar(label,'validPixelHits','validPixelHits','I')
        self.addCandVar(label,'trackerLayers','trackerLayers','I')
        self.addCandVar(label,'pixelLayers','pixelLayers','I')
        self.addCandVar(label,'validTrackerFractionl','validTrackerFractionl','F')
        self.addCandVar(label,'bestTrackPtError','bestTrackPtError','F')
        self.addCandVar(label,'bestTrackPt','bestTrackPt','F')
        self.addCandVar(label,'trackerStandalone','trackerStandalone','F')
        self.addCandVar(label,'trackKink','trackKink','F')
        self.tree.add(lambda rtrow,cands: self.getObjectVariable(rtrow,cands[label],'trackIso')/self.getObjectVariable(rtrow,cands[label],'pt'), '{0}_trackRelIso'.format(label), 'F')
