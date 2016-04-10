# ElectronAnalysis.py
import logging
import time
from AnalysisBase import AnalysisBase
from utilities import ZMASS, deltaPhi, deltaR

import itertools
import operator

import ROOT

class ElectronAnalysis(AnalysisBase):
    '''
    all electrons
    '''

    def __init__(self,**kwargs):
        outputFileName = kwargs.pop('outputFileName','eTree.root')
        outputTreeName = kwargs.pop('outputTreeName','ETree')
        super(ElectronAnalysis, self).__init__(outputFileName=outputFileName,outputTreeName=outputTreeName,**kwargs)

        # setup analysis tree

        # w lepton
        self.addLeptonMet('w','e',('pfmet',0))
        self.addLepton('e')
        self.addDetailedElectron('e')

        # met
        self.addMet('met',('pfmet',0))

    ####################################################
    ### override analyze to store after every lepton ###
    ####################################################
    def perRowAction(self,rtrow):
        '''Per row action, can be overridden'''
        self.cache = {} # cache variables so you dont read from tree as much
        electrons = self.getCands(rtrow,'electrons',lambda rtrow,cands: True)
        for elec in electrons:
            cands = {'e':elec}
            self.tree.fill(rtrow,cands,allowDuplicates=True)

        self.eventsStored += 1


    #########################
    ### detailed electron ###
    #########################
    def addDetailedElectron(self,label):
        '''Add detailed electron variables'''
        self.addCandVar(label,'cutBasedVeto','cutBasedVeto','I')
        self.addCandVar(label,'cutBasedLoose','cutBasedLoose','I')
        self.addCandVar(label,'cutBasedMedium','cutBasedMedium','I')
        self.addCandVar(label,'cutBasedTight','cutBasedTight','I')
        self.addCandVar(label,'wwLoose','wwLoose','I')
        self.addCandVar(label,'heepV60','heepV60','I')
        self.addCandVar(label,'mvaNonTrigValues','mvaNonTrigValues','F')
        self.addCandVar(label,'mvaNonTrigCategories','mvaNonTrigCategories','I')
        self.addCandVar(label,'mvaNonTrigWP80','mvaNonTrigWP80','I')
        self.addCandVar(label,'mvaNonTrigWP90','mvaNonTrigWP90','I')
        self.addCandVar(label,'mvaTrigValues','mvaTrigValues','F')
        self.addCandVar(label,'mvaTrigCategories','mvaTrigCategories','I')
        self.addCandVar(label,'mvaTrigWP80','mvaTrigWP80','I')
        self.addCandVar(label,'mvaTrigWP90','mvaTrigWP90','I')
        self.tree.add(lambda rtrow,cands: self.passMVATrigPre(rtrow,cands[label]), '{0}_mvaTrigPre'.format(label), 'I')
        self.tree.add(lambda rtrow,cands: self.getObjectVariable(rtrow,cands[label],'dr03EcalRecHitSumEt')/self.getObjectVariable(rtrow,cands[label],'pt'), '{0}_ecalRelIso'.format(label), 'F')
        self.tree.add(lambda rtrow,cands: self.getObjectVariable(rtrow,cands[label],'dr03HcalTowerSumEt')/self.getObjectVariable(rtrow,cands[label],'pt'), '{0}_hcalRelIso'.format(label), 'F')
        self.tree.add(lambda rtrow,cands: self.getObjectVariable(rtrow,cands[label],'dr03TkSumPt')/self.getObjectVariable(rtrow,cands[label],'pt'), '{0}_trackRelIso'.format(label), 'F')
        self.addCandVar(label,'superClusterEta','superCluserEta','F')
        self.addCandVar(label,'sigmaIetaIeta','sigmaIetaIeta','F')
        self.addCandVar(label,'hcalOverEcal','hcalOverEcal','F')
        self.addCandVar(label,'deltaEtaSuperClusterTrackAtVtx','deltaEtaSuperClusterTrackAtVtx','F')
        self.addCandVar(label,'deltaPhiSuperClusterTrackAtVtx','deltaPhiSuperClusterTrackAtVtx','F')
        self.addCandVar(label,'passConversionVeto','passConversionVeto','I')
        self.addCandVar(label,'missingHits','missingHits','I')
        self.addCandVar(label,'ecalEnergy','ecalEnergy','F')
        self.addCandVar(label,'eSuperClusterOverP','eSuperClusterOverP','F')
        self.tree.add(lambda rtrow,cands: abs(1.-self.getObjectVariable(rtrow,cands[label],'eSuperClusterOverP'))*1./self.getObjectVariable(rtrow,cands[label],'ecalEnergy'), '{0}_oneOverEMinusOneOverP'.format(label), 'F')


    def passMVATrigPre(self,rtrow,cand):
        pt = self.getObjectVariable(rtrow,cand,'pt')
        sceta = self.getObjectVariable(rtrow,cand,'superClusterEta')
        sigmaIEtaIEta = self.getObjectVariable(rtrow,cand,'sigmaIetaIeta')
        hcalOverEcal = self.getObjectVariable(rtrow,cand,'hcalOverEcal')
        ecalRelIso = self.getObjectVariable(rtrow,cand,'dr03EcalRecHitSumEt')/pt
        hcalRelIso = self.getObjectVariable(rtrow,cand,'dr03HcalTowerSumEt')/pt
        trackRelIso = self.getObjectVariable(rtrow,cand,'dr03TkSumPt')/pt
        dEtaSC = self.getObjectVariable(rtrow,cand,'deltaEtaSuperClusterTrackAtVtx')
        dPhiSC = self.getObjectVariable(rtrow,cand,'deltaPhiSuperClusterTrackAtVtx')
        relIsoRho = self.getObjectVariable(rtrow,cand,'relPFIsoRhoR03')
        passConversion = self.getObjectVariable(rtrow,cand,'passConversionVeto')
        dxy = self.getObjectVariable(rtrow,cand,'dB2D')
        dz = self.getObjectVariable(rtrow,cand,'dz')
        ecalEnergy = self.getObjectVariable(rtrow,cand,'ecalEnergy')
        eSuperClusterOverP = self.getObjectVariable(rtrow,cand,'eSuperClusterOverP')
        ooEmooP = abs((1.-eSuperClusterOverP)*1./ecalEnergy)
        passMVATrigPre = True
        if pt<15: passMVATrigPre = False
        if sceta<1.479:
            if sigmaIEtaIEta>0.012: passMVATrigPre = False
            if hcalOverEcal>0.09:   passMVATrigPre = False
            if ecalRelIso>0.37:     passMVATrigPre = False
            if hcalRelIso>0.25:     passMVATrigPre = False
            if trackRelIso>0.18:    passMVATrigPre = False
            if abs(dEtaSC)>0.0095:  passMVATrigPre = False
            if abs(dPhiSC)>0.065:   passMVATrigPre = False
        else:
            if sigmaIEtaIEta>0.033: passMVATrigPre = False
            if hcalOverEcal>0.09:   passMVATrigPre = False
            if ecalRelIso>0.45:     passMVATrigPre = False
            if hcalRelIso>0.28:     passMVATrigPre = False
            if trackRelIso>0.18:    passMVATrigPre = False
        return passMVATrigPre
